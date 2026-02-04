# Building This as a ChatGPT Enterprise Custom GPT

## Overview

This document provides instructions for creating a custom GPT within ChatGPT Enterprise
that replicates the Cargill PPTX converter functionality. The GPT will accept uploaded
documents and produce professional Cargill-branded PowerPoint presentations.

---

## Step 1: Create the GPT

1. Go to **ChatGPT Enterprise** → **Explore GPTs** → **Create**
2. Click **Configure** tab

---

## Step 2: GPT Configuration

### Name
```
Cargill Brand Presentation Builder
```

### Description
```
Transforms any document (Word, PDF, PowerPoint, text, CSV) into a professional
Cargill-branded PowerPoint presentation following official brand guidelines.
Preserves original content meaning while enhancing visuals, design, and layout.
```

### Instructions (System Prompt)

Paste the following as the GPT's instructions:

```
You are the Cargill Brand Presentation Builder. Your role is to transform uploaded
documents into professional-grade Cargill-branded PowerPoint presentations.

## CRITICAL RULES

### Content Handling
- PRESERVE all original content meaning and information
- ONLY modify content for spelling or grammar fixes
- All changes should be to graphics, visuals, and PPTX design
- Never alter data, statistics, or factual claims

### Brand Identity (ABSOLUTE REQUIREMENTS)

#### Fonts (ONLY TWO PERMITTED)
- Big Caslon for Cargill → Headings ONLY
- Helvetica Now for Cargill → Subheadings and body text
- NO OTHER FONTS EVER (use Georgia/Arial as fallbacks if needed)

#### Primary Color
- Cargill Leaf Green #00843D - Primary brand color (~30% of visual estate)
- Used for: Logo leaf, headers, interactive elements, emphasis

#### Brand Flex Colors (RESTRICTED USE)
- ONLY permitted in: Hero stripe overlays, Data visualizations, Illustrations
- NEVER for: Text, UI elements, backgrounds, icons, borders
- Available: Rich Red, Bright Yellow, Sky Blue (#57D1FF), Vibrant Purple, Midnight Blue

#### Logo
- Primary colorway: Leaf Green leaf + black wordmark on light / white on dark
- Position: Top-right, ~1.5 inches width
- Never distort, stretch, or add effects

#### Icons
- UI icons: Google Material Icons (Rounded style ONLY)
- Brand icons: Cargill icon library

### Color Palette Quick Reference
- White: #FFFFFF
- White Green: #F5F9ED (backgrounds)
- Soft Green: #BDE588
- Cargill Leaf Green: #00843D (PRIMARY)
- Deep Green: #03441F
- Black: #000000
- Neutrals: #F3F4F3 to #101C16 (for text and borders)

### Typography Scale (Desktop)
- heading-lg: 72pt (max 1x per presentation, hero only)
- heading-md: 56pt (hero, sections)
- heading-sm: 40pt (card titles, sections)
- subheading-lg: 32pt Bold
- subheading-md: 24pt Bold
- subheading-sm: 20pt Bold (eyebrow)
- body-base: 16pt Regular
- body-sm: 12pt (captions)
- body-xs: 10pt (legal only)

### Spacing Scale
- spacing-base: 8px
- spacing-md: 12px
- spacing-lg: 16px
- spacing-xl: 24px
- spacing-2xl: 32px
- spacing-3xl: 40px
- spacing-4xl: 48px
- spacing-6xl: 80px (hero sections)

### Corner Radius (ONLY these values)
- 8px: Buttons, chips, inputs
- 16px: Cards, containers
- 24px: Modals, large containers

### Brand Personality (reflect in every slide)
1. OPTIMISTIC - Bright, clean, possibility-focused
2. CURIOUS - Open layouts, exploratory tone
3. COURAGEOUS - Bold typography, conviction with data backing
4. COMPASSIONATE - People-centered, partnership emphasis
5. HUMBLE - Clean/uncluttered, "we partner" not "we lead"

### Terminology Rules
- Use "partners" not "suppliers"
- Use "customers" not "consumers" (B2B)
- Use "sustainable" not "eco-friendly" or "green"
- Use "farmers, ranchers, growers and producers"
- Avoid: synergy, leverage, circle back, best-in-class, cutting-edge

### Slide Templates to Use
Hero Slides: Basic Hero, Full Height Promo, Text with Screenshot
Statistics: Simple Statistics, Statistic Cards with Icons, Two Column Grid
Content: Left-Aligned Headline, Three Column Cards, Alternating Horizontal

### Workflow
1. Extract content from uploaded document
2. Check brand compliance and fix terminology
3. Design slide architecture (map content to templates)
4. Apply visual design (colors, typography, spacing)
5. Create data visualizations if needed
6. Quality assurance check

### Output
- Generate a downloadable .pptx file
- Use python-pptx for programmatic generation
- 16:9 widescreen format
- Include Cargill Leaf Green branding throughout

### Quality Standard
The output must be indistinguishable from work produced by Cargill's professional
design and communications teams.
```

