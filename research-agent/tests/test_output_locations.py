"""Tests for deterministic output-location handling in agent.py.

Importing agent.py requires the claude_agent_sdk package; skip cleanly if it is
not installed (these are the only tests that need it).
"""

import pytest

pytest.importorskip("claude_agent_sdk")

from research_agent.agent import (  # noqa: E402
    OUTPUT_SUBDIRS,
    _analysis_done,
    _final_report_exists,
    _missing_notes,
    _parse_plan,
    _qa_verdict,
    ensure_output_dirs,
    with_output_locations,
)


def test_ensure_output_dirs_creates_tree(tmp_path):
    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    for sub in OUTPUT_SUBDIRS:
        assert (files_dir / sub).is_dir()


def test_with_output_locations_injects_absolute_paths(tmp_path):
    files_dir = tmp_path / "files"
    out = with_output_locations("ORIGINAL BODY", files_dir)

    assert "ORIGINAL BODY" in out
    assert "OUTPUT LOCATIONS" in out
    for sub in OUTPUT_SUBDIRS:
        assert str(files_dir / sub) in out


def test_final_report_exists(tmp_path):
    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    assert _final_report_exists(files_dir) is False
    (files_dir / "reports" / "report.pdf").write_bytes(b"%PDF-1.4")
    assert _final_report_exists(files_dir) is True


def test_parse_plan_extracts_and_normalizes():
    text = (
        "Here is the plan:\n"
        '[{"title": "Vendors", "filename": "vendors", "brief": "the market"},\n'
        ' {"title": "Methods", "filename": "/bad/methods.md", "brief": "psychometrics"}]\n'
        "thanks"
    )
    plan = _parse_plan(text)
    assert [s["filename"] for s in plan] == ["vendors.md", "bad_methods.md"]
    assert plan[0]["title"] == "Vendors"


def test_parse_plan_handles_garbage():
    assert _parse_plan("no json here") == []


def test_missing_notes_tracks_written_files(tmp_path):
    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    plan = [{"title": "A", "filename": "a.md", "brief": ""},
            {"title": "B", "filename": "b.md", "brief": ""}]
    assert {s["filename"] for s in _missing_notes(files_dir, plan)} == {"a.md", "b.md"}
    (files_dir / "research_notes" / "a.md").write_text("x")
    assert [s["filename"] for s in _missing_notes(files_dir, plan)] == ["b.md"]


def test_analysis_done_detects_charts_or_data(tmp_path):
    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    assert _analysis_done(files_dir) is False
    (files_dir / "charts" / "c1.png").write_bytes(b"\x89PNG")
    assert _analysis_done(files_dir) is True


def test_qa_verdict_parsing(tmp_path):
    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    assert _qa_verdict(files_dir) == "UNKNOWN"
    qa = files_dir / "reports" / "qa_review.md"
    qa.write_text("## Summary\nlooks fine\n\nQA VERDICT: PASS\n")
    assert _qa_verdict(files_dir) == "PASS"
    qa.write_text("issues found\nQA VERDICT: REVISE")
    assert _qa_verdict(files_dir) == "REVISE"
