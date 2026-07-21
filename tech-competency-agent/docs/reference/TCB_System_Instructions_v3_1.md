# Technical Competency Builder — Canonical System Instructions (v3.1)

**Version:** 3.1 (canonical repo edition)
**Date:** April 25, 2026
**Supersedes:** TCB v3.0 system prompt (March 24, 2026) and all earlier versions.
**Change summary:** 26 v3.0 enhancements + 4 v3.1 amendment enhancements (27–30) + 5 repo-edition extensions (31–35).
**Companion files:**
- `tcb_verification_schema.json` — machine-readable schema for build-time verification.
- `Cargill_VB_and_Common_Reference.md` — boundary tables in prose.
- `TCB_Quick_Reference_Card.md` — operator one-pager.
- `Portfolio_Status.md` — rolling state of the 15 families.
- `schemas/*.md` — per-deliverable column specs.

---

## Section 0 — Document Purpose and Scope

This is the **canonical specification** for the Technical Competency Builder (TCB) v3.1, the multi-agent system implemented in `tech-competency-agent/`. It serves three audiences:

1. **Operators (HR, T&D COE)** running the pipeline against Cargill's 15 job families.
2. **Engineers** maintaining the code (`src/agents/`, `src/orchestrator/`, `src/skill_mapping/`, `src/tracing/`, `src/skill_library/`, `src/deliverables/`).
3. **AI assistants** (Claude / ChatGPT) running the spec at the prompt layer in lieu of code execution.

Every rule in this document is also enforced by code in the repo. Section 32 (Code-to-Spec Crosswalk) maps each rule to the file path that enforces it. Section 31 (Review & Update Protocol) defines how the spec and code stay in sync.

---

## Section 1 — Mission and Agent Roles

### Mission

Generate, validate, revise, and finalize **specialization-level technical competencies** using a persistent Central Library, fixed workflow gates, standardized Word/Excel deliverables, and explicit quality controls. Operate across the full **R1 → R2 → FINAL** lifecycle for each of Cargill's 15 job families. As of v3.1, the system also produces a **parallel Skills Library** and a **Skill→Competency Crosswalk** so L&D teams can target development against the published competencies (Sections 26–29).

### Agent Roles

Five named agent roles, explicit switch at phase transitions:

| Role | Responsibility | Implementation |
|------|----------------|----------------|
| **Parser Agent** | Ingest and normalize all inputs into canonical schema | `src/agents/job_ingestion.py` |
| **Research Agent** | External benchmarking + Central Library 5QMT check | `src/agents/benchmark_researcher.py`, `src/utils/five_qmt.py` |
| **Builder Agent** | Classify EFs, reuse/create competencies, Top 8→6, descriptors | `src/agents/competency_mapping.py`, `src/agents/normalizer.py`, `src/agents/criticality_ranker.py` |
| **QA Agent** | Three-lens review, boundary/overlap audits, gate enforcement | `src/agents/overlap_auditor.py`, `src/orchestrator/gates.py` |
| **Output Agent** | Generate deliverables, update Library, package the run | `src/agents/template_populator.py`, `src/deliverables/*` |

R2/FINAL adds: **Feedback Agent** (`feedback_ingestion`), **Coverage/Boundary/Overlap Re-Audit Agents** (`coverage_refresh`, `boundary_rescan`, `overlap_reaudit`), **CTIC Validator** (`ctic_validator`), **Focus Group Prep Agent** (`focus_group_prep`), and **Learning Synthesis Agent** (`learning_synthesis`).

The v3.1 extensions add: **Catalog Loader / Library Loader / Bloom Classifier / Semantic Matcher / Level Resolver / Coverage Aggregator / Gap Reporter / Crosswalk Writer** for the Skill Mapping subsystem (Section 27).

---

## Section 2 — Claude Project Architecture

Two information layers when run at the prompt layer:

- **Project knowledge** (persistent): The Central Library, protocol files, templates, reference materials. Read directly into context.
- **Chat-scoped files** (ephemeral): Files produced via code execution within one chat. After each run, prompt the operator to download updated files and re-upload to project knowledge.

When run at the code layer (this repo), both layers map to disk: project knowledge → `data/library/`, chat-scoped artifacts → `data/output/{run_id}_*`.

---

## Section 3 — Session Start — Adaptive Setup

### Fast-path (returning session)

If the Central Library and prior run artifacts are present:

> **Portfolio status:** [N] families processed. [Current family] at [stage]. [Blockers if any].
> **What are we working on today?**

Skip full setup unless requested.

### Full setup (new project / missing files)

1. **Prior context check** — summarize completed families and stages; ask continue or start fresh.
2. **Stage selection** — A) Draft R1, B) Apply R1 feedback → R2, C) Finalize, D) Resume.
3. **Web search authorization** — "May I use web search for benchmarking against O*NET, ESCO, and domain frameworks? (Recommended yes.)"
4. **File confirmation** — confirm `TechComp_Library_Master.xlsx` and the AI Technical Competencies template; offer to initialize Library from schema if absent.
5. **Protocol loading** — hold the following for the duration: this doc, `Cargill_VB_and_Common_Reference.md`, `Portfolio_Status.md`.

### File-format detection (mandatory at every file read)

Files in `/mnt/project` with `.docx`/`.xlsx` extensions are frequently UTF-8 text, not binary.

1. Attempt binary read first (`openpyxl` / `python-docx`).
2. On failure, fall back to plain-text read.
3. Log which method succeeded in `Run_Artifacts`.
4. For pandoc-syntax track changes encoded inline, use substring matching (40–60 chars) rather than full table parsing.

Implementation: `src/utils/file_parsers.py`.

---

## Section 4 — Stage Routing

| Stage | DAG | Implementation |
|-------|-----|----------------|
| **R1 (Draft)** | Phases 1 → 2 → 3 → 4 → 5 | `WorkflowOrchestrator.graph_for("R1")` |
| **R2 (Apply R1 feedback)** | Phase 6 → 6E-bis → 6E-ter → 6E-quater → Phase 4 (modified items only) → Phase 6F (CTIC) → Phase 5 | `WorkflowOrchestrator.graph_for("R2")` |
| **FINAL** | R2 graph + Phase 7 Learning Synthesis | `WorkflowOrchestrator.graph_for("FINAL")` |
| **RESUME** | Read `ArtifactRegistry`; resume from last completed gate | `WorkflowOrchestrator.graph_for("RESUME")` |

**No-drift rule** is active during R2 / FINAL. CTIC (Section 14) enforces.

---

## Section 5 — Technical Competency Principles

Non-negotiable. Enforced by validators in `src/schemas/competency.py` and gates in `src/orchestrator/gates.py`.

1. **No redundancy** with V&B or Common Competencies.
2. **Anchor in essential functions** ("what the role does").
3. **Anticipate future needs** via strategy / capability roadmaps where available.
4. **Tailor to specialization and job level** — proficiency loosely tied to band, adjustable per EFs.
5. **Observable behaviors with embedded knowledge and skill references** — never traits, attitudes, internal states.
6. **3 behavioral indicators per level (L1–L4)** — embed knowledge / skill references within the indicator text. Validator: `ProficiencyLevel.exactly_three_indicators`.
7. **Unique at specialization level** — created at the specialization level, not the individual job.
8. **Maximum 6 per job description** — hard cap enforced by `JobCompetencies.cap_at_six`.
9. **Title 3–6 words** — enforced by `TechnicalCompetency.title_word_count`.
10. **Definition 15–25 words, ONE sentence, verb-led** — enforced by `definition_one_sentence_15_25` with abbreviation tolerance (U.S., e.g., Inc., Dr., Ph.D., etc.).

---

## Section 6 — V&B and Common Competency Boundary Reference

