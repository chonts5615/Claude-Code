# Cargill Brand PPTX Workflow System

Complete documentation of the multi-agent workflow that transforms input documents into professional Cargill-branded PowerPoint presentations.

---

## System Overview

This workflow accepts any input document and produces a presentation that is indistinguishable from work produced by Cargill's professional design and communications teams.

### Supported Input Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| Microsoft Word | .docx, .doc | Full text, tables, headings extracted |
| PDF | .pdf | Text extraction; complex layouts simplified |
| PowerPoint | .pptx, .ppt | Content extracted; design replaced with brand |
| Plain Text | .txt | Structured by paragraph breaks |
| Markdown | .md | Headings and formatting preserved |
| Excel | .xlsx, .xls | Data tables extracted as structured data |
| CSV | .csv | Tabular data for statistics and charts |

### Core Principle

- **PRESERVE**: All original content meaning and information
- **FIX ONLY**: Spelling errors, grammar mistakes, non-brand terminology
- **TRANSFORM**: All graphics, visuals, layouts, and design elements

---

## Workflow Stages

### Stage 1: Intake and Analysis

```
Input Document
    ↓
Content Extraction Agent
    ↓  Outputs: Structured content object with hierarchy,
    ↓  data elements, key messages, section map
    ↓
Brand Compliance Agent (Initial Assessment)
    ↓  Outputs: Corrected terminology, personality scores,
    ↓  compliance warnings
    ↓
Content Classification and Requirements Document
```

**What happens in Stage 1:**
- Document is parsed by the appropriate extractor
- All text, tables, statistics, and metadata are captured
- Content is organized into a hierarchy (H1, H2, H3, body)
- Problematic terminology is auto-corrected (e.g., "suppliers" → "partners")
- Tone is scored against Cargill's 5 personality traits
- A requirements document is generated: slide count estimate, template needs, data viz needs

---

### Stage 2: Architecture and Planning

```
Requirements Document
    ↓
Slide Architecture Agent
    ↓  Outputs: Slide-by-slide plan with template assignments
    ↓  and content mapping
    ↓
Visual Design Agent (Template and Color Selection)
    ↓  Outputs: Design blueprint with color schemes,
    ↓  typography specs, spacing plan for each slide
    ↓
Design Blueprint
```

**What happens in Stage 2:**
- Content is mapped to slide templates using selection logic
- Slide sequence is established (hero → content → data → content → closing)
- Each slide gets an assigned template, color scheme, and typography specification
- Data slides are identified for chart generation

---

### Stage 3: Content Transformation

```
Design Blueprint
    ↓
Content Population (text into templates)
    ↓  Typography standards applied
    ↓  Heading sizes assigned (heading-lg, heading-md, heading-sm)
    ↓  Body text sized to body-base (16pt)
    ↓
Data Visualization Agent
    ↓  Outputs: PNG chart images embedded in chart slides
    ↓  Brand-compliant colors, fonts, grid lines
    ↓
Raw Slide Content Ready
```

**What happens in Stage 3:**
- Each slide is populated with its assigned content
- Typography scale is applied (headings get Big Caslon sizes, body gets Helvetica Now 16pt)
- Tables are formatted with Cargill brand table styles
- Data tables and statistics are sent to the Chart Builder agent
- Charts are generated using brand color sequences, font specs, and grid styling

---

### Stage 4: Visual Enhancement

```
Raw Slides
    ↓
Visual Design Agent (Final Pass)
    ↓  Logo placement: correct colorway for each background
    ↓  Color application: brand palette throughout
    ↓  Corner radius: 8px, 16px, or 24px applied to all shapes
    ↓  Spacing: all padding/margins aligned to spacing scale
    ↓  Graphical devices: leaf element on hero slides
    ↓
Visually Enhanced Slides
```

**What happens in Stage 4:**
- Logo is placed on every slide in the correct colorway (black/green on light, white on dark)
- All shape colors verified against approved palette
- Corner radius corrected to nearest approved value (8/16/24px)
- Spacing tokens applied to all elements
- Leaf graphical device added to opening hero (used sparingly, not on every slide)
- Brand flex colors verified to only appear in hero stripes, data viz, and illustrations

---

### Stage 5: Final Assembly and QA

```
Enhanced Slides
    ↓
Quality Assurance Agent
    ↓  Brand compliance check: 100-point scoring
    ↓  Content quality check: terminology, spelling, personality
    ↓  Visual quality check: alignment, hierarchy, consistency
    ↓  Accessibility check: contrast ratios, text sizes
    ↓
PPTX Builder Agent
    ↓  Renders final .pptx using python-pptx
    ↓
Final Cargill-Branded PowerPoint (.pptx)
```

