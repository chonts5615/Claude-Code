# Bloom Beauty Suites — brand reference

The single source of truth for Bloom's visual identity, mirrored from the React
apps' `theme.js` (`bloom-beauty-suites/src/theme.js`,
`bloom-suites-manager/src/theme.js`). Apply this to every Bloom deliverable.
**Never** use Cargill's Leaf Green here — that palette belongs to a different
plugin and a different brand.

## Palette

| Token | Hex | Use |
|---|---|---|
| `rose` | `#e8a0b4` | Primary accent — headings, key buttons, chart series 1 |
| `roseMed` | `#f8bbd0` | Secondary accent, hovers |
| `roseLight` | `#fce4ec` | Soft fills, callout backgrounds |
| `blush` | `#f9e8e0` | Section backgrounds |
| `cream` | `#fdf6f0` | Card backgrounds |
| `ivory` | `#fffaf5` | Page background |
| `bg` | `#faf7f5` | App canvas background |
| `gold` | `#c9a96e` | Premium accent, dividers, chart series 2 |
| `goldLight` | `#f5e6c8` | Soft gold fills |
| `charcoal` | `#2d2d2d` | Body text |
| `gray` | `#6b6b6b` | Secondary text |
| `grayBorder` | `#e8e0dc` | Borders, rules |
| `white` | `#ffffff` | Surfaces |

**Status colors** (match the app exactly): success `#4caf50` on `#e8f5e9`;
warning/amber `#ff9800` on `#fff3e0`; error `#e53935` on `#ffebee`.

**Chart palette** (`PIE_COLORS` in the app): `#e8a0b4` (rose), `#c9a96e` (gold),
`#b39ddb` (lavender), `#80cbc4` (teal), `#ffab91` (peach).

## Typography

- Headings: an elegant serif (e.g. **Georgia** / "Playfair"-style) in `charcoal`
  or `rose`.
- Body: a clean sans-serif (e.g. **Helvetica/Arial**) in `charcoal`.
- Keep generous white space; the brand reads soft, warm, and premium — not
  corporate.

## Voice

Warm, encouraging, confident, and personal — owner-to-client, not
corporation-to-consumer. First names. Short sentences. Beauty-forward but never
hypey. The owner is **Renee**; the business is **Bloom Beauty Suites & Lash Bar**
at 9325 Upland Ln N, Maple Grove, MN.

## Facts pulled from the apps (keep deliverables consistent with these)

- **Service menu & prices** (`bloom-beauty-suites/src/seed.js`): Classic Full Set
  $165, Hybrid Full Set $195, Volume Full Set $225; Classic Fill (2wk) $75 → Volume
  Fill $110–$125; Lash Lift & Tint $85; Brow Lamination $75; Lash Removal $35.
- **Suite inventory** (`bloom-suites-manager/src/seed.js`): 12 suites — 100 sqft
  @ $550, 140 sqft @ $650, 180 sqft @ $750.
- **Landlord settings**: rent due the 1st, 5-day late grace, 60-day lease-renewal
  window; monthly building expenses ≈ mortgage $4,200 + utilities $680 +
  insurance $240 + cleaning $320 + internet $140 + other $200 = **$5,780**.
