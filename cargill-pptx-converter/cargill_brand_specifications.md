# Cargill Brand Specifications Database

Complete technical reference for all visual identity elements used in Cargill-branded PowerPoint presentations.

---

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

### Brand Flex Colors (RESTRICTED USE - See rules below)

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

**CRITICAL RULE**: Brand flex colors must NEVER be used for:
- General backgrounds
- Text
- UI elements (buttons, form fields, etc.)
- Icons
- Borders
- Any element outside the three permitted contexts (hero stripes, data viz, illustrations)

---

## Typography Specifications

### Font Families

1. **Big Caslon for Cargill** - Headings only (Weights: Regular, Italic)
2. **Helvetica Now for Cargill** - Subheadings and body (Weights: Regular, Italic, Bold, Bold Italic)

If brand fonts are unavailable:
- Georgia → substitute for Big Caslon
- Arial → substitute for Helvetica Now

### Typography Scale

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
| body-xs | 10pt | 10pt | 14pt | 14pt | Legal text only |

---

## Logo Specifications

### Logo Variations

- **Primary Logo**: Full color with Leaf Green leaf + black/white wordmark (DEFAULT)
- **Secondary**: Green palette variations for diverse situations
- **Tertiary**: Full black or white (use ONLY when absolutely necessary)

### Logo Colorways

| Background | Logo Style |
|------------|------------|
| Light/White | Leaf Green leaf + black wordmark |
| Dark/Green | Leaf Green leaf + white wordmark |
| Photography | White leaf + white wordmark |

### Logo Rules

1. **Clear space**: Maintain minimum clear space equal to height of leaf on all sides
2. **Minimum size**: Never scale below 0.5" width
3. **Placement**: Typically top-right of slides
4. **Never**: Distort, stretch, change colors, add effects, rotate, place on busy backgrounds without protection

---

## Layout and Grid System

### PowerPoint Slide Standard

- **Dimensions**: 16:9 widescreen (13.333" x 7.5")
- **Grid**: 12-column layout
- **Margins**: Minimum 0.75" from slide edges for content

### Padding Scale (External Spacing)

| Token | Size |
|-------|------|
| padding-xs | 2px |
| padding-sm | 4px |
| padding-base | 8px |
| padding-lg | 16px |
| padding-xl | 24px |

### Spacing Scale (Internal Elements)

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

## Corner Radius Standards

| Size | Radius | Usage |
|------|--------|-------|
| Base | 8px | Buttons, chips, input fields, tooltips |
| Medium | 16px | Cards, containers, hero images |
| Large | 24px | Containers, modals, overlays |

Only these three values are permitted. No other corner radius values.

---

## Visual Elements

### The Leaf Graphical Device