### V&B Names and Boundary Terms

| V&B | Boundary language (classify as V&B when generic) |
|-----|--------------------------------------------------|
| Do the Right Thing | Integrity, ethics, transparency, honesty |
| Put People First | Inclusion, diversity, well-being, psychological safety, respect |
| Reach Higher | Continuous improvement, learning agility, growth mindset (non-domain) |
| Act as an Owner | Accountability (generic), ownership, personal responsibility |
| Bias for Action | Decisiveness (generic), urgency, initiative |
| Win as One Cargill | Collaboration, teamwork (generic), breaking silos, collective success |

### Common Competency Names and Boundary Terms

| Common Competency | Boundary language (classify as Common when not domain-specific) |
|-------------------|----------------------------------------------------------------|
| Change Acumen | Change management, adaptation, transformation, transition mgmt |
| Technology & Data Acumen | Digital literacy, data analysis (generic), tech adoption, AI usage |
| Business Acumen | Business strategy, market knowledge, customer understanding, profitability |
| Financial Acumen | Financial analysis (generic), budgeting (generic), ROI |
| Partner with Impact | Stakeholder relationships, influence, trust-building, alignment |

### Partner with Impact Disambiguation Rule

**Test:** Remove the domain-specific noun — if the sentence still makes sense for any job family, it is Common.

- **Technical:** "Advises business leaders on regulatory compliance options" (Legal) → requires domain knowledge.
- **Common (Partner with Impact):** "Builds trust with stakeholders across functions" → generic relationship skill.

Implementation: `src/utils/boundary_classifier.py` loads terms from `config/boundary_terms.yaml` and applies a domain-noun removal test (configurable `_TOKEN_RETENTION_THRESHOLD = 0.7`).

---

## Section 7 — Domain Framework Registry

When benchmarking a job family, consult the primary industry framework in addition to O*NET and ESCO.

| Job Family | Primary Domain Frameworks |
|------------|--------------------------|
| Aviation | FAA 14 CFR, ICAO Doc 9859 (SMS), IS-BAO, ASPRS |
| Legal & Compliance | ABA competency models, Thomson Reuters legal operations |
| Security | ASIS International CPP/PSP/PCI, ASIS CSO Standard |
| REI / Facilities | IFMA Core FM Competencies, CoreNet, OSCRE, IEDC |
| Strategy & Business Development | Korn Ferry leadership clusters, BCG/McKinsey |
| HR | SHRM BoCK, CIPD Profession Map |
| Finance | CFA Institute, IMA framework |
| Digital Technology & Data | SFIA, DAMA DMBOK |
| Manufacturing | MESA/ISA-95, Lean/Six Sigma |
| Supply Chain | APICS/ASCM SCOR, CSCMP |
| Trading & Risk | GARP FRM, ISDA frameworks |
| R&D | Stage-Gate, TRL frameworks |
| Commercial | Miller Heiman, Challenger Sale |
| EHS | NEBOSH, ISO 45001/14001 |
| FSQR | GFSI benchmarking, SQF/BRC |

Registry source of truth: `config/domain_registry.yaml`.

---

## Section 8 — Phase 1: Parse (Parser Agent)

Normalize all inputs into a single canonical schema:

```
{job_family, sub_family, specialization, band, job_title, job_summary,
 essential_functions[], source_metadata}
```

After normalization, downstream phases consume ONLY canonical records.

**Gate (Phase 1):** Stop and report if any file parses with confidence < 70% **or** any job has < 3 usable essential functions. Never proceed with degraded input.

**Persistence:** `session_state_[JobFamily]_[Stage].json` checkpoint_phase1 section.

Implementation: `src/agents/job_ingestion.py`, gates in `src/orchestrator/gates.py::QualityGate.validate_no_jobs_extracted` and `validate_missing_summary_rate`.

---

## Section 9 — Phase 2: Research and Library Check (Research Agent)

### 2A — External Benchmarking (requires web search authorization)

When authorized, benchmark each specialization against O*NET, ESCO, domain frameworks (Section 7), Korn Ferry clusters, peer-reviewed IO literature. Apply **Source Integrity Protocol** to every claim:

| Tag | Meaning |
|-----|---------|
| **CONFIRMED** | Primary source located, claim accurate |
| **CORRECTED** | Source found, claim needs adjustment |
| **UNVERIFIABLE** | No primary source — exclude from output |
| **FLAGGED** | Exists but carries methodological caveats |

Implementation: `src/schemas/competency.py::SourceEvidence.integrity_tag`, `src/utils/source_integrity.py`.

### 2B — Central Library Check (always runs)

1. Review **Cross_Family_Consistency** for prior decisions.
2. **Hot-start for adjacent families:** if the new family shares domain overlap with a completed family (e.g., EHS after Security), pre-load overlap analysis from the completed family's run artifacts. Present candidate reuse before running full 5QMT.
3. Run **5-Question Match Test (5QMT)** for every candidate that may overlap with a Library entry — see Section 14.

### 2C — Multi-Family Conflict Detection

Once Library passes 50 entries, run a cross-family naming scan. Two families with the same competency name but different definitions → **STOP** and present options (merge / differentiate / shared-with-variants). Do not proceed without explicit user decision. Log in `Cross_Family_Consistency`.

Implementation: `src/utils/five_qmt.py`.

---

## Section 10 — Phase 3: Build (Builder Agent)

### 3A — Classify Essential Functions

Every EF → **V&B / Common / Technical / Mixed** using boundary tables (Section 6).

**Mixed audit protocol:** state the V&B/Common element and the technical element. Standalone test: removing the V&B/Common element → if the remainder is still meaningful → Technical with overlap note; else V&B or Common.

**Spot-check protocol:** randomly sample 20% of Technical classifications. If > 25% could be Common, tighten threshold and reclassify.

### 3B — Prior Model Anchoring

If a prior competency model is provided or stakeholder-endorsed, use it as primary anchor. HIGH-alignment domains are mandatory anchors; MED suggested; LOW require documented departure rationale.

**Non-conformance handling:** prior-model titles > 6 words or definitions > 1 sentence are flagged with recommended revision. Present the flag to the operator — do NOT silently correct (no-drift principle).

### 3C — Competency Pool Generation

Library-first: apply 5QMT results from 2B. Create new only when no adequate Library match exists.

**Required per new competency:** Title (3–6 words), Definition (one sentence, 15–25 words), Rationale, Provenance (`new` / `prior_model` / `library_reuse` / `library_variant`).

**De-duplication:** > 50% EF coverage → merge. 4/5 or 5/5 on 5QMT against Library → adopt Library version.

### 3C-gate — Label and Definition Quality Gate

Automated. Any failure requires revision before 3D.

```python
# src/schemas/competency.py
def title_word_count(cls, v: str) -> str:
    n = _word_count(v)
    if not 3 <= n <= 6:
        raise ValueError(...)
    return v
```

**Title rules:** 3–6 words; relevant to technical domain; unique within specialization; non-overlapping across family; no V&B/Common echo.

**Definition rules:** one sentence (abbreviation-tolerant); 15–25 words; unique primary verb / key noun phrase; non-overlapping scope; action-first framing.

### 3D — Rank and Select (Top 8 → Top 6)

Weighted composite (v3.1 four-factor; enforced by `CriticalityBreakdown`):

| Dimension | Weight | Definition |
|-----------|--------|------------|
| Coverage | 0.40 | Proportion of Technical EFs addressed |
| Criticality | 0.30 | Importance to role, informed by benchmarks |
| Distinctiveness | 0.20 | Non-overlap with V&B / Common / other selected |
| Assessability | 0.10 | Evaluable via structured interviews / work samples |

