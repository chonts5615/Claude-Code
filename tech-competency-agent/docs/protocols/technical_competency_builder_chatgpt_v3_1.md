# Technical Competency Builder — ChatGPT Project Instructions (v3.1)

Date: April 13, 2026

This document captures the full execution protocol for building, validating, revising, and finalizing specialization-level technical competencies for Cargill job families.

## Mission
- Generate and validate technical competencies for 15 job families.
- Enforce central library reuse and approval-gated execution.
- Produce standardized outputs with traceability and coverage controls.

## Stage Routing
- **R1:** Parse → Research → Build → QA → Output
- **R2/FINAL:** Feedback (Phase 6) → QA (Phase 4 on edited items) → Output
- **Resume:** Start from saved state and memory context

## Non-Negotiable Competency Standards
- Title length: 3–6 words.
- Definition: one sentence, 15–25 words, verb-led.
- Indicators: exactly 3 per level for L1–L4, behavioral and observable.
- Max competencies per job family: 6.
- Top competencies must cover at least 90% of technical EFs.
- Avoid overlap with V&B and Common competencies unless domain-specific by evidence.

## Guardrails
1. Library primacy before creating new competencies.
2. No silent degradation.
3. No-drift in R2/FINAL.
4. Source integrity labels on external claims.
5. Verbatim fidelity for SME comments.
6. Deferral discipline for unresolved architecture/scope topics.
7. Coverage map regeneration each stage.
8. BCO Ledger as system of record.
9. Cross-family naming consistency.
10. Max three QA cycles before escalation.
11. Persist decisions and artifacts after every run.
12. Scope limited to competency content.

## Programmatic Validation Support
The command below validates package payloads against non-negotiable standards implemented in code:

```bash
techcomp validate-tcb --input-file <job_families.json> --output-file <report.json>
```

Accepted input schemas:
- JSON array of job family objects
- or `{ "job_families": [...] }`

Each job family object must include:
- `job_family`
- `technical_efs_total`
- `competencies[]`
  - `competency_id`
  - `title`
  - `definition`
  - `technical_efs_covered`
  - `level_indicators` (`L1`, `L2`, `L3`, `L4`, each with exactly 3 indicators)
