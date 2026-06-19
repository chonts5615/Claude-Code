---
name: report-branding
description: Apply a configurable visual brand to a generated PDF research report — cover page, color palette, typography, and a header/footer with page numbers — using reportlab. Reads a brand config JSON and falls back to a neutral professional default. Use when producing or restyling a report PDF so its visual identity is consistent and polished.
---

# report-branding

Apply a consistent visual identity to the report PDF. This skill **applies**
branding (it changes the output); it does not merely check it.

## 1. Load the brand config

Read the brand config JSON. The lead agent gives you its absolute path; if no
path is provided or the file is missing, use these neutral defaults:

| Key | Default | Use |
|-----|---------|-----|
| `brand_name` | "" (none) | Cover page line above the title (skip if empty) |
| `tagline` | "" | Small line under the title on the cover (skip if empty) |
| `primary_color` | `#1F2937` | Title, H1/H2 headings, section rules |
| `secondary_color` | `#4B5563` | Body de-emphasis, captions |
| `accent_color` | `#2563EB` | Subheadings, table header fills, figure captions, links |
| `background_tint` | `#F5F7FA` | Cover background band, callout/table-zebra fills |
| `heading_font` | `Helvetica-Bold` | All headings (use a reportlab built-in) |
| `body_font` | `Helvetica` | Body text |
| `logo_path` | "" | Logo image on the cover (skip if empty/missing) |
| `footer_text` | `Confidential` | Left side of the page footer |
| `cover_page` | `true` | Whether to render a dedicated cover page |
| `page_numbers` | `true` | Whether to number pages |

Only use reportlab built-in fonts (`Helvetica`, `Helvetica-Bold`, `Times-Roman`,
`Courier`) unless the config names a font you register yourself.

## 2. Apply it in the reportlab build

- **Cover page** (if `cover_page`): a top color band in `primary_color`; the
  `brand_name` (if set) small and uppercase; the report title large in white or
  `primary_color`; the date and `tagline` beneath; the logo (if `logo_path` set
  and the file exists). Keep it clean — one page.
- **Headings**: `heading_font` in `primary_color` for H1/H2, `accent_color` for
  H3/subheadings. Add a thin `primary_color` rule under H1s.
- **Body**: `body_font`, ~10–11pt, generous leading.
- **Tables**: header row filled with `accent_color` (white text); alternate row
  fill with `background_tint`.
- **Figures**: embed charts at a readable width (~6.5in); caption in
  `secondary_color`, prefixed "Figure N." in `accent_color`.
- **Header/footer** (drawn on every page via an `onPage` callback): footer with
  `footer_text` on the left and, if `page_numbers`, "Page X of Y" on the right in
  `secondary_color`; a hairline rule above the footer.

## 3. Pattern

Use a reportlab `canvas` `onPage`/`onLaterPages` callback for the header/footer
and page numbers, and `ParagraphStyle`s derived from the config for headings and
body. Build with `SimpleDocTemplate`. Verify the PDF renders and the cover,
fonts, and footer reflect the config before finishing.

## Definition of done

The PDF has a cover (unless disabled), consistent heading/body fonts and colors
from the config, captioned figures, and a footer with page numbers — and it
would look like it belongs to one coherent brand.
