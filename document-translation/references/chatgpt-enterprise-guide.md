# Running This Workflow in ChatGPT Enterprise

The document-translation workflow is tool-agnostic: the phases (intake → manifest → glossary → translate → reconstruct → QA → deliver) work in any capable AI environment. This guide maps the workflow onto ChatGPT Enterprise so the same process can run there when that is the available or mandated platform. Hand this file to the user when they ask for the ChatGPT-side setup.

## Capability Mapping

| Workflow need | Claude / Cowork | ChatGPT Enterprise |
|---|---|---|
| Read docx/xlsx/pptx/pdf | File upload + document skills | File upload (Advanced Data Analysis reads all four via Python) |
| In-place file reconstruction | Code execution (python-docx, openpyxl, python-pptx) | Advanced Data Analysis / Code Interpreter (same libraries: python-docx, openpyxl, python-pptx are available in its sandbox) |
| Reusable instructions | This skill | A **Project** (with project instructions + glossary as project files) or a **custom GPT** |
| Long documents / many languages | Long context | Work file-by-file and language-by-language; chunk long documents |
| Output delivery | File downloads | Sandbox file downloads (links expire — download promptly) |

The critical shared insight: in both platforms, format fidelity comes from **running code that edits a copy of the original file**, never from asking the model to "output the translated document" as chat text. If the ChatGPT session isn't using Advanced Data Analysis to manipulate the actual file, formatting fidelity is not being preserved.

## One-Time Setup: Create a Translation Project (or Custom GPT)

Create a ChatGPT Project named e.g. **Document Translation — Approved Deliverables** and paste instructions equivalent to this skill. A condensed instruction block that captures the contract:

```
You translate approved English business documents (docx, xlsx, pptx, pdf) into
target languages with two non-negotiable contracts:

1. FORMAT FIDELITY — Use Python (python-docx / openpyxl / python-pptx) to copy
   the uploaded file and replace text in place inside the copy. Never generate a
   new document from scratch. Never alter styles, themes, tables, charts,
   images, branding, column widths, or masters. Translate headers, footers,
   footnotes, text boxes, speaker notes, chart labels, sheet tabs, and cell
   comments — everything a reader can see.

2. MEANING FIDELITY — Translate meaning-for-meaning at professional register.
   A native speaker must come away with the same understanding as an English
   reader. Formal address (Sie / vous / usted / u / Вы / Pan-Pani / 您 / Anda)
   unless told otherwise. Localize dates, number separators, and punctuation
   to the target locale. Keep do-not-translate terms in English.

Target languages and codes: zh-CN, nl-NL, fr-FR, fr-CA, de-DE, id-ID, pl-PL,
pt-BR, ru-RU, es-ES, es-419. fr-FR≠fr-CA and es-ES≠es-419 — always produce
separate files. Never use vosotros in es-419; follow OQLF-leaning vocabulary
and Canadian punctuation spacing in fr-CA; Simplified characters only in zh-CN.

Process for every job:
1. Build a segment inventory of the file (every text element + its location).
2. Apply the attached glossary (DNT terms stay English; LOCKED terms use only
   the approved rendering).
3. Translate one language at a time; write the translation back into a copy of
   the original file with Python; name it <OriginalName>_<locale>.<ext>.
4. QA before delivering: (a) completeness — no untranslated residue, no dropped
   headers/footers/notes; (b) back-translate all headings, questions, and
   rating anchors to English and verify meaning matches; (c) glossary term
   consistency; (d) layout — no overflow/truncation from text expansion
   (German/Russian run ~20-35% longer); (e) locale mechanics.
5. Deliver the files plus a short QA log (defects found and fixed, residual
   risks). Recommend native-speaker review for candidate-facing material.

If the English source is still in draft, say so and stop. If a PDF is uploaded,
ask for the original Word/PowerPoint source first; only reconstruct from the
PDF if no source exists.
```

Attach to the project: the **glossary file** (see `references/terminology.md` — the same artifact serves both platforms) and, if available, this skill's `language-profiles.md` as a reference document.

## Session Pattern

Per job, in a fresh conversation inside the project:

1. Upload the approved file(s). State the target subset: "All 11" or a list.
2. Let it build and show the segment inventory; confirm counts look right (spot-check that headers/footers/notes were found).
3. Run **one language at a time**: "Produce the de-DE version now." Reviewing the first language's output carefully before commissioning the other ten catches systematic errors at 1× cost instead of 11×.
4. Download each file **immediately** — sandbox files expire; a lost sandbox means regenerating.
5. Ask for the QA log at the end and keep it with the deliverables.

## ChatGPT-Specific Cautions

- **Sandbox resets.** Long multi-language sessions can lose the sandbox state; files not yet downloaded are gone. Mitigate by downloading after every language and keeping sessions to a few languages each.
- **Silent scope-shrinking on long files.** On big documents the model may summarize-and-translate rather than translate exhaustively. The segment-count reconciliation in the QA step is the defense — insist on it, and on chunked processing for long files ("translate paragraphs 1–150, then continue").
- **Formula/lookup damage in Excel.** Explicitly restate the never-translate-lookup-keys rule when uploading workbooks with formulas; verify the workbook still calculates after translation.
- **Chat-text output.** If the model starts printing the translation in the chat instead of writing files, stop it and redirect to the code path — chat text has already lost the formatting.
- **Version claims.** Whatever the current model version is branded (e.g., "5.6"), the workflow does not change — the contracts and QA gate are the quality mechanism, not the model version.

## Splitting Work Across Both Platforms

A sane division when both are available: run the full pipeline in one platform per document set (glossary + translation + reconstruction + QA in one place), and use the *other* platform as an **independent back-translation checker** — upload the translated file and the English original, ask it to back-translate the risk-weighted sample and flag meaning divergences. Cross-model QA catches blind spots that same-model QA can miss. Do not split the translation itself across platforms mid-set: voice and terminology will drift.
