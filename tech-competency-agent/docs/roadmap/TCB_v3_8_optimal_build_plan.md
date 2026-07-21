# TCB End-to-End Assurance Build Plan

**Status:** revised planning baseline for the updated Technical Competency Builder (TCB)  
**Date:** 2026-06-05  
**Scope:** Forward-only build plan for applying the operative v3.7 content ruleset and the v3.8 assurance controls to the existing TCB Python/LangGraph system.

## 1. BLUF

The updated TCB should run as one end-to-end quality workflow, not as a time-boxed roadmap. Every phase should produce structured evidence, run rule checks, route uncertain work to multi-lens review, and prevent low-quality first drafts from reaching final packaging. The central design change is to embed the operative content rules directly into the development path instead of treating them as after-the-fact review notes.

The operative content ruleset for this plan is **v3.7, adopted 2026-06-05 under DR-019**. It supersedes the prior v3.6 compilation for new and in-flight work. The key delta is **AS-7 competency count**: the prior hard cap of 6 is replaced by a recommended 4-6 range with parsimony selection, per-competency justification beyond 6, and a hard ceiling of 8. All other v3.6 standards carry forward unless explicitly noted.

TCB v3.8 assurance controls still apply as the operating layer: intake risk-tiering, input-packet completeness, slice-level validation, revision-improvement evidence, judge confidence and abstention, SME-effort targeting, Competency Release Cards, and Phase 9 stewardship.

## 2. Operating principles

1. **Rules are phase-native.** Each AS/GC rule is attached to the phase where defects should be prevented, not just where defects can be detected.
2. **Parsimony beats padding.** Competency sets should use the smallest assigned set that clears the coverage floor; do not pad to 6 when 4 or 5 clears 90% Technical/Mixed EF coverage.
3. **Evidence precedes promotion.** Any claim of coverage, improvement, low overlap, technical specificity, boundary clearance, or beyond-6 necessity must be backed by an artifact.
4. **Uncertainty is routed, not hidden.** Low-confidence judge results, missing source support, weak slices, and ambiguous boundaries route to human review.
5. **Multi-lens review is focused.** SMEs and reviewers spend most effort on contested, borderline, weak-slice, low-agreement, or high-impact items.
6. **No-drift is structural.** Canonical content should be changed through patch-only operations tied to parent hashes; CTIC remains a defense-in-depth check.
7. **FINAL means stewarded.** A FINAL family is not static. It carries a refresh owner, cadence, triggers, limitations, approvals, and release evidence.

## 3. End-to-end TCB workflow

```text
Phase 0 — Intake, risk tiering, and intended use
  -> Phase 1 — Input-packet completeness and source authority checks
  -> Phase 2 — Evidence discovery, benchmark retrieval, and source grounding
  -> Phase 3 — Competency mapping, domain clustering, and boundary pre-screen
  -> Phase 3C — Title/definition uniqueness and technical-referent gate
  -> Phase 4 — Draft competency and indicator generation
  -> Phase 4 QA — Indicator, exemplar, readability, and level-quality checks
  -> Phase 4.5 — Coverage, parsimony, beyond-6, and patch-only edit checks
  -> Phase 4.75 — Evaluator-optimizer judge, confidence, verification, abstention
  -> Phase 5 — Multi-lens human review and frame-of-reference calibration
  -> Phase 5.5 — Boundary audit and Common/V&B technical-extension clearance
  -> Phase 6 — Quantitative validation, slice reporting, and revision-delta evidence
  -> Phase 7 — Release evidence pack and Competency Release Card
  -> Phase 8 — Closeout, attestation, library update, and governance registers
  -> Phase 9 — Stewardship loop, refresh triggers, incidents, and R-cycle routing
```

This is a single operating process. A project run can be shorter or longer depending on family complexity, data readiness, and risk tier, but it should always move through the same rule/evidence checkpoints.

## 4. v3.7 content standards embedded by phase