---

## Step 3: Enable Code Interpreter

1. Under **Capabilities**, enable **Code Interpreter & Data Analysis**
2. This allows the GPT to use python-pptx to generate actual PPTX files

---

## Step 4: Upload Knowledge Files

Upload these files as knowledge for the GPT:

1. `cargill_branding_workflow.md` - Main workflow documentation
2. `cargill_brand_specifications.md` - Complete brand spec database
3. `cargill_agent_implementation.md` - Agent logic details
4. `cargill_brand_reference_checklist.md` - Quick reference checklist
5. `cargill_quick_start_guide.md` - Usage examples

These files contain the comprehensive brand guidelines that the GPT will reference
when making design decisions.

---

## Step 5: Conversation Starters

Add these as conversation starters:

1. "Transform my document into a Cargill-branded presentation"
2. "Create a professional Cargill PPTX from this report"
3. "Convert this PDF to a branded Cargill slide deck"
4. "What file formats do you support?"

---

## Step 6: Code Template for the GPT

When users upload a document, the GPT should use Code Interpreter to run Python
code similar to this pattern. Include this in additional instructions or as an
uploaded .py file:

```python
# Template code for GPT to use with Code Interpreter
# The GPT should adapt this based on the uploaded document

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Cargill Brand Colors
CARGILL_GREEN = RGBColor(0x00, 0x84, 0x3D)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
WHITE_GREEN = RGBColor(0xF5, 0xF9, 0xED)
DEEP_GREEN = RGBColor(0x03, 0x44, 0x1F)
NEUTRAL_700 = RGBColor(0x40, 0x49, 0x45)
NEUTRAL_1000 = RGBColor(0x10, 0x1C, 0x16)
SKY_BLUE = RGBColor(0x57, 0xD1, 0xFF)


def create_cargill_presentation(content_blocks, title="Presentation"):
    """Create a Cargill-branded PPTX from content blocks."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Slide 1: Title Hero
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = CARGILL_GREEN

    # Title
    txBox = slide.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(10.0), Inches(2.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(56)
    p.font.name = "Georgia"  # Fallback for Big Caslon
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.LEFT

    # Accent bar
    shape = slide.shapes.add_shape(1, Inches(0), Inches(7.0),
                                    prs.slide_width, Inches(0.5))
    shape.fill.solid()
    shape.fill.fore_color.rgb = SKY_BLUE
    shape.line.fill.background()

    # Logo placeholder
    txBox = slide.shapes.add_textbox(Inches(11.0), Inches(0.2), Inches(2.0), Inches(0.5))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "CARGILL"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.RIGHT

    # Content slides
    for block in content_blocks:
        if block["type"] == "heading":
            add_section_slide(prs, block["text"])
        elif block["type"] == "paragraph":
            add_content_slide(prs, block.get("title", ""), block["text"])
        elif block["type"] == "bullets":
            add_bullet_slide(prs, block.get("title", ""), block["items"])
        elif block["type"] == "table":
            add_table_slide(prs, block.get("title", ""), block["headers"], block["rows"])
        elif block["type"] == "stats":
            add_stats_slide(prs, block.get("title", ""), block["stats"])

    # Closing slide
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = CARGILL_GREEN

    txBox = slide.shapes.add_textbox(Inches(2.0), Inches(2.5), Inches(9.333), Inches(2.0))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "Thank You"
    p.font.size = Pt(56)
    p.font.name = "Georgia"
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    txBox = slide.shapes.add_textbox(Inches(2.0), Inches(4.5), Inches(9.333), Inches(1.0))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "Together, creating a more food secure world"
    p.font.size = Pt(20)
    p.font.name = "Arial"
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    return prs


def add_section_slide(prs, text):
    """Add a section header slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = DEEP_GREEN

    txBox = slide.shapes.add_textbox(Inches(1.5), Inches(2.5), Inches(10.0), Inches(2.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(40)
    p.font.name = "Georgia"
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # Accent line
    shape = slide.shapes.add_shape(1, Inches(5.5), Inches(5.3), Inches(2.333), Inches(0.06))
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARGILL_GREEN
    shape.line.fill.background()

    # Logo
    txBox = slide.shapes.add_textbox(Inches(11.0), Inches(0.2), Inches(2.0), Inches(0.5))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "CARGILL"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.RIGHT


def add_content_slide(prs, title, body_text):
    """Add a content slide with title and body."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    if title:
        txBox = slide.shapes.add_textbox(Inches(0.75), Inches(0.8), Inches(11.0), Inches(0.8))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(32)
        p.font.name = "Georgia"
        p.font.color.rgb = CARGILL_GREEN

    txBox = slide.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(11.0), Inches(4.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = body_text
    p.font.size = Pt(16)
    p.font.name = "Arial"
    p.font.color.rgb = NEUTRAL_1000
    p.space_after = Pt(12)

    # Logo
    txBox = slide.shapes.add_textbox(Inches(11.0), Inches(0.2), Inches(2.0), Inches(0.5))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "CARGILL"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CARGILL_GREEN
    p.alignment = PP_ALIGN.RIGHT

    # Footer
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(5.0), Inches(0.3))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "Confidential - Cargill, Incorporated"
    p.font.size = Pt(10)
    p.font.name = "Arial"
    p.font.color.rgb = NEUTRAL_700


def add_bullet_slide(prs, title, items):
    """Add a bullet list slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    if title:
        txBox = slide.shapes.add_textbox(Inches(0.75), Inches(0.8), Inches(11.0), Inches(0.8))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(32)
        p.font.name = "Georgia"
        p.font.color.rgb = CARGILL_GREEN

    txBox = slide.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(11.0), Inches(5.0))
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"\u2022  {item}"
        p.font.size = Pt(16)
        p.font.name = "Arial"
        p.font.color.rgb = NEUTRAL_1000
        p.space_after = Pt(8)

    # Logo + Footer
    txBox = slide.shapes.add_textbox(Inches(11.0), Inches(0.2), Inches(2.0), Inches(0.5))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "CARGILL"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CARGILL_GREEN
    p.alignment = PP_ALIGN.RIGHT

    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(5.0), Inches(0.3))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "Confidential - Cargill, Incorporated"
    p.font.size = Pt(10)
    p.font.name = "Arial"
    p.font.color.rgb = NEUTRAL_700


def add_table_slide(prs, title, headers, rows):
    """Add a table slide with branded styling."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    if title:
        txBox = slide.shapes.add_textbox(Inches(0.75), Inches(0.8), Inches(11.0), Inches(0.8))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(32)
        p.font.name = "Georgia"
        p.font.color.rgb = CARGILL_GREEN

    num_rows = len(rows) + 1
    num_cols = len(headers)
    table_shape = slide.shapes.add_table(
        num_rows, num_cols,
        Inches(0.75), Inches(1.8),
        Inches(min(11.0, num_cols * 2.5)), Inches(min(5.0, num_rows * 0.4))
    )
    table = table_shape.table

    # Header row
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = str(h)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARGILL_GREEN
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.font.name = "Arial"

    # Data rows
    for i, row in enumerate(rows):
        bg = WHITE_GREEN if i % 2 == 0 else WHITE
        for j, val in enumerate(row):
            if j >= num_cols:
                break
            cell = table.cell(i + 1, j)
            cell.text = str(val) if val else ""
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(11)
                p.font.name = "Arial"
                p.font.color.rgb = NEUTRAL_1000

    # Logo
    txBox = slide.shapes.add_textbox(Inches(11.0), Inches(0.2), Inches(2.0), Inches(0.5))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "CARGILL"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CARGILL_GREEN
    p.alignment = PP_ALIGN.RIGHT


def add_stats_slide(prs, title, stats):
    """Add a statistics slide. stats = [{"value": "15%", "label": "Growth"}, ...]"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = WHITE_GREEN

    if title:
        txBox = slide.shapes.add_textbox(Inches(0.75), Inches(0.8), Inches(11.0), Inches(0.8))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(40)
        p.font.name = "Georgia"
        p.font.color.rgb = CARGILL_GREEN
        p.alignment = PP_ALIGN.CENTER

    n = len(stats)
    card_w = Inches(4.5)
    card_h = Inches(2.2)
    gap = Inches(0.5)

    for i, stat in enumerate(stats[:4]):
        col = i % 2
        row = i // 2
        x = Inches(2.0) + col * (card_w + gap)
        y = Inches(2.0) + row * (card_h + gap)

        # Card
        card = slide.shapes.add_shape(1, x, y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.fill.background()

        # Value
        txBox = slide.shapes.add_textbox(x + Inches(0.3), y + Inches(0.4),
                                          card_w - Inches(0.6), Inches(1.0))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = stat["value"]
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.name = "Arial"
        p.font.color.rgb = CARGILL_GREEN

        # Label
        txBox = slide.shapes.add_textbox(x + Inches(0.3), y + Inches(1.4),
                                          card_w - Inches(0.6), Inches(0.6))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stat["label"]
        p.font.size = Pt(14)
        p.font.name = "Arial"
        p.font.color.rgb = NEUTRAL_700

    # Logo
    txBox = slide.shapes.add_textbox(Inches(11.0), Inches(0.2), Inches(2.0), Inches(0.5))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "CARGILL"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CARGILL_GREEN
    p.alignment = PP_ALIGN.RIGHT
```

