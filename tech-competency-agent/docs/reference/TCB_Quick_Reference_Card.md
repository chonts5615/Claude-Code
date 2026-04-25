# TCB Quick Reference Card

A one-page cheat sheet for operators of the Technical Competency Builder.

## HRLT Presentation Requirements

- **1 page**, docx, portrait.
- **90-second read**, no IO/HR jargon.
- Title (Georgia 18pt, Cargill Leaf Green) + Run ID line.
- 5 sections in order: Executive summary, Top findings (3 bullets), Coverage,
  Recommended next step.
- No tables, no charts, no acronyms.
- Cargill brand colors only: Leaf Green `#00843D`, White Green `#F5F9ED`,
  Black `#000000`.

## Deliverable Packages

| # | Deliverable | Format | Audience |
|---|-------------|--------|----------|
| 1 | Library Master | xlsx (23 cols) | TCB ops |
| 2 | Job Family Package | xlsx (4 sheets) | Family lead |
| 3 | SME Review Package | xlsx (editable) | SMEs |
| 4 | Change Log | xlsx | Audit |
| 5 | Rosetta Stone | xlsx | Cross-family ops |
| 6 | CTIC Results | xlsx | TCB ops |
| 7 | BCO Ledger | xlsx (3 sheets) | TCB ops |
| 8 | HRLT Summary | docx (1 page) | HRLT |
| 9 | Focus Group Package | xlsx | Focus group facilitator |

## CTIC Enforcement Rule

The four-factor weighted score must use exactly these weights:

```
score = 0.40 * coverage
      + 0.30 * criticality
      + 0.20 * distinctiveness
      + 0.10 * assessability
```

If the weights don't sum to 1.0 or don't match these values, **stop the run**
and re-run scoring.

## Taxonomy

| Class | Meaning |
|-------|---------|
| **V_AND_B** | Cargill Values & Behaviors — describes the person, not the work. |
| **COMMON** | One of the 5 Common Competencies — applies across most roles. |
| **TECHNICAL** | Domain-specific skill with tools, methods, deliverables. |
| **MIXED** | Combines a V&B/Common element with a Technical element — must be split. |

## Gate Fields — `REVIEW_METADATA`

The `review_metadata` dict on every `FeedbackBatch` must contain:

- `reviewer` (str, full name)
- `review_date` (ISO 8601 date)
- `stage` (one of `R1`, `R2`, `FINAL`)

If any of these is missing, the batch is rejected at ingestion.

## Domain Framework Registry

| Framework | Scope | Use for |
|-----------|-------|---------|
| **O*NET** | US occupational data | Cross-family baseline (Operations, Sales, etc.) |
| **ESCO** | European Skills/Competences/Qualifications/Occupations | EU mapping, multilingual aliases |
| **SFIA** | Skills for the Information Age | IT family |
| **NICE** | NIST Cybersecurity Workforce Framework | IT (security), EHS (cyber-physical) |
| **CFA / CPA / IFRS** | Finance professional bodies | Finance |
| **APICS / CSCMP** | Supply chain bodies | Supply Chain, Procurement |
| **ASQ / Six Sigma** | Quality bodies | Quality, Operations |
| **PMI** | Project management | Operations, Engineering |
| **SHRM** | HR body | HR family |