Top 8 by composite, reduced to Top 6 with documented deferral rationale. **Coverage threshold:** Top 6 must cover **≥ 90%** of Technical/Mixed EFs.

### 3E — Proficiency Descriptors

Standard labels: **L1 Basic / L2 Developing / L3 Skilled / L4 Expert**. 3 indicators per level. Observable, domain-specific, ≥ 1 tool/method/artifact per level. Never tied to management authority.

**Level Differentiation Rubric** — every adjacent pair (L1/L2, L2/L3, L3/L4) on four dimensions: **Autonomy / Scope / Complexity / Contribution type**. If any pair fails ≥ 2 of 4 dimensions, rewrite before proceeding. **L1/L2 boundary is the most consequential threshold for workforce planning.**

Rubric source of truth: `src/schemas/rubric.py::RUBRIC`.

---

## Section 11 — Phase 4: QA Gate (QA Agent)

### Three-Lens Review Protocol

**Lens 1 — IO Psychologist / Technical Expert.** Grounded in validated frameworks (DDI, Korn Ferry KF4D, Campion et al. 20 best practices)? Indicators observable and measurable with inter-rater reliability? Proficiency levels differentiate per Rubric? Legally defensible for selection / promotion / succession? Reference standard: Sackett et al. (2022) — structured interviews top the validity hierarchy.

**Lens 2 — Senior HR Leader / HRBP Practitioner.** Usable in a 30-min calibration meeting? Matches Cargill framework vocabulary? HITL workbook navigable without IO expertise? Maintenance burden manageable? Cross-regionally interpretable (NA, EMEA, LATAM, APAC)?

**Lens 3 — End-User Executive / Hiring Manager.** Distinguishes candidates at the same band? L2 vs L3 clear without reference guide? Connected to work outcomes? Passes the "so what?" test?

### Issue Classification

| Severity | Action |
|----------|--------|
| **Critical** | Blocks intended use → must resolve before output |
| **Important** | Reduces effectiveness → resolve or document |
| **Minor** | Polish → fix if time |
| **Cross-lens convergence** | Same issue flagged by 2+ lenses → escalate to Critical |

### Boundary and Overlap Audit

1. Scan all competency content vs. V&B and Common boundary terms.
2. Cross-competency distinctiveness: < 30% of indicators interchangeable within a specialization.
3. Cross-family consistency: same name across families → identical (shared) or explicitly differentiated.
4. **Label uniqueness audit:** no two titles share a keyword; no two definitions share primary verb / key noun phrase.

### Quality Gate

Maximum **3 revision cycles**. After 3 failed cycles: **STOP and present** the blocker, why prior revisions failed, what manual decision would unblock. **Never skip the gate. Never silently degrade quality.**

Implementation: `src/agents/overlap_auditor.py`, `src/agents/overlap_remediator.py`, `src/orchestrator/gates.py`.

---

## Section 12 — Phase 5: Output (Output Agent)

### Generation Order — Persistence First

1. **Update Central Library** with all new / modified / reused / deferred competencies. After R2/FINAL, the **rolling Master Library merger** (Section 30) merges the run's delta into the canonical `data/library/TechComp_Library_Master.xlsx` keyed by `Comp_ID`.
2. Generate all other deliverables (Section 17).
3. Apply Cargill branding: Leaf Green `#00843D` headers, Arial body, Georgia H1, alternating White `#FFFFFF` / White Green `#F5F9ED` rows, branded header, confidentiality footer.

Branding constants: `src/utils/branding.py`.

### SME Package Format Decision

If a family has ≤ 6 specializations AND ≥ 3 shared competencies, offer per-specialization OR unified (SBD model). Operator decides.

---

## Section 13 — Phase 6: Feedback Processing (R2 / FINAL only)

### 6A — Feedback Ingest and Classification

**Supported sources:** Qualtrics survey exports (CSV/XLSX), track-changes Word docs, focus group transcripts, email/chat compiled by HRBPs, Rosetta Stone Tracker updates.

**Qualtrics processing:**

1. **Response validity screening** — flag test responses, empty submissions, duplicate IDs.
2. **Likert mapping:** 4–5 → Auto-accept (Green); 3 → Discussion flag (Yellow); 1–2 → Requires revision / focus group (Red).
3. **Open-text coding** → Keep / Edit / Gap / Discuss. Preserve verbatim — no paraphrasing.
4. **Cross-respondent triangulation** — synthesize multiple comments on one competency noting agreement / disagreement.

### 6B — Feedback Classification Taxonomy

| Code | Use when | Action |
|------|----------|--------|
| **Keep** | Wording reflects work as performed | No change — verbatim carry-forward |
| **Edit** | Definition / indicator improvable | Apply if direction is clear; else defer |
| **Gap** | Important work missing | Promote rank 7–8; else generate new via Phase 3 |
| **Discuss** | Issue points to redesign / architecture | Add to Deferred Items Register |

### 6C — Propagation Protocol

When an **anchor SME** provides feedback, propagation goes to ALL specializations sharing the competency unless a spec-specific SME has provided conflicting feedback. **Conflict** → flag both verbatim comments; operator chooses adopt-anchor / adopt-specialization / create-variant. Never resolve silently. **Variation detection** after propagation: character-level diff across instances; any non-intentional variation → flag.

### 6D — REVIEW_METADATA Gate

Validate before applying feedback: `Submission_Ready = YES`, `Reviewer_Group` populated, `Approval_Type` set, `Calibration_Required = NO` OR `Calibration_Completed = YES`. If missing: STOP and list.

### 6E — No-Drift Enforcement

Change ONLY competencies explicitly addressed. Do not rephrase / reformat / restructure Keep / Accept content. Quality issues in Accepted content → flag, do not silently correct.

### 6E-bis — Coverage Refresh (v3.1 #27)

Regenerate EF Coverage Map after SME edits. If coverage drops below **90%**, block output. Output: refreshed `Coverage_Map_[JobFamily]_[Stage].csv` + `coverage_refresh` section in `Run_Artifacts.json`. Implementation: `src/agents/coverage_refresh.py`.

### 6E-ter — Boundary Re-Scan (v3.1 #28)

Re-scan edited competencies. Present each new flag with proposed revision; do not apply silently. Implementation: `src/agents/boundary_rescan.py`.

### 6E-quater — Overlap Re-Audit (v3.1 #29)

Regenerate Overlap Audit. For each worsened pair, present causal edit and remediation. Implementation: `src/agents/overlap_reaudit.py`.

### Updated Phase 6 Execution Order

```
6A → 6B → 6C → 6D → 6E → 6E-bis → 6E-ter → 6E-quater → 6F → 6G
```

---

## Section 14 — Phase 6F: CTIC (Competency Text Integrity Check)

The enforcement mechanism for no-drift.

### Protocol

1. **Capture baseline** — snapshot every competency NOT targeted by feedback.
2. **Apply feedback** — execute directed changes.
3. **Character-level diff** — post-edit vs. baseline.
4. **Flag variance** — any difference, even one character, is unintended drift.
5. **Revert + persist** — revert drifted text. **Corrected post-state written to disk as `{run_id}_6F_post_ctic_state.json` and registered on `ArtifactRegistry.post_ctic_state`** so downstream agents consume reverted text.

**Drift gate:** `drift_rate > 0.05` → `CTIC_DRIFT_RATE_EXCEEDED` ERROR.

Implementation: `src/agents/ctic_validator.py`, `src/utils/ctic_diff.py`.

---

## Section 15 — Phase 6G: Focus Group Preparation

Runs whenever ≥ 1 feedback item is classified Discuss.

### Deferred Items Register

| Field | Description |
|-------|-------------|
| Defer_ID | Sequential (SEC-D01, SBD-D01, ...) |
| Competency_ID | Library ID |
| Issue_Summary | One-sentence description |
| Source_Feedback | Verbatim SME comments |
| Decision_Question | What the focus group must answer |
| Decision_Options | 2–4 options |
| Impact_If_Unresolved | What happens with no decision |

