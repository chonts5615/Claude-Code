"""Character-level Text Integrity Check (CTIC) — Phase 6F drift control."""

from __future__ import annotations

from copy import deepcopy
from difflib import SequenceMatcher
from typing import Iterable

from src.schemas.ctic import CTICDiff, CTICReport


def compute_diff(before: str, after: str) -> tuple[int, list[str]]:
    before = before or ""
    after = after or ""
    sm = SequenceMatcher(a=before, b=after, autojunk=False)
    char_diff = 0
    opcodes: list[str] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        a_len = i2 - i1
        b_len = j2 - j1
        char_diff += max(a_len, b_len)
        opcodes.append(f"{tag} a[{i1}:{i2}]={before[i1:i2]!r} -> b[{j1}:{j2}]={after[j1:j2]!r}")
    return char_diff, opcodes


def _iter_pairs(before: dict, after: dict) -> Iterable[tuple[str, str, str, str]]:
    for comp_id, fields in before.items():
        if comp_id not in after:
            continue
        after_fields = after[comp_id]
        if not isinstance(fields, dict) or not isinstance(after_fields, dict):
            continue
        for field, before_val in fields.items():
            if field not in after_fields:
                continue
            yield comp_id, field, str(before_val), str(after_fields[field])


def check_drift(
    before: dict,
    after: dict,
    targeted_fields: set[str],
    run_id: str = "",
) -> CTICReport:
    entries: list[CTICDiff] = []
    diffs_detected = 0
    diffs_reverted = 0
    diffs_kept = 0

    for comp_id, field, b_val, a_val in _iter_pairs(before, after):
        char_diff, _opcodes = compute_diff(b_val, a_val)
        if char_diff == 0:
            continue

        diffs_detected += 1
        key = f"{comp_id}:{field}"
        is_targeted = key in targeted_fields or field in targeted_fields
        if not is_targeted:
            entries.append(
                CTICDiff(
                    competency_id=comp_id,
                    field=field,
                    before=b_val,
                    after=a_val,
                    char_diff_count=char_diff,
                    is_targeted_by_feedback=False,
                    reverted=True,
                    rationale="Non-targeted field changed — drift, will be reverted.",
                )
            )
            diffs_reverted += 1
        else:
            entries.append(
                CTICDiff(
                    competency_id=comp_id,
                    field=field,
                    before=b_val,
                    after=a_val,
                    char_diff_count=char_diff,
                    is_targeted_by_feedback=True,
                    reverted=False,
                    rationale="Field explicitly targeted by SME feedback — kept.",
                )
            )
            diffs_kept += 1

    drift_rate = (diffs_reverted / diffs_detected) if diffs_detected else 0.0

    return CTICReport(
        run_id=run_id,
        diffs_detected=diffs_detected,
        diffs_reverted=diffs_reverted,
        diffs_kept=diffs_kept,
        drift_rate=drift_rate,
        entries=entries,
    )


def revert_drift(report: CTICReport, working_state: dict) -> dict:
    state = deepcopy(working_state)
    for entry in report.entries:
        if not entry.reverted:
            continue
        comp = state.get(entry.competency_id)
        if isinstance(comp, dict) and entry.field in comp:
            comp[entry.field] = entry.before
    return state
