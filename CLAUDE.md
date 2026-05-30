# CLAUDE.md

Guidance for Claude / AI assistants working in this repository.

## What this repository is

A **monorepo of Cargill HR / talent-management tooling**. It bundles two
installable Python applications and three self-contained Claude **Skills**.
There is no shared top-level package — each component is independent, with its
own `pyproject.toml` or `SKILL.md` and its own `data/` workspace.

```
Claude-Code/
├── tech-competency-agent/          # Python app — TCB v3.1 multi-agent system + L&D skill mapping
├── cargill-pptx-converter/         # Python app — document → Cargill-branded PPTX converter
├── coverage-audit/                 # Claude Skill — artifact-to-artifact coverage audit (Excel + Word)
├── sme-validation-package/         # Claude Skill — SME focus-group validation packages (Word)
├── structured-interview-generator/ # Claude Skill — BEI guides, BARS, scorecards (Excel + Word)
└── .github/workflows/build-linux.yml  # CI (lints + tests tech-competency-agent ONLY)
```

The two app names overlap with their directory names; when paths in this file
say `src/...`, they are relative to the component directory.

## Components

### 1. `tech-competency-agent/` — the primary, CI-gated codebase

A **LangGraph multi-agent system** implementing the **TCB v3.1** spec
(Technical Competency Builder, April 2026) for Cargill's 15 job families, plus a
downstream **L&D Skill Mapping** module. Read `tech-competency-agent/README.md`
and `CHANGELOG.md` first — they are the authoritative spec.

Two subsystems share schemas and utilities:

- **Competency Builder** (`src/agents/`, `src/orchestrator/`) — a 7-phase
  pipeline (Parse → Research → Build → QA → Output → Feedback → Final
  Synthesis) with `R1` / `R2` / `FINAL` / `RESUME` stage routing.
- **Skill Mapping** (`src/skill_mapping/`) — ingests an L&D training catalog
  (xlsx/csv) + the 23-column Library Master and emits a Skill→Competency→Level
  crosswalk workbook.

Key directories:

| Path | Contents |
|------|----------|
| `src/schemas/` | Pydantic v2 data models — **the contract** all stages flow through |
| `src/agents/` | One agent per pipeline step, each subclasses `BaseAgent` |
| `src/orchestrator/` | LangGraph `graph.py`, `state.py`, quality `gates.py` |
| `src/skill_mapping/` | Catalog/library loaders, bloom classifier, semantic matcher, Excel writer |
| `src/deliverables/` | Branded output writers (Library Master, Job Family Package, BCO Ledger, HRLT summary, Change Log, Rosetta Stone, SME package) |
| `src/utils/` | Boundary classifier, 5QMT, CTIC diff, source integrity, branding, validators |
| `src/cli/main.py` | `techcomp` CLI entrypoint (`run`, `map-skills`, `inspect`, `init-config`) |
| `config/*.yaml` | Thresholds, workflow config, domain registry, bloom verbs, band targets |
| `docs/reference/` | TCB v3.1 spec, V&B/Common reference, quick-reference card, schema docs |

**v3.1 invariants enforced by validators** (do not silently relax these — they
are psychometric/governance requirements, not style):

- Competency titles: 3–6 words. Definitions: ONE sentence, 15–25 words, verb-led.
- Proficiency: exactly four levels `L1`–`L4`, each with **exactly 3 indicators**.
- Top **6** competencies max per JD; top 6 must cover **≥90%** of Technical EFs.
- Criticality = Coverage 0.40 + Criticality 0.30 + Distinctiveness 0.20 + Assessability 0.10.
- Boundary class per competency: `V_AND_B` / `COMMON` / `TECHNICAL` / `MIXED`.
- Source integrity tags: `CONFIRMED` / `CORRECTED` / `UNVERIFIABLE` / `FLAGGED`.
- CTIC drift tolerance ≤ 5% (character-level diff reverts non-targeted edits).
- Max 3 QA cycles, then stop and escalate.

The v3.1 migration was a **hard cut with no aliases** — do not reintroduce v3.0
constructs (6-factor criticality, 6–10 top-N, ≥0.80 coverage gate).

### 2. `cargill-pptx-converter/` — document → branded PPTX

A separate multi-agent pipeline (Content Extraction → Brand Compliance → Slide
Architecture → Visual Design → Chart Building → QA → PPTX Rendering). Mirrors
the same layout (`src/agents/`, `src/orchestrator/`, `src/schemas/`, plus
`src/brand/`, `src/rendering/`, `src/extractors/`, `src/templates/`). CLI
entrypoint is `cargill-pptx` (`src.cli.main:cli`). **Not covered by CI** — run
its tests manually if you touch it.

