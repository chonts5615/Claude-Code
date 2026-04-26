# Document Structure Specification

This file defines the exact section order, heading hierarchy, and content placement rules for the SME Validation Package Word document. Follow this structure precisely for every specialization variant.

---

## Page Setup

| Property | Value | Notes |
|---|---|---|
| Page size | US Letter (8.5" x 11") | 12240 x 15840 DXA |
| Margins | 1" all sides | 1440 DXA each |
| Orientation | Portrait | |
| Content width | 6.5" | 9360 DXA |
| Header | Cargill wordmark (right-aligned) + document title (left-aligned) | Starts on page 2 |
| Footer | "Cargill Confidential" (left) + page number (right) | All pages |

## Font Mapping

| Element | Primary Font | Fallback Font | Size | Color |
|---|---|---|---|---|
| Document title (cover) | Big Caslon for Cargill | Georgia | 28pt | #00843D (Leaf Green) |
| Section headings (H1) | Big Caslon for Cargill | Georgia | 22pt | #00843D (Leaf Green) |
| Subsection headings (H2) | Helvetica Now Bold | Arial Bold | 14pt | #333333 |
| Sub-subsection (H3) | Helvetica Now Bold | Arial Bold | 12pt | #333333 |
| Body text | Helvetica Now Regular | Arial | 11pt | #333333 |
| Table header text | Helvetica Now Bold | Arial Bold | 10pt | #FFFFFF (white on green) |
| Table body text | Helvetica Now Regular | Arial | 10pt | #333333 |
| Competency name (in table) | Helvetica Now Bold | Arial Bold | 11pt | #00843D |
| Rating scale labels | Helvetica Now Regular | Arial | 10pt | #333333 |
| Footer text | Helvetica Now Regular | Arial | 8pt | #666666 |
| Confidentiality notice | Helvetica Now Italic | Arial Italic | 9pt | #666666 |

## Color Application

| Element | Color | Hex |
|---|---|---|
| H1 headings | Cargill Leaf Green | #00843D |
| Cover page title | Cargill Leaf Green | #00843D |
| Horizontal rules | Cargill Leaf Green | #00843D |
| Table header row background | Cargill Leaf Green | #00843D |
| Table header row text | White | #FFFFFF |
| Table alternating row | White Green | #F5F9ED |
| Competency name accent | Cargill Leaf Green | #00843D |
| Body text | Dark Gray | #333333 |
| Secondary text / captions | Medium Gray | #666666 |
| Page borders / table borders | Light Gray | #CCCCCC |

---

## Section Order (Top to Bottom)

### Page 1: Cover Page

No header or footer on cover page. Content centered vertically.

```
[Cargill Logo — if available, otherwise Leaf Green horizontal rule]

[36pt vertical space]

Technical Competency Validation Package
[Big Caslon, 28pt, Leaf Green]

{{SPECIALIZATION_NAME}}
[Helvetica Now Bold, 18pt, #333333]

Cargill Legal & Compliance
[Helvetica Now Regular, 14pt, #666666]

[24pt vertical space]

Prepared for: Subject Matter Expert Review Panel
Prepared by: Assessment, Competency & Career Framework Team
Date: {{SESSION_DATE}}
[Helvetica Now Regular, 11pt, #333333]

[36pt vertical space]

[Confidentiality notice block — Helvetica Now Italic, 9pt, #666666, bordered box with #CCCCCC border]
```

### Page 2: Table of Contents

Auto-generated TOC covering H1 and H2 headings. Dot leaders to page numbers.

### Pages 3+: Document Body

The sections below appear in this exact order. Each H1 section starts at the top of a new page (page break before).

---

#### Section 1: Project Overview (H1)
- Purpose Statement (body text from stable-content.md)
- What We Are Asking You to Do (H2, body text from stable-content.md)

#### Section 2: Focus Group Protocol (H1)
- Session Structure (H2, body text from stable-content.md)
- Ground Rules (H2, body text from stable-content.md)

#### Section 3: Rating Scales (H1)
- Relevance Scale (H2, formatted as a styled table)
- Clarity Scale (H2, formatted as a styled table)
- Level Differentiation Scale (H2, formatted as a styled table)

Rating scale tables use this format:

| Rating | Label | Definition |
|---|---|---|
| 5 | Essential | [definition text] |
| 4 | Important | [definition text] |
| ... | ... | ... |

Table styling: Leaf Green header row, white/White Green alternating body rows, #CCCCCC borders.

#### Section 4: Competency Architecture Reference (H1)
- Three-Layer Model Overview (H2, body text from stable-content.md)
- Proficiency Level Definitions (H2, formatted as a styled table)
- Band Mapping Reference (H2, body text from stable-content.md)

