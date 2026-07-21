---
name: selection-method-advisor
description: >
  Recommend the optimal selection-method mix (assessment battery) for a role and
  justify it with current operational-validity evidence and adverse-impact
  trade-offs. Use this skill whenever the user asks "which assessment should I
  use," "what selection method," "what predicts job performance," "validity of
  [method]," "should we use a cognitive/GMA test," "best predictor," "design an
  assessment battery," "compare selection methods," "structured interview vs
  test," "incremental validity," "what's the most valid way to hire for X," "how
  should we screen candidates," "build a hiring process," or "which tools for
  selection." Also trigger when someone proposes a single tool (e.g. "let's just
  add an IQ test") and the choice should be evidence-based. Defaults to Sackett
  et al. (2022) operational validities — never the outdated Schmidt & Hunter
  (1998) numbers. Produces a Word recommendation memo and an Excel method-
  comparison table.
---

# Selection Method Advisor

Recommend a defensible selection-method mix for a role and document why, using
the **current** operational-validity evidence and explicit adverse-impact
trade-offs. Output a **Word recommendation memo** and an **Excel method-
comparison table**.

## Why This Skill Exists

Selection decisions are where validity turns into dollars and into legal
exposure. The field's canonical validity numbers changed in 2022: Sackett,
Zhang, Berry & Lievens showed that prior meta-analyses had over-corrected for
range restriction, cutting operational validities by roughly .10–.20 and
**re-ordering the hierarchy** — structured interviews (.42) now sit above general
mental ability (.31). Most HR materials still cite the old Schmidt & Hunter
(1998) figures (GMA .51, interview .51). A recommendation built on stale numbers
over-weights cognitive testing, inherits avoidable adverse impact, and looks
unrigorous under scrutiny. This skill encodes the current evidence and forces the
adverse-impact conversation that method choice always implies.

## Mandatory Co-Skills

| Co-Skill | When | Why |
|---|---|---|
| `docx/SKILL.md` | Every recommendation | Word memo is a required output |
| `xlsx/SKILL.md` | Every recommendation | Excel comparison table is a required output |
| `cargill-branding/SKILL.md` | Cargill-bound output | Apply Cargill identity |
| `multi-lens-review/SKILL.md` | High-stakes / executive roles | Pressure-test the recommendation from multiple stakeholder lenses |

## Required Inputs

Ask for anything missing before recommending.

| Input | Required | Notes |
|---|---|---|
| Role / job family & level | Yes | Drives KSAO targets and cost tolerance |
| Analysis of work / KSAOs | Strongly | The validity anchor; if absent, recommend running `job-analysis-facilitator` first |
| Volume & stakes | Yes | Applicants/year, criticality — shapes cost/automation trade-offs |
| Constraints | Optional | Time-to-fill, candidate experience, budget, remote/in-person, legal jurisdiction |
| Diversity goals | Optional | Affects weighting toward lower-adverse-impact methods |

## Process

### Step 1 — Anchor on the work
Tie the recommendation to the role's KSAOs from an analysis of work. Without one,
say so and recommend `job-analysis-facilitator` first — validity claims require a
work-analysis foundation (SIOP Principles, 5th ed.).

### Step 2 — Map KSAOs to candidate methods
For each required-at-entry KSAO, list the methods that measure it well. Pull
operational validities and measurement targets from
`references/validity-coefficients.md` (the single canonical table — Sackett et
al. 2022 as default).

### Step 3 — Assemble a battery, not a single tool
Selection is usually a *composite*. Choose 2–4 complementary methods that cover
the KSAO set with the best **incremental validity** and acceptable adverse
impact. Use `references/battery-design.md` for combination logic, sequencing
(cheap/high-volume screens first), and the incremental-validity rules.

### Step 4 — Surface the adverse-impact trade-off
State each method's typical adverse-impact profile (e.g., cognitive-heavy
batteries carry larger subgroup differences; structured interviews and work
samples generally less). If the user has diversity goals, weight accordingly and
flag where a small validity trade-off buys a large adverse-impact reduction.
Recommend an `adverse-impact-analyzer` pass once real data exists.

### Step 5 — Write the memo and table
Produce the deliverables per `references/battery-design.md`. Cite both authority
layers and the Sackett (2022) source. Append the disclaimer.

## References

- `references/validity-coefficients.md` — the canonical operational-validity
  table (Sackett 2022 default; Schmidt & Hunter 1998 in a labeled "do not mix"
  sidebar), what each method measures, reliability and adverse-impact notes.
- `references/battery-design.md` — incremental validity, sequencing, composite
  logic, and the exact memo/table structure.

## Deliverables

1. **Word — Selection Recommendation Memo.** Role & KSAO anchor, recommended
   battery with rationale, validity evidence (cited), adverse-impact trade-off,
   sequencing, implementation notes, disclaimer.
2. **Excel — Method Comparison.** One row per candidate method: KSAOs measured,
   operational validity (Sackett 2022), reliability, relative cost,
   candidate-experience load, adverse-impact profile, recommend/hold.

## Standard Disclaimer

> Draft recommendation for professional review. Operational validity figures are
> meta-analytic estimates (Sackett et al., 2022) and must be interpreted for this
> context by a qualified I-O psychologist. Local validation and an adverse-impact
> analysis on real selection data are required before operational use. Re-verify
> citations against the source article and the SIOP Principles (5th ed.).

## Hard rules

- **Default to Sackett et al. (2022).** Never present Schmidt & Hunter (1998)
  GMA .51 / interview .51 as current; if shown, label them legacy and explain the
  range-restriction over-correction.
- **Recommend composites, not single predictors**, unless volume/stakes truly
  warrant one screen.
- **Always name the adverse-impact trade-off** — method choice is never
  validity-only.
