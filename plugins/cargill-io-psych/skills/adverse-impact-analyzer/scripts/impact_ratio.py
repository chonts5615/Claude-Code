#!/usr/bin/env python3
"""Adverse-impact calculator — four-fifths rule + significance tests.

Pure standard library (no numpy/scipy). Reads a JSON description of a selection
process and reports, per group: selection rate, impact ratio vs the highest-rate
group, the four-fifths (80%) flag, a two-proportion z-test vs the reference
group, Fisher's exact two-tailed p for small cells, the shortfall-to-parity, and
a small-sample warning.

This is a statistical tool, NOT a legal conclusion. The 0.80 ratio is a rule of
thumb under 29 CFR 1607.4D, not a safe harbor.

Usage:
    python3 impact_ratio.py --input data.json
    python3 impact_ratio.py < data.json
    python3 impact_ratio.py --input data.json --json-only

Input JSON:
    {
      "process": "2026 Analyst hires",
      "basis": "race/ethnicity",
      "groups": [
        {"group": "White", "applicants": 200, "selected": 60},
        {"group": "Black", "applicants": 120, "selected": 24}
      ]
    }
"""
import argparse
import json
import math
import sys

FOUR_FIFTHS = 0.80
SMALL_SELECTED = 5      # selected below this -> small-sample warning
SMALL_APPLICANTS = 30   # applicants below this -> small-sample warning


