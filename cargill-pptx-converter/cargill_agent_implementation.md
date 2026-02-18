# Cargill Agent Implementation Guide

Detailed implementation logic for each of the 7 agents in the document-to-PPTX conversion pipeline.

---

## Agent Architecture Overview

The pipeline consists of 7 sequential agents. Each receives the full state object from the previous agent, processes its domain, and passes the enriched state forward.

```
Input Document
    ↓
Agent 1: Content Extraction
    ↓
Agent 2: Brand Compliance
    ↓
Agent 3: Slide Architecture
    ↓
Agent 4: Visual Design
    ↓
Agent 5: Data Visualization (Chart Builder)
    ↓
Agent 6: Quality Assurance
    ↓
Agent 7: PPTX Builder
    ↓
Output .pptx file
```

---

## Agent 1: Content Extraction Agent

### Purpose
Extract and structure all content from input documents regardless of format.

### Input Formats Supported
- Microsoft Word (.doc, .docx)
- PDF (.pdf)
- PowerPoint (.ppt, .pptx) - content extraction only, no design reuse
- Plain text (.txt)
- Markdown (.md)
- CSV/Excel (.csv, .xlsx) - data extraction

### Processing Logic

1. Detect file format from extension
2. Select appropriate parser (python-docx, pypdf, python-pptx, markdown, pandas)
3. Extract content hierarchy (headings, subheadings, body)
4. Identify data elements (tables, statistics, lists)
5. Extract key messages (most prominent statements)
6. Count slides needed based on content volume

### Output Format

```json
{
  "document_metadata": {
    "title": "Q3 2025 Sales Report",
    "author": "Sales Team",
    "page_count": 12,
    "word_count": 3500,
    "has_images": true,
    "has_tables": true
  },
  "content_hierarchy": [
    {"level": 1, "type": "heading", "text": "Q3 2025 Performance Overview"},
    {"level": 2, "type": "heading", "text": "Regional Breakdown"},
    {"level": 3, "type": "body", "text": "North America exceeded targets by 15%..."}
  ],
  "data_elements": {
    "tables": [
      {
        "table_id": "table_1",
        "headers": ["Region", "Target", "Actual", "Variance"],
        "data": [
          ["North America", "$1.2B", "$1.38B", "+15%"],
          ["EMEA", "$0.8B", "$0.84B", "+5%"]
        ]
      }
    ],
    "statistics": [
      {"value": "15%", "label": "Growth over Q2", "context": "North America"},
      {"value": "$2.3M", "label": "Sustainability investments"}
    ]
  },
  "key_messages": [
    {"text": "Q3 exceeded all targets through sustainable practices", "importance": "primary"},
    {"text": "125 partner farms supported this quarter", "importance": "secondary"}
  ],
  "sections": [
    {"title": "Executive Summary", "word_count": 250, "section_type": "summary"},
    {"title": "Regional Performance", "word_count": 600, "section_type": "data"},
    {"title": "Sustainability Impact", "word_count": 400, "section_type": "narrative"}
  ]
}
```

### Content Limits

- Maximum words per slide: 150 (configurable, default 150)
- Recommended slides: 8-12 for most documents
- Maximum slides: 20

---

## Agent 2: Brand Compliance Agent

### Purpose
Ensure all content aligns with Cargill brand guidelines before design begins. Fix terminology and assess tone.

### Processing Steps

1. **Terminology Check**: Scan all text for problematic terms and apply corrections
2. **Tone Analysis**: Score content against 5 personality traits
3. **Message Alignment**: Check alignment with Cargill purpose statement
4. **Grammar/Spelling**: Flag errors for correction (content, not rewriting)

### Terminology Corrections (Auto-Apply)

```json
{
  "suppliers": "partners",
  "supplier": "partner",
  "consumers": "customers",
  "consumer": "customer",
  "eco-friendly": "sustainable",
  "green solution": "sustainable solution",
  "synergy": "collaboration",
  "leverage": "use",
  "leveraging": "using",
  "best-in-class": "leading",
  "cutting-edge": "innovative",
  "circle back": "follow up",
  "move the needle": "make progress",
  "solutions provider": "partner"
}
```

### Personality Trait Scoring

Score each section 0-100 on how well it reflects each trait:

**Optimistic** (possibility, future-forward):
- Positive indicators: "possibility", "opportunity", "future", "create", "enable", "potential", "grow", "thrive"
- Negative indicators: "problem", "challenge", "difficulty", "obstacle", "struggle", "fail"
- Score: (positive_count / total_sentences) * 100

