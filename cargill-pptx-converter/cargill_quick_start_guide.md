# Cargill Brand PPTX Converter - Quick Start Guide

Practical usage guide for the Cargill document-to-PowerPoint conversion system.

---

## What This System Does

Transforms any document (Word, PDF, PowerPoint, text, CSV, Excel) into a professional Cargill-branded PowerPoint presentation by:

- Preserving 100% of original content meaning and data
- Fixing only spelling, grammar, and terminology (e.g., "suppliers" → "partners")
- Replacing all design, layout, and visual elements with Cargill brand standards
- Generating brand-compliant charts and data visualizations
- Outputting a download-ready .pptx file

---

## How to Use (ChatGPT GPT Version)

### Simple Conversion

Upload your document and type:

```
Transform my document into a Cargill-branded presentation
```

### With Specific Instructions

```
Create a Cargill-branded presentation from this document.
Target audience: Executive leadership
Length: 8-10 slides
Emphasize: Sustainability achievements
```

### For Data-Heavy Documents

```
Convert this report into a Cargill presentation.
Include charts for the regional data.
Use statistic cards for the key metrics on slide 2.
```

---

## Example Prompts That Work Well

### Executive Report

```
Transform my Q3 sales report into an executive-ready Cargill presentation.
Focus on achievements and sustainability impact. Keep it under 10 slides.
```

### Technical Document for External Audience

```
Create a Cargill-branded presentation from this technical specification
document. Target audience is potential customers. Make it compelling and
accessible, not overly technical.
```

### Partner Communication

```
I need a Cargill presentation for our farmer partners about the new
regenerative agriculture program. Emphasize support, partnerships, and
shared success. Use a storytelling approach.
```

### Data-Only Input

```
Create a Cargill-branded presentation about Q3 performance:
- Revenue grew 15% year-over-year
- Sustainability investments reached $2.3M
- 125 partner farms supported
- GHG emissions reduced 30%
- Three key success factors: precision agriculture, water stewardship, soil health
```

### Rebranding Existing Slides

```
I have an existing PowerPoint that isn't Cargill-branded. Convert it to
full Cargill brand standards. Keep all content and data exactly as-is.
Only change the design, colors, and fonts.
```

---

## What the System Handles Automatically

| Element | What Happens |
|---------|--------------|
| Color scheme | Cargill palette applied (Leaf Green primary, neutrals, white) |
| Fonts | Big Caslon (headings) and Helvetica Now (body) |
| Logo | Placed top-right, correct colorway for background |
| Slide templates | Selected based on content type (hero, stats, content, chart) |
| Data visualization | Charts generated with brand colors and typography |
| Spacing | All padding and margins set to brand spacing scale |
| Corner radius | Cards and containers set to 8px, 16px, or 24px |
| Terminology | "suppliers" → "partners", "consumers" → "customers", etc. |
| Quality assurance | Brand compliance checked before output |

---

## Understanding the Output

### File Format

- Format: .pptx (Microsoft PowerPoint)
- Dimensions: 16:9 widescreen (13.333" x 7.5")
- Compatible with: PowerPoint, Keynote (import), Google Slides (import)

### Slide Types You'll See

**Hero Slides** (opening and major sections)
- Green or image background
- Large headline (56-72pt)
- Optional color accent stripe (brand flex color)
- Used for: Title slide, major announcements

**Statistics Slides**
- White Green background
- White cards with green numbers
- Used for: Key metrics, KPIs, performance data

**Content Slides**
- White background
- Green headline
- Used for: Body content, explanations, lists

**Chart Slides**
- White background
- Brand-colored charts
- Used for: Data trends, comparisons, distributions

**Section Dividers**
- Deep green background
- White centered heading
- Used for: Separating major topics

**Closing Slide**
- Leaf Green background
- "Thank You" or custom closing
- Tagline: "Together, creating a more food secure world"

---

## Slide Count Guidance

| Document Length | Recommended Slides |
|----------------|-------------------|
| 1-5 pages | 5-8 slides |
| 5-15 pages | 8-12 slides |
| 15+ pages | 12-20 slides |
| Executive summary | 8-10 slides regardless of source |

Specify your target count in the prompt: "Create a 10-slide presentation"

---

## Quick Reference: Content to Template Mapping

| Content Type | Template Used |
|-------------|---------------|
| Opening, title | Full Height Promo Hero |
| 3-4 key numbers | Statistic Cards with Icons |
| 4-6 related metrics | Two Column Grid |
| Three features or benefits | Three Column Basic Cards |
| Step-by-step narrative | Alternating Horizontal |
| Product or interface demo | Text with Screenshot |
| Data table | Table Slide (branded) |
| Chart or graph | Chart Slide |
| Major section break | Section Divider |
| Closing | Closing Slide |

---

## Terminology Auto-Corrections

These corrections happen automatically:

| Original Term | Corrected To |
|---------------|-------------|
| suppliers | partners |
| consumers (B2B) | customers |
| eco-friendly | sustainable |
| synergy | collaboration |
| leverage / leveraging | use / using |
| best-in-class | leading |
| cutting-edge | innovative |
| circle back | follow up |
| solutions provider | partner |

---

## Color Reference for Context

When asking for specific color choices:

| Color | Hex | Use It For |
|-------|-----|------------|
| Cargill Leaf Green | #00843D | Primary - all brand elements |
| White | #FFFFFF | Backgrounds, text on dark |
| White Green | #F5F9ED | Slide backgrounds, light sections |
| Soft Green | #BDE588 | Accents only |
| Deep Green | #03441F | Dark hero slides, section dividers |
| Sky Blue | #57D1FF | Hero accent stripes, charts only |
| Rich Red | #EA5062 | Hero accent stripes, charts only |
| Bright Yellow | #FFBC27 | Hero accent stripes, charts only |

---

## Tips for Best Results

### Do This

- Upload the original source document (not a screenshot)
- Specify target audience when relevant ("for executive leadership" vs. "for farmer partners")
- Mention key themes to emphasize ("focus on sustainability impact")
- Specify slide count if you have a target
- Tell the system if it's for a specific event ("for the annual meeting")

### Avoid This

- Do not ask the system to change any facts, statistics, or data
- Do not ask for fonts other than Big Caslon and Helvetica Now
- Do not ask for colors outside the Cargill palette (it will be corrected automatically)
- Do not ask for more than 20 slides (quality degrades beyond that)

---

## Troubleshooting

### "The presentation looks generic"

Add more context in your prompt: specify the audience, the purpose, and which content to emphasize. The system preserves your content but needs direction on what to highlight.

### "Some data is missing from the slides"

Long documents are condensed. Specify which sections are most important: "Prioritize the Regional Performance and Sustainability sections."

### "The charts don't look right"

Describe the chart type you need: "Use a bar chart comparing Q1-Q4" or "Show this as a pie chart." The system will follow explicit chart instructions.

### "I need the brand fonts but they're not showing"

Brand fonts (Big Caslon for Cargill and Helvetica Now for Cargill) must be installed on your system. In ChatGPT Code Interpreter, Georgia and Arial are used as fallbacks. For full brand fonts, use the standalone Python package locally.

---

## Quality Standard

Every output from this system is designed to meet one bar:

**The presentation must be indistinguishable from work produced by Cargill's professional design and communications teams.**

If something doesn't meet that standard, describe the issue and request a revision.