| Rule area | Current rule | Phase home | Gate/output |
|---|---|---|---|
| Title | 3-6 words; names one technical construct; no bundled domains; distinct from V&B/Common names and same-specialization titles; no `Domain: Skill Area` prefix. | Phase 3C | AS-1 / G4 title uniqueness report |
| Definition | One sentence, 15-25 words, verb-led, unique vocabulary within specialization, one concrete technical referent; definitions with no technical object fail. | Phase 3C | AS-2 / G4 definition technicality report |
| Indicator count | 3-5 indicators per level; use 5 only when needed to cover the domain; all four levels cover the domain without unnecessary redundancy. | Phase 4 QA | AS-3 / G5 indicator count and redundancy report |
| Indicator quality | Every indicator observable, action-verb led, one concise sentence, anchored in a concrete referent; no same-content restatement across levels without autonomy, complexity, or scope shift. | Phase 4 QA | AS-3 / G5 and G7 indicator anchor report |
| Exemplars | Parenthetical examples only when they materially improve specificity; selective, non-exhaustive, and first to trim when readability flags. | Phase 4 QA | AS-4 / G8 exemplar-use report |
| Levels | Numeric Level 1-4; L1 guided basics, L2 routine capability, L3 independent advanced work, L4 expert technical leadership; L4 must be valid for a principal IC with no direct reports. | Phase 4 QA | AS-5 / G7 level-progression and L4-IC check |
| Boundary | No restating V&B/Common language; boundary-adjacent competencies must pass technical-extension test and name cleared Common Competency. | Phase 5.5 | AS-6 / boundary clearance record |
| Competency count per JD | Recommended 4-6 range; smallest set clearing coverage floor; below 4 flagged to decision owner; each competency beyond 6 requires standalone rationale; hard ceiling 8; 9+ routes to governance. | Phase 4.5 | AS-7 / parsimony and beyond-6 records |
| Beyond-6 documentation | Each addition beyond 6 has competency ID, basis, evidence ID, marginal coverage, approver, and date; rationale basis is exactly one of SME anchor-verified directive or quantified coverage gap. | Phase 4.5 and Phase 7 | AS-7 / HITL Workbook, Executive Decision Brief, Coverage Analysis, Release Card |
| Coverage | Full assigned set covers at least 90% of Technical and Mixed EFs per specialization; beyond-6 additions raise base coverage, never substitute for it. | Phase 4.5 | AS-7 / G2 coverage analysis |
| Readability | FKGL tiers: 8-10 operational, 9-11 senior, 11+ governance with justification; flag only when two or more metrics exceed tier target. | Phase 4 QA | Enhancement-31 / G8 readability report |
| Anti-stacking | Beyond-6 candidates fail if they substantially overlap assigned competencies, regardless of rationale. | Phase 4.5 | AS-7 / GC-8 proportional overlap check |
| Count-agnostic CTIC | CTIC applies to canonical-text drift and is not affected by the 4-6 recommendation or 8 hard ceiling. | Phase 4.5 and Phase 6 | CTIC report |

## 5. Phase-by-phase rule checks, QA, and multi-lens actions

### Phase 0 — Intake, risk tiering, and intended use

**Purpose:** determine how strict the assurance path must be before authoring begins.

**Rule checks**
- Record intended use: development-only, internal taxonomy, talent review, selection, promotion, succession, or other governed use.
- Record stakeholder exposure, regulatory exposure, source authority tier, and decision owner.
- Determine whether G13-G15 fairness, adverse-impact, DIF, and language-bias gates are mandatory or N/A with rationale.

**QA and evidence outputs**
- `risk_tier_assessment`
- gate-scope matrix
- intended-use and out-of-scope-use statement

**Multi-lens action**
- Decision owner confirms the tier before source ingestion begins.

### Phase 1 — Input-packet completeness and source authority checks

**Purpose:** halt incomplete or malformed work before it becomes drafting debt.

**Rule checks**
- Confirm required job descriptions, job models, source packets, SME inputs, prior artifacts, and templates by stage.
- Validate schema, supported file formats, required columns, minimum essential-function counts, and source-authority classification.

**QA and evidence outputs**
- `input_packet_report`
- source-authority manifest
- missing/malformed input remediation list

**Multi-lens action**
- Intake owner resolves missing or malformed inputs; no authoring begins until the packet passes or a governance exception is logged.

### Phase 2 — Evidence discovery, benchmark retrieval, and source grounding

**Purpose:** build the factual and external-alignment substrate before competency drafting.

**Rule checks**
- Retrieve and rank authoritative benchmarks by domain: O*NET, ESCO, SFIA, NICE, MITRE AI maturity, AGROVOC, ASABE, or family-specific sources where applicable.
- Require exact source references for factual, regulatory, tool, method, system, standard, analysis, or deliverable claims.
- Mark unsupported claims as `NO_SOURCE_FOUND` rather than inventing support.

**QA and evidence outputs**
- retrieval manifest
- external benchmark crosswalk
- unsupported span register

