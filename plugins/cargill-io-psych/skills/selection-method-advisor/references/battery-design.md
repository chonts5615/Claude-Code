# Battery Design — combination, sequencing, deliverables

## Incremental-validity logic

1. Start from the KSAO set (from an analysis of work). A method earns a place
   only if it measures a required-at-entry KSAO that the battery does not yet
   cover well.
2. Prefer methods with **low inter-correlation** to each other — that is where
   incremental validity comes from. Two cognitively-loaded measures largely
   duplicate; a structured interview + work sample + integrity test span
   different constructs.
3. Stop at 2–4 methods for most roles. More tools add candidate burden and cost
   faster than validity past that point.
4. Estimate composite validity from the component validities and their
   inter-correlations; present it as an estimate and recommend local validation.

## Sequencing (the funnel)

Order methods cheap-and-scalable → expensive-and-rich:

1. **Screen** (high volume, low cost): application/biodata, job-knowledge or
   short cognitive screen, realistic job preview.
2. **Assess** (focused pool): structured interview, work sample/SJT.
3. **Confirm** (finalists): assessment center or panel + reference/background as
   appropriate.

Put the lowest-adverse-impact valid screens early so the funnel does not
disproportionately remove protected-group candidates before the richer,
fairer methods run.

## Adverse-impact trade-off (always state it)

- Cognitive-loaded methods carry the **largest** subgroup mean differences;
  a GMA-heavy battery maximizes some validity but imports adverse-impact risk.
- Structured interviews, work samples, integrity, and biodata generally show
  smaller differences. Often a small validity trade buys a large adverse-impact
  reduction — name that trade explicitly when the user has diversity goals.
- Recommend an `adverse-impact-analyzer` pass on real selection data, and local
  validity evidence, before go-live.

## Word memo structure — `selection_recommendation_<role>.docx`

1. **Purpose & role** — title, level, volume, stakes.
2. **KSAO anchor** — the required-at-entry KSAOs and their source analysis.
3. **Recommended battery** — the 2–4 methods, in sequence, with one-line
   rationale each.
4. **Validity evidence** — the cited operational validities (Sackett 2022) and
   the composite estimate.
5. **Adverse-impact trade-off** — profiles and the chosen balance.
6. **Implementation** — administration, scoring standardization, rater training,
   candidate experience, cost.
7. **Validation plan** — local validation + adverse-impact monitoring.
8. **Disclaimer.**

## Excel table — `method_comparison_<role>.xlsx`

One row per candidate method considered (not just the chosen ones):

| Column |
|---|
| Method |
| KSAOs measured |
| Operational validity (Sackett 2022) |
| Reliability target |
| Relative cost (Low/Med/High) |
| Candidate-experience load |
| Adverse-impact profile |
| Sequence stage |
| Decision (Recommend / Hold / Reject) + reason |

Conditional-format validity (3-color) and Decision (green/amber/grey).
