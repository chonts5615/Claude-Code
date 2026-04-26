# SME Feedback Capture Form Specification

This reference defines the structure for the optional companion document: the SME Feedback Capture Form. This form is designed for individual SME completion during or immediately after the 60-minute focus group session. The data it collects enables quantitative aggregation (Lawshe CVR computation) and structured qualitative feedback capture.

---

## When to Generate

Generate the feedback form when:
- The user explicitly requests it ("also create the feedback form," "include the rating sheet")
- The user mentions wanting to compute CVR or aggregate ratings
- The user is preparing for a live focus group session (not an asynchronous review)

If the user does not request it, mention its availability but do not generate it automatically.

## File Naming

```
SME_Feedback_Form_{{Specialization}}_{{YYYYMMDD}}.docx
```

---

## Page Setup

Same as the main validation package: US Letter, 1" margins, Cargill branding. This document is typically 3-6 pages depending on competency count.

---

## Document Structure

### Cover / Header (Page 1, top)

```
SME Feedback Capture Form
{{SPECIALIZATION_NAME}} — Technical Competency Validation
[Big Caslon, 20pt, Leaf Green]

Date: {{SESSION_DATE}}
[Helvetica Now Regular, 11pt]

SME Name: ______________________________
SME Title: ______________________________
Years in {{SPECIALIZATION_NAME}}: _________
Years at Cargill: _________
[Form fields — Helvetica Now Regular, 11pt, with underscore lines]
```

### Instructions Block

```
Instructions:
For each competency below, provide your individual ratings and comments. Use the scales defined in the Validation Package document. Your individual responses will be aggregated with other SME panelists. Responses are confidential — individual ratings will not be attributed by name.

Rating Scales (Quick Reference):
  Relevance: 1 (Not relevant) — 5 (Essential)
  Clarity: 1 (Unclear) — 3 (Clear)
  Level Differentiation: 1 (Not differentiated) — 3 (Well differentiated)
```

### Rating Matrix (Repeats per Competency)

For each competency, generate this block:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Competency [N]: {{COMPETENCY_NAME}}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### Rating Table

| Dimension | Rating | Circle One |
|---|---|---|
| **Relevance** | How important is this competency to effective performance in {{SPECIALIZATION_NAME}}? | 1 — 2 — 3 — 4 — 5 |
| **Clarity** | Are the behavioral indicators clearly written and unambiguous? | 1 — 2 — 3 |
| **Level Differentiation** | Do L1-L4 indicators represent meaningfully different proficiency levels? | 1 — 2 — 3 |

Table styling: Leaf Green header row. Three rows (one per dimension). "Circle One" column shows the scale values with dashes between them for print circling.

#### Qualitative Feedback Fields

After each rating table, include these prompted fields:

```
Indicators to ADD (behaviors missing from the current set):
_____________________________________________________________
_____________________________________________________________

Indicators to REVISE (current indicators that need rewording — cite the specific indicator):
_____________________________________________________________
_____________________________________________________________

Indicators to REMOVE (current indicators that are irrelevant or redundant):
_____________________________________________________________
_____________________________________________________________

Essential Functions Mapping — any corrections to the competency-to-EF crosswalk?
_____________________________________________________________

Other Comments:
_____________________________________________________________
_____________________________________________________________
```

Each field should have 2-3 underscore lines for writing space. Use Helvetica Now Regular, 10pt for the prompts, with comfortable line spacing (1.5x) for handwriting between lines.

### Gap Analysis Section (After All Competency Blocks)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GAP ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Are there critical technical capabilities required for effective {{SPECIALIZATION_NAME}} performance that are NOT represented in the competency set reviewed today?

Missing Competency 1:
  Name: ___________________________________________
  Brief Description: _______________________________
  Why it matters: __________________________________

Missing Competency 2:
  Name: ___________________________________________
  Brief Description: _______________________________
  Why it matters: __________________________________

Missing Competency 3:
  Name: ___________________________________________
  Brief Description: _______________________________
  Why it matters: __________________________________
```

### Overall Assessment (Final Page)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OVERALL ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall, how well does this draft competency set represent the critical technical requirements of the {{SPECIALIZATION_NAME}} specialization?

  [ ] Excellent — The set is comprehensive and well-defined. Minor refinements only.
  [ ] Good — The set captures most critical capabilities. Some indicators need revision.
  [ ] Adequate — The set is a reasonable starting point but has meaningful gaps or clarity issues.
  [ ] Needs significant work — Major competencies are missing or indicators are substantially off-target.

Overall comments or recommendations for the project team:
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

Thank you for your time and expertise.
```

### Footer

```
Cargill Confidential | {{SPECIALIZATION_NAME}} SME Feedback Form | Page [N] of [Total]
```

---

## Data Aggregation Notes (For Skill Instructions, Not for the Form Itself)

After collecting completed feedback forms, the following aggregation is performed:

### Lawshe CVR Computation

For each competency:
1. Count the number of SMEs rating Relevance as 4 or 5 ("Essential" or "Important") → this is `n_e`
2. Total number of SME panelists → this is `N`
3. CVR = (n_e - N/2) / (N/2)

CVR interpretation:
- CVR = 1.0 → all SMEs rated as essential/important (unanimous)
- CVR = 0.0 → exactly half rated as essential/important (chance)
- CVR < 0.0 → fewer than half rated as essential/important (below chance)

Critical CVR thresholds (one-tailed, p < .05):
| N (panel size) | Minimum CVR |
|---|---|
| 5 | .99 |
| 6 | .99 |
| 7 | .99 |
| 8 | .75 |
| 9 | .78 |
| 10 | .62 |
| 11 | .59 |
| 12 | .56 |
| 13 | .54 |
| 14 | .51 |
| 15 | .49 |

For Legal & Compliance panels (likely 5-8 SMEs per specialization), the threshold is high. This is expected — small panels require near-unanimity.

### Clarity and Level Differentiation Aggregation

Compute mean ratings and standard deviations. Flag any competency with:
- Mean Clarity < 2.0 (needs rewording)
- Mean Level Differentiation < 2.0 (needs restructuring)
- SD > 1.0 on any dimension (high disagreement among SMEs — warrants discussion)

### Qualitative Feedback Synthesis

Group written feedback by competency and by type (ADD/REVISE/REMOVE). Cross-reference with the TCB v4 SME Disposition Schema (SDS-4) for structured resolution:
- Accept → apply the SME's suggestion
- Accept with Modification → apply a variant of the suggestion
- Defer to Focus Group → escalate for broader SME discussion
- Reject with Rationale → document why the suggestion was not adopted
- Duplicate → already captured elsewhere
- Out of Scope → pertains to Layer 1 or Layer 2 content, not Layer 3
