# Format Fidelity Procedures

How to produce a translated file that is byte-for-byte identical to the source except for the text. The governing rule for every format:

> **Copy the original file. Replace text inside the copy. Never regenerate the document from scratch.**

Generating a "similar-looking" new document always loses something — a style, a footer, a table border, a chart color, the branding. In-place replacement can only lose what you touch.

## General Procedure (all formats)

1. `cp original.ext original_<locale>.ext` — work only on the copy.
2. Walk the file with the format's library and emit the **segment manifest** (address + English text) — this is Phase 1 output.
3. Translate the manifest (Phases 2–3), producing an address → translated-text map.
4. Walk the copy again and write translated text back by address.
5. Open/render the result and run the Phase 5 layout audit.

Rules that apply everywhere:

- **Replace at the run level where possible, paragraph level where necessary.** A paragraph is often split into multiple runs (bold word mid-sentence, tracked-change fragments, spell-check artifacts). If runs split mid-word/mid-phrase, collapse the paragraph's text, translate it whole, then redistribute: put the full translation in the first run and empty the rest, *except* when runs carry distinct formatting (bold/italic/color) — then map the emphasized English span to the corresponding translated span and rebuild runs to match.
- **Never modify** style definitions, themes, masters, numbering definitions, section properties, column widths/row heights (except where the expansion audit forces a deliberate, logged adjustment), images, or brand elements.
- **Whitespace and field codes:** preserve leading/trailing spaces, tabs, line breaks, and field codes (page numbers, TOC fields, cross-references) exactly. Translate a field's *result text* only when it's static text; live fields get re-evaluated by the app.
- **Hyperlinks:** translate the display text, never the URL.

## Word (.docx) — python-docx