**Multi-lens action**
- Domain SME reviews weak or missing source support for high-impact competencies before drafting continues.

### Phase 3 — Competency mapping, domain clustering, and boundary pre-screen

**Purpose:** map responsibilities into a parsimonious candidate competency set.

**Rule checks**
- Map Technical and Mixed EFs to candidate competencies with traceable contribution level.
- Cluster related EFs and detect orphan domains.
- Pre-screen boundary adjacency against V&B and Common Competency language.
- Begin parsimony analysis before titles and definitions are drafted.

**QA and evidence outputs**
- EF-to-competency trace matrix
- orphan-domain report
- boundary pre-screen report
- initial parsimony candidate set

**Multi-lens action**
- Technical lens confirms that clusters represent one technical construct rather than bundled domains.

### Phase 3C — Title/definition uniqueness and technical-referent gate

**Purpose:** enforce AS-1 and AS-2 before indicators are built on weak constructs.

**Rule checks**
- Title is 3-6 words and names one technical construct.
- Title is distinct from V&B/Common names and other same-specialization titles.
- Definition is one sentence, 15-25 words, verb-led, and includes a concrete technical referent.
- Definition does not share the same primary verb or key noun phrase with another definition in the specialization.

**QA and evidence outputs**
- title uniqueness report
- definition technicality report
- same-keyword and shared-vocabulary findings

**Multi-lens action**
- Boundary lens reviews any title/definition near Common or V&B territory.

### Phase 4 — Draft competency and indicator generation

**Purpose:** generate content under structure, not free-form drafting.

**Rule checks**
- Enforce schema-constrained output for competencies, levels, indicators, anchors, and traces.
- Generate 3-5 indicators per level only as justified by domain coverage needs.
- Require every indicator to lead with an action verb and anchor to a concrete tool, method, artifact, system, standard, regulator, analysis, or deliverable.

**QA and evidence outputs**
- draft competency artifact
- per-indicator anchor matrix
- indicator count rationale when a level uses 5 indicators

**Multi-lens action**
- SME lens receives early flags for indicators with weak observability or ambiguous technical referents.

### Phase 4 QA — Indicator, exemplar, readability, and level-quality checks

**Purpose:** catch first-draft quality defects before coverage and count decisions.

**Rule checks**
- Detect redundant indicators within and across levels.
- Confirm L1-L4 autonomy, complexity, scope, and cognitive progression.
- Confirm L4 indicators can be performed by a principal-level IC without direct reports.
- Flag exemplar overuse or closed-set examples.
- Run readability tiers and flag only when two or more metrics exceed the target.

**QA and evidence outputs**
- level-progression report
- L4 principal-IC check
- exemplar-use report
- readability report
- monotonicity proxy report using Bloom/readability/specificity checks

**Multi-lens action**
- Learning/assessment lens reviews level monotonicity and observability issues.

### Phase 4.5 — Coverage, parsimony, beyond-6, and patch-only edit checks

**Purpose:** enforce the v3.7 AS-7 count model and structural no-drift controls.

**Rule checks**
- Select the smallest competency set that clears at least 90% Technical/Mixed EF coverage per specialization.
- Recommended range is 4-6 competencies per JD; do not pad to 6.
- Below-4 sets are flagged to the decision owner during development.
- Competencies 7 and 8 require separate Beyond-6 Rationale Records.
- No pooled beyond-6 rationale is allowed.
- 9+ routes to governance and cannot proceed as standard workflow.
- Anti-stacking check fails beyond-6 candidates with substantial overlap.
- Edits to canonical content are accepted only as JSON Patch or text-editor-style patch operations with parent hash match.

**QA and evidence outputs**
- coverage analysis
- parsimony selection report
- Beyond-6 Rationale Records
- proportional overlap report under GC-8
- patch verification report
- CTIC defense-in-depth report

**Multi-lens action**
- Decision owner approves below-4 flags and each beyond-6 record.
- SME or coverage evidence must support each beyond-6 addition independently.

### Phase 4.75 — Evaluator-optimizer judge, confidence, verification, and abstention

**Purpose:** improve first-iteration quality before human review.

**Rule checks**
- Judge scores the draft against active gates and emits critique before verdict.
- Judge returns calibrated confidence for every model-judgeable gate.
- Low confidence returns `ABSTAIN`, not pass/fail.
- Unsupported factual or regulatory spans route to `NO_SOURCE_FOUND` and human review.
- Up to three refinement passes are allowed; unresolved failures escalate.

