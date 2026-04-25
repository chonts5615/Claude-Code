"""CTIC character-level diff + drift detection."""

from __future__ import annotations

from src.utils import ctic_diff


def test_compute_diff_no_change():
    n, _ = ctic_diff.compute_diff("hello world", "hello world")
    assert n == 0


def test_compute_diff_with_change():
    n, _ = ctic_diff.compute_diff("hello world", "hello brave world")
    assert n > 0


def test_check_drift_reverts_non_targeted_changes():
    before = {
        "c1": {"name": "Alpha", "definition": "A definition that does not change."},
        "c2": {"name": "Beta", "definition": "Original beta definition kept stable for non-target."},
    }
    after = {
        "c1": {"name": "Alpha 2", "definition": "A definition that does not change."},
        "c2": {"name": "Beta", "definition": "Drifted beta definition (should be reverted)."},
    }
    targeted = {"c1:name"}
    report = ctic_diff.check_drift(before, after, targeted)
    drifted = [d for d in report.entries if not d.is_targeted_by_feedback and d.char_diff_count > 0]
    assert any(d.competency_id == "c2" and d.field == "definition" for d in drifted)
    targeted_diffs = [d for d in report.entries if d.is_targeted_by_feedback]
    assert any(d.competency_id == "c1" and d.field == "name" for d in targeted_diffs)


def test_revert_drift_restores_before_values():
    before = {"c2": {"definition": "original"}}
    after = {"c2": {"definition": "drifted"}}
    targeted: set = set()
    report = ctic_diff.check_drift(before, after, targeted)
    reverted_state = ctic_diff.revert_drift(report, after)
    assert reverted_state["c2"]["definition"] == "original"