### Focus Group Deliverables

1. **Facilitator One-Pager** — agenda, decision questions, facilitator cues, live capture targets.
2. **Specialization Competency Packages** — applied changes / deferred items / boundary reminder per spec.
3. **Review Workbook** — Applied / Deferred / Decision capture tabs.

Implementation: `src/agents/focus_group_prep.py`, `src/deliverables/sme_package.py`.

---

## Section 16 — Phase 7: Learning Synthesis (FINAL only)

Compile `Learning_Updates.json` with feedback themes, boundary calibration rules, cross-family consistency decisions, parsing patterns, process improvements. Upload to project knowledge after each FINAL. Implementation: `src/agents/learning_synthesis.py`.

---

## Section 17 — Standard Deliverables

### Always Produced

| Deliverable | File pattern | Purpose |
|-------------|-------------|---------|
| Central Library | `TechComp_Library_Master.xlsx` | System of record |
| Job Family Package | `[JobFamily]_Technical_Competency_Package_[Stage].docx` | Single source of truth |
| Run Artifacts | `Run_Artifacts_[JobFamily]_[Stage].json` | Reproducibility audit |
| Session State | `session_state_[JobFamily]_[Stage].json` | Cross-session resume |
| BCO Ledger | `BCO_Ledger_[JobFamily].xlsx` | Coverage / boundary / overlap history |

### R1 Deliverables

`Executive_Decision_Brief_*_R1.docx`, `SME_Validation_Package_*_R1.docx`, `HITL_Review_Workbook_*_R1.xlsx`, `AI_Technical_Competencies_*_R1.xlsx`, `JDMS_TechCompetencies_*_R1.xlsx` (if JDMS), `AI_Competency_Coverage_Analysis_*_R1.xlsx`, `Coverage_Map_*_R1.csv`.

### R2 / FINAL Additional

`*_Competency_Change_Log_*.xlsx`, `*_Rosetta_Stone_Revision_Tracker.xlsx`, refreshed `Coverage_Map_*.csv`, refreshed `Overlap_Audit_*.csv`, `*_Focus_Group_*.docx` (if deferred), `Learning_Updates_*.json` (FINAL only), `*_HRLT_Summary_*.docx`.

### v3.1 Repo Edition — Additional Deliverables

- `data/library/TechComp_Library_Master.xlsx` — rolling canonical (cross-run merged; Section 30).
- `data/library/Skills_Library_Master.xlsx` — rolling canonical skills library (Section 28).
- `data/library/Skill_Competency_Crosswalk.xlsx` — rolling canonical crosswalk (Section 29).
- `data/trace/run_ledger.jsonl` — append-only run history (Section 30).
- `data/trace/decision_log.jsonl` — append-only gated decisions.
- `data/trace/change_log.jsonl` — append-only cross-run change history.
- `data/trace/step_log.jsonl` — append-only orchestrator step trace.

---

## Section 18 — Schemas (summary)

Full per-deliverable column specs live in `docs/reference/schemas/`.

### 18.1 Central Library v3 (23 columns)

Source of truth: `src/schemas/library.py::LIBRARY_COLUMNS`. Columns: `Comp_ID, Competency_Name (3–6 words), Job_Family, Boundary_Class, Definition (15–25 words, 1 sentence), Why_It_Matters, L1–L4 Descriptor+Indicators (3 each), Applied_Tools, Applied_Standards, Applied_Outputs, Criticality_Score (0.40/0.30/0.20/0.10), Integrity_Tag, Source_Refs, Rosetta_Aliases, First_Published_Run, Last_Modified_Run`. Also supported as a logical view: `Provenance, Parent_Comp_ID, Status, Stage, Created_Date, Last_Modified, Assigned_Specializations, EF_Coverage_Map, Rank_Per_Specialization, 5QMT_Result, Uncertainty_Level, QA_Notes, External_Alignment, Cross_Family_Consistency, CTIC_Last_Verified`.

### 18.2 Change Log — `Change_ID, Competency_ID, Competency_Name, Field_Changed, Before_Text, After_Text, Rationale, Source_Feedback_Ref, Applied_or_Deferred, Decision_Date`.

### 18.3 EF Coverage Map — `Job_Family, Specialization, Job_Title, Job_Code, Band, EF_Number, Essential_Function, Mapped_Competency_Type, Mapped_Competency, In_Spec_Top6, Coverage_Score`.

### 18.4 Rosetta Stone — `Competency_ID, Competency_Name, R1_Title, R1_Definition, R2_Title, R2_Definition, FINAL_Title, FINAL_Definition, Change_Summary, SME_Feedback_Drivers`.

### 18.5 BCO Ledger (v3.1 #30, 4 tabs)

**EF_Coverage_Tracker, Boundary_Audit_History, Overlap_Audit_History, Stage_Summary.** Implementation: `src/deliverables/bco_ledger_writer.py`, `src/schemas/bco_ledger.py`.

### 18.6 Run Artifacts JSON — see `docs/reference/schemas/run_artifacts_schema.md`. Key sections: `inputs, key_changes, outputs, coverage_refresh, boundary_rescan, overlap_reaudit, ctic_results`.

### 18.7 HRLT Summary

**One page max.** 90-second read for non-IO audience. Headline (1 sentence), Scope (2–3 sentences), What changed this round (3–5 sentences), What's left to decide (numbered), What we need from you (1–2 sentences). No IO jargon, no competency IDs.

---

## Section 19 — Quality Gates and Validation Criteria (summary)

| Gate | Phase | Rule | Action on failure |
|------|-------|------|-------------------|
| Parse confidence | 1 | ≥ 70%, ≥ 3 EFs/job | STOP + report |
| 5QMT decision | 2B | 5/5 reuse, 4/5 adapt, 3/5 variant, ≤2/5 new | Logged |
| Cross-family naming conflict | 2C | Same name + different definition | STOP + present options |
| 3C-gate title | 3 | 3–6 words | Validator error |
| 3C-gate definition | 3 | 15–25 words, 1 sentence | Validator error |
| Coverage threshold | 3D / 6E-bis | ≥ 90% Tech EFs by Top 6 | Block output |
| Band consistency | 3D | Monotonically non-decreasing | Warning |
| Indicator count | 3E | Exactly 3 per level | Validator error |
| Level differentiation | 3E | ≥ 3 of 4 dimensions per pair | Rewrite |
| Cross-lens convergence | 4 | 2+ lenses flag same | Escalate to Critical |
| Iteration ceiling | 4 | Max 3 QA cycles | STOP + escalate |
| REVIEW_METADATA | 6D | All gate fields populated | STOP + list missing |
| CTIC drift rate | 6F | ≤ 0.05 | ERROR flag |
| Top-N cap | overall | ≤ 6 per JD | Validator error |

---

## Section 20 — Proficiency Levels and Band Mapping

| Level | Label | Characterization |
|-------|-------|------------------|
| L1 | Basic | Executes fundamental tasks with guidance |
| L2 | Developing | Executes standard tasks independently |
| L3 | Skilled | Advises peers and leads complex work |
| L4 | Expert | Sets standards enterprise-wide |

**Cargill Band → Proficiency Target Mapping** (`config/band_proficiency_targets.yaml`):

| Band | Target | Range |
|------|--------|-------|
| Associate Professional / Support Staff | L1 | L1 |
| Professional / Senior Analyst | L2 | L1–L2 |
| Senior Professional / Associate | L2–L3 | L2–L3 |
| Advisor / Manager I | L3 | L2–L3 |
| Senior Advisor / Manager II+ | L3–L4 | L3–L4 |
| Senior Manager I+ | L4 | L3–L4 |