**QA and evidence outputs**
- `judge_evaluation_report`
- confidence and abstention log
- verification-question report
- refinement history

**Multi-lens action**
- Human reviewers receive only unresolved failures, abstentions, unsupported claims, and high-risk items rather than the whole draft uniformly.

### Phase 5 — Multi-lens human review and frame-of-reference calibration

**Purpose:** use human expertise where judgment is required and calibrate reviewers before scoring.

**Rule checks**
- Reviewers complete frame-of-reference calibration with gold-standard examples before live scoring.
- Every indicator receives relevance, clarity, observability, and level-placement ratings.
- Discussion items are captured as structured evidence, not free-form side notes.

**QA and evidence outputs**
- HITL Workbook
- reviewer calibration record
- SME rating dataset
- contested-item register

**Multi-lens action**
- At minimum, technical/domain, learning/assessment, and boundary/governance lenses review the package.
- GC-16 focuses effort on low-agreement, borderline, high-disagreement, weak-slice, and beyond-6 items.

### Phase 5.5 — Boundary audit and Common/V&B technical-extension clearance

**Purpose:** ensure technical competencies do not restate V&B or Common Competencies.

**Rule checks**
- Boundary-adjacent competencies must explicitly name the Common Competency being cleared.
- Technical-extension test must show what technical object, method, system, standard, artifact, or regulator makes the competency technical.
- A boundary-adjacent competency naming no cleared Common Competency fails.

**QA and evidence outputs**
- boundary clearance record
- Common/V&B adjacency log
- remediation actions

**Multi-lens action**
- Boundary/governance lens signs off before quantitative validation promotion.

### Phase 6 — Quantitative validation, slice reporting, and revision-delta evidence

**Purpose:** convert expert review into psychometric and audit evidence.

**Rule checks**
- Compute Gwet's AC1/AC2 and Krippendorff ordinal alpha for agreement and level placement.
- Compute I-CVI, S-CVI/Ave, modified kappa, Aiken's V, and CVR where rating data support them.
- Report slices by specialization, band where bands differ materially, and IC/manager category where applicable.
- Identify worst slice and require justification for weak slices.
- Test revision improvement using paired bootstrap delta or appropriate paired alternatives.
- Label non-improving changes as parity rather than improvement.

**QA and evidence outputs**
- agreement report
- content-validity report
- AS-12 slice report
- AS-13 revision-delta report
- weak-slice justification log

**Multi-lens action**
- Panel resolves weak slices, parity revisions, or low-agreement items before release packaging.

### Phase 7 — Release evidence pack and Competency Release Card

**Purpose:** make release readiness reviewable in one carded evidence package.

**Rule checks**
- Release Card includes intended use, out-of-scope uses, evaluation summary, slice summary, known limitations, provenance, stewardship, and approvals.
- Beyond-6 records surface in HITL Workbook, Executive Decision Brief, Coverage Analysis, and Release Card.
- Open Items and grandfathered non-conformances are recorded rather than silently normalized.

**QA and evidence outputs**
- Competency Release Card
- Executive Decision Brief
- Coverage Analysis
- Open Items Register entries

**Multi-lens action**
- Decision owner, SME lead, and governance/boundary reviewer approve release evidence.

### Phase 8 — Closeout, attestation, library update, and governance registers

**Purpose:** make the run reproducible and auditable.

**Rule checks**
- Record prompt version, model snapshot, seed where applicable, input hash, output hash, artifact hash, gate verdicts, and approvals.
- Update Decision Registry, Approval Ledger, Change Log, and Library Master.
- Ensure CTIC and patch records align with final artifacts.

**QA and evidence outputs**
- run attestation
- Change Log
- Decision Registry updates
- Approval Ledger updates
- Library Master update

**Multi-lens action**
- Governance owner confirms evidence completeness before lock.

### Phase 9 — Stewardship loop, refresh triggers, incidents, and R-cycle routing

**Purpose:** convert FINAL content into a managed lifecycle asset.

**Rule checks**
- Assign refresh owner, reassessment cadence, and triggers.
- Triggers include material JD/job-architecture changes, standards/regulatory updates, accrued SME feedback threshold, adverse-impact or DIF signals where usage data exist, and source-authority changes.
- Fired triggers route to WR-1 modification routing and increment the R-cycle; they never silently edit locked content.

