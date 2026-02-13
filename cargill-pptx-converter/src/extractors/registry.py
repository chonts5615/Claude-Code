"""
Extractor registry - routes file types to appropriate extractors.
"""

from pathlib import Path

from src.extractors.base import BaseExtractor
from src.extractors.docx_extractor import DocxExtractor
from src.extractors.pdf_extractor import PdfExtractor
from src.extractors.pptx_extractor import PptxExtractor
from src.extractors.tabular_extractor import TabularExtractor
from src.extractors.text_extractor import TextExtractor
from src.schemas.content import ExtractedContent


# Map file extensions to extractor classes
EXTRACTOR_MAP: dict[str, type[BaseExtractor]] = {
    ".docx": DocxExtractor,
    ".doc": DocxExtractor,
    ".pdf": PdfExtractor,
    ".pptx": PptxExtractor,
    ".ppt": PptxExtractor,
    ".txt": TextExtractor,
    ".md": TextExtractor,
    ".markdown": TextExtractor,
    ".text": TextExtractor,
    ".csv": TabularExtractor,
    ".xlsx": TabularExtractor,
    ".xls": TabularExtractor,
}

# Supported format descriptions
SUPPORTED_FORMATS = {
    ".docx": "Microsoft Word Document",
    ".doc": "Microsoft Word Document (Legacy)",
    ".pdf": "PDF Document",
    ".pptx": "Microsoft PowerPoint",
    ".ppt": "Microsoft PowerPoint (Legacy)",
    ".txt": "Plain Text",
    ".md": "Markdown",
    ".markdown": "Markdown",
    ".csv": "Comma-Separated Values",
    ".xlsx": "Microsoft Excel",
    ".xls": "Microsoft Excel (Legacy)",
}


def get_extractor(file_path: str | Path) -> BaseExtractor:
    """
    Get the appropriate extractor for a file based on its extension.

    Args:
        file_path: Path to the input file.

    Returns:
        An initialized extractor instance.

    Raises:
        ValueError: If the file format is not supported.
    """
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext not in EXTRACTOR_MAP:
        supported = ", ".join(sorted(EXTRACTOR_MAP.keys()))
        raise ValueError(
            f"Unsupported file format: '{ext}'. "
            f"Supported formats: {supported}"
        )

    return EXTRACTOR_MAP[ext]()


def extract_content(file_path: str | Path) -> ExtractedContent:
    """
    Extract content from a file using the appropriate extractor.

    Args:
        file_path: Path to the input file.

    Returns:
        ExtractedContent with structured content blocks.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    extractor = get_extractor(path)
    return extractor.extract(path)


def is_supported_format(file_path: str | Path) -> bool:
    """Check if a file format is supported."""
    ext = Path(file_path).suffix.lower()
    return ext in EXTRACTOR_MAP


def get_format_description(file_path: str | Path) -> str:
    """Get a human-readable description of the file format."""
    ext = Path(file_path).suffix.lower()
    return SUPPORTED_FORMATS.get(ext, "Unknown format")