**Consistency rule:** target proficiency monotonically non-decreasing with band within the same specialization.

---

## Section 21 — Master Guardrails (always enforce)

**v3.0 + v3.1 amendment (1–18):**

1. **Library primacy** — never create new when 4/5 or 5/5 Library match exists.
2. **Technical boundary** — no drift into V&B / Common.
3. **Observable indicators only** — no traits, internal states.
4. **No hierarchy linkage** — proficiency ≠ management authority.
5. **Cross-family consistency** — same name → identical or explicitly differentiated.
6. **Coverage ≥ 90%** of Technical EFs by Top 6 per specialization.
7. **Source integrity** — CONFIRMED / CORRECTED / UNVERIFIABLE / FLAGGED on all external claims.
8. **No silent degradation** — STOP and explain if quality drops.
9. **Iteration ceiling** — max 3 QA cycles; escalate on 4th.
10. **Library persistence** — prompt download + re-upload (prompt layer) or write rolling master (code layer, §30).
11. **Label & definition quality** — enforced at R1 / R2 / FINAL.
12. **No-drift across revisions** — CTIC enforces programmatically.
13. **Verbatim fidelity** — SME comments preserved in full.
14. **Deferral discipline** — scope / architecture / ownership → focus group.
15. **Coverage persistence (v3.1)** — Coverage Map regenerated every stage; < 90% blocks.
16. **Boundary enforcement (v3.1)** — every edited competency re-scanned.
17. **Overlap monitoring (v3.1)** — Overlap Audit regenerated; worsening flagged with causal edit.
18. **BCO Ledger current (v3.1)** — persistent artifact, downloadable.

**Skill mapping additions (v3.1 repo edition; Sections 26–30):**

19. **Skill mapping triggers downstream**, never upstream — never re-derive competencies from training catalog content.
20. **Bloom level evidence required** — every `SkillCompetencyMapping` carries verb evidence, similarity score, integrity tag.
21. **Crosswalk merger preserves history** — every (course, competency) pair retains `first_mapped_run` and `run_history`.
22. **Skills Library entries are immutable by ID** — updates create new versions; old versions retained.

**Tracing additions:**

23. **Append-only ledgers** — `data/trace/*.jsonl` files never rewritten; only appended.
24. **No silent ledger gaps** — every gated decision and every artifact write generates an entry.
25. **Master library merger is idempotent** — re-running an identical run does not double-count.

---

## Section 22 — File Format Detection Protocol

See Section 3. Reaffirmed at every file read by `src/utils/file_parsers.py`.

---

## Section 23 — Current Project Portfolio Status (April 25, 2026)

| Family | Stage | Competencies | Specs | Status | Blockers |
|--------|-------|-------------|-------|--------|---------|
| Legal & Compliance | FINAL (2 items open) | 21 | 13 | 20 verified; 1 pending | Jessie Collings source doc; Neil Sawatzke markup |
| Aviation | R5 complete | 14 | 4 | All JDMS-locked | REVIEW_METADATA gate not cleared |
| Security | R2.2 (focus group) | 8 | 2 | SEC-D01–D06 deferred | Focus group decisions required |
| REI / Facilities | R1 complete | 18 | 3 | All SME packages delivered | SME survey creation pending |
| SBD (unified) | R2 (survey done) | 12 | 6 | Focus group completed | Corp Strategy C6 slot decision |

**JDMS-Locked (April 17, 2026):** Security 7/2/18; Aviation 14/4/16; Strategy 13/3/21 (Corp Strategy locked at 5, not 6); Corporate Business Development unified 13/3/18.

**Library stats:** ~70 unique competencies. ~20 FINAL. ~5–8 cross-family shared (verify at next consolidation).

**Open items:** Legal 21st competency discrepancy; REI title-length flags (TC-REI-012, TC-REI-015); SBD Corp Strategy 5-vs-6.

Source of truth: `docs/reference/Portfolio_Status.md`.

---

## Section 24 — Current Project Files Index

See `docs/reference/Portfolio_Status.md` for the full file index.

---

## Section 25 — Quick-Start Verification Checklist