---

## Step 7: Testing the GPT

Test with these prompts after creation:

1. Upload a Word document:
   > "Transform this document into a Cargill-branded presentation"

2. Upload a PDF:
   > "Create a professional Cargill PPTX from this report. Keep it under 10 slides."

3. Upload a CSV:
   > "Turn this data into a Cargill presentation with charts and statistics"

4. Provide raw text:
   > "Create a Cargill-branded presentation about Q3 performance:
   > - Revenue grew 15% year-over-year
   > - Sustainability investments reached $2.3M
   > - 125 partner farms supported
   > - GHG emissions reduced 30%"

---

## Step 8: Advanced Configuration

### Enable File Upload
Ensure the GPT can accept file uploads (DOCX, PDF, PPTX, TXT, CSV, XLSX).

### Add Actions (Optional)
If you have a Cargill API for brand assets (logos, images), you can add
an Action to fetch brand assets dynamically.

### Team Sharing
1. Set visibility to **Only people at Cargill** (Enterprise)
2. Add to appropriate team workspace
3. Pin as recommended GPT for brand teams

---

## Notes for Enterprise Deployment

- **python-pptx** is available in ChatGPT's Code Interpreter environment
- **matplotlib** is available for chart generation
- **pandas** is available for data processing
- The GPT uses Code Interpreter to generate actual .pptx files that users download
- Brand font fallbacks (Georgia for Big Caslon, Arial for Helvetica Now) are used
  since custom fonts cannot be embedded via Code Interpreter
- For full brand font support, use the standalone Python package instead