**QA and evidence outputs**
- stewardship register
- refresh-trigger log
- incident and feedback log
- R-cycle routing record

**Multi-lens action**
- Refresh owner triages triggers with domain, boundary/governance, and assessment lenses as required by risk tier.

## 6. Revised gate architecture

| Gate | Name | Applies when | Pass evidence |
|---|---|---|---|
| G0 | Intake risk tier | Every family/use case | Decision context, stakeholder exposure, regulatory exposure, gate scope |
| G1 | Input packet completeness | Every run | Required files present, schema-conformant, source authority classified |
| G2 | Coverage floor | Phase 3 onward | Assigned set covers at least 90% Technical/Mixed EFs per specialization |
| G3 | Title/definition technicality | Phase 3C | AS-1/AS-2 title and definition checks pass |
| G4 | Competency format | Draft and revisions | Title, definition, level labels, and content schema valid |
| G5 | Indicator count and quality | Draft and revisions | 3-5 indicators per level, anchored, observable, nonredundant |
| G6 | Boundary technical-extension | Boundary-adjacent content | Common/V&B clearance with named competency and technical referent |
| G7 | Level progression | Draft and revisions | L1-L4 progression and L4 principal-IC validity pass |
| G8 | Readability and exemplar discipline | Draft and revisions | Tiered readability and exemplar rules pass or are justified |
| G9 | AS-7 parsimony and beyond-6 | Phase 4.5 | 4-6 recommended, no padding, each 7/8 justified, 9+ governance route |
| G10 | Patch-only no-drift | Any canonical edit | Valid patch operation, parent hash match, CTIC defense-in-depth pass |
| G11 | Evaluator confidence and grounding | Phase 4.75 | Critique, confidence, verification, and abstention routing complete |
| G12 | Human review readiness | Before Phase 5 | HITL Workbook complete, contested items highlighted |
| G13 | Quantitative validity | Phase 6 | AC1/alpha/CVI/Aiken/CVR/slice/revision-delta evidence complete |
| G14 | Fairness, DIF, and language bias | Risk-tiered governed uses | Impact, DIF eligibility/results, and wording-bias evidence or N/A rationale |
| G15 | Release and stewardship | FINAL | Release Card, attestation, approvals, owner, cadence, and triggers complete |

## 7. Required output artifacts

| Artifact | Created by | Required content |
|---|---|---|
| Risk Tier Assessment | Phase 0 | Intended use, stakeholder exposure, regulatory exposure, gate scope |
| Input Packet Report | Phase 1 | Source presence, schema conformance, source authority, remediation list |
| EF Trace Matrix | Phase 3 | EF-to-competency mapping and contribution level |
| Title/Definition Technicality Report | Phase 3C | AS-1/AS-2 pass/fail and remediation findings |
| Indicator Anchor Matrix | Phase 4 | Per-indicator concrete referent and action verb |
| Readability and Level Progression Report | Phase 4 QA | FKGL tier checks, Bloom/readability/specificity progression, L4 IC validity |
| Coverage and Parsimony Report | Phase 4.5 | 90% coverage, smallest set, below-4 flags, anti-padding evidence |
| Beyond-6 Rationale Record | Phase 4.5 | Competency ID, single basis, evidence ID, marginal coverage, approver, date |
| Patch Verification and CTIC Report | Phase 4.5/6 | Parent hash, patch operations, drift result |
| Judge Evaluation Report | Phase 4.75 | Critique, confidence, abstentions, verification questions, refinement history |
| HITL Workbook | Phase 5 | Multi-lens ratings, contested items, beyond-6 records, reviewer calibration |
| Boundary Clearance Record | Phase 5.5 | Common/V&B adjacency and technical-extension decisions |
| Quantitative Validation Report | Phase 6 | AC1/AC2, Krippendorff alpha, CVI, Aiken, CVR, slices, revision delta |
| Competency Release Card | Phase 7 | Intended use, evaluation, slices, limits, provenance, stewardship, approvals |
| Run Attestation | Phase 8 | Prompt/model/input/output/gate hash and approval evidence |
| Stewardship Register | Phase 9 | Owner, cadence, triggers, incidents, feedback, R-cycle routing |

## 8. Implementation workstreams

### Workstream A — v3.7/v3.8 schemas and state

