---
name: adverse-impact-analyzer
description: >
  Compute and document an adverse-impact analysis for any selection, promotion,
  or screening process — the four-fifths (80%) rule plus a statistical-
  significance test and small-sample caveats — and frame the validation path if
  impact is found. Use this skill when the user asks to "run an adverse impact
  analysis," "check the 4/5ths rule," "four-fifths rule," "disparate impact,"
  "impact ratio," "selection rate analysis," "is this process biased," "EEO/EEOC
  compliance check," "does this screen out [group]," "compute impact ratios,"
  "Uniform Guidelines analysis," "Section 4D analysis," "are our hiring rates
  fair," "adverse impact on promotions," or uploads selection counts by group.
  Produces an Excel impact-ratio matrix and a Word defensibility narrative, and
  ships a tested Python calculator (scripts/impact_ratio.py). It computes the
  ratio, never asserts legal conclusions, and always pairs 4/5ths with a
  significance test.
---

# Adverse Impact Analyzer

Quantify and document whether a selection process disproportionately screens out
a protected group. Output an **Excel impact-ratio matrix** and a **Word
defensibility narrative**, computed by the bundled, tested
`scripts/impact_ratio.py`.

## Why This Skill Exists

Adverse-impact analysis is where selection meets the law. The *Uniform
Guidelines* (29 CFR 1607.4D) set the four-fifths rule: a group's selection rate
below 80% of the highest group's rate is **generally regarded as evidence** of
adverse impact. But 0.80 is an explicit **"rule of thumb," not a legal safe
harbor** — small differences can still matter when statistically and practically
significant, and small samples make the ratio unstable. Done casually, the
analysis either misses real impact or cries wolf on noise. This skill computes
the ratio *and* a significance test, flags small-sample fragility, and points to
which validation strategy must support the procedure if impact is present —
without ever stating a legal conclusion (that is counsel's call).

## Mandatory Co-Skills

| Co-Skill | When | Why |
|---|---|---|
| `xlsx/SKILL.md` | Every analysis | Impact-ratio matrix is a required output |
| `docx/SKILL.md` | Every analysis | Defensibility narrative is a required output |
| `cargill-branding/SKILL.md` | Cargill-bound output | Apply Cargill identity |

## Required Inputs

Ask for anything missing before computing.

| Input | Required | Notes |
|---|---|---|
| Process & job | Yes | What decision (hire/promotion/screen), which job, what period |
| Counts by group | Yes | For each group: **applicants** (or eligible) and **selected** |
| Grouping basis | Yes | Sex and/or race/ethnicity; one analysis per basis |
| Stage | Optional | Overall process vs a single component (§4C bottom-line) |

If only selection rates (not counts) are given, request counts — significance
tests and stability need raw N.

## Process

### Step 1 — Assemble the data
One row per group with applicants and selected. Run separate analyses for each
protected-class basis (sex; race/ethnicity). Note the period and the decision
point.

### Step 2 — Run the calculator
Use `scripts/impact_ratio.py` (pure Python, no dependencies). It computes per
group: selection rate; impact ratio vs the **highest-rate** group; the 4/5ths
PASS/FAIL flag; a two-proportion z-test vs the highest group; and, for small
cells, a Fisher's exact two-tailed p-value plus a small-sample warning. See
`references/significance-tests.md` for interpretation.

```bash
python3 scripts/impact_ratio.py --input data.json          # JSON in, table + JSON out
python3 scripts/impact_ratio.py < data.json                # or via stdin
```

Input shape:
```json
{
  "process": "2026 Financial Analyst — external hires",
  "basis": "race/ethnicity",
  "groups": [
    {"group": "White",  "applicants": 200, "selected": 60},
    {"group": "Black",  "applicants": 120, "selected": 24},
    {"group": "Hispanic", "applicants": 90, "selected": 21},
    {"group": "Asian",  "applicants": 80, "selected": 26}
  ]
}
```

### Step 3 — Interpret with the caveats
Apply the rules in `references/uniform-guidelines.md` and
`references/significance-tests.md`:
- Flag any impact ratio < 0.80, **but** treat 0.80 as a rule of thumb.
- Pair the ratio with the significance test (2-of-3 logic: practical + statistical).
- For any group with small selected/applicant counts, foreground the
  small-sample warning — the ratio may flip on one or two decisions.

### Step 4 — Frame the validation path (if impact is present)
If impact is indicated, the procedure needs validity evidence under one of the
three Uniform Guidelines strategies (criterion / content / construct). Name which
is most appropriate and reference the §15 documentation categories. Recommend a
`selection-method-advisor` review if the method choice itself is driving impact.

### Step 5 — Generate deliverables
Produce the Excel matrix and Word narrative per
`references/uniform-guidelines.md`. Append the disclaimer.

## References

- `references/uniform-guidelines.md` — §4C/§4D/§5/§14/§15 in plain language, the
  rule-of-thumb framing, the validation strategies, the §15 record categories,
  and the deliverable structure.
- `references/significance-tests.md` — the two-proportion z-test and Fisher's
  exact, the 2-of-3 / practical-significance logic, and small-sample handling.

## Deliverables

1. **Excel — Impact-Ratio Matrix.** One row per group: applicants, selected,
   selection rate, impact ratio vs highest group, 4/5ths flag, z/Fisher p,
   small-sample warning. Highlight rows < 0.80 (amber) and statistically
   significant shortfalls (red). A `Summary` tab with the process, basis, period,
   and the overall read.
2. **Word — Defensibility Narrative.** Method, results, the rule-of-thumb framing,
   significance and small-sample caveats, the validation strategy if impact is
   present, the §15 documentation note, and the disclaimer.

## Standard Disclaimer

> This is a statistical analysis, **not a legal conclusion**. The four-fifths
> ratio is a rule of thumb under 29 CFR 1607.4D, not a safe harbor; adverse
> impact and its defense are fact-specific legal determinations for qualified
> counsel and a qualified I-O psychologist. Re-verify all regulatory citations
> against 29 CFR Part 1607 and the SIOP Principles (5th ed.) before use.

## Hard rules

- **Never state a legal conclusion** ("this is illegal/legal"). Report the
  statistics and the framework; defer the legal call.
- **Never present 0.80 as a safe harbor.** Pair it with significance + practical
  significance and small-sample caveats every time.
- **Require counts, not just rates**, for any significance or stability claim.
