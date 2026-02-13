"""
PDF document (.pdf) content extractor.
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


class PdfExtractor(BaseExtractor):
    """Extract content from PDF documents."""

    def supported_extensions(self) -> list[str]:
        return [".pdf"]

    def extract(self, file_path: Path) -> ExtractedContent:
        from pypdf import PdfReader

        reader = PdfReader(str(file_path))
        blocks: list[ContentBlock] = []
        warnings: list[str] = []
        word_count = 0

        for page_idx, page in enumerate(reader.pages):
            try:
                text = page.extract_text()
                if not text or not text.strip():
                    warnings.append(f"Page {page_idx + 1}: No extractable text (may be image-based)")
                    continue

                page_blocks = self._parse_page_text(text, page_idx)
                blocks.extend(page_blocks)

                for block in page_blocks:
                    if block.text:
                        word_count += len(block.text.split())
                    for item in block.items:
                        word_count += len(item.split())

            except Exception as e:
                warnings.append(f"Page {page_idx + 1}: Extraction error - {e}")

        # Extract images from pages
        image_blocks = self._extract_images(reader, warnings)
        blocks.extend(image_blocks)

        # Get PDF metadata
        pdf_meta = reader.metadata or {}
        title = ""
        if pdf_meta:
            title = getattr(pdf_meta, "title", "") or ""

        if not title:
            title = self._infer_title(blocks)

        metadata = DocumentMetadata(
            title=title,
            author=getattr(pdf_meta, "author", None) if pdf_meta else None,
            page_count=len(reader.pages),
            word_count=word_count,
            has_images=len(image_blocks) > 0,
            has_tables=any(b.content_type == ContentType.TABLE for b in blocks),
        )

        return ExtractedContent(
            source_file=str(file_path),
            source_format="pdf",
            blocks=blocks,
            metadata=metadata,
            extraction_warnings=warnings,
        )

    def _parse_page_text(self, text: str, page_idx: int) -> list[ContentBlock]:
        """Parse extracted page text into content blocks."""
        blocks = []
        # Split on double newlines to separate paragraphs
        paragraphs = re.split(r"\n{2,}", text.strip())

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            block_id = f"pdf_p{page_idx}_{uuid4().hex[:6]}"

            # Detect headings (heuristic: short lines, possibly uppercase or bold indicators)
            lines = para.split("\n")
            first_line = lines[0].strip()

            if self._is_likely_heading(first_line, para):
                blocks.append(ContentBlock(
                    block_id=block_id,
                    content_type=ContentType.HEADING,
                    text=first_line,
                    level=self._estimate_heading_level(first_line),
                    metadata={"page": page_idx + 1},
                ))
                # If there's more text after the heading line, add as paragraph
                remaining = "\n".join(lines[1:]).strip()
                if remaining:
                    blocks.append(ContentBlock(
                        block_id=f"pdf_p{page_idx}_{uuid4().hex[:6]}",
                        content_type=ContentType.PARAGRAPH,
                        text=remaining,
                        metadata={"page": page_idx + 1},
                    ))
            elif self._is_bullet_list(para):
                items = self._extract_bullet_items(para)
                blocks.append(ContentBlock(
                    block_id=block_id,
                    content_type=ContentType.BULLET_LIST,
                    items=items,
                    metadata={"page": page_idx + 1},
                ))
            elif self._looks_like_table(para):
                table_data = self._parse_tabular_text(para)
                if table_data:
                    blocks.append(ContentBlock(
                        block_id=block_id,
                        content_type=ContentType.TABLE,
                        table_data=table_data[1:] if len(table_data) > 1 else table_data,
                        table_headers=table_data[0] if table_data else None,
                        metadata={"page": page_idx + 1},
                    ))
                else:
                    blocks.append(ContentBlock(
                        block_id=block_id,
                        content_type=ContentType.PARAGRAPH,
                        text=para,
                        metadata={"page": page_idx + 1},
                    ))
            else:
                blocks.append(ContentBlock(
                    block_id=block_id,
                    content_type=ContentType.PARAGRAPH,
                    text=para,
                    metadata={"page": page_idx + 1},
                ))

        return blocks

    def _is_likely_heading(self, line: str, full_para: str) -> bool:
        """Heuristic: determine if a line is likely a heading."""
        if not line:
            return False
        # Short text (< 100 chars), no period at end, might be all caps
        if len(line) > 100:
            return False
        if line.endswith("."):
            return False
        if line == line.upper() and len(line) > 3:
            return True
        # Single line paragraph that's short
        if "\n" not in full_para and len(line) < 60:
            return True
        return False

    def _estimate_heading_level(self, text: str) -> int:
        """Estimate heading level based on text characteristics."""
        if text == text.upper():
            return 1
        if len(text) < 30:
            return 2
        return 3

    def _is_bullet_list(self, text: str) -> bool:
        """Check if text appears to be a bullet list."""
        lines = text.strip().split("\n")
        bullet_patterns = [r"^\s*[\u2022\u2023\u25E6\u2043\-\*]\s", r"^\s*\d+[\.\)]\s"]
        bullet_count = 0
        for line in lines:
            for pattern in bullet_patterns:
                if re.match(pattern, line):
                    bullet_count += 1
                    break
        return bullet_count >= 2 and bullet_count / len(lines) > 0.5

    def _extract_bullet_items(self, text: str) -> list[str]:
        """Extract individual bullet items from text."""
        items = []
        for line in text.strip().split("\n"):
            cleaned = re.sub(r"^\s*[\u2022\u2023\u25E6\u2043\-\*\d+\.\)]\s*", "", line).strip()
            if cleaned:
                items.append(cleaned)
        return items

    def _looks_like_table(self, text: str) -> bool:
        """Heuristic: check if text looks like tabular data."""
        lines = text.strip().split("\n")
        if len(lines) < 2:
            return False
        # Check for consistent tab or multi-space separation
        tab_lines = sum(1 for l in lines if "\t" in l or "  " in l)
        return tab_lines / len(lines) > 0.7

    def _parse_tabular_text(self, text: str) -> list[list[str]]:
        """Parse tabular text into rows and columns."""
        rows = []
        for line in text.strip().split("\n"):
            if "\t" in line:
                cells = [c.strip() for c in line.split("\t") if c.strip()]
            else:
                cells = [c.strip() for c in re.split(r"\s{2,}", line) if c.strip()]
            if cells:
                rows.append(cells)
        return rows if rows else []

    def _extract_images(self, reader, warnings: list[str]) -> list[ContentBlock]:
        """Extract embedded images from PDF pages."""
        image_blocks = []
        for page_idx, page in enumerate(reader.pages):
            try:
                if "/XObject" in (page.get("/Resources") or {}):
                    xobjects = page["/Resources"]["/XObject"].get_object()
                    for obj_name in xobjects:
                        obj = xobjects[obj_name].get_object()
                        if obj.get("/Subtype") == "/Image":
                            try:
                                data = obj.get_data()
                                block_id = f"pdf_img_{page_idx}_{uuid4().hex[:6]}"
                                image_blocks.append(ContentBlock(
                                    block_id=block_id,
                                    content_type=ContentType.IMAGE,
                                    image_data=data,
                                    image_format="png",
                                    metadata={"page": page_idx + 1},
                                ))
                            except Exception:
                                pass
            except Exception:
                pass

        return image_blocks

    def _infer_title(self, blocks: list[ContentBlock]) -> str:
        """Infer title from first heading."""
        for block in blocks:
            if block.content_type == ContentType.HEADING:
                return block.text or ""
        return ""
