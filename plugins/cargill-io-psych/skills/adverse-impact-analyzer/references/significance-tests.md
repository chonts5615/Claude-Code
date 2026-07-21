# Significance & small-sample handling

The four-fifths ratio answers "how big is the gap." A significance test answers
"is the gap likely real or noise." Report **both** — the agencies and the courts
look for practical *and* statistical significance, not the ratio alone.

## The 2-of-3 logic (practical + statistical)

Treat a finding as a serious adverse-impact signal when it shows:
1. **Practical significance** — impact ratio < 0.80 (the 4/5ths gap), AND/OR a
   meaningful **shortfall** (how many additional selections the focal group would
   need to reach parity — the "N needed to flip"), AND
2. **Statistical significance** — a test (below) rejects "rates are equal" at a
   conventional level (commonly two-tailed, ~1.96 SD / p < .05).

A gap that is large but not statistically reliable (tiny N) is fragile; a gap
that is statistically significant but trivially small in practical terms may not
warrant action. Say which you have.

## Two-proportion z-test (default for adequate N)

Compares the focal group's selection rate to the reference (highest-rate) group:

```
p_pool = (x1 + x2) / (n1 + n2)
SE     = sqrt( p_pool * (1 - p_pool) * (1/n1 + 1/n2) )
z      = (rate1 - rate2) / SE
```

Two-tailed p from z. |z| ≥ 1.96 ⇒ significant at .05. The bundled
`scripts/impact_ratio.py` computes this per group vs the highest-rate group.

## Fisher's exact test (small samples)

When any cell is small (a common rule: expected count < 5, or selected/applicant
counts in the low double digits or less), the z-test approximation is unreliable.
Use **Fisher's exact** two-tailed p instead. The calculator computes it from the
2×2 table (group vs reference × selected vs not) using exact hypergeometric
probabilities. When N is small, **lead with the small-sample warning**: one or
two different decisions can flip the ratio and the verdict.

## Small-sample warning rules (the calculator emits these)

- Flag any group with **selected < 5** or **applicants < 30** as small-sample.
- For flagged groups, present the ratio as *indicative, not stable*, and prefer
  Fisher's exact over the z-test.
- Note that the 4/5ths rule itself is unreliable for small applicant pools
  (§4D's own caveat).

## Interpretation guardrails

- The output is descriptive statistics, **not** a legal conclusion. Never write
  "the process is discriminatory/legal."
- The reference group is the one with the **highest** selection rate, by
  convention — state it explicitly.
- If impact is indicated, the next question is validity (see
  `uniform-guidelines.md` §5/§14), not a verdict.
