# Translation QA Protocol

The Phase 5 gate. Run per file, per language. Nothing ships until every check passes clean — defects found here are fixed and the affected checks re-run. The output is a QA log the user can hand to a stakeholder as evidence of process.

## Check 1 — Completeness Audit

**Question:** Did every piece of the original make it into the translation?

- Reconcile the output against the Phase 1 segment manifest: every manifest address must contain translated text (or its DNT English). Count parity first (segments in = segments out), then spot-verify addresses.
- Sweep the output for **English residue**: any Latin-alphabet sentence fragments in a non-Latin-script file are trivially findable; for Latin-script targets, search for high-frequency English function words (` the `, ` and `, ` of `, ` with `) and English-only spellings — every hit must be justified by the DNT list.
- Verify the easily-dropped locations one by one: headers, footers, footnotes, text boxes, speaker notes, chart labels, sheet tabs, cell comments, alt text.
- Verify nothing was **added**: no translator notes, no duplicated paragraphs, no leftover placeholder text.

## Check 2 — Back-Translation Spot Check

**Question:** Does the translation mean what the original means?

Back-translate a risk-weighted sample into English *without looking at the original source text during the back-translation*, then compare:

| Sample tier | Coverage |
|---|---|
| All headings and titles | 100% |
| All instructions, interview questions, probes | 100% |
| All rating anchors and scale labels | 100% |
| All numbered requirements / policy statements | 100% |
| Remaining body text | random 10% of segments |

Compare meaning, not wording. Classify each divergence:

- **Meaning shift** (defect — must fix): the back-translation would lead a reader to a different understanding, action, or rating.
- **Register shift** (defect if audience-relevant): correct meaning, wrong formality or tone for the audience.
- **Benign restructuring** (pass): different sentence shape, identical meaning — this is what good translation looks like; do not "fix" it toward literalness.

For high-stakes files, upgrade the body-text sample to 25% or 100% at the user's request.

## Check 3 — Terminology Consistency Scan

Per `references/terminology.md` enforcement section: approved renderings present everywhere the English term appeared; rival renderings at zero; raw English only where DNT permits. Scan **across files in a set**, not just within one file — a cross-file mismatch on a competency title is a defect even if both files are internally consistent.

## Check 4 — Format and Layout Audit

**Question:** Is it the same document?

- File opens without repair prompts in its native application (or clean render check where the app isn't available).
- Structural inventory matches the original: page/slide/sheet count intent, style usage, table dimensions, image count and placement, chart count and type, header/footer presence, branding elements (logo, colors, fonts) untouched.
- **Overflow sweep** (the expansion languages' main failure mode): no clipped text in table cells, no text outside shape bounds, no truncated chart labels, no `#####`-style clipping in Excel columns, no pushed pagination that orphans headings. Check German and Russian outputs first — if they fit, shorter languages almost certainly do.
- Font rendering: zh-CN and ru-RU outputs display actual glyphs, not tofu boxes (□□□) — confirms the companion-font rule was applied where needed.
- Every deliberate layout adjustment made under the format-fidelity remedies (widened column, −2pt font) appears in the QA log.

## Check 5 — Locale Mechanics

Verify against the file's language profile: date formats, decimal/thousands separators in text, quotation mark style, list punctuation, spacing rules (fr-FR non-breaking spaces before `: ; ? !`; fr-CA's narrower rule), mandatory marks (es opening ¿ ¡), capitalization conventions (de noun caps, nl/fr sentence-case headings), correct formal address used consistently (no mid-document Sie→du or usted→tú slips), and **no variant mixing** (no vosotros in es-419, no fr-FR anglicisms in fr-CA, no Traditional characters in zh-CN).

## The QA Log

One row per file × language:

| Field | Content |
|---|---|
| File / Language | `Interview_Guide_de-DE.docx` |
| Segments | manifest count / translated count |
| Checks 1–5 | PASS or PASS-after-fix (with defect count) |
| Defects fixed | one line each: location, what was wrong, what was done |
| Deliberate adjustments | logged layout remedies, TOC-refresh instructions, PDF reconstruction notes |
| Residual risks | anything the user should know (OCR confidence, pan-regional number-format choice, recommendation for native review) |

## Native-Speaker Review (Recommended Final Mile)

For candidate-facing, legal-adjacent, or externally published material, recommend a native-speaker review after the gate passes. Make it cheap for the reviewer: offer a **bilingual review table** per file (columns: address | English | translation | reviewer comment), generated from the segment manifest, so a reviewer can work through a document in minutes without flipping between files. Reviewer edits flow back through the glossary drift rule (terminology changes are project-wide) and re-trigger checks 3–5 on affected files.
