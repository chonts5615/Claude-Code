#!/usr/bin/env python3
"""Quality-gate audit for Round 2 SME Review Packet data files.

Checks each data/*.json against the locked-format completeness contract
(see CLAUDE.md) so a packet cannot ship with a missing competency, a missing
appendix, or a missing feedback (disposition) register. Run before generating.

CRITICAL RULE (complete coverage): every competency that ANY participating
specialization touches must appear in the coverage matrix WITH a role — both
the shared (union) competencies and the specialization-specific (non-shared)
ones. Declare each specialization's full competency set in
`coverage.specialization_sets`; the audit verifies the matrix against it per
specialization and fails CRITICAL on any gap.

Usage:
    python audit.py                 # audit every data/*.json
    python audit.py data/x.json     # audit one file

Exit code is non-zero if any packet fails, so this doubles as a test.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

VALID_DISPOSITIONS = {
    "Applied", "Synthesized / Used", "Via level", "Deferred", "Corrected", "Kept",
}
LEVELS = ["L1", "L2", "L3", "L4"]


def _coverage_competencies(data):
    return [r["competency"] for r in data.get("coverage", {}).get("rows", [])]


def _is_deferred_only(row):
    """A row whose only role anywhere is 'def' (deferred out of the set)."""
    roles = [(c or "").strip() for c in row.get("roles", [])]
    nonblank = [r for r in roles if r]
    return bool(nonblank) and all(r == "def" for r in nonblank)


def audit(data, name):
    """Return a list of failure strings ([] == pass)."""
    fails = []
    cov_rows = data.get("coverage", {}).get("rows", [])
    cov_names = _coverage_competencies(data)
    cov_set = set(cov_names)
    # Deferred-only competencies stay in the matrix to show they were held out,
    # but they need no full indicator table (just a disposition entry).
    deferred = {r["competency"] for r in cov_rows if _is_deferred_only(r)}
    indicator_required = [c for c in cov_names if c not in deferred]

    # A. every coverage row carries at least one role (blank = "no role", but a
    #    row with no role anywhere should not be in the matrix).
    for r in cov_rows:
        if not any((c or "").strip() for c in r.get("roles", [])):
            fails.append(f"coverage row '{r['competency']}' has no role in any specialization")

    # B. CRITICAL — complete-coverage rule. Every competency that ANY
    #    participating specialization touches must appear in the matrix WITH a
    #    role: both the shared (union) competencies and the specialization-
    #    specific (non-shared) ones. None may be dropped because another group
    #    owns it, rates it lower, only uses it, or it is "held in the library."
    coverage = data.get("coverage", {})
    specs = coverage.get("specializations", [])
    spec_sets = coverage.get("specialization_sets", {})
    declared_union = set()
    if spec_sets:
        for spec_name, comps in spec_sets.items():
            declared_union |= set(comps)
            if spec_name not in specs:
                fails.append(
                    f"CRITICAL: specialization_sets names '{spec_name}', which is not a "
                    "column in coverage.specializations"
                )
                continue
            col = specs.index(spec_name)
            for comp in comps:
                row = next((r for r in cov_rows if r["competency"] == comp), None)
                if row is None:
                    fails.append(
                        f"CRITICAL: '{comp}' is in the {spec_name} set but missing from the "
                        "coverage matrix (complete-coverage violation)"
                    )
                elif col >= len(row.get("roles", [])) or not (row["roles"][col] or "").strip():
                    fails.append(
                        f"CRITICAL: '{comp}' is listed for {spec_name} but its matrix cell "
                        "for that specialization is blank (no role marked)"
                    )

    # A flat required_union may also be declared; it must equal the set union.
    required = coverage.get("required_union")
    if required:
        missing = [c for c in required if c not in cov_set]
        if missing:
            fails.append(
                "CRITICAL: complete-coverage violation — coverage matrix is missing "
                + str(len(missing)) + " required competency(ies): " + ", ".join(missing)
            )
        if spec_sets and set(required) != declared_union:
            only_req = set(required) - declared_union
            only_set = declared_union - set(required)
            detail = []
            if only_req:
                detail.append("in required_union only: " + ", ".join(sorted(only_req)))
            if only_set:
                detail.append("in specialization_sets only: " + ", ".join(sorted(only_set)))
            fails.append(
                "CRITICAL: required_union does not match the union of specialization_sets ("
                + "; ".join(detail) + ")"
            )

    # C. every non-deferred coverage competency must have an Appendix B entry.
    appx = {c["name"]: c for c in data.get("appendix", {}).get("competencies", [])}
    for c in indicator_required:
        if c not in appx:
            fails.append(f"competency '{c}' is in the coverage matrix but missing from the appendix")

    # D. feedback appendix (disposition register) must exist and cover every
    #    coverage competency — this is the "where your feedback went" record.
    dr = data.get("disposition_register", {})
    entries = {e["competency"]: e for e in dr.get("entries", [])}
    if not entries:
        fails.append("missing disposition register (feedback appendix) — no entries")
    else:
        for c in cov_names:
            if c not in entries:
                fails.append(f"disposition register has no entry for coverage competency '{c}'")
        for comp, e in entries.items():
            disp = e.get("disposition", "")
            if disp not in VALID_DISPOSITIONS:
                fails.append(f"disposition register entry '{comp}' has invalid disposition '{disp}'")

    # E. indicator tables: every appendix competency needs L1-L4, >=3 each.
    for cname, comp in appx.items():
        by_level = {lv: 0 for lv in LEVELS}
        for ind in comp.get("indicators", []):
            if ind.get("level") in by_level:
                by_level[ind["level"]] += 1
        for lv in LEVELS:
            if by_level[lv] < 3:
                fails.append(f"competency '{cname}' has {by_level[lv]} {lv} indicators (need >=3)")

    # F. status legend counts are derivable and consistent (sanity).
    n_items = len(data.get("part_a", {}).get("items", [])) + len(
        data.get("part_b", {}).get("items", [])
    )
    if n_items == 0:
        fails.append("packet has no Part A or Part B items")

    return fails


def main(argv):
    here = Path(__file__).resolve().parent
    if argv:
        files = [Path(a) for a in argv]
    else:
        files = sorted((here / "data").glob("*.json"))

    any_fail = False
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        name = data.get("metadata", {}).get("sub_family", f.stem)
        fails = audit(data, name)
        cov_n = len(_coverage_competencies(data))
        if fails:
            any_fail = True
            n_crit = sum(1 for m in fails if m.startswith("CRITICAL"))
            tag = f"✗ FAIL  {name}  ({cov_n} competencies"
            tag += f", {n_crit} CRITICAL)" if n_crit else ")"
            print(tag)
            for msg in fails:
                print(f"        - {msg}")
        else:
            print(f"✓ PASS  {name}  ({cov_n} competencies, appendix + disposition register complete)")
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