**Curious** (exploration, questioning):
- Positive indicators: "explore", "discover", "question", "what if", "how might", "learn", "understand"
- Negative indicators: "always", "never", "absolutely", "definitely", "certain" (when used rigidly)

**Courageous** (conviction, boldness):
- Positive indicators: "commit", "bold", "leading", "innovative", "transform", "invest", "dedicated"
- Negative indicators: "might", "perhaps", "possibly", "uncertain", "maybe"

**Compassionate** (people-first, partnership):
- Positive indicators: "partner", "support", "together", "care", "people", "community", "farmers", "families"
- Negative indicators: "dominate", "control", "force", "demand", "require"

**Humble** (collaborative, not boastful):
- Positive indicators: "collaborate", "listen", "learn", "respect", "together", "we partner", "we work with"
- Negative indicators: "best", "superior", "dominate", "number one", "we lead", "we are the"

### Output Format

```json
{
  "compliance_score": 94,
  "terminology_corrections": [
    {"original": "suppliers", "corrected": "partners", "count": 3}
  ],
  "personality_scores": {
    "optimistic": 88,
    "curious": 72,
    "courageous": 85,
    "compassionate": 91,
    "humble": 78
  },
  "warnings": [
    "Use of 'best-in-class' detected on page 3 - corrected to 'leading'",
    "Courageous score below 80 - consider strengthening conviction in messaging"
  ],
  "corrected_content": { ... }
}
```

---

## Agent 3: Slide Architecture Agent

### Purpose
Design optimal slide structure, sequence, and layout selection based on extracted content.

### Available Templates

**Hero Slides**:
- `basic_hero`: Image background with text overlay. Best for: Opening slides, section dividers
- `text_with_screenshot`: Split layout showcasing product/interface. Best for: Product demos
- `full_height_promo`: Large format hero with prominent imagery. Best for: Major announcements

**Statistics Slides**:
- `simple_statistics`: Clean horizontal row of numbers (3-4 metrics)
- `statistic_cards_icons`: Statistics in cards with brand icons (4 metrics)
- `simple_with_headline`: Statistics preceded by contextual headline
- `two_column_grid`: Comparative statistics in grid (4-6 metrics)

**Content Slides**:
- `left_aligned_headline`: Standard section with left-aligned headline. Default content template.
- `centered_headline`: Symmetric layout with centered headline. Best for: Quotes, key statements
- `three_column_basic_cards`: Simple card grid for 3 items
- `three_column_rich_media`: Enhanced cards with images for 3 items
- `alternating_horizontal`: Image-text alternating for narrative flow

**Special Slides**:
- `section_divider`: Deep green background, centered heading, thin accent line
- `table_slide`: Branded data table with green header row
- `chart_slide`: Chart with headline, axis labels, data labels
- `closing_slide`: Leaf Green background, thank you message, tagline

### Template Selection Logic

```
IF section_type == "hero" or section_type == "announcement":
    IF has_high_quality_image AND is_major_announcement:
        use full_height_promo
    ELSE:
        use basic_hero

IF section_type == "data" and has_statistics:
    IF stat_count >= 4 AND stats_have_icon_potential:
        use statistic_cards_icons
    ELIF stat_count >= 4 AND stat_count <= 6:
        use two_column_grid
    ELSE:
        use simple_statistics

IF section_type == "table":
    use table_slide

IF section_type == "data" and has_chart_data:
    use chart_slide

IF section_type is new major section:
    INSERT section_divider before content slides

IF section content is list-based with exactly 3 items:
    IF items have images:
        use three_column_rich_media
    ELSE:
        use three_column_basic_cards

IF section is narrative with alternating image-text pairs:
    use alternating_horizontal

IF section is closing or conclusion:
    use closing_slide

DEFAULT:
    use left_aligned_headline
```

### Output Format

```json
{
  "total_slides": 9,
  "slide_plan": [
    {
      "slide_number": 1,
      "template": "full_height_promo",
      "title": "Q3 2025 Performance Overview",
      "content_summary": "Achievement headline with key metric",
      "content_source": "key_messages[0]"
    },
    {
      "slide_number": 2,
      "template": "statistic_cards_icons",
      "title": "Q3 Key Metrics",
      "statistics": ["15% growth", "$2.3M invested", "125 partners", "30% GHG reduction"],
      "content_source": "data_elements.statistics"
    },
    {
      "slide_number": 3,
      "template": "section_divider",
      "title": "Regional Performance"
    },
    {
      "slide_number": 4,
      "template": "table_slide",
      "title": "Regional Breakdown",
      "content_source": "data_elements.tables[0]"
    }
  ]
}
```

