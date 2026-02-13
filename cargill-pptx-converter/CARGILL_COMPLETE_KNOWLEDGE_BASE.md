# Cargill Brand PPTX Converter - Complete Knowledge Base

This document contains all brand specifications, workflow documentation, agent implementation details, and reference checklists needed to build a ChatGPT Enterprise GPT that transforms documents into professional Cargill-branded PowerPoint presentations.

---

# PART 1: BRAND REFERENCE CHECKLIST (Quick Reference)

## CRITICAL BRAND RULES

### ⚠️ ABSOLUTE REQUIREMENTS

1. **FONTS - ONLY TWO PERMITTED**
   - ✅ Big Caslon for Cargill (Headings only)
   - ✅ Helvetica Now for Cargill (Subheadings and body)
   - ❌ NO OTHER FONTS EVER

2. **PRIMARY COLOR - CARGILL LEAF GREEN #00843D**
   - Must be used as primary brand color (~30% of visual estate)
   - Logo leaf color
   - Interactive elements
   - Headers and emphasis

3. **BRAND FLEX COLORS - RESTRICTED USE**
   - ✅ ONLY permitted in: Hero stripe overlays, Data visualizations, Illustrations
   - ❌ NEVER use for: Text, UI elements, General backgrounds, Icons, Borders
   - Colors: Rich Red, Bright Yellow, Sky Blue, Vibrant Purple, Midnight Blue

4. **LOGO USAGE**
   - ✅ Use correct colorway: Black wordmark on light, White on dark
   - ❌ Never distort, stretch, or modify
   - ❌ No effects (shadows, glows, etc.)

5. **ICONS - GOOGLE MATERIAL ROUNDED ONLY**
   - ✅ UI icons: Google Material Icons (Rounded style)
   - ✅ Brand icons: From Cargill icon library
   - ❌ Never use Sharp, Two-tone, or other styles

---

## COLOR PALETTE QUICK REFERENCE

### Primary Brand Colors (Use Frequently)
| Color Name | Hex | Usage |
|------------|-----|-------|
| **Cargill Leaf Green** | **#00843D** | **PRIMARY - Headers, logo, interactive** |
| White | #FFFFFF | Backgrounds, text on dark |
| White Green | #F5F9ED | Page backgrounds |
| Soft Green | #BDE588 | Accents |
| Deep Green | #03441F | Dark contrast |
| Black | #000000 | Text, logo on light |

### Neutrals (Text, Borders - Use Sparingly)
| Color | Hex | Usage |
|-------|-----|-------|
| Neutral 300 | #DBDDDC | Borders |
| Neutral 500 | #707773 | Secondary text |
| Neutral 700 | #404945 | Primary icons, body text |
| Neutral 1000 | #101C16 | Primary text on light |

### Emphasis (Warnings, Information)
| Color | Hex | Use Case |
|-------|-----|----------|
| Ruby Red 500 | #C50F1F | Errors, alerts |
| Yolk Yellow 100 | #FEA800 | Warnings |
| Sapphire Blue 500 | #0F49C5 | Information |

### Brand Flex (RESTRICTED - See Critical Rules)
| Palette | Light | Mid | Deep |
|---------|-------|-----|------|
| Rich Red | #F7B9C0 | #EA5062 | #9E2A2F |
| Bright Yellow | #FFD77D | #FFBC27 | #FFD77D |
| Sky Blue | #BCEDFF | #57D1FF | #007681 |
| Vibrant Purple | #C6C2FF | #7166FF | #393380 |
| Midnight Blue | #99ADC2 | #003266 | #001A33 |

---

## TYPOGRAPHY QUICK REFERENCE

### Headings (Big Caslon for Cargill)
| Style | Desktop | Mobile | Line Height | Use |
|-------|---------|--------|-------------|-----|
| heading-lg | **72pt** | 48pt | 80pt / 52pt | Top hero (max 1×) |
| heading-md | **56pt** | 40pt | 62pt / 48pt | Hero, sections (multiple) |
| heading-sm | **40pt** | 32pt | 48pt / 36pt | Cards, sections |

