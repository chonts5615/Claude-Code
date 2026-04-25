# Technical Competency Builder v3.1 + Skill Mapping

LangGraph multi-agent system that operationalizes the **TCB v3.1** spec
(April 2026) for Cargill's 15 job families, plus a downstream **L&D Skill
Mapping** module that aligns training catalogs to published competencies.

## Overview

Two subsystems share schemas and utilities:

1. **Competency Builder (`src/agents/`, `src/orchestrator/`)** — 7-phase
   pipeline (Parse → Research → Build → QA → Output → Feedback → Final
   Synthesis) with R1 / R2 / FINAL / Resume stage routing, V&B / Common
   boundary discipline, no-drift CTIC enforcement, and Cargill-branded
   deliverables (Library Master, Job Family Package, BCO Ledger, HRLT
   summary, Change Log, Rosetta Stone, Focus Group package).
2. **Skill Mapping (`src/skill_mapping/`)** — ingests an L&D training
   catalog (xlsx/csv) plus the published 23-column Library Master and
   produces a Skill→Competency→Level crosswalk Excel with a Coverage Map,
   Gaps, Surplus, and Common/V&B tabs.

### v3.1 standards (enforced by validators)

- Titles: 3–6 words.
- Definitions: ONE sentence, 15–25 words, verb-led.
- Proficiency: exactly four levels (L1–L4), each with exactly 3 indicators
  (12 indicators total per competency).
- Top 6 competencies max per JD; top 6 must cover ≥90% of Technical EFs.
- Criticality = Coverage 0.40 + Criticality 0.30 + Distinctiveness 0.20 +
  Assessability 0.10.
- Boundary class per competency: V_AND_B / COMMON / TECHNICAL / MIXED.
- Source integrity tags: CONFIRMED / CORRECTED / UNVERIFIABLE / FLAGGED.
- CTIC drift tolerance ≤ 5 %.
- Max 3 QA cycles before stop and escalate.

### Reference docs

Bundled under `docs/reference/`: `TCB_System_Instructions_v3_1.md`,
`Cargill_VB_and_Common_Reference.md`, `TCB_Quick_Reference_Card.md`,
`Portfolio_Status.md`, plus per-deliverable schema docs.

## Quick Start

### 1. Installation

```bash
# Clone repository
git clone <repo-url>
cd tech-competency-agent

# Install dependencies (using Poetry)
poetry install

# Or using pip
pip install -e .
```

### 2. Configuration

```bash
# Generate default config files
techcomp init-config

# Edit thresholds and settings
vim config/thresholds.yaml
vim config/workflow_config.yaml
```

### 3. Set up environment

```bash
cp .env.example .env
# Add your Anthropic API key
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

### 4. Run a competency build (R1 — full pipeline)

```bash
techcomp run --stage R1 --family Finance \
  --jobs-file data/input/finance_jobs.xlsx \
  --tech-sources data/input/finance_tech_sources.xlsx \
  --leadership-file data/input/core_leadership.xlsx \
  --template-file data/input/template.xlsx
```

### 5. Run an SME-feedback round (R2 / FINAL)

```bash
techcomp run --stage R2 --family Finance \
  --feedback-file data/input/finance_r2_feedback.json
# stage FINAL also runs Phase 7 learning synthesis
```

### 6. Map an L&D training catalog to v3.1 competencies

```bash
techcomp map-skills \
  --library data/output/TechComp_Library_Master.xlsx \
  --catalog data/lnd/finance_catalog.xlsx \
  --family Finance \
  --out data/output/skill_mapping/
