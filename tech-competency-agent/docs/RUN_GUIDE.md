# TCB Run Guide (Inputs, Execution, Outputs)

This guide provides an explicit, step-by-step procedure to run the Technical Competency Builder (TCB) workflow.

---

## 0) Prerequisites

From repository root:

```bash
cd tech-competency-agent
```

Install dependencies:

```bash
poetry install
```

or

```bash
pip install -e .
```

If your configured LLM provider requires credentials, export the provider key before running.

---

## 1) Create input folder structure

Put input files under `data/input/`:

```text
data/input/
  jobs.xlsx
  tech_competencies.xlsx
  core_leadership.xlsx
  template.xlsx
```

Required CLI arguments and exact file types:

1. `--jobs-file` (Excel `.xlsx`)
   - job titles, summaries, and responsibilities.
2. `--tech-sources` (one or more Excel `.xlsx` files)
   - technical competency sources / reference competency library.
3. `--leadership-file` (Excel `.xlsx`)
   - core/leadership competencies for overlap controls.
4. `--template-file` (Excel `.xlsx`)
   - output workbook template to populate.

---

## 2) Initialize/verify configuration

Generate baseline config files if they are missing:

```bash
techcomp init-config --output-dir config
```

Then review these files:

- `config/workflow_config.yaml`
- `config/thresholds.yaml`

Important contract-aligned values to confirm:

- `ranking.top_n_competencies: 6`
- `ranking.min_responsibility_coverage: 0.90`
- `ranking.min_competencies_per_job: 6`
- `ranking.max_competencies_per_job: 6`

---

## 3) Run the workflow (single source file)

```bash
techcomp run \
  --jobs-file data/input/jobs.xlsx \
  --tech-sources data/input/tech_competencies.xlsx \
  --leadership-file data/input/core_leadership.xlsx \
  --template-file data/input/template.xlsx \
  --output-dir data/output \
  --config config/workflow_config.yaml
```

Optional run-id for traceability:

```bash
--run-id tcb_r1_demo_20260514
```

### Multi-source example
If you need multiple tech source files, repeat `--tech-sources`:

```bash
techcomp run \
  --jobs-file data/input/jobs.xlsx \
  --tech-sources data/input/tech_source_a.xlsx \
  --tech-sources data/input/tech_source_b.xlsx \
  --leadership-file data/input/core_leadership.xlsx \
  --template-file data/input/template.xlsx \
  --output-dir data/output
```

---

## 4) Where outputs are written

All outputs are written to `data/output/`.

Expected per-run artifacts:

- `<run_id>_s1_jobs_extracted.json`
- `<run_id>_s2_competency_map_v1.json`
- `<run_id>_s3_normalized_v2.json`
- `<run_id>_s4_overlap_audit_v1.json`
- `<run_id>_s5_clean_v3.json`
- `<run_id>_s6_benchmarked_v4.json`
- `<run_id>_s7_ranked_top8_v5.json`
- `<run_id>_s8_populated_template.xlsx`
- `<run_id>_final_state.json`
- `<run_id>_review_package.zip`

> Note: the zip package includes every artifact path that exists at packaging time; missing artifacts are listed in the manifest.

---

## 5) How to inspect the final ZIP package

`<run_id>_review_package.zip` contains:

- `manifest.json`
- `artifacts/<filename>` for each included artifact

`manifest.json` includes:

- `run_id`
- `packaged_at_utc`
- `artifacts_included`
- `artifacts_missing`

Quick shell check:

```bash
python - <<'PY'
import zipfile, json
z = "data/output/<run_id>_review_package.zip"
with zipfile.ZipFile(z) as f:
    print(f.namelist())
    print(json.loads(f.read("manifest.json")))
PY
```

---

## 6) Post-run validation checks

Run the validation suite from `tech-competency-agent/`:

```bash
pytest -q
ruff check src/ tests/
mypy src/
```

---

## 7) Troubleshooting checklist

If run fails:

1. Confirm all input file paths exist and are `.xlsx`.
2. Confirm your provider credentials are set for the configured provider.
3. Confirm `config/thresholds.yaml` is valid YAML.
4. Re-run with explicit `--run-id` and inspect `<run_id>_final_state.json`.
5. Check `data/output/workflow.log` for step-level failure details.
