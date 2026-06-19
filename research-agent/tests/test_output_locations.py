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


def test_build_options_raises_buffer_and_registers_qa(tmp_path):
    from research_agent.agent import MAX_BUFFER_SIZE, build_options
    from research_agent.utils.subagent_tracker import SubagentTracker

    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    opts = build_options(files_dir, SubagentTracker(None, tmp_path), "haiku")
    assert opts.max_buffer_size == MAX_BUFFER_SIZE
    assert MAX_BUFFER_SIZE > 1024 * 1024  # bigger than the SDK default
    assert "qa-reviewer" in opts.agents


def test_heavy_model_never_below_sonnet():
    from research_agent.agent import heavy_model

    assert heavy_model("haiku") == "sonnet"
    assert heavy_model("sonnet") == "sonnet"
    assert heavy_model("opus") == "opus"


def test_skills_attached_and_discoverable(tmp_path):
    from research_agent.agent import DEFAULT_BRAND_CONFIG, PROJECT_DIR, build_options
    from research_agent.utils.subagent_tracker import SubagentTracker

    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    opts = build_options(files_dir, SubagentTracker(None, tmp_path), "haiku")
    assert opts.agents["report-writer"].skills == ["report-branding"]
    assert "io-psych-exec-review" in opts.agents["qa-reviewer"].skills
    assert "report-format-qc" in opts.agents["qa-reviewer"].skills
    # the heavy agents must not run below sonnet
    assert opts.agents["report-writer"].model == "sonnet"
    assert opts.agents["qa-reviewer"].model == "sonnet"
    # skills live under the project .claude and the default brand config exists
    for name in ("report-branding", "report-format-qc", "io-psych-exec-review"):
        assert (PROJECT_DIR / ".claude" / "skills" / name / "SKILL.md").exists()
    assert DEFAULT_BRAND_CONFIG.exists()


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


def test_report_done_requires_markdown_and_pdf(tmp_path):
    from research_agent.agent import _report_done, _report_missing

    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    assert _report_done(files_dir) is False
    assert "files/reports/report.md" in _report_missing(files_dir)

    (files_dir / "reports" / "report.pdf").write_bytes(b"%PDF-1.4")
    assert _report_done(files_dir) is False  # md still missing
    assert _report_missing(files_dir) == ["files/reports/report.md"]

    (files_dir / "reports" / "report.md").write_text("# report")
    assert _report_done(files_dir) is True
    assert _report_missing(files_dir) == []


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
