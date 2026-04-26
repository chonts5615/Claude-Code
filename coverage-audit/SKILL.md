---
name: coverage-audit
description: >
  Audit the coverage between any two talent management artifacts — interview questions vs.
  behavioral indicators, competency models vs. essential functions, assessment batteries vs.
  leadership enablers, job analysis task statements vs. selection tool content, success
  profiles vs. 360 instruments, or any pairing where one artifact should systematically
  map to another. Use this skill whenever the user asks to "audit coverage," "check
  coverage," "coverage matrix," "map these to those," "what's missing," "gap analysis,"
  "check alignment between," "verify indicator coverage," "behavioral indicator coverage,"
  "are all competencies covered," "do these questions hit all the indicators," "what gaps
  exist," "content validity check," "crosswalk these," or uploads two artifacts and asks
  whether one adequately addresses the other. Also trigger when the user is building or
  reviewing interview guides, structured assessment protocols, competency-to-tool mappings,
  or any content validity exercise. Even if the user doesn't say "coverage" explicitly, use
  this skill whenever two HR/talent artifacts need systematic alignment verification. This
  skill produces a paired Excel workbook (coverage matrix with PASS/PARTIAL/GAP scoring)
  and Word executive summary as deliverables.
---

# Coverage Audit

Systematically evaluate whether Artifact A adequately covers the elements defined in Artifact B, producing a scored coverage matrix with PASS/PARTIAL/GAP verdicts, quantified coverage ratios, and a paired Excel + Word deliverable set ready for executive review or SME validation sessions.

## Why This Skill Exists

Coverage gaps are the silent killer of talent management systems. An interview guide that misses two of twelve behavioral indicators creates a psychometric blind spot that degrades criterion-related validity. A competency model that maps to only 60% of essential job functions fails the content validity standard required under the SIOP Principles and the Uniform Guidelines. A 360 instrument that omits an entire leadership enabler produces developmental feedback that systematically ignores a critical performance domain.

These gaps are rarely caught by casual review because the artifacts *look* comprehensive — long lists of questions, detailed competency definitions, multi-page assessment protocols. The problem is structural: without systematic cell-by-cell mapping, coverage failures hide in the volume. This skill forces the rigorous, exhaustive mapping that content validity demands.

## Mandatory Co-Skills

Read and apply these companion skills before producing any deliverables:

| Co-Skill | When to Read | Why |
|---|---|---|
| `xlsx/SKILL.md` | Every audit (Excel workbook is a required output) | Ensures proper workbook construction with formatting, conditional formatting, and formulas |
| `docx/SKILL.md` | Every audit (Word summary is a required output) | Ensures proper executive summary document construction |
| `cargill-branding/SKILL.md` | When output is destined for Cargill audiences | Apply Cargill visual identity to both deliverables |
| `multi-lens-review/SKILL.md` | When the artifacts being audited are Cargill talent documents | Apply the Multi-Persona Review Protocol to the audit findings |

Read the relevant co-skills BEFORE writing any code or creating any files.

## Input Requirements

The audit requires exactly two artifacts:

**Artifact A (the "Coverage Source")** — The artifact being evaluated for adequacy. Examples: an interview guide, a set of BEI probes, a 360 feedback instrument, an assessment battery configuration, a training curriculum, a job posting.

**Artifact B (the "Coverage Target")** — The authoritative reference that Artifact A should cover. Examples: a competency model with behavioral indicators, a list of essential job functions, a set of leadership enablers, a job analysis task inventory, a success profile.

The user may provide these as uploaded files (.docx, .xlsx, .pdf, .md, .txt), as pasted text in the conversation, or as references to documents accessible via connected platforms. If only one artifact is provided, ask the user for the second before proceeding.

## The Audit Process

### Step 1: Parse and Inventory Both Artifacts

Extract every discrete, scorable element from each artifact.

**From the Coverage Target (Artifact B)**, extract the atomic elements that require coverage. These are the rows of the coverage matrix. Depending on the artifact type:

- Competency model → Extract each behavioral indicator at each proficiency level
- Essential functions list → Extract each essential function or task statement
- Leadership enabler model → Extract each enabler and its sub-dimensions
- Success profile → Extract each competency, knowledge requirement, experience requirement, and personal attribute
- Job analysis inventory → Extract each task statement or KSA

**From the Coverage Source (Artifact A)**, extract every discrete content element that could provide coverage. These become the evidence citations in the matrix. Depending on the artifact type:

- Interview guide → Extract each question, probe, and follow-up
- Assessment battery → Extract each scale, subscale, or measurement dimension
- 360 instrument → Extract each item or item cluster
- Training curriculum → Extract each learning objective or module
- Job posting → Extract each requirement, responsibility, or qualification statement

Present the extracted inventories to the user for confirmation before scoring. The inventory step is where errors compound — a missed behavioral indicator or a misclassified question corrupts every downstream verdict.

### Step 2: Build the Coverage Matrix

Construct a matrix where:
- **Rows** = Every element from the Coverage Target (Artifact B)
- **Columns** = Identification metadata + verdict + evidence + coverage ratio fields

For each target element, systematically scan every source element and determine whether coverage exists. Read `references/methodology.md` for the formal scoring rules, threshold definitions, and ratio calculation methodology.

### Step 3: Score Each Cell

Apply the three-tier scoring rubric defined in `references/methodology.md`:

