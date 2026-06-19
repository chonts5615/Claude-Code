---
name: report-format-qc
description: Quality-check the formatting and brand consistency of a drafted research report (its markdown copy at files/reports/report.md). Flags missing/empty sections, heading-hierarchy problems, uncaptioned or missing figures, inconsistent typography vs the brand, missing page numbers, and reference-formatting issues, and returns actionable fixes. Use during QA so formatting problems feed the revision pass.
---

# report-format-qc

A formatting and brand-consistency checklist for QA. This skill **checks and
flags** (it does not rewrite the report). Review `files/reports/report.md` and
the chart filenames in `files/charts/`; never open the binary PDF or PNGs.

Score each item Pass / Minor / Fail and record specific, actionable fixes.

## Structure
- Title and date present.
- Executive summary present and non-empty.
- A clear section for each subtopic; no empty or stub sections.
- Conclusion / key takeaways present.
- References section present.

## Headings & hierarchy
- One H1 (title); sections use consistent heading levels (no skips like H1→H3).
- No duplicate or orphan headings; sentence/title case is consistent.

## Figures
- Every chart in `files/charts/` is either used or intentionally omitted.
- Each embedded figure is referenced in the text and has a caption.
- No figure is so large it pushes content off the page (flag if likely).

## Consistency & brand
- Headings/body use the brand fonts; colors used match the brand palette.
- Terminology, units, and number formatting are consistent throughout.
- Cover page and footer/page numbers are present (per the brand config).

## References & citations
- Reference style is consistent.
- Source URLs are included where the notes provide them.
- In-text claims are traceable to a reference.

## Output
Add a `## Formatting & branding` section to the QA review listing each Fail/Minor
with the exact location and a concrete fix (e.g. "Section 3 has no figure caption
— add 'Figure 2. …'"). Treat any **Fail** in Structure or References as grounds
for `QA VERDICT: REVISE`.
