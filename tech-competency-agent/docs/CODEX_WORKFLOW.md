# Codex Workflow for `tech-competency-agent`

This document defines how Codex should execute work in this repository.

## Working rules
1. Do not change product behavior outside the TCB v3.2 contract unless explicitly requested.
2. Treat `docs/PRODUCT_CONTRACT.md`, schemas, and threshold config as the source of truth.
3. Never commit confidential role data, SME feedback, credentials, or generated run artifacts.
4. Keep changes PR-sized and reviewable.

## Recommended implementation order
1. Contract/version alignment.
2. Threshold and gate consistency.
3. Deterministic I/O completion.
4. R1 path completion.
5. Source traceability.
6. R2/FINAL hardening.
7. Resume/checkpoint correctness.
8. CI + regression coverage.

## Pre-edit inspection checklist
- `README.md`
- `pyproject.toml`
- `config/thresholds.yaml`
- `config/workflow_config.yaml`
- `src/orchestrator/graph.py`
- `src/schemas/competency.py`

## Required validation commands
Run after edits (where environment permits):
- `pytest`
- `ruff check src/ tests/`
- `mypy src/`

## Change summary expectations
Every Codex change should include:
- files changed,
- rationale,
- checks run,
- known risks or follow-up tasks.