Enumerate, in order: body paragraphs, tables (cell by cell — cells contain paragraphs and possibly nested tables), headers and footers per section, footnotes/endnotes (python-docx exposes these only via the XML part — walk `document.part` related parts or use `docx`'s `footnotes_part`; do not skip them), text boxes and shapes (in `w:txbxContent` — reachable only via XML: iterate `document.element.body.iter()` for `//w:txbxContent//w:t`), and core properties if reader-visible.

```python
import copy, docx
doc = docx.Document("copy_de-DE.docx")

def iter_paragraphs(container):
    for p in container.paragraphs:
        yield p
    for t in container.tables:
        for row in t.rows:
            for cell in row.cells:
                yield from iter_paragraphs(cell)

for p in iter_paragraphs(doc):
    replace_paragraph_text(p, translations)   # run-aware replacement per rules above
for section in doc.sections:
    for hdrftr in (section.header, section.footer,
                   section.first_page_header, section.first_page_footer,
                   section.even_page_header, section.even_page_footer):
        for p in iter_paragraphs(hdrftr):
            replace_paragraph_text(p, translations)
doc.save("copy_de-DE.docx")
```

Traps: `cell.paragraphs` on merged cells yields the same paragraph via multiple cells — dedupe by paragraph XML identity or you'll double-replace. A TOC lists English headings until refreshed; after replacement, either update the TOC field results in XML or instruct the user to right-click → Update Field on first open (state which in the QA log). Tracked changes in an "approved" doc should not exist — if present, stop and ask whether to accept them first (recommended) rather than translating both the deleted and inserted text.

## Excel (.xlsx) — openpyxl

Translate: string cell values, sheet tab names, chart titles/axis titles, defined print headers/footers, cell comments/notes, data-validation input/error messages, text inside string literals of formulas (`="Total: "&B2` → translate `"Total: "` only).

**Never translate:** formula function names (`SUM`, `VLOOKUP` — locale display is Excel's job, the stored names are always English), defined names referenced by formulas, named-range strings used as lookup keys, or any cell whose text other cells match against (`VLOOKUP`/`MATCH`/`COUNTIF` criteria) — translating a lookup key breaks the formula silently. Before translating any cell, check whether its value is referenced as a string elsewhere: scan all formulas for the cell's text as a literal and for references to its address inside lookup functions. If a display label is also a lookup key, translate the label and the matching criteria together, and verify the workbook recalculates correctly.

```python
import openpyxl
wb = openpyxl.load_workbook("copy_pl-PL.xlsx")   # keep default rich features; do NOT use read_only
for ws in wb.worksheets:
    ws.title = translations.get(ws.title, ws.title)
    for row in ws.iter_rows():
        for cell in row:
            if cell.data_type == "s" and cell.value in translations:
                cell.value = translations[cell.value]
            elif cell.data_type == "f":
                cell.value = translate_string_literals(cell.value, translations)
wb.save("copy_pl-PL.xlsx")
```

Traps: openpyxl drops some content it doesn't model (certain chart types, VBA unless `keep_vba=True`, some conditional-formatting edge cases) — after saving, **diff the feature inventory** against the original (sheet count, chart count, CF rule count, validation count) and if anything was lost, fall back to editing the sheet XML inside the zip directly. Column widths sized for English labels will clip German/Russian — widen only the specific columns that clip, and log each adjustment. Do not touch number formats: locale-specific display (decimal comma) is applied by the reader's Excel locale, not by the file — but *text* cells containing hand-typed numbers must follow the language profile.

## PowerPoint (.pptx) — python-pptx

Translate: every shape with a text frame on every slide, tables in graphic frames, chart titles/axis/legend/data labels, grouped shapes (recurse into groups), speaker notes (`slide.notes_slide`), headers/footers, and slide-master/layout text **only** if it's real content (a footer tagline) rather than placeholder prompts.

```python
from pptx import Presentation
prs = Presentation("copy_fr-FR.pptx")

def walk_shapes(shapes):
    for sh in shapes:
        if sh.shape_type == 6:                     # group
            yield from walk_shapes(sh.shapes)
        elif sh.has_text_frame:
            yield sh
        elif sh.has_table:
            for row in sh.table.rows:
                for cell in row.cells:
                    yield cell                     # cell has .text_frame

for slide in prs.slides:
    for sh in walk_shapes(slide.shapes):
        replace_text_frame(sh.text_frame, translations)   # run-aware, per general rules
    if slide.has_notes_slide:
        replace_text_frame(slide.notes_slide.notes_text_frame, translations)
prs.save("copy_fr-FR.pptx")
```

Traps: PPTX is the format most punished by text expansion — titles and labels are sized to the English text. Autofit behavior lives on the text frame; where translated text overflows a fixed shape, prefer (in order): let existing autofit shrink it, reduce font size by max 2pt on that shape only (log it), or minimally rephrase tighter (log it). Never resize or move shapes — that changes the design. SmartArt text lives in a separate diagram part python-pptx doesn't model; edit `ppt/diagrams/data*.xml` inside the zip directly. Charts with cached data render label text from the cached values — translate the cached strings in the chart XML, and if the chart links to an embedded workbook, translate the matching cells there too so an edit-data action doesn't revert to English.

## PDF (.pdf)

PDFs are a rendered output format, not an editable source. Choose the path in this order:

1. **Original source file exists (Word/PPTX/Excel).** Always ask. Translate the source with the procedures above, then export to PDF. This is the only path that guarantees true fidelity — push for it.
2. **Digital PDF, no source.** Extract full text + layout (per `pdf/SKILL.md`). Reconstruct a Word/HTML intermediate that reproduces the layout (pages, columns, tables, images extracted and re-embedded, fonts matched as closely as licensing allows), verify the *English* reconstruction against the original page-by-page **before translating** — fidelity errors found after translation cost eleven times as much to fix. Then translate the intermediate and render to PDF.
3. **Scanned PDF.** OCR first (per `pdf/SKILL.md`), then path 2. Flag OCR confidence issues in the QA log; garbled OCR input produces confidently wrong translations.

For paths 2–3, set expectations with the user at intake: the translated PDF will be a faithful reconstruction, not a modification of the original file, and minor rendering differences (font metrics, exact line breaks) are expected and will be listed in the QA log.

## Text Expansion Management

| Direction | Languages | Planning factor |
|---|---|---|
| Expansion | de-DE (worst), ru-RU, fr-FR, fr-CA, pl-PL, es-*, pt-BR, nl-NL, id-ID | +10% to +35% |
| Contraction | zh-CN | −20% to −50% |

After replacement, audit every fixed-size container: table cells, text boxes, slide titles, chart labels, Excel columns, headers/footers. The allowed remedies, in order of preference: rely on existing wrap/autofit → tighten the translation (a shorter synonym with identical meaning) → widen the specific column / shrink the specific font by ≤2pt (logged) → escalate to the user if the layout genuinely cannot hold the language. Silent truncation or invisible overflow is a shipped defect — the QA layout audit exists to catch exactly this.