---

## Agent 4: Visual Design Agent

### Purpose
Apply Cargill visual identity elements to each slide according to the architecture plan.

### Color Scheme Application by Template

**Hero Slides**:
```json
{
  "primary": "#00843D",
  "accent_stripe": "[flex_color - Sky Blue #57D1FF recommended]",
  "background": "white or image",
  "headline": "#FFFFFF",
  "subheading": "#FFFFFF",
  "cta_button": {"background": "#00843D", "text": "white"}
}
```

**Statistics Slides**:
```json
{
  "slide_background": "#F5F9ED",
  "card_background": "#FFFFFF",
  "headline": "#00843D",
  "numbers": "#00843D",
  "labels": "#404945",
  "icons": "#00843D"
}
```

**Content Slides**:
```json
{
  "slide_background": "#FFFFFF",
  "headline": "#00843D",
  "subheading": "#012912",
  "body": "#101C16",
  "card_border": "#DBDDDC"
}
```

**Section Dividers**:
```json
{
  "background": "#03441F",
  "headline": "#FFFFFF",
  "accent_line": "#00843D"
}
```

**Closing Slide**:
```json
{
  "background": "#00843D",
  "headline": "#FFFFFF",
  "tagline": "#FFFFFF"
}
```

### Typography Application

| Context | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Hero headline | Big Caslon | 56-72pt | Regular | White |
| Section headline | Big Caslon | 40pt | Regular | Leaf Green |
| Card title | Big Caslon | 32pt | Regular | Leaf Green |
| Subheading | Helvetica Now | 24-32pt | Bold | Neutral-1000 |
| Body text | Helvetica Now | 16pt | Regular | Neutral-1000 |
| Captions | Helvetica Now | 12pt | Regular | Neutral-700 |
| Statistic numbers | Helvetica Now | 32pt | Bold | Leaf Green |
| Statistic labels | Helvetica Now | 16pt | Regular | Neutral-700 |

### Spacing Application

| Context | Spacing |
|---------|---------|
| Hero content padding | 80px (spacing-6xl) |
| Hero headline to body | 16px (spacing-lg) |
| Hero body to CTA | 32px (spacing-2xl) |
| Statistics slide padding | 48px (spacing-4xl) |
| Statistics card padding | 24px (spacing-xl) |
| Statistics card gap | 16px (spacing-lg) |
| Content slide padding | 40px (spacing-3xl) |
| Content headline margin bottom | 24px (spacing-xl) |
| Content paragraph spacing | 12px (spacing-md) |

### Logo Placement Rules

- **Light backgrounds**: Leaf Green leaf + black wordmark, top-right corner
- **Dark/Green backgrounds**: Leaf Green leaf + white wordmark, top-right corner
- **Size**: Approximately 1.5" width
- **Position**: Top-right, 0.2" from top, 0.3" from right edge

---

## Agent 5: Data Visualization (Chart Builder) Agent

### Purpose
Transform data tables and statistics into brand-compliant charts embedded in slides.

### Chart Type Selection

```
IF data is time-series (dates/periods in columns): use line_chart
IF data sums to approximately 100% AND categories <= 8: use pie_chart or donut_chart
IF categories <= 10: use vertical_bar_chart
IF categories 10-20: use horizontal_bar_chart
IF multiple groups over time: use grouped_bar_chart
IF single metric over time: use line_chart
DEFAULT: use vertical_bar_chart
```

### Brand Styling for Charts

```json
{
  "color_sequence": ["#00843D", "#BDE588", "#03441F", "#57D1FF", "#404945", "#81AB40"],
  "background": "#FFFFFF",
  "title_font": "Helvetica Now for Cargill Bold",
  "title_size": "24pt",
  "title_color": "#00843D",
  "axis_label_font": "Helvetica Now for Cargill Regular",
  "axis_label_size": "16pt",
  "axis_label_color": "#404945",
  "data_label_font": "Helvetica Now for Cargill Regular",
  "data_label_size": "12pt",
  "data_label_color": "#1C2722",
  "legend_font": "Helvetica Now for Cargill Regular",
  "legend_size": "16pt",
  "legend_color": "#404945",
  "grid_line_color": "#E7E8E8",
  "axis_line_color": "#DBDDDC"
}
```

