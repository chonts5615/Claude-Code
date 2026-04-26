---
name: structured-interview-generator
description: Generate complete structured Behavioral Event Interview (BEI) guides, interview rubrics, STAR-L question banks, behaviorally anchored rating scales (BARS), and interviewer scorecards from competency input. Use when asked to build an interview guide, generate behavioral questions, create a structured interview for a role, write BEI questions, produce an interview rubric, draft STAR questions, build an interview scorecard, create BARS for interviews, author an interviewer guide, design a selection interview, construct a promotion interview, generate behavioral event interview content, create interview question banks, or produce assessment interview materials. Produces Excel workbooks and Word interviewer guides as deliverables.
---

# Structured Interview Generator

Generate psychometrically defensible Behavioral Event Interview guides from competency definitions. Produce two deliverables: an Excel workbook (Interview Content + Coverage Analysis) and a Word interviewer guide with Cargill branding.

## Why This Skill Exists

Unstructured interviews predict job performance at roughly r = .20. Structured behavioral interviews with anchored rating scales reach r = .50+. The difference between these two numbers represents millions of dollars in hiring utility across a global enterprise. This skill enforces the methodological discipline that separates valid selection from expensive gut-feel.

---

## Step 1: Intake

Collect competency input from the user. Accept either format:

**Option A — Direct paste.** The user provides competency definitions inline. Each competency needs:
- Competency name
- Behavioral definition
- Level-scaled behavioral indicators for the target levels

**Option B — File reference.** The user points to a competency model file (.xlsx, .docx, .csv, or .json). Read the file and extract the competency architecture.

If the user provides competencies without level indicators, ask which levels to generate for. The standard Cargill levels are:

| Code | Level | Characteristic Scope |
|------|-------|---------------------|
| UR | University Recruiting | Academic projects, internships, near-term task execution |
| JL1 | Individual Contributor | Own work, 0-12 month horizon, defined problems |
| JL2 | Manager | Team of ICs, 1-2 year horizon, cross-functional coordination |
| JL3 | Senior Manager | Function or large program, 2-3 year horizon, systemic problems |
| JL4 | Director / VP / SM1 | Enterprise scope, 3-5+ year horizon, strategic ambiguity, portfolio trade-offs |

The critical dimension that shifts across levels is not difficulty but rather time horizon, scope of impact, stakeholder complexity, ambiguity tolerance, and trade-off sophistication. A JL1 "Collaboration" question asks about working with a teammate on a shared deliverable. A JL4 "Collaboration" question asks about aligning competing executive priorities across business units to achieve a multi-year strategic outcome.

---

## Step 2: Load References

Load reference files from the `references/` directory as needed during generation:

- `references/question-stems.md` — 80+ question stem templates organized by competency category (leadership, collaboration, analytical thinking, etc.). Draw from these to ensure variety and avoid repetitive phrasing.
- `references/probe-patterns.md` — Follow-up probe patterns for three response scenarios: strong responses (depth probes), weak or vague responses (clarification probes), and evasive responses (redirect probes).
- `references/rubric-anchors.md` — Anchor-writing patterns with exemplar behavioral descriptions across performance levels. Use these patterns to write anchors that are observable, specific, and free of evaluative adjectives.
- `references/level-differentiation.md` — Detailed guidance on adapting the same competency construct across JL1 through JL4 and University Recruiting, with examples of how scope, complexity, and time horizon shift.

If a reference file does not exist yet, proceed with internal knowledge but note which files are missing so they can be created later.

---

## Step 3: Load Branding

Read the cargill-branding skill to apply Cargill brand identity to the Word document deliverable:

```
Read /mnt/.claude/skills/user/cargill-branding/SKILL.md
```

