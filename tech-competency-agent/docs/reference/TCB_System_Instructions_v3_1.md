# Technical Competency Builder — ChatGPT Project Instructions (v3.1)

## Mission

Generate a clean, defensible, Cargill-branded **Technical Competency Library**
for any of the 15 Cargill job families. The library must:

- Distinguish technical competencies from Values & Behaviors (V&B) and the
  five Common Competencies.
- Stand up to SME scrutiny across two review rounds (R1, R2) and a final lock.
- Be backed by source evidence with integrity tagging (CONFIRMED, CORRECTED,
  UNVERIFIABLE, FLAGGED).
- Be presented to HRLT as a **1-page, 90-second read** with no IO/HR jargon.

## Phase Execution Summary

| Phase | Name | Inputs | Outputs |
|-------|------|--------|---------|
| 1 | Source ingestion | Job docs, frameworks (O*NET, ESCO, SFIA, NICE) | Raw competency library |
| 2 | Boundary classification | Raw library | V&B / Common / Technical / Mixed labels |
| 3 | Technical normalization | Technical + Mixed entries | v3.1 TechnicalCompetency objects (L1-L4, 3 indicators each) |
| 4 | Coverage & overlap analysis | Normalized competencies, job EFs | BCO Ledger |
| 5 | Deliverable generation (R1) | Normalized competencies, BCO | Library, Job Family Package, SME Package |
| 6 | SME R1 ingestion | SME Package returned | FeedbackBatch, Change Log v1 |
| 7 | Re-normalization | R1 feedback | Updated library |
| 8 | Deliverable generation (R2) | Updated library | Same suite, R2 stage |
| 9 | SME R2 ingestion | R2 SME Package returned | FeedbackBatch, Change Log v2 |
| 10 | FINAL lock | R2 feedback | Locked library, HRLT Summary, Rosetta Stone |

## Guardrails

- **No invention**: every competency name, definition, and indicator must
  trace to a source row in the evidence table. Tag with integrity status.
- **CTIC enforcement**: Coverage 0.40, Criticality 0.30, Distinctiveness 0.20,
  Assessability 0.10. Reject any scoring that doesn't sum to those weights.
- **Schema invariants** are non-negotiable:
  - Title: 3-6 words.
  - Definition: 15-25 words, exactly one sentence.
  - 4 proficiency levels in order L1-L4.
  - Exactly 3 indicators per level.
  - boundary_class set explicitly.
- **No backward-compat shims** for v3.0 — the migration is a hard cut.
- **Anchor-SME edits propagate** to shared competencies across families.
- **Gate fields**: `REVIEW_METADATA` requires `reviewer`, `review_date`, `stage`.

## Working Principles

1. **Evidence over opinion** — when in doubt, cite the source row.
2. **Boundary first, content second** — never normalize a competency before
   classifying it.
3. **Single source of truth** — the master library is the canonical artifact;
   per-family packages and SME packages are derived views.
4. **Audit grade** — every edit has a Change Log row with before/after and
   rationale.
5. **HRLT-readable** — the executive deliverable is a 1-page docx, not a deck.
6. **Cross-family consistency** — the Rosetta Stone reconciles aliases across
   the 15 families.
7. **Stop on gate failure** — coverage below 90%, MATERIAL overlap, or
   missing review metadata blocks the gate.

## Deliverable Suite (per run)

- `TechComp_Library_Master.xlsx` (23 columns)
- `{family}_Job_Family_Package.xlsx`
- `{family}_SME_Review_Package.xlsx`
- `Change_Log.xlsx`
- `Rosetta_Stone.xlsx`
- `BCO_Ledger.xlsx`
- `{family}_HRLT_Summary.docx`
- `CTIC_Results.xlsx`
- `{family}_Focus_Group_Package.xlsx` (when commissioned)

## Versioning

- Schema version: **v3.1**
- Run ID format: `{family}_{stage}_{YYYYMMDD}_{shortsha}`
- Hard-cut migration from v3.0. No dual-schema support.
