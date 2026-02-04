"""
Plain text and Markdown content extractor.
"""

import re
from pathlib import Path
from uuid import uuid4

from src.extractors.base import BaseExtractor
from src.schemas.content import (
    ContentBlock,
    ContentType,
    DocumentMetadata,
    ExtractedContent,
)


class TextExtractor(BaseExtractor):
    """Extract content from plain text and Markdown files."""

    def supported_extensions(self) -> list[str]:
        return [".txt", ".md", ".markdown", ".text"]

    def extract(self, file_path: Path) -> ExtractedContent:
        text = Path(file_path).read_text(encoding="utf-8", errors="replace")
        is_markdown = file_path.suffix.lower() in (".md", ".markdown")

        if is_markdown:
            blocks = self._parse_markdown(text)
        else:
            blocks = self._parse_plain_text(text)

        word_count = sum(
            len(b.text.split()) if b.text else sum(len(i.split()) for i in b.items)
            for b in blocks
        )

        title = ""
        for block in blocks:
            if block.content_type == ContentType.HEADING:
                title = block.text or ""
                break

        metadata = DocumentMetadata(
            title=title,
            word_count=word_count,
            has_tables=any(b.content_type == ContentType.TABLE for b in blocks),
        )

        return ExtractedContent(
            source_file=str(file_path),
            source_format="markdown" if is_markdown else "text",
            blocks=blocks,
            metadata=metadata,
        )

    def _parse_markdown(self, text: str) -> list[ContentBlock]:
        """Parse Markdown text into content blocks."""
        blocks = []
        lines = text.split("\n")
        i = 0
        current_paragraph = []

        while i < len(lines):
            line = lines[i]

            # Heading (# syntax)
            heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if heading_match:
                # Flush accumulated paragraph
                if current_paragraph:
                    blocks.append(self._make_paragraph("\n".join(current_paragraph)))
                    current_paragraph = []

                level = len(heading_match.group(1))
                blocks.append(ContentBlock(
                    block_id=f"md_{uuid4().hex[:8]}",
                    content_type=ContentType.HEADING,
                    text=heading_match.group(2).strip(),
                    level=level,
                ))
                i += 1
                continue

            # Setext heading (underline style)
            if i + 1 < len(lines):
                next_line = lines[i + 1] if i + 1 < len(lines) else ""
                if re.match(r"^=+\s*$", next_line) and line.strip():
                    if current_paragraph:
                        blocks.append(self._make_paragraph("\n".join(current_paragraph)))
                        current_paragraph = []
                    blocks.append(ContentBlock(
                        block_id=f"md_{uuid4().hex[:8]}",
                        content_type=ContentType.HEADING,
                        text=line.strip(),
                        level=1,
                    ))
                    i += 2
                    continue
                elif re.match(r"^-+\s*$", next_line) and line.strip() and not re.match(r"^\s*[-*]\s", line):
                    if current_paragraph:
                        blocks.append(self._make_paragraph("\n".join(current_paragraph)))
                        current_paragraph = []
                    blocks.append(ContentBlock(
                        block_id=f"md_{uuid4().hex[:8]}",
                        content_type=ContentType.HEADING,
                        text=line.strip(),
                        level=2,
                    ))
                    i += 2
                    continue

            # Bullet list
            bullet_match = re.match(r"^\s*[-*+]\s+(.+)$", line)
            if bullet_match:
                if current_paragraph:
                    blocks.append(self._make_paragraph("\n".join(current_paragraph)))
                    current_paragraph = []

                items = [bullet_match.group(1).strip()]
                i += 1
                while i < len(lines):
                    m = re.match(r"^\s*[-*+]\s+(.+)$", lines[i])
                    if m:
                        items.append(m.group(1).strip())
                        i += 1
                    else:
                        break

                blocks.append(ContentBlock(
                    block_id=f"md_{uuid4().hex[:8]}",
                    content_type=ContentType.BULLET_LIST,
                    items=items,
                ))
                continue

            # Numbered list
            num_match = re.match(r"^\s*\d+[\.\)]\s+(.+)$", line)
            if num_match:
                if current_paragraph:
                    blocks.append(self._make_paragraph("\n".join(current_paragraph)))
                    current_paragraph = []

                items = [num_match.group(1).strip()]
                i += 1
                while i < len(lines):
                    m = re.match(r"^\s*\d+[\.\)]\s+(.+)$", lines[i])
                    if m:
                        items.append(m.group(1).strip())
                        i += 1
                    else:
                        break

                blocks.append(ContentBlock(
                    block_id=f"md_{uuid4().hex[:8]}",
                    content_type=ContentType.NUMBERED_LIST,
                    items=items,
                ))
                continue

            # Code block
            if line.strip().startswith("```"):
                if current_paragraph:
                    blocks.append(self._make_paragraph("\n".join(current_paragraph)))
                    current_paragraph = []

                code_lines = []
                lang = line.strip()[3:].strip()
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    code_lines.append(lines[i])
                    i += 1
                i += 1  # skip closing ```

                blocks.append(ContentBlock(
                    block_id=f"md_{uuid4().hex[:8]}",
                    content_type=ContentType.CODE_BLOCK,
                    text="\n".join(code_lines),
                    metadata={"language": lang} if lang else {},
                ))
                continue

            # Blockquote
            quote_match = re.match(r"^>\s*(.*)$", line)
            if quote_match:
                if current_paragraph:
                    blocks.append(self._make_paragraph("\n".join(current_paragraph)))
                    current_paragraph = []

                quote_text = [quote_match.group(1).strip()]
                i += 1
                while i < len(lines):
                    qm = re.match(r"^>\s*(.*)$", lines[i])
                    if qm:
                        quote_text.append(qm.group(1).strip())
                        i += 1
                    else:
                        break

                blocks.append(ContentBlock(
                    block_id=f"md_{uuid4().hex[:8]}",
                    content_type=ContentType.BLOCKQUOTE,
                    text=" ".join(qt for qt in quote_text if qt),
                ))
                continue

            # Table (pipe-delimited)
            if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?[\s\-:|]+\|", lines[i + 1]):
                if current_paragraph:
                    blocks.append(self._make_paragraph("\n".join(current_paragraph)))
                    current_paragraph = []

                table_rows = self._parse_md_table(lines, i)
                if table_rows:
                    headers = table_rows[0] if table_rows else []
                    data = table_rows[2:] if len(table_rows) > 2 else []  # skip separator row
                    blocks.append(ContentBlock(
                        block_id=f"md_{uuid4().hex[:8]}",
                        content_type=ContentType.TABLE,
                        table_data=data,
                        table_headers=headers,
                    ))
                    i += len(table_rows)
                    continue

            # Blank line
            if not line.strip():
                if current_paragraph:
                    blocks.append(self._make_paragraph("\n".join(current_paragraph)))
                    current_paragraph = []
                i += 1
                continue

            # Regular text - accumulate
            current_paragraph.append(line)
            i += 1

        # Flush remaining paragraph
        if current_paragraph:
            blocks.append(self._make_paragraph("\n".join(current_paragraph)))

        return blocks

    def _parse_plain_text(self, text: str) -> list[ContentBlock]:
        """Parse plain text into content blocks."""
        blocks = []
        paragraphs = re.split(r"\n{2,}", text.strip())

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # Check for bullet-like patterns
            if self._is_bullet_list(para):
                items = [
                    re.sub(r"^\s*[-*\u2022]\s*", "", line).strip()
                    for line in para.split("\n")
                    if line.strip()
                ]
                blocks.append(ContentBlock(
                    block_id=f"txt_{uuid4().hex[:8]}",
                    content_type=ContentType.BULLET_LIST,
                    items=items,
                ))
            else:
                # First paragraph might be a title
                if not blocks and len(para) < 100 and "\n" not in para:
                    blocks.append(ContentBlock(
                        block_id=f"txt_{uuid4().hex[:8]}",
                        content_type=ContentType.HEADING,
                        text=para,
                        level=1,
                    ))
                else:
                    blocks.append(self._make_paragraph(para))

        return blocks

    def _make_paragraph(self, text: str) -> ContentBlock:
        """Create a paragraph content block."""
        # Clean up markdown formatting
        cleaned = re.sub(r"\*\*(.+?)\*\*", r"\1", text)  # bold
        cleaned = re.sub(r"\*(.+?)\*", r"\1", cleaned)    # italic
        cleaned = re.sub(r"`(.+?)`", r"\1", cleaned)      # inline code
        cleaned = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", cleaned)  # links

        return ContentBlock(
            block_id=f"txt_{uuid4().hex[:8]}",
            content_type=ContentType.PARAGRAPH,
            text=cleaned.strip(),
        )

    def _is_bullet_list(self, text: str) -> bool:
        """Check if text looks like a bullet list."""
        lines = text.strip().split("\n")
        bullet_count = sum(1 for l in lines if re.match(r"^\s*[-*\u2022]\s", l))
        return bullet_count >= 2 and bullet_count / len(lines) > 0.5

    def _parse_md_table(self, lines: list[str], start: int) -> list[list[str]]:
        """Parse a Markdown pipe table starting at given line index."""
        rows = []
        i = start
        while i < len(lines) and "|" in lines[i]:
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            rows.append(cells)
            i += 1
        return rows