Apply the brand standards (Leaf Green #00843D, Big Caslon headings, Helvetica Now body text) to the Word interviewer guide cover page, headers, and section formatting. If the branding skill is unavailable, use Cargill Leaf Green (#00843D) as the primary accent color with clean sans-serif typography.

---

## Step 4: Generate Interview Content

For each competency at each target level, generate the following:

### 4a. Behavioral Event Questions (2-3 per competency per level)

Write questions in STAR-L format (Situation, Task, Action, Result, Lessons Learned). Each question stem asks the candidate to describe a specific past experience. The "L" component — Lessons Learned — distinguishes BEIs from standard STAR interviews by probing metacognition and self-awareness.

**Psychometric guardrails that protect validity:**

- Every question asks about actual past behavior, never hypothetical scenarios. Hypotheticals measure verbal reasoning and social desirability, not behavioral tendencies. A question like "What would you do if..." is not a behavioral question regardless of how it is framed.
- No leading questions. "Tell me about a time you successfully led a team through change" presupposes success and biases the response. Instead: "Tell me about a time you were responsible for leading a team through a significant change. Walk me through what happened."
- Every question traces to a specific behavioral indicator from the competency model. If a question cannot be linked to a defined indicator, it does not belong in the guide because it cannot be scored against the rubric.
- Review question language for cultural assumptions. Questions that assume Western-normative workplace structures (e.g., "Tell me about a time you pushed back on your manager") may disadvantage candidates from high power-distance cultures. Flag these and provide culturally neutral alternatives.

### 4b. Follow-Up Probes (2-3 per question)

Each question includes follow-up probes for three scenarios:

- **Depth probes** (candidate gives a strong initial response): Push for specificity on the Action and Result components. "What specifically was your role versus the team's role?" "What metrics changed as a result?"
- **Clarification probes** (candidate is vague or general): Redirect to concrete behavior. "Can you walk me through the specific steps you took?" "What did you personally do, as opposed to what the team did?"
- **Redirect probes** (candidate drifts to hypothetical or unrelated territory): Anchor back to the behavioral event. "That's helpful context — can you take me back to the specific situation and tell me what you actually did?"

### 4c. Scoring Rubric (1-5 scale with behavioral anchors)

Each question receives a behaviorally anchored rating scale. Anchors are required at levels 1, 3, and 5 at minimum. Levels 2 and 4 may be included when the behavioral distinction is clear.

**Anchor-writing principles:**

- Anchors describe observable behavior, not inferred traits. "Identified three stakeholder groups and scheduled alignment meetings within the first week" rather than "Showed strong stakeholder management skills."
- Anchors are calibrated to the target level. A "5" for a JL1 candidate looks different from a "5" for a JL4 candidate because the expected scope of impact differs.
- No bare numeric scales. A rubric that says "1 = Poor, 3 = Average, 5 = Excellent" provides zero inter-rater reliability because assessors will define those words differently. Every number gets a behavioral description.

---

## Step 5: Coverage Analysis

### 5a. Check for External Coverage-Audit Skill

```
Check if /mnt/.claude/skills/user/coverage-audit/SKILL.md exists
```

If the coverage-audit skill is installed, read it and follow its protocol for validating the generated interview content. Pass the completed competency x level x question matrix to the audit skill and incorporate its findings.

### 5b. Internal Coverage Analysis (fallback)

If no external coverage-audit skill exists, run an internal analysis:

**Competency x Level Coverage Matrix.** Build a matrix with competencies as rows and levels as columns. Each cell shows the number of questions generated. Flag:
- **Coverage gaps**: Any cell with zero questions (a competency-level combination with no assessment coverage).
- **Thin coverage**: Any cell with only one question (insufficient for reliability — a single question creates a single-point-of-failure in assessment).
- **Redundancy**: Questions across competencies that are semantically similar enough that they assess the same underlying construct. Redundant questions waste interview time without adding incremental validity.

**Behavioral Indicator Traceability.** Verify that every behavioral indicator in the source competency model is assessed by at least one question. Unassessed indicators represent blind spots in the interview protocol.

**Time Estimation.** Estimate total interview duration based on 5-7 minutes per behavioral question (including probes and note-taking). Flag if the total exceeds 60 minutes for a single interviewer session, because interviewer fatigue degrades rating quality after approximately one hour.

---

## Step 6: Produce Deliverables

Generate two files. Use the xlsx and docx skills for file creation.

### 6a. Excel Workbook (.xlsx)

**Tab 1: "Interview Content"**

| Column | Content |
|--------|---------|
| Competency | Competency name |
| Level | Target level (UR, JL1, JL2, JL3, JL4) |
| Question# | Sequential number within competency-level |
| Stem | Full behavioral question text |
| Probe1 | First follow-up probe |
| Probe2 | Second follow-up probe |
| Probe3 | Third follow-up probe (if applicable) |
| Anchor_1 | Behavioral anchor for rating = 1 |
| Anchor_3 | Behavioral anchor for rating = 3 |
| Anchor_5 | Behavioral anchor for rating = 5 |
| Notes | Competency indicator traced, cultural sensitivity flags, administration notes |

Apply Cargill Leaf Green (#00843D) to the header row with white text. Freeze the top row. Auto-size columns for readability.

**Tab 2: "Coverage Analysis"**

Row headers: competency names. Column headers: levels (UR, JL1, JL2, JL3, JL4). Cell values: question count. Apply conditional formatting:
- Green fill (#00843D at 20% opacity): 2-3 questions (adequate coverage)
- Yellow fill: 1 question (thin coverage)
- Red fill: 0 questions (gap)

Below the matrix, include:
- Total estimated interview duration per level
- List of unassessed behavioral indicators (if any)
- Redundancy flags with the specific question pairs identified

### 6b. Word Document (.docx) — Interviewer Guide

Structure the document as follows:

**Cover Page.** Title: "[Role/Program Name] Structured Interview Guide." Subtitle: "Behavioral Event Interview Protocol." Cargill logo placement area. Date and version number. Confidentiality notice: "For authorized assessors only. Do not distribute to candidates."

**Section 1: Interviewer Instructions.**
- Overview of the STAR-L methodology and why behavioral interviewing works (candidates' past behavior in comparable situations is the strongest available predictor of future behavior in the target role).
- Rating calibration protocol: before the interview, assessors review the anchors. After the interview, assessors score independently before any group discussion to prevent anchoring bias.
- Note-taking protocol: record verbatim behavioral examples, not impressions or evaluative judgments. Notes should capture what the candidate did, not whether the interviewer thinks it was good.
- Standardized administration: ask every candidate the same questions in the same order. Probes may vary based on responses, but stems are fixed. This standardization is what makes the interview legally defensible.

**Section 2: Interview Content.** One sub-section per competency. Each sub-section contains:
- Competency name and behavioral definition
- Target level and relevant behavioral indicators
- Questions with probes (formatted for easy reading during a live interview)
- Scoring rubric with behavioral anchors displayed in a table

**Section 3: Appendix — Quick-Reference Scorecard.** A single-page summary table with all competencies, question numbers, and blank rating cells (1-5) for the interviewer to record scores during or immediately after the interview.

Apply Cargill branding throughout: Leaf Green accent color on headings and table headers, appropriate heading fonts, professional formatting.

---

## Psychometric Integrity Checks (applied throughout)

These are not optional enhancements. They protect the organization from adverse impact liability and ensure the interview protocol measures what it claims to measure.

- **Job relevance.** Every question traces to a behavioral indicator from a validated competency model. If the user has not provided evidence of job analysis, note that the interview content should be validated against job analysis data before operational deployment.
- **Standardization.** The guide enforces identical questions for all candidates at a given level. Deviation from the script degrades validity and creates legal exposure.
- **Adverse impact language review.** Flag questions containing culturally loaded assumptions, idioms that do not translate, or scenarios that presuppose specific organizational structures. Provide alternative phrasing.
- **No unanchored scales.** Every numeric rating has a behavioral description. This is the single most important factor in inter-rater reliability.
- **Construct coverage.** The coverage analysis ensures the interview samples broadly across the competency model rather than over-indexing on one or two constructs.

---

## Output Naming Convention

Name files using this pattern:
- `{Role_or_Program}_BEI_Guide_{YYYY-MM-DD}.xlsx`
- `{Role_or_Program}_Interviewer_Guide_{YYYY-MM-DD}.docx`

If the user does not specify a role or program name, ask for one before generating files. The name appears on the cover page and in file metadata.