# Research Agent — Improvement Evaluation

A prioritized roadmap for evolving the research agent beyond its current beta.
Each item notes **what**, **why**, **how it fits the current architecture**, and
rough **effort**.

## Current state (baseline)

Deterministic, code-driven pipeline:
`plan → research (parallel researcher subagents) → analyze (data-analyst) →
report (controlled query) → branded PDF render (code) → QA loop (controlled
query, bounded re-QA-to-PASS) → cleanup`, with per-subagent tool tracking,
transcripts/JSONL logs, three embedded skills (branding, format-QC,
I-O/exec review), configurable brand, and `--resume`.

Known limits this roadmap targets: no independent verification of claims; no
coverage/gap check on research; generic (non-specialised) researchers; charts
of uneven quality; no cost/usage telemetry; single output format (PDF/MD); no
research reuse across runs; cannot ingest a user-provided source document.

---

## Tier 1 — High impact, near-term (fits the existing loop pattern)

### 1. Fact-checker / verifier agent (new agent + process step)
- **What:** After research, a `verifier` re-checks the report's load-bearing
  claims by fetching the cited URLs (WebFetch) and confirming the quote/number
  actually appears, flagging unsupported or misattributed claims.
- **Why:** The biggest risk in an AI research tool is confident fabrication. QA
  currently judges plausibility, not ground truth. Spot-checks this session found
  real citations — make that a guarantee, not luck.
- **How:** New phase between report and QA (or fold into QA): a controlled call
  with WebFetch allowed, emitting a `verification.md` (claim → supported/uncertain
  /unsupported + source). Unsupported material → forces a REVISE.
- **Effort:** Medium.

### 2. Research coverage-critic loop (mirror the QA loop, one phase earlier)
- **What:** After the first research pass, a `research-critic` compares notes to
  the plan/brief, identifies missing angles/contradictions/thin areas, and
  triggers targeted follow-up searches before analysis.
- **Why:** Research is currently one-shot per subtopic; depth is luck-of-the-draw.
  A bounded deepen-until-sufficient loop raises floor quality.
- **How:** Reuse the bounded-loop pattern from QA: critic emits gaps → spawn
  focused researchers for the gaps → re-critique, cap at N rounds.
- **Effort:** Medium.

### 3. Cost & usage telemetry
- **What:** Capture tokens / cost / per-phase wall-clock from the SDK
  `ResultMessage` and write a `run_summary.json` (and print a footer).
- **Why:** Runs are multi-call and sometimes long; there's currently zero
  visibility into spend or where time goes. Essential for tuning and trust.
- **How:** Read `ResultMessage` in `_run_turn` / the query helpers; aggregate per
  phase in the tracker.
- **Effort:** Low.

### 4. Source-document ingestion (new input capability)
- **What:** `--source FILE` (pptx/pdf/docx/md) extracted into a brief the
  researchers fact-check and contextualise — exactly the Cargill-deck workflow,
  but built in instead of done by hand.
- **Why:** Recurring real use case (the deck reviews). Today the researchers
  can't read files; ingestion must happen up front.
- **How:** Pre-step extracts text (python-pptx/pypdf) → prepended to the brief;
  optionally a per-element "verify this deck claim" mode.
- **Effort:** Low–Medium.

---

## Tier 2 — Capability depth

### 5. Editor / synthesis pass (new agent)
- **What:** An `editor` polishes the drafted report for narrative flow, a tight
  exec summary, cross-section consistency, and de-duplication — distinct from QA
  (which critiques) and from drafting (which synthesises).
- **Why:** The single report query is good but uneven across long reports; a
  dedicated editing pass lifts coherence.
- **Effort:** Low (another controlled query) — sequence editor → QA.

### 6. Citation manager
- **What:** Normalise/dedupe references, validate URLs resolve, and verify every
  in-text claim maps to a reference; emit a clean reference list + a
  claim↔source map.
- **Why:** Traceability is a headline value; today it relies on the model.
- **Effort:** Medium (mostly deterministic code + a link-check).

### 7. Multi-format output (leverage the monorepo)
- **What:** Add DOCX and **PPTX** output. The PPTX path can hand off to the
  repo's `cargill-pptx-converter`; DOCX via python-docx.
- **Why:** Execs want a deck/Word doc, not just a PDF. High stakeholder value,
  and it reuses existing sibling tooling.
- **Effort:** Medium.

### 8. Domain-specialist researchers
- **What:** Researcher variants with tailored search strategies & source
  preferences: `scholar` (peer-reviewed/meta-analytic), `regulatory`
  (laws/agencies), `market` (vendors/analysts), `news` (recent events). The plan
  step assigns the right specialist per subtopic.
- **Why:** A generic researcher under-weights authoritative sources; specialists
  improve credibility and recency (the Sackett-2022 lesson).
- **Effort:** Medium (new AgentDefinitions + plan routing).

### 9. Confidence scoring & uncertainty surfacing
- **What:** Tag each key finding High/Medium/Low confidence (source quality +
  corroboration) and render a confidence column/badge.
- **Why:** Decision-makers need to know what's solid vs. emerging — the report
  already separates these prose-wise; make it systematic.
- **Effort:** Low–Medium.

---

## Tier 3 — Platform / strategic

### 10. Research cache + prompt caching
- **What:** Persist notes/sources in a small knowledge store keyed by
  topic/date; reuse across runs and warm prompt caches for repeated context.
- **Why:** Cuts cost/latency for related queries; compounding value for a team.
- **Effort:** High.

### 11. Human-in-the-loop approval gates (optional)
- **What:** Optional checkpoints — approve the plan, approve the draft — surfaced
  in interactive mode; one-shot stays autonomous.
- **Why:** For high-stakes deliverables, a plan sign-off avoids wasted runs.
- **Effort:** Medium.

### 12. Evaluation harness + CI
- **What:** A rubric-based scorer (coverage, citation density, recency, structure)
  run over sample briefs to catch quality regressions; add the component to CI
  with the offline tests.
- **Why:** Lets us change prompts/models with confidence; today quality is judged
  ad hoc.
- **Effort:** Medium–High.

### 13. Resilience: retry/backoff + structured errors
- **What:** Wrap model calls with retry/backoff for transient overload/rate-limit;
  capture structured error records. (Checkpoint/`--resume` already shipped.)
- **Why:** Long runs hit transient failures; today they can abort a phase.
- **Effort:** Low–Medium.

### 14. Configurable depth / fan-out
- **What:** `--depth` / `--max-subtopics` to scale rigor vs. cost; deeper fan-out
  (sub-subtopics) for "intensive" requests.
- **Why:** "Intensive 50k+ benchmarking" should be able to go deeper on demand.
- **Effort:** Low.

---

## Recommended sequence

1. **Cost telemetry (#3)** and **source ingestion (#4)** — low effort, immediate value.
2. **Fact-checker (#1)** and **coverage-critic loop (#2)** — the biggest quality/trust gains.
3. **Editor (#5)** + **citation manager (#6)** — polish and traceability.
4. **Multi-format output (#7)** + **domain specialists (#8)** — stakeholder value & credibility.
5. Tier 3 as the tool graduates from beta to a shared platform.
