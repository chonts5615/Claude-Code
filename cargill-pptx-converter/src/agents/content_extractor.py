"""
Agent 1: Content Extraction Agent

Extracts and structures content from input documents regardless of format.
"""

from pathlib import Path

from src.agents.base import BaseAgent
from src.extractors.registry import extract_content, is_supported_format
from src.schemas.content import ContentSection, ContentType, KeyMessage
from src.schemas.run_state import RunState


class ContentExtractorAgent(BaseAgent):
    """Extract and structure content from any input document format."""

    def __init__(self):
        super().__init__("S1", "Content Extraction")

    def execute(self, state: RunState) -> RunState:
        state.current_step = self.agent_id
        self.logger.info(f"Extracting content from: {state.inputs.input_file}")

        input_path = Path(state.inputs.input_file)

        # Validate input file
        if not input_path.exists():
            self._add_flag(state, "CRITICAL", f"Input file not found: {input_path}")
            return state

        if not is_supported_format(input_path):
            self._add_flag(state, "CRITICAL", f"Unsupported file format: {input_path.suffix}")
            return state

        # Extract content
        try:
            extracted = extract_content(input_path)
        except Exception as e:
            self._add_flag(state, "CRITICAL", f"Content extraction failed: {e}")
            return state

        if not extracted.blocks:
            self._add_flag(state, "CRITICAL", "No content blocks extracted from document")
            return state

        # Build sections from content hierarchy
        extracted.sections = self._build_sections(extracted)

        # Identify key messages
        extracted.key_messages = self._identify_key_messages(extracted)

        # Update metadata
        extracted.metadata.word_count = extracted.get_word_count()
        extracted.metadata.has_images = len(extracted.get_images()) > 0
        extracted.metadata.has_tables = len(extracted.get_tables()) > 0

        state.extracted_content = extracted

        # Log summary
        self.logger.info(
            f"Extracted {len(extracted.blocks)} blocks, "
            f"{len(extracted.sections)} sections, "
            f"{extracted.metadata.word_count} words"
        )

        if extracted.extraction_warnings:
            for warning in extracted.extraction_warnings:
                self._add_flag(state, "WARNING", warning)

        return state

    def _build_sections(self, extracted) -> list[ContentSection]:
        """Build logical sections from content blocks based on headings."""
        sections = []
        current_section = None
        section_idx = 0

        for block in extracted.blocks:
            if block.content_type == ContentType.HEADING and block.level <= 2:
                # Start a new section
                if current_section:
                    sections.append(current_section)

                section_idx += 1
                current_section = ContentSection(
                    section_id=f"sec_{section_idx}",
                    title=block.text,
                    blocks=[block.block_id],
                    word_count=len(block.text.split()) if block.text else 0,
                    section_type="general",
                )
            elif current_section:
                current_section.blocks.append(block.block_id)
                if block.text:
                    current_section.word_count += len(block.text.split())
                for item in block.items:
                    current_section.word_count += len(item.split())
            else:
                # Content before any heading - create default section
                section_idx += 1
                current_section = ContentSection(
                    section_id=f"sec_{section_idx}",
                    title=None,
                    blocks=[block.block_id],
                    word_count=len(block.text.split()) if block.text else 0,
                )

        if current_section:
            sections.append(current_section)

        # Classify section types
        for section in sections:
            section.section_type = self._classify_section(section, extracted)

        return sections

    def _classify_section(self, section: ContentSection, extracted) -> str:
        """Classify a section's type based on its content."""
        table_count = 0
        stat_count = 0
        text_count = 0

        for block_id in section.blocks:
            block = extracted.get_block(block_id)
            if not block:
                continue
            if block.content_type == ContentType.TABLE:
                table_count += 1
            elif block.content_type in (ContentType.STATISTIC, ContentType.CHART_DATA):
                stat_count += 1
            elif block.content_type in (ContentType.PARAGRAPH, ContentType.BULLET_LIST):
                text_count += 1

        if table_count + stat_count > text_count:
            return "data_heavy"
        elif section.word_count < 100:
            return "summary"
        else:
            return "narrative"

    def _identify_key_messages(self, extracted) -> list[KeyMessage]:
        """Identify key messages from content."""
        key_messages = []
        msg_idx = 0

        # First heading is likely the primary message
        headings = extracted.get_headings()
        if headings:
            msg_idx += 1
            key_messages.append(KeyMessage(
                message_id=f"msg_{msg_idx}",
                text=headings[0].text or "",
                importance="primary",
                supporting_blocks=[headings[0].block_id],
            ))

        # Statistics and significant data points
        stats = extracted.get_statistics()
        for stat in stats[:3]:
            msg_idx += 1
            label = stat.metadata.get("label", "")
            key_messages.append(KeyMessage(
                message_id=f"msg_{msg_idx}",
                text=f"{label}: {stat.text}" if label else stat.text or "",
                importance="secondary",
                supporting_blocks=[stat.block_id],
            ))

        # Section titles as secondary messages
        for section in extracted.sections:
            if section.title and len(key_messages) < 8:
                msg_idx += 1
                key_messages.append(KeyMessage(
                    message_id=f"msg_{msg_idx}",
                    text=section.title,
                    importance="supporting",
                    supporting_blocks=section.blocks[:3],
                ))

        return key_messages