### Subheadings (Helvetica Now Bold)
| Style | Desktop | Mobile | Line Height | Use |
|-------|---------|--------|-------------|-----|
| subheading-lg | **32pt** | 24pt | 42pt / 32pt | Section titles |
| subheading-md | **24pt** | 20pt | 32pt / 26pt | Card titles |
| subheading-sm | **20pt** | 18pt | 26pt / 24pt | Eyebrows |

### Body (Helvetica Now Regular)
| Style | Size | Line Height | Use |
|-------|------|-------------|-----|
| body-base | **16pt** | 24pt | Body copy |
| body-sm | **12pt** | 18pt | Captions |
| body-xs | **10pt** | 14pt | Legal text |

---

## SPACING QUICK REFERENCE

### Spacing (Internal Elements)
| Token | Desktop | Use |
|-------|---------|-----|
| spacing-sm | 4px | Minimal internal |
| spacing-base | 8px | Standard |
| spacing-md | 12px | Medium |
| spacing-lg | **16px** | **Large (common)** |
| spacing-xl | **24px** | **Extra large (common)** |
| spacing-2xl | 32px | 2× large |
| spacing-3xl | 40px | 3× large |
| spacing-4xl | 48px | 4× large |
| spacing-6xl | **80px** | **Hero sections** |

---

## CORNER RADIUS STANDARDS

| Size | Radius | Apply To |
|------|--------|----------|
| **Base** | **8px** | Buttons, chips, inputs, tooltips |
| **Medium** | **16px** | Cards, containers, hero images |
| **Large** | **24px** | Containers, modals, overlays |

---

## TEMPLATE LIBRARY

### Hero Slides
| Template | Best For |
|----------|----------|
| Basic Hero | Opening slides, section dividers |
| Text with Screenshot | Product demonstrations |
| Full Height Promo | Major announcements, dramatic openings |

### Statistics Slides
| Template | Best For |
|----------|----------|
| Simple Statistics | 3-4 key metrics in row |
| Statistic Cards with Icons | 4 metrics with thematic icons |
| Two Column Grid | 4-6 related metrics |

### Content Slides
| Template | Best For |
|----------|----------|
| Left-Aligned Headline | General content, multiple paragraphs |
| Centered Headline | Balanced content, quotes, key statements |
| Three Column Basic Cards | Lists, features, benefits (3 items) |
| Alternating Horizontal | Storytelling, processes, step-by-step |

---

## BRAND PERSONALITY

### Five Core Traits (Reflect in Every Slide)

**1. OPTIMISTIC**
- Design: Bright, clean, ample white space, uplifting imagery
- Copy: Possibility-focused, solutions-oriented, future-positive

**2. CURIOUS**
- Design: Open layouts, exploratory flow, questions as headers
- Copy: Inquisitive tone, open-ended statements, invitation to discover

**3. COURAGEOUS**
- Design: Bold typography (large heading-lg), confident layout, strong contrasts
- Copy: Conviction-based messaging, bold claims with data backing

**4. COMPASSIONATE**
- Design: People-centered imagery, warm tones, accessible layouts
- Copy: People-first language, caring tone, partnership emphasis

**5. HUMBLE**
- Design: Clean, uncluttered, letting content shine, not overly flashy
- Copy: Respectful tone, partnership language, "we work with" not "we lead"

---

## APPROVED TERMINOLOGY

### ✅ Use These Terms:
- "Farmers, ranchers, growers and producers"
- "Customers" and "partners" (interchangeably in appropriate contexts)
- "Sustainable" (not "eco-friendly" or "green" except color references)
- "Our purpose is 'Nourishing the world in a safe, responsible and sustainable way'"

### ❌ Avoid These Terms:
- "Suppliers" (use "partners" instead)
- "Consumers" in B2B context (use "customers")
- Corporate jargon: "synergy", "leverage", "circle back", "move the needle"
- Overly corporate: "solutions provider", "best-in-class", "cutting-edge"