def _phi(z):
    """Standard normal CDF."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def two_proportion_z(x1, n1, x2, n2):
    """Two-tailed z-test p-value comparing two selection rates.

    Returns (z, p) or (None, None) when undefined (pooled rate 0 or 1, or zero N).
    """
    if n1 == 0 or n2 == 0:
        return None, None
    p_pool = (x1 + x2) / (n1 + n2)
    if p_pool in (0.0, 1.0):
        return None, None
    se = math.sqrt(p_pool * (1.0 - p_pool) * (1.0 / n1 + 1.0 / n2))
    if se == 0:
        return None, None
    z = (x1 / n1 - x2 / n2) / se
    p = 2.0 * (1.0 - _phi(abs(z)))
    return z, p


def fisher_exact_two_tailed(a, b, c, d):
    """Two-tailed Fisher's exact p for the 2x2 table [[a,b],[c,d]].

    a = group selected, b = group not selected,
    c = reference selected, d = reference not selected.
    """
    n1 = a + b           # group applicants (row 1 total)
    n2 = c + d           # reference applicants (row 2 total)
    k = a + c            # total selected (col 1 total)
    n = n1 + n2          # grand total
    if n == 0 or n1 == 0 or n2 == 0:
        return None

    def hyp(x):
        # P(group selected = x) given the margins.
        lo_ok = max(0, k - n2) <= x <= min(k, n1)
        if not lo_ok:
            return 0.0
        return (math.comb(n1, x) * math.comb(n2, k - x)) / math.comb(n, k)

    p_obs = hyp(a)
    lo = max(0, k - n2)
    hi = min(k, n1)
    eps = 1e-9
    total = sum(hyp(x) for x in range(lo, hi + 1) if hyp(x) <= p_obs + eps)
    return min(1.0, total)


def analyze(data):
    process = data.get("process", "(unnamed process)")
    basis = data.get("basis", "(unspecified basis)")
    groups = data["groups"]

    rows = []
    for g in groups:
        applicants = int(g["applicants"])
        selected = int(g["selected"])
        if applicants < 0 or selected < 0 or selected > applicants:
            raise ValueError(
                f"Invalid counts for group '{g.get('group')}': "
                f"selected={selected}, applicants={applicants}"
            )
        rate = selected / applicants if applicants else 0.0
        rows.append({
            "group": g["group"],
            "applicants": applicants,
            "selected": selected,
            "selection_rate": rate,
        })

    if not rows:
        raise ValueError("No groups provided.")

    # Reference group = highest selection rate.
    ref = max(rows, key=lambda r: r["selection_rate"])
    ref_rate = ref["selection_rate"]

    for r in rows:
        is_ref = r is ref
        r["is_reference"] = is_ref
        r["impact_ratio"] = (r["selection_rate"] / ref_rate) if ref_rate > 0 else None
        r["four_fifths_pass"] = (
            None if r["impact_ratio"] is None else r["impact_ratio"] >= FOUR_FIFTHS
        )
        # Shortfall to parity with the reference rate.
        parity_selected = ref_rate * r["applicants"]
        r["shortfall_to_parity"] = max(0.0, parity_selected - r["selected"])
        # Small-sample warning.
        r["small_sample"] = (
            r["selected"] < SMALL_SELECTED or r["applicants"] < SMALL_APPLICANTS
        )
        if is_ref:
            r["z"], r["p_z"], r["p_fisher"] = None, None, None
            continue
        z, p = two_proportion_z(
            r["selected"], r["applicants"], ref["selected"], ref["applicants"]
        )
        r["z"], r["p_z"] = z, p
        a = r["selected"]
        b = r["applicants"] - r["selected"]
        c = ref["selected"]
        d = ref["applicants"] - ref["selected"]
        r["p_fisher"] = fisher_exact_two_tailed(a, b, c, d)

    return {"process": process, "basis": basis, "reference_group": ref["group"], "rows": rows}


def _fmt_pct(x):
    return f"{x * 100:5.1f}%" if x is not None else "   n/a"


def _fmt_ratio(x):
    return f"{x:5.2f}" if x is not None else "  n/a"


def _fmt_p(x):
    if x is None:
        return "   n/a"
    return f"{x:6.4f}"


def render_table(result):
    lines = []
    lines.append(f"Adverse-Impact Analysis — {result['process']}")
    lines.append(f"Basis: {result['basis']}   |   Reference group (highest rate): {result['reference_group']}")
    lines.append("")
    header = (
        f"{'Group':<16}{'Appl':>6}{'Sel':>5}{'Rate':>8}{'Ratio':>7}"
        f"{'4/5?':>6}{'z-p':>8}{'Fisher-p':>10}{'Short':>7}  Notes"
    )
    lines.append(header)
    lines.append("-" * len(header))
    for r in result["rows"]:
        if r["is_reference"]:
            flag = "REF"
        elif r["four_fifths_pass"] is None:
            flag = "n/a"
        else:
            flag = "PASS" if r["four_fifths_pass"] else "FAIL"
        notes = []
        if r["small_sample"]:
            notes.append("SMALL-SAMPLE: ratio unstable; prefer Fisher")
        if (not r["is_reference"] and r["four_fifths_pass"] is False
                and r["p_z"] is not None and r["p_z"] < 0.05):
            notes.append("gap is statistically significant (p<.05)")
        lines.append(
            f"{r['group']:<16}{r['applicants']:>6}{r['selected']:>5}"
            f"{_fmt_pct(r['selection_rate']):>8}{_fmt_ratio(r['impact_ratio']):>7}"
            f"{flag:>6}{_fmt_p(r['p_z']):>8}{_fmt_p(r['p_fisher']):>10}"
            f"{r['shortfall_to_parity']:>7.1f}  " + "; ".join(notes)
        )
    lines.append("")
    lines.append("Reminder: 0.80 is a RULE OF THUMB (29 CFR 1607.4D), not a safe harbor. "
                 "This is a statistical analysis, not a legal conclusion.")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Adverse-impact (four-fifths) calculator.")
    parser.add_argument("--input", help="Path to input JSON (default: stdin).")
    parser.add_argument("--json-only", action="store_true",
                        help="Emit only the JSON result (no human table).")
    args = parser.parse_args(argv)

    raw = open(args.input).read() if args.input else sys.stdin.read()
    data = json.loads(raw)
    result = analyze(data)

    if args.json_only:
        print(json.dumps(result, indent=2))
    else:
        print(render_table(result))
        print()
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
