---
name: job-analysis-facilitator
description: >
  Plan, run, and document an analysis of work (job analysis) — the SIOP-required
  foundation under every competency model, selection tool, and career level. Use
  this skill whenever the user wants to "do a job analysis," "analysis of work,"
  "task analysis," "work analysis," "KSAO analysis," "identify essential
  functions," "build a task inventory," "rate task criticality," "link tasks to
  competencies," "establish content validity," "define what this job actually
  does," "SME workshop for a role," "job analysis questionnaire," "task-KSAO
  matrix," "what knowledge skills and abilities does this role need," "document
  job requirements for selection," or "create the foundation for a competency
  model / interview / assessment." Also trigger when the user is about to build a
  selection tool, competency model, or career level and has no documented work
  analysis to anchor it. Produces an Excel task × KSAO linkage matrix and a Word
  analysis-of-work report ready to feed competency modeling, selection design,
  and adverse-impact defense.
---

# Job Analysis Facilitator

Run a defensible analysis of work and turn it into two artifacts: an **Excel
task × KSAO linkage matrix** (with criticality ratings) and a **Word
analysis-of-work report**. These are the evidentiary foundation that makes every
downstream competency model, interview, assessment, and career level
content-valid and legally defensible.

## Why This Skill Exists

Under the SIOP *Principles* (5th ed., 2018) and the *Uniform Guidelines* (29 CFR
Part 1607), a selection procedure's content validity rests on a documented
analysis of work that defines the tasks performed and the knowledge, skills,
abilities, and other characteristics (KSAOs) required **at job entry**. Skip it
and everything built on top — the competency model, the interview, the
assessment battery — inherits a content-validity gap that surfaces precisely
when a selection decision is challenged. This skill enforces the discipline:
sample the work systematically, rate it, and link every required KSAO back to an
observable task. It is the *front end* of the talent system; it does not
re-author competency models (that is the TCB v3.1 builder's job) — it produces
the inputs they consume.

## Mandatory Co-Skills

Read and apply these before producing deliverables:

| Co-Skill | When | Why |
|---|---|---|
| `xlsx/SKILL.md` | Every analysis (Excel matrix is required output) | Proper workbook construction, conditional formatting, frozen headers |
| `docx/SKILL.md` | Every analysis (Word report is required output) | Proper report construction |
| `cargill-branding/SKILL.md` | Cargill-bound output | Apply Leaf Green `#00843D` / White Green `#F5F9ED`, Arial body / Georgia H1 |

## Required Inputs

Collect these; **ask** for anything missing before generating.

| Input | Required | Notes |
|---|---|---|
| Target role / job title | Yes | One role per analysis (or a tight job family) |
| Job level | Yes | Use the role's career level; affects KSAO "at entry" scope |
| Source material | Strongly | JD, prior task list, O*NET code, SOPs, performance docs — anything observable |
| SME access | Recommended | Names/roles of subject-matter experts; how ratings will be collected |
| Method preference | Optional | Defaults below if unspecified |
| Purpose | Yes | Selection, competency model, career leveling, restructuring — shapes emphasis |

If there is no source material and no SME access, proceed in **draft mode** from
role knowledge and O*NET, and label the output **UNVALIDATED — requires SME
confirmation**.

## Process

### Step 1 — Choose the method
Default to a **hybrid task-and-KSAO analysis**: a task-inventory approach to
capture *what is done*, plus a worker-oriented (KSAO) approach to capture *what
it takes*. Read `references/methodology.md` for when to weight one over the other
(routine/standardized work → task-heavy; judgment/knowledge work → KSAO-heavy).

### Step 2 — Build the task inventory
Write **task statements** in the standard grammar: *action verb + object +
context/tool + purpose*, one observable unit of work each (e.g. "Reconciles
intercompany balances in SAP each close cycle to ensure consolidated accuracy").
Aim for 20–40 task statements for a single role; cluster them into 4–8 duty
areas. See `references/methodology.md` for statement rules and anti-patterns.

### Step 3 — Rate task criticality
Have SMEs (or, in draft mode, your best estimate flagged as such) rate each task
on the standard scales: **Frequency**, **Importance/Criticality**, and
**Difficulty** (and optionally *time spent* and *consequence of error*). Compute
a composite task-criticality index per `references/methodology.md`. Essential
functions are the tasks that clear the importance threshold.

### Step 4 — Derive KSAOs
For each significant task, ask "what must a person know, be able to do, or be
like to perform this well at entry?" Write KSAO statements as observable,
verb-led requirements and classify each as **Knowledge / Skill / Ability /
Other characteristic**. Mark whether each is **required at entry** or
*developed on the job* — only at-entry KSAOs may anchor selection. See
`references/methodology.md` for the K/S/A/O definitions and writing rules.

### Step 5 — Build the task × KSAO linkage matrix
Cross every KSAO against every task. Each KSAO must link to **at least one** task
(no free-floating requirements — that is the classic content-validity failure).
Each essential task should map to at least one KSAO. Capture the linkage strength
and flag orphans in both directions.

### Step 6 — Generate the deliverables
Produce the Excel matrix and the Word report per
`references/deliverable-spec.md`. Append the standard disclaimer (below).

## References

- `references/methodology.md` — methods, task-statement grammar, criticality
  scales and composite formula, K/S/A/O definitions and writing rules, linkage
  and orphan rules, SME sampling and agreement guidance. Read before Step 1.
- `references/deliverable-spec.md` — exact Excel tab architecture and Word report
  structure. Read before Step 6.

## Deliverables

1. **Excel — Analysis of Work.** Tabs: `Task Inventory` (statements + criticality
   ratings + composite + essential flag), `KSAO Inventory` (classified, at-entry
   flag), `Task×KSAO Matrix` (linkage grid with orphan highlighting), `Summary`
   (essential functions, top KSAOs, method & SME notes). Cargill-branded,
   conditional formatting on criticality.
2. **Word — Analysis-of-Work Report.** Method, participants/SMEs, task inventory,
   KSAO requirements at entry, criticality results, content-validity statement
   linking KSAOs→tasks, and the disclaimer.

## Standard Disclaimer (append to every artifact)

> Draft analysis of work for professional review. Content-validity, selection,
> and classification decisions based on this analysis must be reviewed by a
> qualified I-O psychologist and, where used for employment decisions, legal
> counsel. Where ratings were not SME-validated, the artifact is labeled
> UNVALIDATED. Re-verify regulatory citations against 29 CFR Part 1607 and the
> SIOP Principles (5th ed.).

## What this skill does NOT do

- It does not author competency titles, definitions, or proficiency levels —
  that is the **TCB v3.1** builder (`tech-competency-agent/`). This skill hands
  it a validated task/KSAO foundation.
- It does not write interview questions (`structured-interview-generator`) or
  score coverage (`coverage-audit`). It produces the work analysis those skills
  assume already exists.
