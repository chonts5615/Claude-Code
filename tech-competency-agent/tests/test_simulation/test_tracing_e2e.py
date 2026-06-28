"""End-to-end simulation: continuous tracing infrastructure (spec §30).

Verifies the contract that every gated decision, step transition, run, and
field-level change produces exactly one append-only JSONL line — and that
multi-run aggregation grows the ledger monotonically.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.tracing import (
    record_change,
    record_decision,
    record_review,
    record_run_complete,
    record_run_start,
    record_step_enter,
    record_step_exit,
)
from src.tracing.ledger import read_all


@pytest.fixture
def trace_root(tmp_path: Path, monkeypatch) -> Path:
    """Redirect tracing to a tmp_path so simulation tests don't pollute repo."""
    root = tmp_path / "trace"
    monkeypatch.chdir(tmp_path)
    return root


def test_single_run_emits_full_ledger_set(trace_root: Path):
    """One end-to-end TCB R1 run produces start + N step entries + decisions + complete."""
    run_id = "Finance_R1_20260425_aaaa1111"

    record_run_start(run_id, "TCB", stage="R1", family="Finance", root=trace_root)
    record_step_enter(run_id, "S1_extract_jobs", root=trace_root)
    record_decision(run_id, "5QMT", competency_candidate="Risk Modeling",
                    verdict="4/5 reuse-with-adapt", rationale="...", root=trace_root)
    record_step_exit(run_id, "S1_extract_jobs", root=trace_root)
    record_step_enter(run_id, "S3_normalize", root=trace_root)
    record_decision(run_id, "BOUNDARY", competency_id="TC-FIN-001",
                    verdict="TECHNICAL", matched_terms=["risk"], root=trace_root)
    record_decision(run_id, "CRITICALITY_RANK", competency_id="TC-FIN-001",
                    rank=1, weighted_score=0.853, root=trace_root)
    record_step_exit(run_id, "S3_normalize", root=trace_root)
    record_change(run_id, "TC-FIN-001", "definition",
                  before="old", after="new", source="SME",
                  rationale="SME feedback CHG-001", root=trace_root)
    record_run_complete(
        run_id,
        agents_run=["S1", "S3"],
        gates={"S1_Gate": "passed"},
        artifacts_produced=["data/output/Finance_R1.xlsx"],
        flag_summary={"INFO": 1, "WARNING": 0, "ERROR": 0},
        root=trace_root,
    )

    runs = read_all("run_ledger.jsonl", root=trace_root)
    steps = read_all("step_log.jsonl", root=trace_root)
    decisions = read_all("decision_log.jsonl", root=trace_root)
    changes = read_all("change_log.jsonl", root=trace_root)

    assert len(runs) == 2, "expected RUN_START + RUN_COMPLETE"
    assert runs[0]["event"] == "RUN_START"
    assert runs[1]["event"] == "RUN_COMPLETE"
    assert runs[1]["flag_summary"] == {"INFO": 1, "WARNING": 0, "ERROR": 0}

    assert len(steps) == 4, "two enter + two exit"
    assert [s["event"] for s in steps] == ["enter", "exit", "enter", "exit"]

    decisions_by_kind = {d["decision"] for d in decisions}
    assert decisions_by_kind == {"5QMT", "BOUNDARY", "CRITICALITY_RANK"}

    assert len(changes) == 1
    assert changes[0]["source"] == "SME"
    assert changes[0]["field"] == "definition"


def test_multi_run_aggregation_grows_monotonically(trace_root: Path):
    """Three sequential runs each append; total event count strictly increases."""
    counts: list[int] = []
    for i in range(3):
        run_id = f"Finance_R1_run{i}"
        record_run_start(run_id, "TCB", stage="R1", family="Finance", root=trace_root)
        record_decision(run_id, "5QMT", verdict=f"run-{i}-decision", root=trace_root)
        record_run_complete(run_id, root=trace_root)
        all_runs = read_all("run_ledger.jsonl", root=trace_root)
        counts.append(len(all_runs))

    assert counts == [2, 4, 6], f"run_ledger should accumulate 2 events per run; got {counts}"

    decisions = read_all("decision_log.jsonl", root=trace_root)
    assert len(decisions) == 3
    assert [d["verdict"] for d in decisions] == [
        "run-0-decision",
        "run-1-decision",
        "run-2-decision",
    ]


def test_ledger_lines_are_valid_jsonl(trace_root: Path):
    """Every line must be valid JSON with `at_utc` populated."""
    run_id = "X"
    record_run_start(run_id, "TCB", stage="R1", root=trace_root)
    record_step_enter(run_id, "step_A", root=trace_root)

    raw = (trace_root / "run_ledger.jsonl").read_text(encoding="utf-8").splitlines()
    for line in raw:
        record = json.loads(line)
        assert "at_utc" in record
        # ISO 8601 sanity check.
        assert "T" in record["at_utc"]


def test_review_log_records_severity_counts(trace_root: Path):
    """§31.4 review cycles persist severity counts and PR list."""
    record_review(
        "REV-001",
        findings=[
            {"id": "F1", "severity": "HIGH", "summary": "..."},
            {"id": "F2", "severity": "MEDIUM", "summary": "..."},
        ],
        severity_counts={"CRITICAL": 0, "HIGH": 1, "MEDIUM": 1, "LOW": 0},
        prs_opened=["https://github.com/.../pull/7"],
        triggered_by="OPERATOR",
        root=trace_root,
    )
    reviews = read_all("review_log.jsonl", root=trace_root)
    assert len(reviews) == 1
    r = reviews[0]
    assert r["severity_counts"]["HIGH"] == 1
    assert r["finding_count"] == 2
    assert r["prs_opened"] == ["https://github.com/.../pull/7"]
