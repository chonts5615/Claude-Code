# Cargill IO-Psych Toolkit

Five skills that cover the talent-system steps **around** competency authoring,
each producing a defensible, branded deliverable. Grounded in:

- **Uniform Guidelines on Employee Selection Procedures** — 29 CFR Part 1607 (1978): the
  four-fifths rule (§4D), the three validation strategies (§5/§14), and the §15
  documentation categories.
- **SIOP Principles for the Validation and Use of Personnel Selection
  Procedures, 5th ed.** (2018) — validity as a *unitary* concept built on an
  analysis of work.
- **Sackett, Zhang, Berry & Lievens (2022)**, *J. Applied Psychology* 107(11),
  2040–2068 — the range-restriction re-analysis that re-ordered operational
  validities (structured interview **.42** now above general mental ability **.31**).

| Skill | Domain | Produces |
|---|---|---|
| `job-analysis-facilitator` | Competency Modeling foundation / content validity | Task × KSAO linkage matrix (Excel) + analysis-of-work report (Word) |
| `selection-method-advisor` | Talent Assessment | Validity-grounded method/battery recommendation memo (Word) + comparison table (Excel) |
| `assessment-center-designer` | Talent Assessment | Dimension × exercise matrix (Excel) + AC design doc & assessor-training outline (Word) |
| `career-architecture-builder` | Career Frameworks | Job family → level architecture matrix (Excel) + leveling-guide narrative (Word) |
| `adverse-impact-analyzer` | Psychometrics & Validation | Impact-ratio matrix (Excel) + defensibility narrative (Word); ships a tested Python calculator |

## Design rules these skills enforce

- Cite **two authority layers** — legal (Uniform Guidelines) and professional
  (SIOP Principles) — in every defensibility narrative.
- Default to **Sackett et al. (2022)** validities; legacy Schmidt & Hunter (1998)
  numbers appear only in a clearly-labeled "do not mix" sidebar.
- Treat the **0.80 four-fifths ratio as a rule of thumb, not a safe harbor** —
  always pair it with a statistical-significance test and a small-sample caveat.
- Never label a single-exercise or single/untrained-rater tool an "assessment
  center" (≥2 simulations, ≥2 trained assessors, defined data integration).
- Honor the repo's **TCB v3.1** competency invariants — these skills feed and
  consume competency models but never re-author them.

## Co-skills

Document deliverables rely on the `xlsx` and `docx` skills; Cargill-branded
output relies on `cargill-branding`. These are declared in each `SKILL.md`.

## Disclaimer

Every artifact is a **draft for professional review**. Validity claims,
adverse-impact analyses, and selection decisions must be reviewed by a qualified
I-O psychologist and legal counsel, and regulatory citations re-verified against
29 CFR Part 1607 and the current SIOP Principles, before operational use.
