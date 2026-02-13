"""
Base extractor interface for all document format extractors.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from src.schemas.content import ExtractedContent


class BaseExtractor(ABC):
    """Abstract base class for document extractors."""

    @abstractmethod
    def extract(self, file_path: Path) -> ExtractedContent:
        """
        Extract structured content from a document.

        Args:
            file_path: Path to the input document.

        Returns:
            ExtractedContent with all blocks, metadata, and warnings.
        """
        ...

    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return list of supported file extensions (e.g., ['.docx'])."""
        ...
