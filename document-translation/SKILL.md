---
name: document-translation
description: >
  Turn an approved English document or document set (Word, Excel, PowerPoint, PDF, or a
  mix) into format-identical, contextually accurate translated versions in one or more
  target languages. Built for the standard Cargill target set — Chinese (Simplified),
  Dutch, French, French-Canadian, German, Indonesian (Bahasa), Polish, Portuguese,
  Russian, Spanish, and Latin American Spanish — but handles any language the user
  names. Use this skill whenever the user asks to "translate this document," "create
  translated versions," "localize the interview guide," "produce the Chinese, German,
  or Spanish version," "we need this in 11 languages," "make language versions of the
  packet," or uploads an approved deliverable (interview guide, SME package, competency
  document, training material, policy, survey, scorecard) and asks for it in another
  language. Also trigger for translation QA requests — "check this translation,"
  "back-translate this," "is this translation accurate" — and for setting up a
  reusable translation glossary or terminology list. The deliverable contract: one
  output file per language per source document, identical in format, layout, and
  branding to the English original, such that a native speaker reading the translated
  version comes away with the same understanding as an English reader of the original.
---

# Document Translation

Convert approved English documents into translated versions that are **format-identical** (same file type, layout, styles, branding, pagination intent) and **meaning-identical** (a native speaker gains the same understanding an English reader would), across any combination of Word, Excel, PowerPoint, and PDF sources.

## The Two Non-Negotiable Contracts

1. **Format fidelity.** The translated file is the same file type as the source with every style, table, header/footer, chart, image, and branding element intact. Only the text changes. A side-by-side page flip of English vs. translated should look like the same document in a different language.
2. **Meaning fidelity.** Translation is meaning-for-meaning, not word-for-word. Idioms, HR/talent terminology, instructions, and rating anchors must land with the same intent, register, and usability for a native speaker. Literal translations that a native speaker would find stilted, ambiguous, or unintentionally comic are defects.

## Mandatory Co-Skills

Read and apply these companion skills before producing any deliverables:

| Co-Skill | When to Read | Why |
|---|---|---|
| `docx/SKILL.md` | Source or output includes Word | In-place text replacement that preserves styles, tracked structure, tables |
| `xlsx/SKILL.md` | Source or output includes Excel | Cell-level replacement preserving formulas, validation, conditional formatting |
| `pptx/SKILL.md` | Source or output includes PowerPoint | Shape/placeholder text replacement preserving layouts and masters |
| `pdf/SKILL.md` | Source includes PDF | Text/structure extraction, OCR for scanned pages, rebuild-and-render path |
| `cargill-branding/SKILL.md` | Output destined for Cargill audiences | Branding must survive translation untouched |
| `document-fidelity-guard/SKILL.md` | Any revision round on a translated version | Prevents drift when translations are iterated |

## Standard Target Languages

The default request set. Confirm which subset the user needs; if they say "all languages" or "the usual set," use all eleven.

| Language | Locale code | File suffix |
|---|---|---|
| Chinese (Simplified) | zh-CN | `_zh-CN` |
| Dutch | nl-NL | `_nl-NL` |
| French | fr-FR | `_fr-FR` |
| French (Canadian) | fr-CA | `_fr-CA` |
| German | de-DE | `_de-DE` |
| Indonesian (Bahasa Indonesia) | id-ID | `_id-ID` |
| Polish | pl-PL | `_pl-PL` |
| Portuguese (Brazilian) | pt-BR | `_pt-BR` |
| Russian | ru-RU | `_ru-RU` |
| Spanish (European) | es-ES | `_es-ES` |
| Spanish (Latin American) | es-419 | `_es-419` |

Confirm one ambiguity at intake: "Portuguese" defaults to **pt-BR** (ask if pt-PT is intended). French and French-Canadian, and European vs. Latin American Spanish, are **distinct deliverables** — never ship one file for both. Per-language register, mechanics, and terminology guidance lives in `references/language-profiles.md`.

## The Workflow

### Phase 0 — Intake and Inventory

1. Inventory every source file: filename, format, page/slide/sheet count.
2. Confirm the target-language subset and the Portuguese variant.
3. Confirm the source documents are **approved/final**. Translation multiplies every later edit by the number of languages — if the English is still moving, say so and recommend waiting or scoping to a frozen version.
4. For PDFs, determine the path: (a) the user has the original Word/PPTX source — always prefer it; (b) digital PDF with extractable text; (c) scanned PDF requiring OCR. State which path applies before starting.

### Phase 1 — Extraction and Segment Manifest

Build a **segment manifest** per document: every translatable text element with a stable address (paragraph index, table row/cell, slide/shape, sheet/cell, header/footer, footnote). This manifest is the completeness contract — Phase 5 audits against it.

Sweep the easily-missed locations: headers/footers, footnotes/endnotes, table of contents entries, text boxes, chart titles/axis labels/data labels, SmartArt, slide speaker notes, alt text, Excel sheet-tab names, cell comments, data-validation messages, print headers, document properties shown to readers. Anything a reader can see is in scope.