---

## QUALITY ASSURANCE CHECKLIST

### Every Slide Must Have:
- [ ] Logo in correct colorway for background
- [ ] Only Big Caslon (headings) and Helvetica Now (body/subheadings)
- [ ] Colors only from approved palette
- [ ] Spacing from defined padding/spacing scale
- [ ] Corner radius = 8px, 16px, or 24px only
- [ ] Content aligned to 12-column grid
- [ ] Brand personality evident in messaging

### Brand Flex Color Usage:
- [ ] Used ONLY in: hero stripes, data viz, or illustrations
- [ ] NEVER in: text, UI elements, backgrounds, icons, borders

---

## FORBIDDEN PRACTICES

### ❌ NEVER:
1. Use fonts other than Big Caslon or Helvetica Now
2. Use brand flex colors outside hero stripes, data viz, illustrations
3. Apply brand flex colors to text, UI, icons, general backgrounds, borders
4. Use Google Material Icons in non-Rounded styles
5. Distort, stretch, or modify logo
6. Apply effects to logo (shadows, glows, bevels)
7. Use corner radius other than 8px, 16px, 24px
8. Ignore spacing scale - always use defined values
9. Create custom colors outside palette
10. Overuse leaf graphical device
11. Use clip art or low-quality stock imagery
12. Violate grid alignment
13. Use conflicting personality traits (e.g., arrogant language)
14. Use "suppliers" → use "partners"

---

# PART 2: COMPLETE BRAND SPECIFICATIONS DATABASE

## Complete Color Palette

### Primary Brand Colors (Core Identity - Use ~30% of visual estate)
```json
{
  "white": {"hex": "#FFFFFF", "usage": "Backgrounds, logo colorway, text on dark"},
  "white_green": {"hex": "#F5F9ED", "usage": "Light backgrounds, page backgrounds"},
  "soft_green": {"hex": "#BDE588", "usage": "Accents, backgrounds"},
  "green_300": {"hex": "#81AB40", "usage": "Digital only, hover states"},
  "cargill_leaf_green": {
    "hex": "#00843D",
    "cmyk": "100, 0, 71, 48",
    "pantone": "Pantone 7724 C",
    "usage": "PRIMARY BRAND COLOR - Logo, headers, interactive elements",
    "prominence": "30% of visual identity",
    "importance": "CRITICAL"
  },
  "green_700": {"hex": "#01632D", "usage": "Digital only, text, darker accents"},
  "deep_green": {"hex": "#03441F", "usage": "Dark backgrounds, contrast"},
  "green_900": {"hex": "#012912", "usage": "Digital only, darkest backgrounds"},
  "black": {"hex": "#000000", "usage": "Text, logo wordmark on light backgrounds"}
}
```

### Neutral Palette (Text, borders - use sparingly)
```json
{
  "neutral_100": {"hex": "#F3F4F3", "usage": "Subtle backgrounds"},
  "neutral_200": {"hex": "#E7E8E8", "usage": "Borders, dividers"},
  "neutral_300": {"hex": "#DBDDDC", "usage": "Borders, backgrounds"},
  "neutral_400": {"hex": "#9FA4A2", "usage": "Secondary text, borders"},
  "neutral_500": {"hex": "#707773", "usage": "Body text, icons"},
  "neutral_600": {"hex": "#58605C", "usage": "Emphasized text"},
  "neutral_700": {"hex": "#404945", "usage": "Primary icons, text"},
  "neutral_800": {"hex": "#28332D", "usage": "Dark backgrounds"},
  "neutral_900": {"hex": "#1C2722", "usage": "Dark backgrounds"},
  "neutral_1000": {"hex": "#101C16", "usage": "Darkest backgrounds, text on light"}
}
```