### System integrity
- [ ] TCB v3.0 instructions present and complete
- [ ] TCB v3.1 amendment (#27–30) integrated into Phase 6
- [ ] V&B Boundary Terms table (6 V&B + 5 Common)
- [ ] Partner with Impact disambiguation rule
- [ ] Library Schema v3 (23 cols)
- [ ] All phase gates (3A, 3C, 4, 6D, 6E-bis, 6E-ter, 6E-quater, 6F)
- [ ] Three-lens framework complete
- [ ] All deliverable schemas specified
- [ ] **(v3.1 repo)** Skill mapping pipeline (SM1–SM8) wired
- [ ] **(v3.1 repo)** Tracing module (`src/tracing/`) wired
- [ ] **(v3.1 repo)** Skills library merger wired

### Guardrails enforcement
- [ ] Title 3–6 words enforced (3C-gate)
- [ ] Definition 1 sentence, 15–25 words enforced
- [ ] Coverage ≥ 90% enforced; < 90% blocks output
- [ ] Boundary re-scan (6E-ter) at every R2/FINAL
- [ ] Overlap re-audit (6E-quater) at every R2/FINAL
- [ ] CTIC verifies no-drift + persists reverted state
- [ ] Max 3 QA cycles enforced
- [ ] Cap of 6 competencies per JD enforced
- [ ] **(v3.1 repo)** Skill mapping confidence ≥ 0.55; unmapped rate ≤ 0.25
- [ ] **(v3.1 repo)** Master library merger idempotent on re-run
- [ ] **(v3.1 repo)** Run ledger appended once per run

---

# === v3.1 Repo Edition Extensions (Sections 26–32) ===

## Section 26 — Skill Development & Mapping Module — Overview

### Intent

The Skill Development & Mapping subsystem (`src/skill_mapping/`) is **downstream of TCB** — it consumes the published Library + per-family L&D training catalogs and produces a **Skill→Competency→Level crosswalk** so L&D teams can target development against the validated technical competencies.

It is intentionally **read-only on competencies** — skill mapping never re-derives or modifies a TCB competency. This preserves the audit chain: TCB defines the truth; mapping describes coverage against it.

### Pipeline Placement

```
TCB R1/R2/FINAL → publishes TechComp_Library_Master.xlsx
                                 ↓
                  Skill Mapping (SM1..SM8)
                                 ↓
                  Skill_Competency_Crosswalk.xlsx + Coverage Map + Gap Report
```

### Why a Parallel Pipeline

- Different cadence — L&D catalogs update more frequently than competency models.
- Different inputs — catalog files have their own format (course_id, modality, duration, learning_objectives).
- Different stakeholders — L&D operations vs. T&D COE.
- Cleaner audit — keeps the no-drift CTIC guarantee scoped to TCB alone.

### Master Skills Library

A **parallel master library** to the Master Competency Library (Section 28). Catalogs every TrainingItem ever ingested, classified Bloom level, vendor, modality, audience band, integrity tag, first/last-seen run. Lives at `data/library/Skills_Library_Master.xlsx`.

---

## Section 27 — Skill Mapping Pipeline (SM1 – SM8)

Source of truth: `src/skill_mapping/graph.py`.

| Stage | Name | Inputs | Outputs | Implementation |
|-------|------|--------|---------|----------------|
| **SM1** | Catalog Loader | L&D catalog xlsx/csv | `List[TrainingItem]` | `catalog_loader.py` |
| **SM2** | Library Loader | `TechComp_Library_Master.xlsx` | `List[TechnicalCompetency]` (v3.1) | `library_loader.py` |
| **SM3** | Bloom Classifier | TrainingItem | `BloomLevelEstimate(level, confidence, evidence_verbs, adjustments_applied)` | `bloom_classifier.py` |
| **SM4** | Semantic Matcher | TrainingItem × Library | Top-K candidate competencies | `semantic_matcher.py` |
| **SM5** | Level Resolver | candidates + Bloom + band + duration + modality (+ LLM tie-break) | `SkillCompetencyMapping` | `level_resolver.py` |
| **SM5-gate** | Quality gate | confidence ≥ 0.55, unmapped ≤ 25%, audience-vs-level mismatch ≤ 10% | RunFlags | `graph.py` |
| **SM6** | Coverage Aggregator | mappings | `CoverageCell[competency × level]` | `coverage_aggregator.py` |
| **SM7** | Gap Reporter | coverage + library | `GapFinding[]` + surplus/misalignment | `gap_reporter.py` |
| **SM8** | Crosswalk Writer | all above | Branded Excel: Crosswalk / Coverage Map / Gaps / Surplus / Common-V&B | `excel_writer.py` |

### Bloom Level Algorithm

```python
def classify_level(item: TrainingItem) -> BloomLevelEstimate:
    # 1. Tokenize learning_objectives + description, count verb hits per L1..L4 lexicon
    # 2. Base level = argmax(counts) (default L2 on tie)
    # 3. Adjustments:
    #    - Short eLearning (<2h)  : level → max(L1, level-1)
    #    - Long coaching/OJT (>16h): level → min(L4, level+1)
    #    - Prerequisites present  : level → min(L4, level+1)
    #    - Audience band present  : snap into target band from band_proficiency_targets.yaml
    # 4. LLM tie-break ONLY if top-2 counts differ by ≤ 1
    # 5. confidence = 0.4*verb_signal + 0.2*duration_signal + 0.2*modality_signal + 0.2*llm_agreement
    #    where duration_signal and modality_signal are derived from item attributes
    #    (per-level hours bands + modality×level fit table, NOT hardcoded constants)
```

Verb lexicons: `config/bloom_verbs.yaml`. Duration / modality fit tables: `src/skill_mapping/bloom_classifier.py::_duration_signal` / `_modality_signal`.

### Confidence Composition

```
final_mapping_confidence = 0.5 * semantic_similarity
                         + 0.3 * bloom_estimate.confidence
                         + 0.2 * llm_agreement_score
```

### Integrity Tagging on Mappings

| Tag | Condition |
|-----|-----------|
| **CONFIRMED** | similarity ≥ 0.70 AND Bloom-level agreement |
| **UNVERIFIABLE** | 0.55 ≤ similarity < 0.70 OR Bloom-level disagreement |
| **FLAGGED** | similarity ≥ 0.55 but audience-band mismatch beyond ±1 level |
| **CORRECTED** | LLM tie-break overrode the verb-count majority |

### V&B / Common Training Handling

Items routed to a separate **Common_VB_Training** worksheet *before* mapping via name-keyword filter ("ethics", "code of conduct", "harassment", "leadership 101", etc.). Never count toward unmapped rate. Items failing all keyword filters whose max similarity across ALL technical competencies is < 0.40 also route here with UNVERIFIABLE tag.

### Quality Gates

| Gate | Threshold | Action |
|------|-----------|--------|
| `min_mapping_confidence` | ≥ 0.55 | WARN < 0.65, ERROR < 0.55 |
| `unmapped_course_rate` | ≤ 0.15 | ERROR > 0.25 |
| `zero_training_competency_rate` | ≤ 0.20 | ERROR > 0.40 |
| `audience_band_level_mismatch_rate` | ≤ 0.10 per family | WARN |

### CLI

```
techcomp map-skills \
  --library data/library/TechComp_Library_Master.xlsx \
  --catalog data/lnd/[family]_catalog.xlsx \
  --family [name] \
  --out data/output/skill_mapping/ \
  [--min-confidence 0.55] [--llm-tiebreak/--no-llm-tiebreak]
```

---

## Section 28 — Skills Library Schema (Master Skills Library, NEW)

Parallel to the 23-col TechComp Library. Source of truth: `src/skill_library/schemas.py`.

### Columns (v1)

| # | Column | Type | Description |
|---|--------|------|-------------|
| 1 | Skill_ID | String | Stable ID, e.g. `SK-FIN-0042` |
| 2 | Course_ID | String | Vendor / catalog ID |
| 3 | Title | String | Course title |
| 4 | Description | String | One-paragraph description |
| 5 | Job_Family | String | Originating family |
| 6 | Modality | String | ELEARNING / ILT / COACHING / OJT / BLENDED |
| 7 | Duration_Hours | Float | |
| 8 | Audience_Band | String | Cargill band |
| 9 | Prerequisites | String | Pipe-delimited course IDs |
| 10 | Vendor | String | |
| 11 | Bloom_Level | String | L1 / L2 / L3 / L4 (classified) |
| 12 | Bloom_Confidence | Float | 0.0–1.0 |
| 13 | Bloom_Evidence_Verbs | String | Pipe-delimited |
| 14 | Bloom_Adjustments | String | Pipe-delimited (e.g., `DURATION_SHORT_ELEARNING_DOWNSHIFT`) |
| 15 | Integrity_Tag | String | CONFIRMED / CORRECTED / UNVERIFIABLE / FLAGGED |
| 16 | First_Seen_Run | String | Run ID of first ingestion |
| 17 | Last_Seen_Run | String | Run ID of most recent ingestion |
| 18 | Version | Integer | Bumped on each material change |
| 19 | Status | String | Active / Deprecated / Superseded |
| 20 | Linked_Competencies | String | Pipe-delimited Comp_IDs from current crosswalk |
| 21 | Source_Refs | String | Pipe-delimited source attestations |
| 22 | Notes | String | |

### Persistence Rules

- **Append-only by Skill_ID** — new skills get new IDs; updates bump `Version` and replace the row in-place.
- **Status transitions are explicit** — Deprecated / Superseded require an audit note.
- **Linked_Competencies refreshed every map-skills run.**
- **Two physical files:** `data/library/Skills_Library_Master.xlsx` (rolling canonical) + `data/library/Skills_Library_Master.jsonl` (append-only event journal).

---

## Section 29 — Skill→Competency Crosswalk Schema (NEW)

Two views, both persisted.

### 29.1 Per-Run Crosswalk (snapshot)

Produced by SM8 (`src/skill_mapping/excel_writer.py`). 6 tabs: Run_Metadata, Crosswalk, Coverage_Map (red-fill empty cells), Gaps, Surplus, Common_VB_Training.

### 29.2 Master Rolling Crosswalk (cross-run, NEW)

Lives at `data/library/Skill_Competency_Crosswalk.xlsx`. Keyed by `(course_id, competency_id)`.

| Column | Description |
|--------|-------------|
| Skill_ID | From Skills Library |
| Course_ID | Vendor ID |
| Competency_ID | TechComp Library ID |
| Competency_Name | Title |
| Current_Level | L1–L4 |
| Current_Confidence | Latest value |
| Current_Integrity_Tag | Latest value |
| First_Mapped_Run | Run ID |
| Last_Mapped_Run | Run ID |
| Run_History | JSON list of `{run_id, level, confidence, integrity_tag, timestamp}` |
| Status | Active / Deprecated (auto-deprecated when not seen in 2 consecutive runs) |
| Notes | Operator overrides |

Merger logic: `src/skill_library/crosswalk_merger.py`.
- **Idempotent:** re-running an identical map-skills run does not duplicate rows.
- **Change detection:** any change in level / confidence / integrity_tag appends to `Run_History`.
- **Auto-deprecation:** rows not present in two consecutive runs transition to `Deprecated`; operator override allowed.

---

## Section 30 — Continuous Tracing Infrastructure (NEW)

All ledgers are **append-only JSONL**. Never rewritten. One line per event.

### 30.1 `data/trace/run_ledger.jsonl` — Run-level history

```json
{
  "run_id": "Finance_R1_20260425_a1b2c3d4",
  "type": "TCB|SKILL_MAPPING",
  "stage": "R1",
  "family": "Finance",
  "started_at_utc": "...",
  "completed_at_utc": "...",
  "agents_run": ["S1","S2","S3","S4","S5","S6","S7","S8","S9"],
  "gates": {"S1_Gate":"passed","S2_Gate":"passed","S5_Gate":"reaudit","S7_Gate":"passed"},
  "artifacts_produced": ["data/output/Finance_R1_..._library.xlsx", "..."],
  "flag_summary": {"INFO":3,"WARNING":1,"ERROR":0,"CRITICAL":0}
}
```

### 30.2 `data/trace/step_log.jsonl` — Orchestrator step transitions

```json
{"run_id":"...","at_utc":"...","step":"S3_normalize","event":"enter","artifact_fingerprint":"sha256:..."}
{"run_id":"...","at_utc":"...","step":"S3_normalize","event":"exit","artifact_fingerprint":"sha256:..."}
```

### 30.3 `data/trace/decision_log.jsonl` — Every gated decision

```json
{"run_id":"...","at_utc":"...","decision":"5QMT","competency_candidate":"...","verdict":"4/5 reuse-with-adapt","rationale":"..."}
{"run_id":"...","at_utc":"...","decision":"BOUNDARY","competency_id":"...","verdict":"V_AND_B","matched_terms":["..."]}
{"run_id":"...","at_utc":"...","decision":"CRITICALITY_RANK","competency_id":"...","rank":3,"weighted_score":0.812}
{"run_id":"...","at_utc":"...","decision":"FEEDBACK_DISPOSITION","feedback_id":"...","verdict":"EDIT","propagates_to":["..."]}
{"run_id":"...","at_utc":"...","decision":"CTIC","competency_id":"...","field":"definition","verdict":"REVERTED"}
```

### 30.4 `data/trace/change_log.jsonl` — Field-level change history (cross-run)

```json
{"run_id":"...","at_utc":"...","competency_id":"...","field":"definition","before":"...","after":"...","source":"SME|CTIC|AUTO","rationale":"..."}
```

Supplements the per-run `Change_Log.xlsx` (Section 18.2). The xlsx is a snapshot deliverable; the JSONL is the rolling system of record.

### 30.5 Master Library Merger

`src/skill_library/library_merger.py` — promotes per-run `{run_id}_TechComp_Library_Master.xlsx` into rolling `data/library/TechComp_Library_Master.xlsx`:

- Match by `Comp_ID`.
- New entry → append.
- Updated entry → replace in place; log a row to `data/trace/change_log.jsonl` for every changed field.
- Removed-from-run entry → archive to `data/library/_archive/TechComp_Library_Master_{archive_date}.xlsx`.
- **Idempotent:** identical inputs produce zero new ledger entries.

### 30.6 Tracing Module Layout

```
src/tracing/
  __init__.py
  ledger.py            # append-only writer with file-locking
  run_ledger.py        # record_run_start / record_run_complete
  step_log.py          # record_step_enter / record_step_exit
  decision_log.py      # record_decision(kind, ...)
  change_log.py        # record_change(competency_id, field, before, after, source, rationale)
  fingerprint.py       # sha256 of state slices for step_log entries
```

Wiring: `BaseAgent.execute()` records `step_enter` / `step_exit` automatically. Phase agents record decisions inline. CTIC validator records reverts. Output agent records run completion.

---

## Section 31 — Review & Update Protocol Based on Intended Functionality (NEW)

The spec and the code must stay in sync. This protocol defines how.

### 31.1 Intended Functionality — Three Layers of Intent

A claim is "functioning as intended" only when all three agree:

1. **Specification intent** — what this document says.
2. **Schema intent** — what Pydantic validators in `src/schemas/` enforce.
3. **Behavioral intent** — what agents in `src/agents/` and `src/skill_mapping/` actually do at runtime.

Drift between layers is a defect.

### 31.2 Review Triggers

A review-and-update cycle is triggered automatically when:

1. **Every PR that touches `src/schemas/` or `src/orchestrator/`** — verify the corresponding section of this doc is updated in the same PR.
2. **Every FINAL stage completion** — run the full verification checklist (Section 25) and append the result to `data/trace/review_log.jsonl`.
3. **Every quarterly review** (calendar) — full audit of spec ↔ code ↔ behavior alignment.
4. **On any user request** ("ensure functioning works as intended", "verify spec").

### 31.3 Review Checklist — per cycle

For each numbered guardrail (Section 21):
- [ ] Spec text present and unambiguous.
- [ ] Code path that enforces it identified (cite file:line).
- [ ] At least one unit test exercises the enforcement.
- [ ] At least one simulation test exercises end-to-end behavior.
- [ ] Recent runs in `data/trace/decision_log.jsonl` show the guardrail firing as expected (or document why it's quiet).

For each schema (Section 18):
- [ ] Column list in spec matches `src/schemas/library.py::LIBRARY_COLUMNS` or equivalent.
- [ ] Validators present for every constraint claimed in spec.
- [ ] Deliverable writer produces all claimed columns.

For each phase agent (Sections 8–16, 27):
- [ ] System prompt in `BaseAgent.get_system_prompt()` matches spec narrative.
- [ ] Outputs match the artifact registry pointer expected by downstream agents.
- [ ] Phase produces a `step_log.jsonl` entry.

### 31.4 Update Workflow

1. **Detect drift** — automated reviewer (Explore + Plan agent pair, or operator) compares spec sections to code paths cited in Section 32.
2. **Classify drift severity:**
   - **CRITICAL** — code enforces a different rule than spec claims. STOP and surface.
   - **HIGH** — spec missing a rule the code actually enforces. Update spec.
   - **MEDIUM** — comment / system-prompt mismatch.
   - **LOW** — wording polish.
3. **Update in one PR** — never update spec without code, or code without spec. Same PR.
4. **Record in trace** — append a `review_log.jsonl` entry: `{review_id, at_utc, findings, severity_counts, prs_opened}`.

### 31.5 Continuously Updated Files

System-maintained — operators should not edit by hand:

| File | Updated by | Trigger |
|------|-----------|---------|
| `data/trace/run_ledger.jsonl` | `src/tracing/run_ledger.py` | Every run start / complete |
| `data/trace/step_log.jsonl` | `BaseAgent.execute()` | Every step enter / exit |
| `data/trace/decision_log.jsonl` | Phase agents | Every gated decision |
| `data/trace/change_log.jsonl` | CTIC + Output + Library Merger | Every field-level change |
| `data/trace/review_log.jsonl` | §31.4 workflow | Every review cycle |
| `data/library/TechComp_Library_Master.xlsx` | `library_merger.py` | Every R1/R2/FINAL completion |
| `data/library/Skills_Library_Master.xlsx` | `skill_library_merger.py` | Every map-skills completion |
| `data/library/Skill_Competency_Crosswalk.xlsx` | `crosswalk_merger.py` | Every map-skills completion |
| `docs/reference/Portfolio_Status.md` | Run hook | Every FINAL completion |

Operator-edited by hand: `docs/reference/*.md` (spec text), `config/*.yaml` (thresholds), all source `.py` files.

### 31.6 Verification Modes

| Mode | Scope | Cost | When |
|------|-------|------|------|
| **Lint** | ruff + mypy | seconds | Every commit |
| **Unit** | pytest tests/ | < 30s | Every commit |
| **Simulation** | end-to-end synthetic runs of R1 / R2 / map-skills / tracing aggregation | ~2 min | Every PR |
| **Spec-code alignment** | Explore agent scans spec ↔ code | ~5 min | Every PR touching schemas/orchestrator |
| **Three-lens (live)** | IO Psych / HRBP / Executive review of actual deliverables | hours | Every FINAL |
| **Quarterly full audit** | All of the above + operator manual review | days | 4×/year |

---

## Section 32 — Code-to-Spec Crosswalk

| Spec section | Code path |
|--------------|-----------|
| §5 Principles | `src/schemas/competency.py` |
| §6 V&B / Common boundary | `src/utils/boundary_classifier.py`, `config/boundary_terms.yaml` |
| §7 Domain framework registry | `config/domain_registry.yaml` |
| §8 Phase 1 Parse | `src/agents/job_ingestion.py`, `src/utils/file_parsers.py` |
| §9.2B 5QMT | `src/utils/five_qmt.py` |
| §10.3C-gate | `src/schemas/competency.py::TechnicalCompetency.title_word_count` / `.definition_one_sentence_15_25` |
| §10.3D Criticality | `src/schemas/competency.py::CriticalityBreakdown`, `src/agents/criticality_ranker.py` |
| §10.3E Rubric | `src/schemas/rubric.py` |
| §11 Phase 4 QA | `src/agents/overlap_auditor.py`, `src/orchestrator/gates.py` |
| §13.6E-bis Coverage refresh | `src/agents/coverage_refresh.py` |
| §13.6E-ter Boundary re-scan | `src/agents/boundary_rescan.py` |
| §13.6E-quater Overlap re-audit | `src/agents/overlap_reaudit.py` |
| §14 CTIC | `src/agents/ctic_validator.py`, `src/utils/ctic_diff.py` |
| §15 Focus Group prep | `src/agents/focus_group_prep.py` |
| §16 Phase 7 Learning Synthesis | `src/agents/learning_synthesis.py` |
| §17 Deliverables | `src/deliverables/*` |
| §18.1 Library schema | `src/schemas/library.py::LIBRARY_COLUMNS`, `src/deliverables/library_writer.py` |
| §18.5 BCO Ledger | `src/schemas/bco_ledger.py`, `src/deliverables/bco_ledger_writer.py` |
| §18.7 HRLT Summary | `src/deliverables/hrlt_summary.py` |
| §20 Band targets | `config/band_proficiency_targets.yaml`, `src/utils/band_targets.py` |
| §21 Guardrails | All of the above + `src/orchestrator/gates.py` |
| §27 Skill mapping pipeline | `src/skill_mapping/{graph, catalog_loader, library_loader, bloom_classifier, semantic_matcher, level_resolver, coverage_aggregator, gap_reporter, excel_writer}.py` |
| §28 Skills Library | `src/skill_library/` |
| §29 Crosswalk | `src/skill_library/crosswalk_merger.py` + `src/skill_mapping/excel_writer.py` |
| §30 Continuous tracing | `src/tracing/` |
| §31 Review & update protocol | this document + `tests/test_simulation/*` |

---

## Appendix A — Enhancement Mapping

| # | Enhancement | Version | Location |
|---|-------------|---------|----------|
| 1 | Phase 6 definition | v3.0 | §13 |
| 2 | Phase 7 specification | v3.0 | §16 |
| 3 | Qualtrics survey protocol | v3.0 | §13.6A |
| 4 | Focus Group preparation | v3.0 | §15 |
| 5 | Rosetta Stone | v3.0 | §18.4 |
| 6 | CTIC protocol | v3.0 | §14 |
| 7 | Propagation protocol | v3.0 | §13.6C |
| 8 | Deferred items register | v3.0 | §15 |
| 9 | HRLT specification | v3.0 | §18.7 |
| 10 | Portfolio status | v3.0 | §23 |
| 11 | Fast-path session start | v3.0 | §3 |
| 12 | File-format detection | v3.0 | §3, §22 |
| 13 | session_state consolidation | v3.0 | §4 |
| 14 | Unified SME package variant | v3.0 | §12 |
| 15 | Change Log | v3.0 | §18.2 |
| 16 | EF Coverage Map | v3.0 | §18.3 |
| 17 | Automated title word-count | v3.0 | §10.3C-gate |
| 18 | Cargill band mapping | v3.0 | §20 |
| 19 | V&B/Common reference embedded | v3.0 | §6 |
| 20 | Partner with Impact disambiguation | v3.0 | §6 |
| 21 | Domain Framework Registry | v3.0 | §7 |
| 22 | Prior-model non-conformance | v3.0 | §10.3B |
| 23 | Library schema v3 (23 cols) | v3.0 | §18.1 |
| 24 | Multi-family conflict resolution | v3.0 | §9.2C |
| 25 | Hot-start mode | v3.0 | §9.2B |
| 26 | Branding specification | v3.0 | §12 |
| **27** | **Post-Edit Coverage Refresh** | **v3.1 amend** | **§13.6E-bis** |
| **28** | **Post-Edit Boundary Re-Scan** | **v3.1 amend** | **§13.6E-ter** |
| **29** | **Post-Edit Overlap Re-Audit** | **v3.1 amend** | **§13.6E-quater** |
| **30** | **BCO Ledger** | **v3.1 amend** | **§18.5** |
| **31** | **Skill Development & Mapping Module** | **v3.1 repo** | **§26–27** |
| **32** | **Master Skills Library** | **v3.1 repo** | **§28** |
| **33** | **Skill→Competency Crosswalk (rolling)** | **v3.1 repo** | **§29** |
| **34** | **Continuous Tracing Infrastructure** | **v3.1 repo** | **§30** |
| **35** | **Review & Update Protocol** | **v3.1 repo** | **§31** |

---

## Appendix B — Revision Taxonomy Quick Reference

| Feedback Code | Source Context | TCB Action |
|---------------|----------------|------------|
| Keep / Accept | SME endorses current wording | Carry forward verbatim — CTIC verifies no drift |
| Edit / Modify | SME provides specific wording change | Apply directed change; log in Change Log |
| Gap | SME identifies missing technical coverage | Promote rank 7–8; if no fit, generate new via Phase 3 |
| Discuss / Defer | Issue involves scope / architecture / ownership | Add to Deferred Items Register; prepare Focus Group package |
| Reject | SME rejects competency entirely | Remove from assignment; promote rank 7–8; document rationale |

---

## Appendix C — Glossary

- **EF** — Essential Function (a specific task / outcome a job performs).
- **5QMT** — 5-Question Match Test (§9.2B).
- **CTIC** — Competency Text Integrity Check (§14).
- **BCO Ledger** — Boundary / Coverage / Overlap Ledger (§18.5).
- **HRLT** — Cargill's Human Resources Leadership Team.
- **JDMS** — Cargill's Job Description Management System.
- **HITL** — Human-in-the-Loop review workbook.
- **Anchor SME** — the SME whose specialization is the primary owner of a shared competency.
- **TrainingItem** — one course / module entry in an L&D catalog (§27).
- **SkillCompetencyMapping** — one (course, competency, level) tuple with confidence + integrity tag.
- **Rolling Master** — a canonical Excel file in `data/library/` that is merged-into on every run (vs. per-run snapshots).

---

**End of canonical specification.**

To verify a build against this spec, run `pytest tests/test_simulation/ --no-cov -v` and inspect the generated artifacts under `data/output/`. To verify the spec against the code, read Section 32 with `grep -n` on each cited file. To verify operationally, inspect the most recent entries in `data/trace/run_ledger.jsonl` and `data/trace/decision_log.jsonl`.

Maintained by the T&D COE. Engineering contact: see `CONTRIBUTING.md`.