1. Add `RiskTierAssessment`, `InputPacketCompleteness`, `TitleDefinitionCheck`, `IndicatorAnchorCheck`, `CoverageParsimonyReport`, `BeyondSixRationaleRecord`, `PatchOperation`, `JudgeDecision`, `HumanReviewRoute`, `SliceValidationSummary`, `RevisionImprovementEvidence`, `RunAttestation`, `StewardshipPlan`, and `CompetencyReleaseCard` schemas.
2. Extend `ArtifactRegistry` with the required artifacts listed above.
3. Preserve load compatibility for grandfathered FINAL families and in-flight families that enter AS-7 at their next R-cycle.

### Workstream B — content-rule enforcement

1. Update validators from fixed v3.1 assumptions to v3.7 rules: 3-5 indicators per level and AS-7 4-6 recommended range with 8 hard ceiling.
2. Add parsimony selection logic and below-4 decision-owner flags.
3. Add per-competency beyond-6 rationale validation.
4. Add anti-stacking overlap checks for beyond-6 additions.
5. Update README, reference docs, tests, and templates to remove obsolete hard-6 language where the v3.7 plan is being implemented.

### Workstream C — statistical validation

1. Implement Gwet AC1/AC2, Krippendorff ordinal alpha, Brennan-Prediger, and ICC where continuous ratings are used.
2. Implement I-CVI, S-CVI/Ave, modified kappa, Aiken's V with confidence intervals, and Lawshe CVR.
3. Implement AS-12 slice reporting by specialization, band, and IC/manager type.
4. Implement AS-13 paired revision-delta evidence.
5. Add monotonicity checks using Bloom classification, readability/specificity proxies, and later empirical Mokken/Samejima methods when usage data exist.

### Workstream D — generation, grounding, and no-drift controls

1. Replace full-document rewrite steps with patch-only operations for canonical content.
2. Require parent artifact hashes and reject mismatched patches.
3. Add hybrid retrieval, source support checks, and `NO_SOURCE_FOUND` routing.
4. Add semantic overlap checks using embeddings and cross-encoder reranking.
5. Retain CTIC as a count-agnostic defense-in-depth check.

### Workstream E — evaluator, QA, and eval harness

1. Build Phase 4.75 evaluator-optimizer with critique-before-score behavior.
2. Calibrate judge confidence and route low-confidence results to human review.
3. Add golden-dataset evals and unit assertions for every gate.
4. Add prompt/model version recording and run attestations.
5. Add trace metadata for phase, gate, prompt, model, cost, latency, and guardrail outcomes.

### Workstream F — multi-lens review and governance

1. Add frame-of-reference calibration artifacts for reviewers.
2. Implement GC-16 targeted review queues for low-agreement, borderline, weak-slice, boundary-adjacent, and beyond-6 items.
3. Add risk-tiered fairness, adverse-impact, DIF, and language-bias gates.
4. Add Phase 9 stewardship register and refresh-trigger routing.
5. Ensure five FINAL families remain grandfathered and non-conformances route to the Open Items Register.

### Workstream G — ChatGPT Agents, GitHub connector, and skill packaging

1. Add a TCB skill package for ChatGPT Agents usage through GitHub connector access.
2. Document repository paths, branch workflow, input packet locations, output artifact paths, and PR expectations.
3. Provide agent scripts that can run without hidden platform dependencies.
4. Keep Claude Code, ChatGPT Agents, and M365 publication flows aligned to the same schemas and evidence artifacts.
5. Add MCP connector inventory as the future abstraction for source authorities and artifact stores.

## 9. Definition of done

The updated TCB build is ready when:

1. Every run begins with risk-tier assessment and input-packet completeness.
2. The operative v3.7 content rules are enforced in the phases listed above.
3. Competency count follows AS-7: recommended 4-6, parsimony first, each 7/8 independently justified, 9+ governance route.
4. Every indicator is anchored, observable, level-appropriate, and nonredundant.
5. Canonical edits are patch-only and hash-verified, with CTIC retained as defense-in-depth.
6. Multi-lens reviewers receive calibrated review instructions and targeted contested-item queues.
7. Quantitative validation produces agreement, content-validity, slice, and revision-delta evidence.
8. Selection, promotion, succession, or other high-risk uses cannot bypass risk-tiered fairness, DIF eligibility, language-bias, and human oversight controls.
9. Every FINAL package includes a Competency Release Card, release evidence, beyond-6 records where applicable, approvals, limitations, and Phase 9 stewardship triggers.
10. ChatGPT Agents can use GitHub connector instructions to inspect inputs, run or review the agent scripts, and write evidence artifacts to a branch using the same contracts as Claude Code.