### Emphasis Colors (Warnings, information, status)
```json
{
  "ruby_red_100": {"hex": "#EB5655", "usage": "Alerts, warnings (light)"},
  "ruby_red_500": {"hex": "#C50F1F", "usage": "Alerts, errors"},
  "yolk_yellow_100": {"hex": "#FEA800", "usage": "Warnings, caution"},
  "sapphire_blue_100": {"hex": "#55A5EB", "usage": "Information (light)"},
  "sapphire_blue_500": {"hex": "#0F49C5", "usage": "Announcements, info"}
}
```

### Brand Flex Colors (RESTRICTED USE)
```json
{
  "rich_red": {
    "light": "#F7B9C0", "mid": "#EA5062", "deep": "#9E2A2F",
    "usage": "ONLY: Leaf stripe overlays, data viz, illustrations"
  },
  "bright_yellow": {
    "light": "#FFD77D", "mid": "#FFBC27", "deep": "#FFD77D",
    "usage": "ONLY: Leaf stripe overlays, data viz, illustrations"
  },
  "sky_blue": {
    "light": "#BCEDFF", "mid": "#57D1FF", "deep": "#007681",
    "usage": "ONLY: Leaf stripe overlays, data viz, illustrations"
  },
  "vibrant_purple": {
    "light": "#C6C2FF", "mid": "#7166FF", "deep": "#393380",
    "usage": "ONLY: Leaf stripe overlays, data viz, illustrations"
  },
  "midnight_blue": {
    "light": "#99ADC2", "mid": "#003266", "deep": "#001A33",
    "usage": "ONLY: Leaf stripe overlays, data viz, illustrations"
  }
}
```

**CRITICAL RULE**: Brand flex colors should NEVER be used for:
- General backgrounds
- Text
- UI elements (buttons, form fields, etc.)
- Icons
- Borders
- Any element outside the three permitted contexts

---

## Typography Specifications

### Font Families
1. **Big Caslon for Cargill** - Headings only (Weights: Regular, Italic)
2. **Helvetica Now for Cargill** - Subheadings and body (Weights: Regular, Italic, Bold, Bold Italic)

### Typography Scale (Desktop / Mobile)

**Headings (Big Caslon for Cargill)**:
| Style | Desktop | Mobile | Line Height Desktop | Line Height Mobile | Usage |
|-------|---------|--------|---------------------|-------------------|-------|
| heading-lg | 72pt | 48pt | 80pt | 52pt | Top hero headline (max 1x per presentation) |
| heading-md | 56pt | 40pt | 62pt | 48pt | Hero, section titles (multiple uses) |
| heading-sm | 40pt | 32pt | 48pt | 36pt | Card titles, section titles (multiple uses) |

**Subheadings (Helvetica Now for Cargill Bold)**:
| Style | Desktop | Mobile | Line Height Desktop | Line Height Mobile | Usage |
|-------|---------|--------|---------------------|-------------------|-------|
| subheading-lg | 32pt | 24pt | 42pt | 32pt | Section titles |
| subheading-md | 24pt | 20pt | 32pt | 26pt | Card titles, section titles |
| subheading-sm | 20pt | 18pt | 26pt | 24pt | Eyebrow text |

**Body (Helvetica Now for Cargill Regular)**:
| Style | Desktop | Mobile | Line Height Desktop | Line Height Mobile | Usage |
|-------|---------|--------|---------------------|-------------------|-------|
| body-base | 16pt | 16pt | 24pt | 24pt | Body copy |
| body-sm | 12pt | 12pt | 18pt | 18pt | Captions |
| body-xs | 10pt | 10pt | 14pt | 14pt | Legal text |

---

## Logo Specifications

### Logo Variations
- **Primary Logo**: Full color with Leaf Green leaf + black/white wordmark (DEFAULT)
- **Secondary**: Green palette variations for diverse situations
- **Tertiary**: Full black or white (use ONLY when absolutely necessary)

### Logo Rules
1. **Clear space**: Maintain minimum clear space around logo equal to height of leaf
2. **Minimum size**: Never scale below 0.5" width
3. **Placement**: Typically top-right of slides
4. **Never**: Distort, stretch, change colors, add effects, rotate, place on busy backgrounds