```

Produces a 6-tab branded crosswalk: Run Metadata, Crosswalk, Coverage Map,
Gaps, Surplus, Common-V&B Training.

### 7. Inspect a run

```bash
techcomp inspect data/output/run_<timestamp>_final_state.json
```

## Project Structure

```
tech-competency-agent/
├── config/                      # Configuration files
│   ├── workflow_config.yaml    # Orchestrator settings
│   ├── thresholds.yaml         # Quality gate thresholds
│   ├── competency_format.yaml  # Writing standards
│   └── template_specs/         # Output template specs
├── src/
│   ├── schemas/                # Pydantic data models
│   ├── agents/                 # Individual agent modules
│   ├── orchestrator/           # LangGraph workflow
│   ├── utils/                  # Shared utilities
│   └── cli/                    # Command-line interface
├── tests/                      # Test suite
├── data/
│   ├── input/                  # User-provided files
│   ├── output/                 # Generated artifacts
│   └── reference/              # Benchmark sources
└── docs/                       # Documentation
```

## Workflow Steps

### R1 (full pipeline, Phases 1–5)
1. **Job Ingestion** — extract and normalize job descriptions.
2. **Competency Mapping** — map EFs to candidate competencies (5QMT against Library).
3. **Normalization** — emit L1–L4 with 3 indicators per level, 15–25-word definitions.
4. **Overlap Audit** & **Remediation** — material/minor thresholds 0.82 / 0.72.
5. **Benchmarking** — O*NET / ESCO / SFIA / NICE per `config/domain_registry.yaml`.
6. **Criticality Ranking** — 4-factor weighted (0.40 / 0.30 / 0.20 / 0.10), top-6 hard cap.
7. **Output** — Library Master FIRST, then Job Family Package, BCO Ledger, HRLT Summary.

### R2 / FINAL (Phase 6 feedback)
1. **Feedback Ingestion** — Keep / Edit / Gap / Discuss / Reject classification.
2. **REVIEW_METADATA gate** — reviewer / review_date / stage required.
3. **6E-bis Coverage Refresh** — re-map EFs, flag jobs <90 % coverage.
4. **6E-ter Boundary Re-Scan** — reclassify V&B / Common / Technical / Mixed.
5. **6E-quater Overlap Re-Audit** — flag worsened or new MATERIAL overlap.
6. **6F CTIC** — character-level diff on non-targeted competencies; revert drift.
7. **6G Focus Group Prep** — package for SMEs when DISCUSS items exist.
8. **Phase 5 Output** — re-emit deliverables.
9. **Phase 7 Learning Synthesis (FINAL only)** — cross-family learnings JSON.

### Skill Mapping (downstream of v3.1)
1. Catalog Loader (xlsx/csv) → 2. Library Loader (23-col) → 3. Bloom Classifier
(verb-driven heuristic, LLM tie-break only) → 4. Semantic Matcher (sentence-transformers
cosine, threshold 0.55) → 5. Level Resolver (confidence = 0.5·sim + 0.3·bloom + 0.2·llm)
→ 6. Coverage Aggregator → 7. Gap Reporter → 8. Excel Writer (branded, 6 sheets).

## Configuration

### Quality Thresholds

Edit `config/thresholds.yaml` to customize:

- Minimum responsibilities per job
- Overlap detection thresholds
- Coverage requirements
- Top N competency count

### Agent Settings

Edit `config/workflow_config.yaml` to customize:

- LLM model and parameters
- Similarity models
- Ranking weights
- Benchmarking sources

## Input File Formats

### Jobs File (Excel)

| Job Title | Job Family | Job Level | Summary | Responsibilities |
|-----------|-----------|-----------|---------|------------------|
| Data Scientist | Analytics | Senior | ... | • Responsibility 1<br>• Responsibility 2 |

### Technical Competencies Source (Excel)

| Competency Name | Definition | Indicators | Tags |
|-----------------|-----------|-----------|------|
| Data Analysis: Statistical Modeling | ... | • Indicator 1<br>• Indicator 2 | analysis, statistics |

## Output Artifacts

Each run generates:

- `s1_jobs_extracted.json`: Normalized job structures
- `s2_competency_map_v1.json`: Responsibility-competency mappings
- `s3_normalized_v2.json`: Normalized competencies
- `s4_overlap_audit_v1.json`: Overlap audit results
- `s5_clean_v3.json`: Remediated competencies
- `s6_benchmarked_v4.json`: Benchmarked competencies
- `s7_ranked_top8_v5.json`: Ranked top competencies
- `s8_populated_template.xlsx`: Final output template
- `final_state.json`: Complete workflow state

## Development

### Run tests

```bash
pytest
```

### Type checking

```bash
mypy src/
```

### Format code

```bash
black src/ tests/
```

### Lint code

```bash
ruff check src/ tests/
```

## Architecture

### Schema-First Design

All data flows through strongly-typed Pydantic models:

- `RunState`: Workflow execution state
- `Job`, `Responsibility`: Job structure
- `TechnicalCompetency`: Competency structure
- `CompetencyMapping`: Mapping relationships
- `OverlapAudit`, `Ranking`: Validation outputs

### Agent Pattern

Each agent:
- Inherits from `BaseAgent`
- Implements `execute(state: RunState) -> RunState`
- Has a dedicated system prompt
- Adds flags to state for quality tracking

### Quality Gates

Quality gates validate outputs at critical points:
- Post-extraction: Job count, missing summaries
- Post-mapping: Unmapped responsibilities
- Post-remediation: Overlap resolution
- Post-ranking: Coverage threshold

## Customization

### Add New Agent

1. Create agent class in `src/agents/`
2. Inherit from `BaseAgent`
3. Implement `execute()` and `get_system_prompt()`
4. Add to orchestrator graph in `src/orchestrator/graph.py`

### Add Quality Gate

1. Add validation method to `QualityGate` class
2. Call from gate node in orchestrator
3. Configure thresholds in `config/thresholds.yaml`

### Add Benchmark Source

1. Update `config/workflow_config.yaml` sources list
2. Implement fetcher in `BenchmarkResearchAgent`
3. Map source format to `SourceEvidence` schema

## Troubleshooting

### Issue: Jobs not extracted

- Check Excel file format matches expected columns
- Review `extraction_warnings` in output
- Verify file path is correct

### Issue: High unmapped responsibility rate

- Lower `min_relevance_threshold` in config
- Add more competency sources
- Review responsibility text quality

### Issue: Material overlap detected

- Review overlap audit output
- Adjust `material_threshold` in config
- Manually review flagged competencies

## License

[Add license information]

## Contributing

[Add contribution guidelines]

## Support

For issues or questions:
- GitHub Issues: [repo-url]/issues
- Documentation: `docs/` directory
- Email: [support email]
