"""
Content schemas for extracted document data.
"""

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class ContentType(str, Enum):
    """Types of content blocks extracted from documents."""
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    BULLET_LIST = "bullet_list"
    NUMBERED_LIST = "numbered_list"
    TABLE = "table"
    IMAGE = "image"
    CHART_DATA = "chart_data"
    CODE_BLOCK = "code_block"
    BLOCKQUOTE = "blockquote"
    STATISTIC = "statistic"


class ContentBlock(BaseModel):
    """A single block of content extracted from a document."""
    block_id: str
    content_type: ContentType
    text: Optional[str] = None
    level: int = 0  # Heading level (1-6) or nesting depth
    items: list[str] = Field(default_factory=list)  # For bullet/numbered lists
    table_data: Optional[list[list[str]]] = None  # rows of columns
    table_headers: Optional[list[str]] = None
    image_data: Optional[bytes] = None
    image_path: Optional[str] = None
    image_format: Optional[str] = None
    chart_data: Optional[dict] = None
    metadata: dict = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


class DocumentMetadata(BaseModel):
    """Metadata about the source document."""
    title: Optional[str] = None
    author: Optional[str] = None
    date_created: Optional[str] = None
    page_count: Optional[int] = None
    word_count: int = 0
    has_images: bool = False
    has_tables: bool = False
    has_charts: bool = False


class KeyMessage(BaseModel):
    """An identified key message from the document."""
    message_id: str
    text: str
    importance: str = "secondary"  # "primary", "secondary", "supporting"
    supporting_blocks: list[str] = Field(default_factory=list)


class ContentSection(BaseModel):
    """A logical section of the document."""
    section_id: str
    title: Optional[str] = None
    blocks: list[str] = Field(default_factory=list)  # block_ids
    word_count: int = 0
    section_type: str = "general"  # "summary", "data_heavy", "narrative", "general"


class ExtractedContent(BaseModel):
    """Complete extracted content from a source document."""
    source_file: str
    source_format: str
    blocks: list[ContentBlock]
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata)
    key_messages: list[KeyMessage] = Field(default_factory=list)
    sections: list[ContentSection] = Field(default_factory=list)
    extraction_warnings: list[str] = Field(default_factory=list)

    def get_block(self, block_id: str) -> Optional[ContentBlock]:
        """Get a content block by ID."""
        for block in self.blocks:
            if block.block_id == block_id:
                return block
        return None

    def get_all_text(self) -> str:
        """Get all text content concatenated."""
        texts = []
        for block in self.blocks:
            if block.text:
                texts.append(block.text)
            if block.items:
                texts.extend(block.items)
        return " ".join(texts)

    def get_word_count(self) -> int:
        """Calculate total word count."""
        return len(self.get_all_text().split())

    def get_tables(self) -> list[ContentBlock]:
        """Get all table blocks."""
        return [b for b in self.blocks if b.content_type == ContentType.TABLE]

    def get_images(self) -> list[ContentBlock]:
        """Get all image blocks."""
        return [b for b in self.blocks if b.content_type == ContentType.IMAGE]

    def get_headings(self) -> list[ContentBlock]:
        """Get all heading blocks."""
        return [b for b in self.blocks if b.content_type == ContentType.HEADING]

    def get_statistics(self) -> list[ContentBlock]:
        """Get all statistic blocks."""
        return [b for b in self.blocks if b.content_type == ContentType.STATISTIC]