---

## Layout & Grid System

### PowerPoint Slide Standard
- **Dimensions**: 16:9 widescreen (13.333" × 7.5")
- **Grid**: 12-column for desktop layouts

### Spacing Scale

**Padding (external spacing)**:
| Token | Size |
|-------|------|
| padding-xs | 2px |
| padding-sm | 4px |
| padding-base | 8px |
| padding-lg | 16px |
| padding-xl | 24px |

**Spacing (internal elements)**:
| Token | Size |
|-------|------|
| spacing-sm | 4px |
| spacing-base | 8px |
| spacing-md | 12px |
| spacing-lg | 16px |
| spacing-xl | 24px |
| spacing-2xl | 32px |
| spacing-3xl | 40px |
| spacing-4xl | 48px |
| spacing-5xl | 56px |
| spacing-6xl | 80px |

---

## Visual Elements

### Corner Radius Standards
| Size | Radius | Usage |
|------|--------|-------|
| Base | 8px | Buttons, chips, input fields, tooltips |
| Medium | 16px | Cards, containers, hero images |
| Large | 24px | Containers, modals, overlays |

### Graphical Devices

**The Leaf**:
- Usage: Sparingly (homepage/opening slides primarily)
- Color: Typically Cargill Leaf Green (#00843D)

**Leaf with Stripe Over Image**:
- When: Hero sections, high-impact opening slides
- Color: THIS IS THE PRIMARY USE CASE FOR BRAND FLEX COLORS
- Image selection: Choose images with color hints complementing flex color

---

## Data Visualization Guidelines

### Chart Colors
| Series Count | Color Palette |
|--------------|---------------|
| 1 series | Leaf Green only (#00843D) |
| 2 series | Leaf Green + Neutral-500 (#707773) |
| 3 series | Green palette (Leaf, Soft, Deep) |
| 4+ series | Green palette + justified flex color |

### Chart Typography
- **Title**: Helvetica Now Bold 24pt, Leaf Green
- **Axis labels**: Helvetica Now Regular 16pt, Neutral-700
- **Data labels**: Helvetica Now Regular 12pt, Neutral-900
- **Legend**: Helvetica Now Regular 16pt, Neutral-700

---

## Accessibility Standards

### Contrast Ratios
- **Normal text**: Minimum 4.5:1 (WCAG AA)
- **Large text** (18pt+): Minimum 3:1
- **Interactive elements**: Minimum 3:1

### Text Sizes
- **Minimum body text**: 16pt (body-base)
- **Minimum caption**: 12pt (body-sm)
- **Never go below**: 10pt (body-xs for legal only)

---

# PART 3: AGENT IMPLEMENTATION GUIDE

## Agent Architecture Overview

Each agent operates as an independent module with defined inputs, processes, and outputs.

---

## Agent 1: Content Extraction Agent

### Purpose
Extract and structure all content from input documents regardless of format.

### Input Formats Supported
- Microsoft Word (.doc, .docx)
- PDF (.pdf)
- PowerPoint (.ppt, .pptx)
- Plain text (.txt)
- Markdown (.md)
- CSV/Excel (data extraction)

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
    "tables": [{"table_id": "table_1", "headers": ["Region", "Target", "Actual"], "data": [...]}],
    "statistics": [{"value": "15%", "label": "Growth over Q2"}]
  },
  "key_messages": [
    {"text": "Q3 exceeded all targets through sustainable practices", "importance": "primary"}
  ],
  "sections": [
    {"title": "Executive Summary", "word_count": 250, "section_type": "summary"}
  ]
}
```

---

## Agent 2: Brand Compliance Agent

### Purpose
Ensure all content aligns with Cargill brand guidelines before design begins.

### Processing Steps
1. **Tone Analysis**: Score content against personality traits (optimistic, curious, courageous, compassionate, humble)
2. **Terminology Check**: Verify approved vs. problematic language
3. **Message Alignment**: Check alignment with "Nourishing the world in a safe, responsible and sustainable way"

### Personality Trait Indicators

**Optimistic**:
- Positive: possibility, opportunity, future, create, enable, potential
- Negative: problem, challenge, difficulty, obstacle

**Curious**:
- Positive: explore, discover, question, what if, how might
- Negative: always, never, absolutely, definitely

**Courageous**:
- Positive: commit, bold, leading, innovative, transform
- Negative: might, perhaps, possibly, uncertain

**Compassionate**:
- Positive: partner, support, together, care, people, community
- Negative: dominate, control, force, demand

**Humble**:
- Positive: collaborate, listen, learn, respect, together
- Negative: best, superior, dominate, leader

### Terminology Corrections
```json
{
  "suppliers": "partners",
  "consumers": "customers",
  "eco-friendly": "sustainable",
  "synergy": "collaboration",
  "leverage": "use",
  "best-in-class": "leading",
  "cutting-edge": "innovative"
}
```

---

## Agent 3: Slide Architecture Agent

### Purpose
Design optimal slide structure, sequence, and layout selection based on content.

### Available Templates

**Hero Slides**:
- `basic_hero`: Image background with text overlay and CTA
- `text_with_screenshot`: Split layout showcasing product/interface
- `full_height_promo`: Large format hero with prominent imagery

**Statistics Slides**:
- `simple_statistics`: Clean horizontal row of numbers (3-4 metrics)
- `statistic_cards_icons`: Statistics in cards with brand icons (4 metrics)
- `simple_with_headline`: Statistics preceded by contextual headline
- `two_column_grid`: Comparative statistics in grid (4-6 metrics)

**Content Slides**:
- `left_aligned_headline`: Standard section with left-aligned headline
- `centered_headline`: Symmetric layout with centered headline
- `three_column_basic_cards`: Simple card grid (3 items)
- `three_column_rich_media`: Enhanced cards with images
- `alternating_horizontal`: Image-text alternating for narrative flow

### Template Selection Logic

```
IF content is achievement/announcement:
    IF has high-quality image: use full_height_promo
    ELSE: use basic_hero

IF content has 3-4 statistics with icon potential:
    use statistic_cards_icons
ELIF content has 3-4 statistics:
    use simple_statistics
ELIF content has 4-6 statistics:
    use two_column_grid

IF section has 3+ images:
    use three_column_rich_media
ELIF section is list-based with 3 items:
    use three_column_basic_cards
ELIF section is narrative:
    use alternating_horizontal
ELSE:
    use left_aligned_headline
```

---

## Agent 4: Visual Design Agent

### Purpose
Apply Cargill visual identity elements to slides following architecture plan.

### Color Scheme Selection

**Hero Slides**:
```json
{
  "primary": "#00843D",
  "accent": "[flex_color]",
  "background": "white",
  "text_on_image": "white",
  "cta_button": {"background": "#00843D", "text": "white"}
}
```

**Statistics Slides**:
```json
{
  "primary": "#00843D",
  "background": "#F5F9ED",
  "card_background": "white",
  "numbers": "#00843D",
  "labels": "#404945",
  "icons": "#00843D"
}
```

**Content Slides**:
```json
{
  "primary": "#00843D",
  "background": "white",
  "headline": "#00843D",
  "subheading": "#012912",
  "body": "#101C16",
  "card_border": "#DBDDDC"
}
```

### Typography Application

**Hero Slides**: heading-lg (72pt) or heading-md (56pt)
**Section Headers**: heading-sm (40pt)
**Statistics Numbers**: 32pt Bold
**Body Text**: 16pt Regular

### Spacing Application

**Hero**: content_padding 80px, headline_to_body 16px, body_to_cta 32px
**Statistics**: slide_padding 48px, card_padding 24px, card_gap 16px
**Content**: slide_padding 40px, headline_margin_bottom 24px, paragraph_spacing 12px

---

## Agent 5: Data Visualization Agent

### Purpose
Transform data tables and statistics into brand-compliant charts.

### Chart Type Selection

```
IF time-series data: use line_chart
IF data sums to ~100% with ≤8 categories: use pie_chart
IF ≤10 categories: use bar_chart
IF 10-20 categories: use horizontal_bar_chart
ELSE: use column_chart
```

### Brand Chart Styling

```json
{
  "colors": ["#00843D", "#BDE588", "#03441F", "#57D1FF", "#404945"],
  "typography": {
    "chart_title": "Helvetica Now Bold 24pt #00843D",
    "axis_labels": "Helvetica Now Regular 16pt #404945",
    "data_labels": "Helvetica Now Regular 12pt #1C2722",
    "legend": "Helvetica Now Regular 16pt #404945"
  },
  "background": "#FFFFFF",
  "grid_lines": {"color": "#E7E8E8", "style": "solid", "width": "1px"}
}
```

---

## Agent 6: Quality Assurance Agent

### Purpose
Final comprehensive review ensuring 100% brand compliance.

### QA Checklist

**Brand Compliance**:
- [ ] Color accuracy - all colors from approved palette
- [ ] Typography compliance - Big Caslon + Helvetica Now only
- [ ] Logo usage - correct colorway on all slides
- [ ] Icon compliance - Google Material Rounded only
- [ ] Spacing standards - all spacing from defined scale
- [ ] Corner radius - only 8px, 16px, 24px values
- [ ] Flex color usage - only in approved contexts

**Content Quality**:
- [ ] No spelling/grammar errors
- [ ] Message consistency
- [ ] Personality alignment
- [ ] Tone appropriateness

**Visual Quality**:
- [ ] Image quality - no pixelation
- [ ] Grid alignment
- [ ] Visual hierarchy
- [ ] Consistency throughout

**Accessibility**:
- [ ] Color contrast ratios (minimum 4.5:1 for text)
- [ ] Minimum text size (16pt body)
- [ ] Icon sizes (minimum 24×24px)

### Scoring
- **100%**: All checks pass
- **95-99%**: Minor warnings
- **80-94%**: Approved with recommendations
- **<80%**: Needs revision

---

# PART 4: WORKFLOW SYSTEM

## System Overview

This multi-agent workflow transforms any input document (Word, PDF, PPT, text) into professional-grade Cargill-branded PowerPoint presentations.

## Workflow Stages

### Stage 1: Intake & Analysis
```
Input Document → Content Extraction Agent
↓
Structured Content Object
↓
Brand Compliance Agent (Initial Assessment)
↓
Content Classification & Requirements Document
```

### Stage 2: Architecture & Planning
```
Requirements Document → Slide Architecture Agent
↓
Slide Structure Plan (slide types, sequence, layout specifications)
↓
Visual Design Agent (Template Selection)
↓
Design Blueprint with mapped templates
```

### Stage 3: Content Transformation
```
Design Blueprint → Content Population
↓
Apply typography standards
↓
Data Visualization Agent (for statistics/charts)
↓
Raw slide content with proper text formatting
```

### Stage 4: Visual Enhancement
```
Raw Slides → Visual Design Agent
↓
Apply brand elements:
- Logo placement
- Color schemes
- Icons from brand library
- Graphical devices
- Corner radius
- Spacing
↓
Visually enhanced slides
```

### Stage 5: Final Assembly & QA
```
Enhanced Slides → Quality Assurance Agent
↓
Brand compliance check
↓
Final Cargill-Branded PowerPoint
```

---

## Example Workflow Execution

**Input**: Word document with Q3 sales analysis (12 pages, 3 charts, 5 sections)

**Stage 1 Output**:
- 5 main sections identified
- 3 data tables extracted
- 2 hero slide opportunities identified
- Key message: "Q3 exceeded targets through sustainable practices"

**Stage 2 Output**:
- Slide 1: Hero (Full Height Promo) - Q3 Achievement
- Slide 2: Statistics (Cards with icons) - Key metrics
- Slide 3: Content (Two column grid) - Regional breakdown
- Slide 4: Data Visualization (Chart) - YoY comparison
- Slide 5: Content (Alternating horizontal) - Success factors
- Slide 6: Hero (Basic) - Sustainability impact
- Slide 7: Statistics (Cards with icons) - Environmental metrics
- Slide 8: Closing - Thank You

**Stage 3 Output**:
- All text converted to Big Caslon (headings) and Helvetica Now (body)
- Font sizes applied per typography scale

**Stage 4 Output**:
- Cargill Leaf Green applied as primary color
- Sky Blue (brand flex) used for hero stripe
- Icons from brand library added to statistics cards
- Leaf graphical device on opening hero
- Corner radius (16px) applied to all cards

**Stage 5 Output**:
- QA verification: 100% compliance
- Final .pptx ready for delivery

---

## Final Quality Standard

**The output must be indistinguishable from work produced by Cargill's professional design and communications teams.**

Every presentation should demonstrate:
- ✅ Perfect brand compliance
- ✅ Professional polish and refinement
- ✅ Clear personality and tone
- ✅ Logical structure and flow
- ✅ High-quality visuals
- ✅ Accessibility standards
- ✅ Consistent execution throughout

**If any element doesn't meet this standard, it requires revision.**

---

# PART 5: QUICK START GUIDE

## Basic Usage

### Simple Command
```
Transform my document into a Cargill-branded presentation
```

### With Specific Requirements
```
Create a Cargill-branded presentation from this document.
Target audience: Executive leadership
Length: 8-10 slides
Emphasize: Sustainability achievements
```

## Examples of Great Starting Prompts

```
"Transform my Q3 sales report into an executive-ready Cargill presentation.
Focus on achievements and sustainability impact. Keep it under 10 slides."
```

```
"Create a Cargill-branded presentation from this technical specification
document. Target audience is potential customers. Make it compelling and
accessible, not overly technical."
```

```
"I need a Cargill presentation for our farmer partners about the new
regenerative agriculture program. Emphasize support, partnerships, and
shared success. Use storytelling approach."
```

## What the System Handles Automatically

✅ Color schemes (automatically applies Cargill palette)
✅ Font choices (Big Caslon and Helvetica Now)
✅ Logo placement (correct colorway)
✅ Icon selection (brand library)
✅ Spacing and layout (brand standards)
✅ Data visualization styling (brand-compliant)
✅ Terminology corrections
✅ Quality assurance

## File Output

- **Format**: Microsoft PowerPoint (.pptx)
- **Dimensions**: 16:9 widescreen
- **Quality**: Design team grade, 100% brand compliant

---

## Quick Decision Trees

### "What color should I use?"
1. Primary brand element? → **Cargill Leaf Green (#00843D)**
2. Text or border? → **Neutral palette**
3. Warning/error? → **Emphasis colors (Ruby Red, Yolk Yellow)**
4. Information? → **Emphasis colors (Sapphire Blue)**
5. Hero stripe, data viz, illustration? → **Brand flex colors PERMITTED**
6. Anything else? → **Primary green palette**

### "What typography should I use?"
1. Headline? → **Big Caslon (Regular or Italic)**
2. Subheading? → **Helvetica Now Bold**
3. Body text? → **Helvetica Now Regular**

### "What template should I use?"
1. Opening slide with impact? → **Full Height Promo hero**
2. Show 3-4 key numbers? → **Statistic Cards with Icons**
3. Detailed data table? → **Two Column Grid**
4. Storytelling with images? → **Alternating Horizontal**
5. Three equal features? → **Three Column Cards**
6. Product demonstration? → **Text with Screenshot**

### "Can I use this flex color?"
1. Hero stripe over image? → **Yes, if image complements color**
2. Data visualization? → **Yes, if justified by data context**
3. Illustration? → **Yes**
4. Anything else? → **No - use primary green palette**

---

**END OF KNOWLEDGE BASE**

This document serves as the authoritative reference for all brand decisions in the Cargill PPTX conversion workflow.