| Verdict | Symbol | Meaning |
|---|---|---|
| **PASS** | ✅ | The source artifact directly and substantively addresses this target element |
| **PARTIAL** | ⚠️ | The source artifact touches on this target element but incompletely — missing depth, scope, or specificity |
| **GAP** | ❌ | The source artifact does not address this target element at all |

Every verdict must include a **justification** — a brief explanation of why the element received that score, referencing the specific source content that provides (or fails to provide) coverage. Verdicts without justification are not defensible in SME validation sessions.

### Step 4: Calculate Coverage Ratios

Compute coverage ratios at multiple levels of aggregation as defined in `references/methodology.md`. At minimum:

- **Overall coverage ratio** — across the entire matrix
- **Category-level ratios** — grouped by competency, function area, or enabler domain
- **Verdict distribution** — count and percentage of PASS, PARTIAL, and GAP across the matrix

### Step 5: Generate the Deliverable Pair

Produce two files:

**Excel Workbook** — The primary analytical deliverable. Structure per `references/methodology.md` Tab Architecture section. Must include conditional formatting (green/yellow/red for PASS/PARTIAL/GAP), frozen header rows, auto-filters, and summary formulas.

**Word Executive Summary** — The decision-ready companion document. Structure per `references/methodology.md` Executive Summary Architecture section. Designed for the CHRO, VP of Talent Acquisition, or Lead I-O Psychologist to consume in under five minutes.

## Handling Ambiguous Coverage

Coverage judgments are inherently interpretive. These guidelines reduce subjectivity:

**Substantive vs. superficial coverage.** A question that uses the same keyword as a behavioral indicator does not automatically constitute coverage. The question must elicit behavioral evidence that would allow a trained assessor to rate the candidate on that indicator. "Tell me about a time you led a team" does not cover the indicator "Builds cross-functional coalitions to accelerate decision-making across P&L boundaries" — the scope, complexity, and specificity are mismatched.

**Partial coverage is not failure.** PARTIAL is a legitimate and informative verdict. An interview question that addresses the right competency domain but at the wrong organizational level (e.g., team-level leadership when the indicator specifies enterprise-level) earns PARTIAL, not GAP. The distinction matters for remediation — PARTIAL elements need refinement, GAP elements need creation.

**One source element can cover multiple targets.** A well-crafted behavioral event interview probe may provide evidence across two or three related indicators. Map it to all applicable target elements. However, be conservative — a single broad question rarely provides deep coverage of more than two to three indicators.

**One target element can require multiple sources.** A complex behavioral indicator may need multiple interview probes, assessment scales, or 360 items to achieve PASS-level coverage. If a single source element provides only partial evidence, the verdict is PARTIAL even if the indicator is partially addressed.

## Quality Standards

**Exhaustive mapping.** Every target element must receive a verdict. No rows left blank. No "N/A" unless the user explicitly designates an element as out of scope.

**Bidirectional awareness.** While the primary audit direction is "does A cover B," also flag source elements from Artifact A that map to nothing in Artifact B. These orphaned elements represent assessment content that is not tied to the competency framework — potential legal exposure if used for selection decisions, and wasted candidate time regardless.

**Level sensitivity.** When both artifacts include organizational level designations (e.g., Manager vs. VP vs. C-suite), coverage must be evaluated at the correct level. A Manager-level behavioral indicator is not covered by a VP-level interview question, and vice versa.

**Psychometric defensibility.** The coverage matrix is a content validity artifact. It must be constructed to the standard required by the SIOP Principles for the Validation and Use of Personnel Selection Procedures. This means the mapping should be transparent enough that an independent I-O psychologist could replicate the verdicts, and the justifications should reference observable content rather than inferred intent.

## Post-Audit Actions

After delivering the coverage matrix and executive summary, offer these next steps:

1. **Remediation recommendations** — For each GAP, suggest specific content that would close the gap (e.g., draft interview probes, recommend additional assessment scales, propose 360 items)
2. **SME validation protocol** — Outline a structured SME review session where subject matter experts independently rate the coverage verdicts, establishing inter-rater reliability
3. **Quantitative content validity** — If sufficient SMEs are available, calculate Lawshe Content Validity Ratios for each target element
4. **Iterative refinement** — After the user modifies Artifact A to address gaps, re-run the audit to verify gap closure and confirm no regression in previously PASS-rated elements

## Common Audit Pairings

These are the most frequent coverage audit scenarios. The skill handles any artifact pairing, but these represent the highest-value applications:

| Coverage Source (A) | Coverage Target (B) | What the Audit Reveals |
|---|---|---|
| Interview guide (BEI probes) | Behavioral indicators from competency model | Whether the interview systematically elicits evidence for every competency the role requires |
| Assessment battery (Hogan, HBRI, simulations) | Leadership enabler model (Spencer Stuart) | Whether the assessment configuration measures all enablers that predict executive success |
| 360 feedback instrument | Competency framework | Whether raters are evaluating all competencies defined for the target role |
| Job posting / JD | Essential functions from job analysis | Whether the posting accurately reflects the job's actual requirements for legal defensibility |
| Training curriculum / L&D program | Competency development targets | Whether the learning design addresses all competencies identified as developmental priorities |
| Succession criteria | Success profile requirements | Whether succession readiness is evaluated against the full profile, not a convenient subset |
| Onboarding program | First-90-day competency expectations | Whether new hires receive structured exposure to all competencies expected at initial performance review |
