# Cargill PPTX Converter

Transform any document into a professional Cargill-branded PowerPoint presentation.

## Supported Input Formats

| Format | Extensions |
|--------|-----------|
| Microsoft Word | `.docx`, `.doc` |
| PDF | `.pdf` |
| PowerPoint | `.pptx`, `.ppt` |
| Plain Text | `.txt` |
| Markdown | `.md`, `.markdown` |
| CSV | `.csv` |
| Excel | `.xlsx`, `.xls` |

## Installation

```bash
cd cargill-pptx-converter
pip install -e .
```

Or with Poetry:

```bash
poetry install
```

## Usage

### CLI

```bash
# Convert a document
cargill-pptx convert document.docx

# Convert with custom output path
cargill-pptx convert report.pdf -o branded_report.pptx

# Use fallback fonts (if brand fonts not installed)
cargill-pptx convert document.docx --fallback-fonts

# Verify brand compliance on existing PPTX
cargill-pptx verify presentation.pptx

# List supported formats
cargill-pptx formats
```

### Python API

```python
from src.orchestrator.pipeline import convert_document
from src.schemas.run_state import RunConfig

# Basic conversion
state = convert_document("input.docx")
print(f"Output: {state.output_file}")

# With configuration
config = RunConfig(
    max_words_per_slide=120,
    max_bullets_per_slide=6,
    use_brand_fonts=False,  # Use fallback fonts
)
state = convert_document("report.pdf", output_path="branded.pptx", config=config)
```

## Architecture

The converter uses a multi-agent pipeline:

1. **Content Extraction** - Parses input document into structured content blocks
2. **Brand Compliance** - Checks terminology and tone against Cargill guidelines
3. **Slide Architecture** - Maps content to optimal slide templates and layouts
4. **Visual Design** - Applies Cargill colors, typography, and spacing
5. **Chart Building** - Creates brand-compliant data visualizations
6. **Quality Assurance** - Verifies 100% brand compliance
7. **PPTX Rendering** - Generates the final PowerPoint file

## Brand Guidelines

All presentations follow the official Cargill brand specifications:

- **Colors**: Cargill Leaf Green (#00843D) as primary, with approved palette
- **Typography**: Big Caslon for headings, Helvetica Now for body text
- **Spacing**: Defined scale from 2px to 80px
- **Corner Radius**: 8px, 16px, or 24px only
- **Icons**: Google Material Rounded style
- **Personality**: Optimistic, curious, courageous, compassionate, humble

## ChatGPT Enterprise GPT

See [CHATGPT_GPT_BUILDER.md](CHATGPT_GPT_BUILDER.md) for instructions on
deploying this as a custom GPT within ChatGPT Enterprise.

## Project Structure

```
cargill-pptx-converter/
├── src/
│   ├── agents/          # Pipeline agents (7 steps)
│   ├── brand/           # Brand constants, palette, terminology
│   ├── cli/             # CLI entry point
│   ├── extractors/      # Document format extractors
│   ├── orchestrator/    # Pipeline orchestration
│   ├── schemas/         # Pydantic data models
│   └── utils/           # Shared utilities
├── config/              # YAML configuration
├── data/                # Input/output directories
├── tests/               # Test suite
└── pyproject.toml       # Package configuration
```
