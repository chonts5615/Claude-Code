# Technical Competency Builder (TCB) Product Contract

**Active Contract Version:** TCB v3.2  
**Status:** Authoritative workflow contract for this repository.

## Purpose
This repository implements the Technical Competency Builder operating model for converting role inputs into validated technical competency outputs with governance controls.

## Non-negotiable workflow
1. AI-assisted competency build from role/JD inputs.
2. SME validation and refinement.
3. Leadership approval.
4. Central library deployment.

## Core phases
1. Parse and normalize source role inputs.
2. Research and benchmark against approved frameworks.
3. Build candidate competencies.
4. Execute quality assurance gates.
5. Run SME survey loop.
6. Run focus group review.
7. Route leadership approval.
8. Publish to library system-of-record.

## Guardrails
- No-drift rule: outputs must remain tied to role responsibilities.
- Central Library is system of record.
- CTIC overlap constraints must be enforced.
- Three-Lens QA required before finalization.
- Maximum six technical competencies per JD/family in final package.

## Deterministic quality gates
- Competency title format, count, and definition constraints enforced by schema + validators.
- Exactly four proficiency levels (L1-L4).
- Exactly three indicators per level.
- Coverage and overlap thresholds enforced from `config/thresholds.yaml`.
- Maximum QA cycles governed by runtime configuration.

## Artifact contract
R1 must produce deterministic, schema-valid artifacts for:
- normalized competencies
- benchmarked competencies
- ranked competencies
- populated templates

R2/FINAL must operate on R1 artifacts without manual state edits.

## Version policy
- This repo is version-locked to **TCB v3.2**.
- Any contract changes require explicit update to:
  - this file,
  - README references,
  - workflow config version label,
  - and tests asserting threshold/version consistency.
