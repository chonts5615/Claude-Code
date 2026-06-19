---
name: io-psych-exec-review
description: Critically review a talent/assessment research report through two expert lenses — an experienced I-O psychology research-practitioner (scientific and psychometric rigor) and a principal executive consultant (strategic relevance and decision usefulness). Flags weak validity evidence, outdated coefficients, over-claiming, missing caveats, and content that is academically sound but not decision-useful. Use during QA for reports on assessment, selection, or talent topics.
---

# io-psych-exec-review

Review `files/reports/report.md` (and the research notes for grounding) as two
senior experts would. This skill **checks and flags**; it does not rewrite. Be
genuinely critical and specific — cite the exact claim and a concrete fix.

## Lens 1 — I-O psychology research-practitioner (rigor)

Judge whether the science would survive peer/SIOP scrutiny:

- **Validity evidence quality.** Are criterion/construct validity claims backed
  by meta-analytic or peer-reviewed evidence, not vendor marketing? Are
  coefficients operational vs. observed, and is that distinction respected?
- **Currency.** Flag validity figures that rely on superseded sources — e.g.
  pre-2022 selection-validity numbers that Sackett, Zhang, Berry & Lievens (2022)
  meaningfully revised (cognitive ability, structured interviews, etc.). Current
  figures should be used or the revision explicitly noted.
- **Constructs & psychometrics.** Are models (Big Five/HEXACO/etc.), reliability
  (α, test–retest), norming, and IRT vs. CTT claims used correctly? Flag
  conflation of reliability with validity.
- **Faking, fairness, adverse impact.** Are response distortion, the 4/5ths rule,
  adverse-impact monitoring, and differential validity treated where relevant?
- **Causality & over-claiming.** Flag correlational findings stated as causal,
  single studies generalized too far, and missing confidence intervals/caveats.

## Lens 2 — Principal executive consultant (decision usefulness)

Judge whether a senior leader could act on it:

- **So-what & actionability.** Does each section drive to a recommendation or
  decision, or is it inert background? Flag "academically correct but not useful."
- **Executive communication.** Is there a crisp executive summary leading with the
  recommendation and the few numbers that matter? Flag burying the lede.
- **Prioritization & tradeoffs.** Are options compared on the dimensions leaders
  care about (cost, risk, time-to-value, defensibility), with a clear point of
  view rather than a neutral survey?
- **Risk & cost realism.** Are ROI/value claims framed as ranges with assumptions,
  not false precision? Are compliance/reputational risks surfaced?
- **Decision support.** Is there guidance on "which option for which situation"
  (e.g. a decision matrix), and clear next steps?

## Output

Add an `## Expert review (I-O + executive)` section to the QA review with two
subsections (Rigor, Decision usefulness). List each issue with the exact claim,
why an expert would object, and a specific fix. Any **material** rigor problem
(e.g. outdated/over-claimed validity, reliability/validity conflation) or a report
with no actionable recommendations is grounds for `QA VERDICT: REVISE`.