### Chart Dimensions (for PPTX embedding)

- Chart width: 9.5 inches
- Chart height: 5.5 inches
- Position: Centered on slide, below headline

### Output

Chart is saved as PNG and embedded in the slide. Chart data also stored for potential interactive use.

---

## Agent 6: Quality Assurance Agent

### Purpose
Final comprehensive review ensuring brand compliance before PPTX generation.

### QA Scoring Categories

**Brand Compliance (40 points)**:
- Color accuracy: All colors from approved palette (10 pts)
- Typography compliance: Big Caslon + Helvetica Now only (10 pts)
- Logo usage: Correct colorway on all slides (5 pts)
- Icon compliance: Google Material Rounded only (5 pts)
- Spacing standards: From defined scale (5 pts)
- Corner radius: Only 8px, 16px, 24px (5 pts)

**Content Quality (30 points)**:
- No spelling/grammar errors (10 pts)
- Terminology compliance (10 pts)
- Brand personality alignment (10 pts)

**Visual Quality (20 points)**:
- Grid alignment (10 pts)
- Visual hierarchy (5 pts)
- Consistency throughout (5 pts)

**Accessibility (10 points)**:
- Color contrast ratios minimum 4.5:1 (5 pts)
- Minimum text size 16pt body (3 pts)
- Icon sizes minimum 24px (2 pts)

### Score Thresholds

| Score | Status |
|-------|--------|
| 100% | Perfect - ready for delivery |
| 95-99% | Minor warnings - acceptable |
| 80-94% | Approved with recommendations |
| Below 80% | Needs revision before delivery |

### Common Issues and Fixes

| Issue | Fix |
|-------|-----|
| Wrong font used | Replace with Big Caslon (headings) or Helvetica Now (body) |
| Flex color on text | Change text to neutral palette |
| Logo wrong colorway | Swap to correct version for background |
| Incorrect corner radius | Adjust to nearest approved value (8/16/24px) |
| Spacing not on scale | Round to nearest spacing token |
| "suppliers" in text | Replace with "partners" |

### Output Format

```json
{
  "overall_score": 96,
  "status": "approved",
  "category_scores": {
    "brand_compliance": 38,
    "content_quality": 28,
    "visual_quality": 20,
    "accessibility": 10
  },
  "warnings": [
    "Slide 4: Corner radius 12px detected - adjusted to 16px",
    "Slide 7: Body text at 14pt - minimum is 16pt, adjusted"
  ],
  "errors": [],
  "pass": true
}
```

---

## Agent 7: PPTX Builder Agent

### Purpose
Render the final PowerPoint file using python-pptx based on all previous agent outputs.

### Slide Dimensions

```python
prs.slide_width = Inches(13.333)  # 16:9 widescreen
prs.slide_height = Inches(7.5)
```

### Render Pipeline

For each slide in the plan:
1. Add blank slide layout
2. Apply background color or image
3. Add logo (correct colorway for background)
4. Render headline text with typography spec
5. Render body content (paragraphs, bullets, tables, or chart)
6. Add footer if applicable
7. Apply corner radius to shapes
8. Verify spacing against spec

### Font Handling

```python
# Try brand fonts first, fall back gracefully
def get_heading_font(use_brand_fonts=True):
    if use_brand_fonts:
        return "Big Caslon for Cargill"
    return "Georgia"  # Fallback

def get_body_font(use_brand_fonts=True):
    if use_brand_fonts:
        return "Helvetica Now for Cargill"
    return "Arial"  # Fallback
```

### Table Rendering

- Header row: Leaf Green background, white text, 12pt Bold
- Even rows: White Green (#F5F9ED) background
- Odd rows: White (#FFFFFF) background
- All cells: Neutral-1000 text, 11pt Regular

### Output

- File format: .pptx (Microsoft PowerPoint)
- Dimensions: 16:9 (13.333" x 7.5")
- Includes all slides in sequence
- Returns file path to generated .pptx

---

## State Object Schema

The full state object passed between agents:

```json
{
  "input_path": "/path/to/input.docx",
  "output_path": "/path/to/output.pptx",
  "config": {
    "max_words_per_slide": 150,
    "use_brand_fonts": true,
    "target_slide_count": null
  },
  "extracted_content": { ... },
  "compliance_result": { ... },
  "slide_plan": { ... },
  "visual_design": { ... },
  "charts": { ... },
  "qa_result": { ... },
  "final_path": "/path/to/output.pptx",
  "errors": [],
  "warnings": []
}
```
