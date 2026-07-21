---
name: assessment-center-designer
description: >
  Design a defensible assessment center (AC) or development center built on a
  dimension × exercise matrix that meets the International Task Force essential
  elements. Use this skill when the user asks to "design an assessment center,"
  "AC design," "build a dimension by exercise matrix," "create simulation
  exercises," "in-basket exercise," "role-play exercise," "leaderless group
  discussion," "case analysis exercise," "assessor training," "behavioral
  simulation," "develop a development center," "design a selection day," "build an
  exercise matrix," "assessor scoring guide," or "how do we run an assessment
  center." Also trigger when someone calls a single interview or one untrained
  rater an "assessment center" (it isn't — this skill enforces the standard).
  Produces an Excel dimension × exercise matrix and a Word AC design document plus
  an assessor-training outline.
---

# Assessment Center Designer

Design an assessment center that can legitimately be called one. Output an
**Excel dimension × exercise matrix**, a **Word AC design document**, and an
**assessor-training outline**.

## Why This Skill Exists

"Assessment center" is a term of art with a published standard — the *Guidelines
and Ethical Considerations for Assessment Center Operations* (6th ed., 2015;
*Journal of Management* 41(4):1244–1273). Calling a single interview or a lone
untrained rater an "assessment center" is both inaccurate and indefensible. A
real AC observes multiple behavioral dimensions across **multiple simulation
exercises**, scored by **multiple trained assessors**, integrated through a
defined process. This skill builds that structure from the job's competencies and
refuses to mislabel anything that doesn't meet the essential elements.

## Mandatory Co-Skills

| Co-Skill | When | Why |
|---|---|---|
| `xlsx/SKILL.md` | Every design | The dimension × exercise matrix is a required output |
| `docx/SKILL.md` | Every design | Design doc and assessor outline are required outputs |
| `cargill-branding/SKILL.md` | Cargill-bound output | Apply Cargill identity |

## Required Inputs

Ask for anything missing before designing.

| Input | Required | Notes |
|---|---|---|
| Target role / level | Yes | Sets dimension difficulty and exercise realism |
| Dimensions (competencies) | Yes | 4–7 behaviorally-defined dimensions; from a competency model / analysis of work |
| Purpose | Yes | Selection vs development (changes feedback design and stakes) |
| Constraints | Optional | Time (half/full day), # candidates, # assessors, remote/in-person |
| Existing materials | Optional | Prior exercises, competency definitions |

If dimensions are vague or trait-like, refine them into observable behavioral
constructs first (or recommend `job-analysis-facilitator` / the TCB builder).

## Process

### Step 1 — Lock the dimensions
4–7 behaviorally-defined dimensions, each with observable indicators. Too many
dimensions overload assessors and degrade reliability; cluster or cut.

### Step 2 — Select exercises
Choose ≥2 simulation exercises (the minimum for a true AC; 3–4 typical) from
`references/exercise-library.md`, matched to the dimensions. Vary the stimulus
type (individual vs group, written vs interactive) so each dimension is observed
in more than one context.

### Step 3 — Build the dimension × exercise matrix
Cross dimensions (rows) against exercises (columns). Mark which dimensions each
exercise assesses. Enforce the rules in `references/essential-elements.md`: every
dimension observed in **≥2 exercises**; every exercise targets a manageable
number of dimensions (≈3–4, not all of them).

### Step 4 — Write assessor scoring guides
For each dimension × exercise cell that is "on," provide behavioral indicators
and a behaviorally-anchored rating scale (BARS). See
`references/exercise-library.md` for anchor-writing patterns.

### Step 5 — Define data integration & assessor training
Specify the integration method — **consensus discussion OR a validated
statistical model** (name which) — and an assessor-training plan (frame of
reference, behavior recording, rotation so no assessor sees one candidate twice
in the same exercise). See `references/essential-elements.md`.

### Step 6 — Generate deliverables and run the guardrail check
Before finalizing, confirm the design clears every essential element. If it does
not (e.g., only one exercise, untrained raters), **do not label it an assessment
center** — relabel it accurately and tell the user what's missing.

## References

- `references/essential-elements.md` — the 10 essential elements, the matrix
  rules, integration options, assessor-training requirements, and the
  guardrail checklist. Read before Steps 3–6.
- `references/exercise-library.md` — in-basket, role-play, LGD, case analysis,
  presentation, fact-find; what each measures well; BARS anchor patterns.

## Deliverables

1. **Excel — Dimension × Exercise Matrix.** Rows = dimensions, columns =
   exercises; cells mark coverage; per-dimension and per-exercise counts with
   rule-violation flags; a `Schedule` tab (candidate/assessor rotation).
2. **Word — AC Design Document.** Purpose, dimensions (behaviorally defined),
   exercises, the matrix, scoring guides/BARS, integration method, schedule,
   validity/defensibility statement, disclaimer.
3. **Word — Assessor Training Outline.** Frame-of-reference training, behavior
   recording (ORCE: Observe–Record–Classify–Evaluate), calibration, ethics.

## Standard Disclaimer

> Draft assessment-center design for professional review. An AC used for
> employment decisions requires trained assessors, piloting, and validity
> evidence appropriate to its use, reviewed by a qualified I-O psychologist and
> legal counsel. This document is a design, not a validated instrument.

## Guardrail — the non-negotiables

A design may be called an **assessment center** only if it has: ≥2 simulation
exercises; ≥2 trained assessors; behaviorally-defined dimensions linked to
exercises (the matrix); systematic behavior recording; and a defined integration
method (consensus or validated statistical). If any is missing, relabel it (e.g.
"structured simulation," "single-exercise screen") and state the gap.
