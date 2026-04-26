# Coverage Audit Methodology

Formal scoring rules, threshold definitions, ratio calculations, and deliverable architecture for the coverage audit skill.

## Table of Contents

1. [Scoring Rubric](#scoring-rubric)
2. [Threshold Definitions](#threshold-definitions)
3. [Coverage Ratio Calculations](#coverage-ratio-calculations)
4. [Excel Workbook Architecture](#excel-workbook-architecture)
5. [Executive Summary Architecture](#executive-summary-architecture)
6. [Conditional Formatting Specification](#conditional-formatting-specification)
7. [Inter-Rater Reliability Protocol](#inter-rater-reliability-protocol)

---

## Scoring Rubric

### PASS (Score = 1.0)

A target element receives PASS when the source artifact contains content that directly, substantively, and specifically addresses the target element at the appropriate organizational level and complexity.

**Criteria — all must be met:**

1. **Direct alignment**: The source content explicitly addresses the same behavioral domain, knowledge area, or task as the target element. Alignment is based on substantive content match, not keyword overlap.

2. **Sufficient depth**: The source content probes, measures, or develops the target element with enough specificity that a trained assessor, rater, or instructor could reliably evaluate or develop the competency based on the evidence elicited.

3. **Appropriate level**: If both artifacts include organizational level designations, the source content addresses the target at the correct level of complexity, scope, and stakeholder horizon. A Manager-level probe does not earn PASS against a VP-level indicator.

4. **Behavioral observability**: The source content elicits or measures observable behavior, not self-reported traits or intentions. "Do you consider yourself strategic?" does not cover the indicator "Develops 3-year market strategies integrating competitive, regulatory, and capability scenarios."

**Example PASS:**
- Target: Behavioral indicator — "Builds cross-functional coalitions to accelerate decision-making across P&L boundaries"
- Source: BEI probe — "Describe a situation where you needed to gain alignment across multiple business units or P&L owners to make a significant strategic decision. What was at stake, who were the key stakeholders, how did you navigate competing priorities, and what was the outcome?"
- Justification: The probe directly elicits behavioral evidence of cross-functional coalition-building at the enterprise level, with sufficient specificity to rate the candidate on scope (multiple BUs/P&Ls), process (navigating competing priorities), and outcome.

### PARTIAL (Score = 0.5)

A target element receives PARTIAL when the source artifact addresses the target element's domain but with insufficient depth, specificity, scope, or level alignment to constitute full coverage.

**Criteria — one or more of the following applies:**

1. **Domain match, depth miss**: The source content addresses the correct competency or function area but does not probe deeply enough to generate reliable behavioral evidence. A general question about "leadership" partially covers a specific indicator about "cascading transformative cultural shifts."

2. **Level mismatch**: The source content addresses the correct behavioral domain but at the wrong organizational level. A team-level question partially covers an enterprise-level indicator.

3. **Partial scope**: The target element is multi-dimensional (e.g., "navigates financial constraints while optimizing cross-functional networks") and the source content addresses only one dimension.

4. **Indirect coverage**: The source content would likely elicit some relevant evidence as a secondary output, but the target element is not the primary focus of the source content. A question about strategic planning might incidentally reveal financial acumen, but it does not directly assess it.

**Example PARTIAL:**
- Target: Behavioral indicator — "Cascades transformative cultural shifts across a global organization"
- Source: BEI probe — "Tell me about a time you had to implement a significant change on your team. How did you get buy-in?"
- Justification: The probe addresses change leadership (correct domain) but at team level, not global/organizational level. It does not elicit evidence of cultural transformation scope or cascading mechanisms across geographies.

### GAP (Score = 0.0)

A target element receives GAP when the source artifact contains no content that addresses the target element's behavioral domain, knowledge area, or task — even indirectly.

**Criteria:**

1. No source element maps to the target element's core behavioral or functional domain
2. The target element represents a competency, function, or requirement that the source artifact does not touch at any level of depth or specificity
3. Superficial keyword overlap without substantive content alignment does not prevent a GAP verdict

**Example GAP:**
- Target: Behavioral indicator — "Applies quantitative risk modeling to evaluate capital allocation scenarios under uncertainty"
- Source: Full interview guide reviewed — no questions address quantitative risk modeling, capital allocation, or financial scenario analysis
- Justification: The interview guide contains no probes in the financial/quantitative risk domain. This indicator is entirely unaddressed.

---

## Threshold Definitions

### Overall Coverage Assessment

| Rating | Overall Coverage Ratio | Interpretation |
|---|---|---|
| **Strong** | ≥ 85% | The source artifact provides comprehensive coverage of the target framework. Minor gaps may exist but do not represent systemic omissions. Suitable for deployment with targeted refinements. |
| **Adequate** | 70% – 84% | The source artifact covers the majority of the target framework but has meaningful gaps that should be addressed before deployment. Remediation is targeted and feasible. |
| **Insufficient** | 50% – 69% | The source artifact has significant coverage deficiencies. Substantial redesign or supplementation is required before the artifact can serve its intended purpose. |
| **Critical** | < 50% | The source artifact fails to cover the target framework at a fundamental level. The artifact may need to be rebuilt rather than patched. |

### Category-Level Coverage Assessment

Apply the same thresholds at the category level (e.g., per competency, per function area, per enabler domain). Category-level ratings identify where coverage failures are concentrated, enabling targeted remediation rather than wholesale redesign.

### GAP Severity Classification

Not all GAPs carry equal weight. When reporting GAPs, classify each by severity:

| Severity | Definition | Remediation Priority |
|---|---|---|
| **Critical GAP** | The missing element is a core, high-weight competency or essential function. Its absence creates legal, psychometric, or strategic risk. | Must be addressed before deployment |
| **Important GAP** | The missing element is a meaningful competency or function. Its absence reduces the artifact's effectiveness but does not create immediate risk. | Should be addressed in the current revision cycle |
| **Minor GAP** | The missing element is a supplementary or lower-weight competency or function. Its absence is noted but does not materially degrade the artifact's purpose. | Address in future iterations |

---

## Coverage Ratio Calculations

### Overall Coverage Ratio (OCR)

```
OCR = (Σ element scores) / (total elements) × 100

Where:
  PASS = 1.0
  PARTIAL = 0.5
  GAP = 0.0
```

**Example:** 20 target elements, with 12 PASS, 5 PARTIAL, 3 GAP:
```
OCR = (12 × 1.0 + 5 × 0.5 + 3 × 0.0) / 20 × 100 = 72.5%
```

### Category Coverage Ratio (CCR)

Calculate OCR independently for each logical grouping of target elements (competency cluster, function area, enabler domain). This reveals whether coverage failures are distributed or concentrated.

### Verdict Distribution

Report the raw counts and percentages:
```
PASS:    12 / 20 (60%)
PARTIAL:  5 / 20 (25%)
GAP:      3 / 20 (15%)
```

### Weighted Coverage Ratio (WCR) — Optional

When the user provides or the target artifact specifies element weights (e.g., competency criticality ratings, essential function importance scores), calculate:

```
WCR = (Σ element score × element weight) / (Σ element weights) × 100
```

The weighted ratio prevents low-criticality GAPs from inflating the overall deficit and ensures high-criticality GAPs are appropriately alarming.

---

## Excel Workbook Architecture

### Tab 1: Coverage Matrix (Primary Analytical Tab)

This is the core deliverable tab. Structure:

| Column | Header | Content | Width |
|---|---|---|---|
| A | **Target Category** | The grouping/cluster of the target element (competency name, function area, enabler domain) | 25 |
| B | **Target Element** | The specific behavioral indicator, task statement, or requirement being evaluated | 45 |
| C | **Target Level** | Organizational level if applicable (e.g., SM1, VP, Manager) | 12 |
| D | **Verdict** | PASS / PARTIAL / GAP | 10 |
| E | **Score** | 1.0 / 0.5 / 0.0 | 8 |
| F | **Source Evidence** | The specific question, scale, item, or content element from Artifact A that provides coverage | 50 |
| G | **Source Reference** | Location identifier (e.g., "Question 7," "HDS Scale: Bold," "Module 3.2") | 18 |
| H | **Justification** | Why this verdict was assigned — the analytical reasoning linking source to target | 50 |
| I | **GAP Severity** | For GAP verdicts only: Critical / Important / Minor | 12 |
| J | **Remediation Note** | For PARTIAL and GAP: Specific recommendation to close the gap | 45 |

**Formatting requirements:**
- Row 1: Header row, bold, frozen (freeze panes at A2)
- Auto-filter enabled on all columns
- Column widths set as specified above
- Conditional formatting on Column D (see Conditional Formatting Specification below)
- Rows grouped/outlined by Target Category for collapsible sections
- Text wrapping enabled on columns B, F, H, and J

### Tab 2: Coverage Summary (Dashboard Tab)

Summary statistics and visualizations:

**Section 1: Overall Metrics (Rows 1–8)**

| Cell | Content |
|---|---|
| A1 | "Coverage Audit Summary" (merged A1:D1, bold, 14pt) |
| A3 | "Source Artifact:" |
| B3 | [Name of Artifact A] |
| A4 | "Target Artifact:" |
| B4 | [Name of Artifact B] |
| A5 | "Audit Date:" |
| B5 | [Date] |
| A6 | "Overall Coverage Ratio:" |
| B6 | [OCR as percentage, formatted with conditional color] |

**Section 2: Verdict Distribution (Rows 10–14)**

| Verdict | Count | Percentage | Visual Bar |
|---|---|---|---|
| PASS | [n] | [%] | [green data bar] |
| PARTIAL | [n] | [%] | [yellow data bar] |
| GAP | [n] | [%] | [red data bar] |
| **Total** | [N] | 100% | |

**Section 3: Category-Level Coverage (Rows 16+)**

A table showing each category (competency, function area) with its individual coverage ratio, verdict distribution, and rating (Strong/Adequate/Insufficient/Critical).

### Tab 3: Orphaned Elements (Optional)

List any source elements from Artifact A that do not map to any target element in Artifact B. These represent assessment content, interview questions, or curriculum modules that are not tied to the competency or job analysis framework.

| Column | Header |
|---|---|
| A | Source Element |
| B | Source Reference |
| C | Assessment | Notes on whether the element should be retained, repurposed, or removed |

### Tab 4: Remediation Tracker (Optional)

A structured remediation log for tracking gap closure:

| Column | Header |
|---|---|
| A | Target Element |
| B | Current Verdict |
| C | Gap Severity |
| D | Recommended Action |
| E | Owner |
| F | Status (Open / In Progress / Closed) |
| G | Revised Verdict (after remediation) |
| H | Notes |

---

## Executive Summary Architecture

The Word document follows this structure:

### Page 1: Executive Decision Brief

**Title:** Coverage Audit: [Artifact A Name] × [Artifact B Name]

**BLUF (Bottom Line Up Front):** Two to three sentences stating the overall coverage ratio, the rating (Strong/Adequate/Insufficient/Critical), the count of critical GAPs, and the primary recommendation (deploy as-is, deploy with targeted remediation, hold for substantial revision).

**Coverage Snapshot Table:**

| Metric | Value |
|---|---|
| Overall Coverage Ratio | [X%] |
| Rating | [Strong / Adequate / Insufficient / Critical] |
| Total Elements Evaluated | [N] |
| PASS | [n] ([%]) |
| PARTIAL | [n] ([%]) |
| GAP | [n] ([%]) |
| Critical GAPs | [n] |

### Page 2: Category-Level Analysis

A table showing coverage by category (competency cluster, function area, enabler domain) with the category-level coverage ratio and a one-sentence interpretation for each.

Narrative paragraphs identifying:
- Categories with strongest coverage (and why — what the source artifact does well)
- Categories with weakest coverage (and the specific nature of the gaps)
- Patterns across categories (e.g., "Coverage is strong for operational competencies but systematically weak for strategic/enterprise-level indicators")

### Page 3: Critical GAPs and Remediation Recommendations

For each Critical and Important GAP, a structured entry:

**GAP: [Target Element]**
- Category: [Competency / Function Area]
- Severity: [Critical / Important]
- Impact: One sentence on why this gap matters (legal, psychometric, strategic)
- Recommended remediation: Specific, actionable recommendation (e.g., "Add BEI probe: 'Describe a situation where you had to reallocate resources across business units during a financial constraint. What data informed your decision, and how did you communicate the trade-offs?'")

### Page 4 (if needed): Methodology Note

Brief description of the audit methodology, scoring rubric, and threshold definitions. This section establishes the credibility of the audit for readers who are not familiar with the methodology and provides the documentation required for psychometric defensibility.

---

## Conditional Formatting Specification

Apply these formats to the Verdict column (Column D) in the Coverage Matrix tab:

| Verdict | Cell Background | Font Color | Font Weight |
|---|---|---|---|
| PASS | #C6EFCE (light green) | #006100 (dark green) | Normal |
| PARTIAL | #FFEB9C (light yellow) | #9C6500 (dark amber) | Normal |
| GAP | #FFC7CE (light red) | #9C0006 (dark red) | Bold |

Apply the same color scheme to:
- The Score column (Column E) using the same background colors
- The Coverage Ratio cells in the Summary tab (green ≥85%, yellow 70–84%, orange 50–69%, red <50%)
- The GAP Severity column: Critical = red background, Important = orange background, Minor = yellow background

---

## Inter-Rater Reliability Protocol

When the coverage audit will be used for formal content validity documentation (e.g., supporting a validation study or legal defensibility review), establish inter-rater reliability:

### Step 1: Independent Rating
Provide the coverage matrix to two or more SMEs (or I-O psychologists). Each rater independently assigns PASS/PARTIAL/GAP to each target element without seeing the other raters' verdicts.

### Step 2: Calculate Agreement
Compute percent agreement and Cohen's kappa (for two raters) or Fleiss' kappa (for three or more):

- **Percent agreement target**: ≥ 80%
- **Kappa target**: ≥ 0.70 (substantial agreement)

### Step 3: Reconciliation
For elements where raters disagree, conduct a structured discussion to reach consensus. Document the rationale for each resolved disagreement. The final reconciled verdicts become the official coverage matrix.

### Step 4: Documentation
Record the IRR statistics, the number and nature of disagreements, and the resolution rationale. This documentation is required for any formal content validity report and provides the evidentiary foundation for legal defensibility.