**What happens in Stage 5:**
- QA agent runs all compliance checks and produces a score (aim for 95%+)
- Any issues below threshold trigger auto-correction
- PPTX Builder renders each slide to python-pptx objects
- Final file is saved as .pptx in 16:9 widescreen format

---

## Slide Sequence Guidelines

### Recommended Deck Structure

| Position | Slide Type | Template |
|----------|------------|----------|
| 1 | Opening hero | Full Height Promo or Basic Hero |
| 2 | Key statistics | Statistic Cards with Icons |
| 3 | Section divider | Section Divider |
| 4-6 | Content slides | Left-Aligned Headline |
| 7 | Data visualization | Chart Slide |
| 8 | Section divider (if needed) | Section Divider |
| 9-10 | Additional content | Three Column Cards or Alternating Horizontal |
| Last | Closing | Closing Slide (Leaf Green background) |

### Slide Count Guidelines

- **Short document (1-5 pages)**: 5-8 slides
- **Medium document (5-15 pages)**: 8-12 slides
- **Long document (15+ pages)**: 12-20 slides (maximum recommended: 20)
- **Executive presentation**: Target 8-10 slides regardless of source length

---

## Example Workflow Execution

**Input**: Word document - Q3 Sales Analysis (12 pages, 3 data tables, 5 sections, 3,500 words)

### Stage 1 Output

Content extracted:
- 5 main sections identified
- 3 data tables extracted
- 8 key statistics found
- Primary message: "Q3 exceeded all targets through sustainable practices"
- Terminology corrections: 3 instances of "suppliers" → "partners"
- Personality scores: Optimistic 88, Curious 72, Courageous 85, Compassionate 91, Humble 78

### Stage 2 Output

Slide plan:
- Slide 1: Full Height Promo hero - "Q3 2025: Delivering on Our Purpose"
- Slide 2: Statistic Cards with Icons - 4 key metrics
- Slide 3: Section Divider - "Regional Performance"
- Slide 4: Table Slide - Regional breakdown data
- Slide 5: Chart Slide - Year-over-year comparison bar chart
- Slide 6: Section Divider - "Sustainability Impact"
- Slide 7: Statistic Cards with Icons - Environmental metrics
- Slide 8: Three Column Cards - Success factors
- Slide 9: Closing - "Thank You"

### Stage 3 Output

- All text assigned typography specs
- Q3 comparison chart generated: grouped bar, Leaf Green + Midnight Blue mid (#003266)
- Regional table formatted: green header, alternating row colors

### Stage 4 Output

- Hero: Sky Blue (#57D1FF) flex color stripe, white logo, leaf device
- Stats slides: White Green background (#F5F9ED), white cards, green numbers
- Content slides: White background, green headlines, neutral body text
- Logo: Leaf Green leaf + black wordmark on light slides, white on dark

### Stage 5 Output

- QA score: 96/100
- Warnings: 1 corner radius adjusted (12px → 16px on slide 4 card)
- Status: Approved
- Final .pptx saved

---

## Quality Standard

**The output must be indistinguishable from work produced by Cargill's professional design and communications teams.**

Every presentation must demonstrate:

- Perfect brand compliance (correct colors, fonts, spacing, logo)
- Professional polish and refinement
- Clear brand personality (optimistic, curious, courageous, compassionate, humble)
- Logical structure and narrative flow
- High-quality visual layout
- Accessibility compliance (contrast ratios, text sizes)
- Consistent execution throughout all slides

**If any element does not meet this standard, it must be revised before delivery.**

---

## Brand Compliance Rules Summary

### Color Rules

1. Cargill Leaf Green (#00843D) is the primary brand color - use it for ~30% of visual estate
2. White (#FFFFFF) and White Green (#F5F9ED) for backgrounds
3. Neutral palette for text and borders
4. Brand flex colors ONLY in: hero stripe overlays, data visualizations, illustrations
5. Brand flex colors NEVER in: text, UI elements, general backgrounds, icons, borders

### Typography Rules

1. Only two fonts: Big Caslon for Cargill (headings) and Helvetica Now for Cargill (body/subheadings)
2. Heading sizes: 72pt (hero max 1x), 56pt (hero/section), 40pt (cards/section)
3. Body minimum: 16pt
4. Legal text minimum: 10pt

### Layout Rules

1. Slide dimensions: 16:9 (13.333" x 7.5")
2. Corner radius: 8px (buttons), 16px (cards), 24px (containers/modals)
3. Spacing from defined scale only (multiples of 4px, specific tokens)
4. Logo: Every slide, top-right, correct colorway

### Content Rules

1. Never alter original facts, data, or statistics
2. Only fix: spelling errors, grammar mistakes, non-brand terminology
3. Never rewrite or summarize content beyond slide condensing
4. Maintain all source attribution and context
