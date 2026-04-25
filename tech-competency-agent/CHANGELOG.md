# Changelog

## 0.3.0 — TCB v3.1 + Skill Mapping (this branch)

### Added — TCB v3.1 spec compliance
- **Stage routing**: `R1` (full pipeline), `R2` / `FINAL` (Phase 6 feedback +
  6E-bis / ter / quater + CTIC + 6G + Phase 7), `RESUME`.
- **New phase agents** (`src/agents/`): `feedback_ingestion`, `coverage_refresh`
  (6E-bis), `boundary_rescan` (6E-ter), `overlap_reaudit` (6E-quater),
  `ctic_validator` (6F), `focus_group_prep` (6G), `learning_synthesis` (Phase 7).
- **Boundary classifier** (`src/utils/boundary_classifier.py`) — V&B / Common
  with the "remove the domain noun" test.
- **5QMT Library reuse test** (`src/utils/five_qmt.py`).
- **CTIC drift detection** (`src/utils/ctic_diff.py`) — character-level diff,
  reverts non-targeted changes.
- **Source integrity tagging** (`src/utils/source_integrity.py`) —
  CONFIRMED / CORRECTED / UNVERIFIABLE / FLAGGED.
- **Band-to-Proficiency targets** (`config/band_proficiency_targets.yaml`,
  `src/utils/band_targets.py`).
- **Cargill branding** (`src/utils/branding.py`) — Leaf Green `#00843D`,
  White Green `#F5F9ED`, Arial body, Georgia H1. Duplicated locally; future
  follow-up extracts a shared `cargill-brand-py` package.
- **23-column Library Master** schema (`src/schemas/library.py`) and writer
  (`src/deliverables/library_writer.py`).
- **Deliverable suite** (`src/deliverables/`): library, family package, SME
  package, change log, Rosetta Stone, BCO Ledger, HRLT 1-page summary.
- **Reference docs** (`docs/reference/`): TCB v3.1 spec, V&B / Common reference,
  Quick Reference Card, Portfolio Status, schema docs.

### Changed — schema migration to v3.1 (hard cut, no aliases)
- `ProficiencyLevel` enum is now `L1`/`L2`/`L3`/`L4` with **exactly 3 indicators
  per level** (validator-enforced).
- `TechnicalCompetency.name` validator: 3–6 words.
- `TechnicalCompetency.definition` validator: 15–25 words, exactly one sentence.
- `TechnicalCompetency.boundary_class` is now required.
- `TechnicalCompetency.integrity_tag` defaults to `CONFIRMED`.
- `CriticalityBreakdown` (4 factors, weighted 0.40 / 0.30 / 0.20 / 0.10) replaces
  the v3.0 6-factor model.
- Top-N hard cap: 6 (was 6–10).
- Coverage gate: ≥0.90 (was ≥0.80).
- `min_responsibilities_per_job`: 3 (was 5) per v3.1 stop-rule.
- `RunConfig.stage` and `family` fields added.
- `ArtifactRegistry` extended with `library_master`, `bco_ledger`,
  `pre_feedback_snapshot`, `feedback_batch`, `coverage_refresh`,
  `boundary_rescan`, `overlap_reaudit`, `ctic_report`, `focus_group_package`,
  `learning_synthesis`, plus deliverable paths.

### Added — Skill Development & Mapping module (NEW subsystem)
- New package `src/skill_mapping/` with mini-pipeline `SM1..SM8`:
  `catalog_loader`, `library_loader`, `bloom_classifier`, `semantic_matcher`,
  `level_resolver`, `coverage_aggregator`, `gap_reporter`, `excel_writer`,
  `graph` (`SkillMappingPipeline.run`).
- Configs: `config/skill_mapping.yaml`, `config/bloom_verbs.yaml`.
- CLI subcommand `techcomp map-skills` with `--llm-tiebreak`, `--min-confidence`.
- Branded crosswalk Excel with 6 sheets (Run Metadata, Crosswalk, Coverage Map,
  Gaps, Surplus, Common-V&B Training).

### Added — tests
- `tests/test_schemas/test_proficiency_v31.py` — 11 invariant checks on the
  new competency schema.
- `tests/test_utils/test_branding.py`, `test_band_targets.py`, `test_ctic_diff.py`.
- `tests/test_skill_mapping/test_bloom_classifier.py` — 8 cases covering each
  level lexicon and every adjustment.

### Internal
- `src/utils/__init__.py` and `src/orchestrator/__init__.py` no longer eagerly
  import heavy submodules (langgraph, sentence_transformers, pandas) — fixes
  test collection without dev-only deps installed.
- `pyproject.toml` bumped to `0.3.0`; `rapidfuzz>=3.6` added.