### 3. Claude Skills (`coverage-audit/`, `sme-validation-package/`, `structured-interview-generator/`)

Each is a standalone skill defined by a `SKILL.md` with YAML front-matter
(`name`, `description`) plus `references/` and/or `scripts/`. They are **prompt
+ reference assets**, not Python packages — there is nothing to `pip install`.
When editing a skill, keep the `description` trigger phrases intact (they drive
skill selection) and preserve the documented deliverable contracts (e.g.
coverage-audit produces a paired Excel matrix + Word summary). Several skills
declare **mandatory co-skills** (`xlsx`, `docx`, `cargill-branding`,
`multi-lens-review`) — honor those dependencies.

## Development workflows

Both Python apps share identical tooling. **Run all commands from inside the
component directory** (the CI even sets `working-directory: tech-competency-agent`).

```bash
cd tech-competency-agent      # or cargill-pptx-converter

poetry install                # or: pip install -e .

pytest                        # tests (config enables --cov by default)
ruff check src/ tests/        # lint  (matches CI exactly)
black src/ tests/             # format (line-length 100)
mypy src/                     # type check
```

- **Python 3.11**, managed with **Poetry** (build-backend `poetry-core`).
- **black**: line-length 100, target `py311`.
- **ruff**: line-length 100, rules `E, F, I, N, W`, ignores `E501`.
- **mypy**: `ignore_missing_imports = true`, untyped defs allowed.
- **pytest**: discovers `tests/`, files `test_*.py`, classes `Test*`,
  functions `test_*`; `--cov=src` is in `addopts`. Pass `--no-cov -q` to skip
  coverage (this is what CI does).

### CI (`.github/workflows/build-linux.yml`)

Runs on every push to any branch and on PRs. It **only** builds
`tech-competency-agent`: installs deps via `pip` (pinned ranges, not Poetry),
then runs `ruff check src/ tests/` and `pytest tests/ --no-cov -q`. Before
pushing changes to that component, make sure both pass locally with the same
commands. `cargill-pptx-converter` and the skills are not in CI.

### Running the apps

```bash
# Competency build (R1 = full pipeline)
techcomp run --stage R1 --family Finance --jobs-file ... --tech-sources ... \
  --leadership-file ... --template-file ...

# SME feedback round (R2 / FINAL)
techcomp run --stage R2 --family Finance --feedback-file ...

# Map an L&D catalog to v3.1 competencies
techcomp map-skills --library ... --catalog ... --family Finance --out ...

# Inspect a saved run
techcomp inspect data/output/run_<timestamp>_final_state.json
```

Set `ANTHROPIC_API_KEY` in `.env` (copy from `.env.example`).

## Architecture conventions

- **Schema-first.** Every stage consumes and returns strongly-typed Pydantic
  models. When adding a field, change the schema in `src/schemas/` first; let
  validators carry the v3.1 rules. Never bypass a validator to make a test pass.
- **Agent pattern.** A new pipeline step subclasses `BaseAgent`, implements
  `execute(state) -> state` and `get_system_prompt()`, and is wired into
  `src/orchestrator/graph.py`. Register it in `src/agents/__init__.py`.
- **Quality gates** live in `src/orchestrator/gates.py`; thresholds belong in
  `config/thresholds.yaml`, not in code.
- **Cargill branding** is centralized in `src/utils/branding.py` (Leaf Green
  `#00843D`, White Green `#F5F9ED`, Arial body, Georgia H1). It is intentionally
  duplicated per app today; a shared `cargill-brand-py` package is a known
  future follow-up. Match the existing constants — do not invent new colors.
- **Outputs are deterministic artifacts.** Stages write numbered JSON snapshots
  (`s1_…` through `final_state.json`); deliverable writers in `src/deliverables/`
  own the user-facing Excel/Word/PPTX. Keep that separation.

## Working principles for AI assistants

Behavioral guidelines to reduce common LLM coding mistakes. Merge with the
project-specific instructions above as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial
tasks, use judgment.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

## Git & contribution workflow

- Feature work happens on dedicated branches (e.g. `claude/...`); `main` is
  updated via merged PRs. Don't push directly to `main`.
- Keep commit messages clear and descriptive; match the existing history style
  (imperative summary, e.g. "Add coverage-audit skill…").
- After pushing a branch, open a **draft PR** if one doesn't already exist.
- Respect component boundaries — a change to one app/skill should not reach into
  another's `src/` or `data/`.