Mark **do-not-translate (DNT)** segments in the manifest: proper nouns (Cargill, product/system names), trademarked assessment names, formula references, file paths, email addresses, legal entity names, and any term the glossary locks. See `references/terminology.md`.

### Phase 2 — Terminology and Glossary

Before translating anything, establish the project glossary per `references/terminology.md`:

- DNT list (stays in English in every language).
- Locked renderings for recurring HR/talent terms (competency, behavioral indicator, proficiency level, rating anchors like "Meets Expectations") — one approved translation per term per language, applied everywhere.
- Decisions the user must make once, not per file: Do competency titles stay English with translation in parentheses, or translate fully? Are rating-scale anchors translated? Is the company voice formal or informal in each language (see language profiles for defaults)?

If a prior translation project exists for this document family, reuse its glossary — consistency across a document set outranks a marginally better new rendering.

### Phase 3 — Translation

Translate the manifest, one language at a time, applying `references/language-profiles.md` for that language:

- Meaning-for-meaning. Restructure sentences where the target language demands it.
- Apply the locked glossary renderings mechanically — no synonyms for locked terms.
- Match register: professional HR documents default to formal address (Sie, vous, usted, u, Pan/Pani conventions per profile) unless the user directs otherwise.
- Localize mechanics: dates, decimal/thousands separators, quotation marks, list punctuation per profile.
- Instructions and questions must remain **actionable**: an interviewer reading the translated probe must be able to ask it naturally aloud. Read translated questions "aloud" mentally — if a native speaker would rephrase before speaking it, rephrase it now.
- Preserve inline emphasis boundaries: if the English bolds one phrase, the translation bolds the corresponding phrase, not a literal word-position span.

### Phase 4 — Format-Identical Reconstruction

Rebuild each output file by **in-place text replacement in a copy of the original file** — never by generating a new document from scratch. Per-format procedures (python-docx, openpyxl, python-pptx, PDF rebuild path, text-expansion handling) are in `references/format-fidelity.md`. Key rules:

- Copy the source file first; replace text run-by-run/cell-by-cell inside the copy.
- Never touch styles, themes, masters, column widths, or branding elements.
- Plan for text expansion (German/Russian/French run 15–35% longer than English; Chinese runs shorter) — check for overflow, wrap, and truncation after replacement.
- Excel: translate displayed text only; **never** translate formula function names, defined names, or values other cells compute on. If a formula concatenates literal English strings, translate the string literal inside the formula, not the function.
- PDF: output a PDF whose layout matches the original page-for-page, produced via the best available path from Phase 0.

Naming convention: `<OriginalName>_<locale>.<ext>` (e.g., `Interview_Guide_Plant_Manager_de-DE.docx`). Keep the English filename stem untranslated so file sets sort together.

### Phase 5 — QA Gate (Required Before Delivery)

Run the full protocol in `references/qa-protocol.md`. Minimum bar, per language, per file:

1. **Completeness audit** — every manifest segment has a translated counterpart; no English residue outside the DNT list; no dropped footnotes, notes, or hidden-but-visible elements.
2. **Back-translation spot check** — back-translate a risk-weighted sample (all headings, all instructions/questions, all rating anchors, plus a random 10% of body segments) to English and compare meaning against the original. Meaning shifts are defects.
3. **Terminology consistency scan** — every glossary term appears only in its locked rendering.
4. **Format/layout audit** — file opens cleanly; styles, tables, charts, branding intact; no text overflow, truncation, or pagination breakage from expansion.
5. **Locale mechanics check** — dates, numbers, punctuation, and address forms match the language profile.

Report QA results in a per-language log (source file, language, segment count, defects found and fixed, residual risks). Defects found in QA are fixed and re-checked — the gate passes only clean.

### Phase 6 — Delivery

Deliver one file per language per source document plus a short **translation QA summary** (one table: file × language × QA status × notes). Recommend, but do not require, a native-speaker review pass for high-stakes documents — state plainly that machine-era translation plus this QA protocol is strong but a native reviewer is the final mile for legal or candidate-facing material. Offer to produce a reviewer-friendly bilingual table (English | translation, segment by segment) on request to make that review fast.

## Multi-Document Sets

When the request is a set (e.g., an interview guide + scorecard + rating workbook):

- Build **one glossary for the whole set** before translating anything, so shared terms render identically across files.
- Translate set-by-language, not file-by-language (all files into German, then all into Polish) — this keeps per-language voice and terminology coherent.
- Cross-file consistency is part of QA: a competency titled one way in the guide and another way in the scorecard is a defect even if each rendering is individually fine.

## Scope Boundaries

- **This skill translates approved content; it does not edit it.** If the English source contains an error, flag it to the user — do not silently fix it in eleven languages and leave the English wrong, and do not propagate it silently either.
- Certified/sworn translation for legal filings is out of scope — say so if the user's use case implies it.
- Running the equivalent workflow in ChatGPT Enterprise (as a Project / custom GPT) is documented in `references/chatgpt-enterprise-guide.md` — hand that file to the user when they ask for the ChatGPT-side setup.