#### Section 5: Technical Competencies Under Review (H1) — VARIABLE

This is the core section. For EACH competency provided by the user, generate:

##### Competency Block Structure (repeats per competency)

```
Competency [N] of [Total]: {{COMPETENCY_NAME}}
[H2, Helvetica Now Bold, 14pt, preceded by a Leaf Green horizontal rule]

Definition: {{COMPETENCY_DEFINITION}}
[Body text, italicized]

[Competency indicator table — see below]

SME Rating Box:
  Relevance (1-5): ___    Clarity (1-3): ___    Level Differentiation (1-3): ___
  Comments: _______________________________________________

[If shared competency: "Note: This competency is shared across multiple specializations. Your feedback will be considered alongside input from other specialization SME panels."]
```

##### Competency Indicator Table Format

| Level | Behavioral Indicators |
|---|---|
| **L4 — Expert / Thought Leader** | [indicator 1] |
| | [indicator 2] |
| | [indicator 3] |
| **L3 — Advanced Practitioner** | [indicator 1] |
| | [indicator 2] |
| | [indicator 3] |
| **L2 — Practitioner** | [indicator 1] |
| | [indicator 2] |
| | [indicator 3] |
| **L1 — Foundational** | [indicator 1] |
| | [indicator 2] |
| | [indicator 3] |

Table styling:
- Present L4 first (top) through L1 (bottom) — descending order so SMEs see the highest level first
- Level column: 1.5" wide, Leaf Green background with white bold text
- Indicators column: 5" wide, white/White Green alternating per indicator row
- Each indicator on its own row within the level grouping
- Borders: #CCCCCC, 0.5pt

#### Section 6: Essential Functions Crosswalk (H1) — VARIABLE

##### Essential Functions by Band (H2)

Present the essential functions for each band in separate subsections:

```
Manager II Essential Functions (H3)
[Numbered list of essential functions from the JD]

Advisor Essential Functions (H3)
[Numbered list of essential functions from the JD]
```

##### Competency-to-Essential-Function Mapping (H2)

A crosswalk matrix table:

| Competency | EF 1 | EF 2 | EF 3 | EF 4 | EF 5 | EF 6 |
|---|---|---|---|---|---|---|
| {{Competency 1}} | X | X | | | X | |
| {{Competency 2}} | | X | X | | | X |
| ... | | | | | | |

Where "X" indicates the competency is exercised in performing that essential function. Use abbreviations for EF column headers if the full text is too long (provide a key below the table).

Table styling: Leaf Green header row. The mapping cells use centered "X" marks. Empty cells are blank. Compact font (10pt).

##### SME Prompt (body text)
```
Review the mapping above. For each competency:
  — Is the mapping accurate? Are there essential functions that should be linked (or unlinked)?
  — Are there essential functions not covered by any competency? If so, what technical capability is missing?
```

#### Section 7: Validation Methodology Note (H1)
- Body text from stable-content.md
- This section is intentionally brief — SMEs do not need deep psychometric detail, but the methodology note supports audit defensibility.

#### Section 8: Confidentiality and Data Handling (H1)
- Body text from stable-content.md

#### Section 9: Contact Information (H1)
- Body text from stable-content.md

---

### Appendices

#### Appendix A: Job Description — {{SPECIALIZATION_NAME}} (H1) — VARIABLE
- Full or excerpted JD content provided by the user
- Formatted as body text with the original JD structure preserved
- This appendix gives SMEs direct access to the source JD for reference during discussion

#### Appendix B: Glossary of Terms (H1)
- Body text from stable-content.md
- Formatted as a two-column table (Term | Definition)

#### Appendix C: SME Panel Roster (H1) — VARIABLE, OPTIONAL
- Only included if SME panel info is provided

| Name | Title | Specialization | Years of Experience |
|---|---|---|---|
| {{name}} | {{title}} | {{specialization}} | {{years}} |

---

## Spacing Rules

| Between | Space |
|---|---|
| H1 and first paragraph | 240 DXA (before: 360, after: 240) |
| H2 and first paragraph | 180 DXA (before: 240, after: 180) |
| Body paragraphs | 120 DXA after |
| Before competency block | Page break or 480 DXA minimum |
| Table and following paragraph | 240 DXA |
| Rating box and next competency | 360 DXA |

## Horizontal Rules

Use Cargill Leaf Green (#00843D) horizontal rules:
- Below the cover page title
- Before each competency block in Section 5
- Before each appendix

Implemented as paragraph bottom borders (not table-based rules):
```
border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "00843D", space: 1 } }
```