- Usage: Sparingly (homepage/opening slides primarily, not every slide)
- Color: Typically Cargill Leaf Green (#00843D)
- Purpose: Brand recognition, visual interest

### Leaf with Stripe Over Image (Hero Sections)

- When: Hero sections, high-impact opening slides
- Color: This is the primary use case for brand flex colors
- Image selection: Choose images with color hints that complement the flex color overlay
- The stripe is a diagonal band across the lower portion of the hero image

### Icon Standards

- **UI Icons**: Google Material Icons (Rounded style ONLY)
  - Never use: Sharp, Two-tone, Outlined, or Filled styles
- **Brand Icons**: Cargill icon library
  - These are specialized icons representing Cargill's agricultural and business domains

---

## Data Visualization Guidelines

### Chart Color Sequences

| Series Count | Color Palette |
|--------------|---------------|
| 1 series | Leaf Green only (#00843D) |
| 2 series | Leaf Green + Neutral-500 (#707773) |
| 3 series | Green palette (Leaf, Soft, Deep) |
| 4+ series | Green palette + justified flex color |

### Chart Typography

- **Title**: Helvetica Now Bold 24pt, Leaf Green (#00843D)
- **Axis labels**: Helvetica Now Regular 16pt, Neutral-700 (#404945)
- **Data labels**: Helvetica Now Regular 12pt, Neutral-900 (#1C2722)
- **Legend**: Helvetica Now Regular 16pt, Neutral-700 (#404945)

### Chart Styling

```json
{
  "background": "#FFFFFF",
  "grid_lines": {
    "color": "#E7E8E8",
    "style": "solid",
    "width": "1px"
  },
  "axis_line": {
    "color": "#DBDDDC",
    "width": "1px"
  },
  "plot_area_background": "#FFFFFF"
}
```

### Chart Type Selection Guide

| Data Type | Recommended Chart |
|-----------|-------------------|
| Time-series / trends | Line chart |
| Part-to-whole (<=8 categories) | Pie or donut chart |
| Category comparison (<=10) | Vertical bar chart |
| Category comparison (10-20) | Horizontal bar chart |
| Multiple variables over time | Grouped bar chart |
| Distribution | Histogram |

---

## Slide Color Schemes by Type

### Hero Slides

```json
{
  "primary": "#00843D",
  "accent_stripe": "[brand_flex_color]",
  "background": "white or image",
  "headline": "#FFFFFF",
  "subheading": "#FFFFFF",
  "cta_button_background": "#00843D",
  "cta_button_text": "#FFFFFF"
}
```

### Statistics Slides

```json
{
  "slide_background": "#F5F9ED",
  "card_background": "#FFFFFF",
  "headline": "#00843D",
  "statistic_numbers": "#00843D",
  "statistic_labels": "#404945",
  "icon_color": "#00843D",
  "card_border": "#DBDDDC"
}
```

### Content Slides

```json
{
  "slide_background": "#FFFFFF",
  "headline": "#00843D",
  "subheading": "#012912",
  "body_text": "#101C16",
  "card_background": "#FFFFFF",
  "card_border": "#DBDDDC",
  "accent": "#00843D"
}
```

### Section Divider Slides

```json
{
  "slide_background": "#03441F",
  "headline": "#FFFFFF",
  "accent_line": "#00843D"
}
```

### Closing Slides

```json
{
  "slide_background": "#00843D",
  "headline": "#FFFFFF",
  "subheading": "#FFFFFF",
  "tagline_color": "#BDE588"
}
```

---

## Accessibility Standards

### Contrast Ratios

- **Normal text** (under 18pt): Minimum 4.5:1 (WCAG AA)
- **Large text** (18pt+): Minimum 3:1
- **Interactive elements**: Minimum 3:1

### Text Size Minimums

- **Body text**: Minimum 16pt (body-base)
- **Captions**: Minimum 12pt (body-sm)
- **Legal text**: Minimum 10pt (body-xs) - use only when required

### Icon Sizes

- Minimum display size: 24x24 pixels equivalent
- Preferred: 32x32 or 48x48 for primary UI icons

---

## Template Specifications

### Hero Slide - Basic Hero

- Background: Full-bleed image or solid Leaf Green
- Leaf graphical device: Optional, bottom-left or lower-right
- Flex color stripe: Diagonal band, hero sections only
- Headline: heading-md or heading-lg, white
- Subheading: subheading-md, white
- CTA button: Leaf Green background, white text, 8px radius
- Logo: Top-right, white colorway

### Statistics Slide - Statistic Cards with Icons

- Background: White Green (#F5F9ED)
- Card count: 4 cards in 2x2 grid or 3-4 in single row
- Card background: White (#FFFFFF)
- Card border-radius: 16px
- Statistic value: 32pt Bold, Leaf Green
- Statistic label: 16pt Regular, Neutral-700
- Icon: 48px, Leaf Green, Google Material Rounded

### Content Slide - Left-Aligned Headline

- Background: White (#FFFFFF)
- Headline: heading-sm (40pt), Leaf Green, left-aligned
- Body text: body-base (16pt), Neutral-1000
- Slide padding: 40px
- Headline margin bottom: 24px
- Paragraph spacing: 12px

### Content Slide - Three Column Cards

- Card background: White or Neutral-100
- Card border-radius: 16px
- Card border: 1px Neutral-300
- Card padding: 24px
- Card icon: 48px, top of card, Leaf Green
- Card headline: subheading-md (24pt), Neutral-1000
- Card body: body-base (16pt), Neutral-700

### Closing Slide

- Background: Leaf Green (#00843D)
- Headline: heading-md (56pt), White, centered
- Tagline: "Together, creating a more food secure world"
- Tagline style: subheading-md (24pt), White or Soft Green
