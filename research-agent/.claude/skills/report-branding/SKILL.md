---
name: report-branding
description: The brand specification applied to every generated report PDF — cover page, color palette, typography, and a footer with page numbers — driven by a configurable brand config JSON with a neutral professional default. Implemented deterministically by the PDF renderer (research_agent/render.py) so branding is consistent on every run.
---

# report-branding

This skill is the **brand specification** for report PDFs. Branding is applied
deterministically in code (`research_agent/render.py`) from a brand config JSON,
which guarantees a consistent visual identity without relying on an agent to
style the document. Pass a custom config with `--brand-config path/to/brand.json`
(or edit `research_agent/config/brand.json`); any missing key falls back to the
neutral default below.

## Brand config keys

| Key | Default | Effect |
|-----|---------|--------|
| `brand_name` | "" | Small uppercase line above the title on the cover (skipped if empty) |
| `tagline` | "" | Line under the title on the cover (skipped if empty) |
| `primary_color` | `#1F2937` | Title, H1/H2 headings |
| `secondary_color` | `#4B5563` | Captions, footer, table grid |
| `accent_color` | `#2563EB` | H3/subheadings, table header fill |
| `background_tint` | `#F5F7FA` | Zebra-striped table rows |
| `heading_font` | `Helvetica-Bold` | Headings (reportlab built-in font) |
| `body_font` | `Helvetica` | Body text |
| `logo_path` | "" | Reserved for a cover logo |
| `footer_text` | `Confidential` | Left side of the page footer |
| `cover_page` | `true` | Render a dedicated cover page |
| `page_numbers` | `true` | Show "Page N" in the footer |

Use only reportlab built-in fonts (`Helvetica`, `Helvetica-Bold`, `Times-Roman`,
`Courier`) unless you register a custom font.

## What the renderer produces

- A cover page (title + optional brand name/tagline) when `cover_page` is set.
- Headings, body, and tables styled from the palette/fonts above.
- All charts in `files/charts/` embedded in a "Figures" section with captions.
- A footer with `footer_text` and, if `page_numbers`, the page number on every page.

## Definition of done

The PDF has a consistent cover, heading/body fonts and colors from the config,
captioned figures, and a page-numbered footer — coherent, single-brand output.
