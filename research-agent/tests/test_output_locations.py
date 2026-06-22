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


def test_build_options_raises_buffer(tmp_path):
    from research_agent.agent import MAX_BUFFER_SIZE, build_options
    from research_agent.utils.subagent_tracker import SubagentTracker

    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    opts = build_options(files_dir, SubagentTracker(None, tmp_path), "haiku")
    assert opts.max_buffer_size == MAX_BUFFER_SIZE
    assert MAX_BUFFER_SIZE > 1024 * 1024  # bigger than the SDK default


def test_heavy_model_never_below_sonnet():
    from research_agent.agent import heavy_model

    assert heavy_model("haiku") == "sonnet"
    assert heavy_model("sonnet") == "sonnet"
    assert heavy_model("opus") == "opus"


def test_delegated_subagents_and_skill_docs_exist(tmp_path):
    from research_agent.agent import DEFAULT_BRAND_CONFIG, PROJECT_DIR, build_options
    from research_agent.utils.subagent_tracker import SubagentTracker

    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    opts = build_options(files_dir, SubagentTracker(None, tmp_path), "haiku")
    # Only research + analysis are delegated to subagents; report/QA run as
    # controlled queries, not subagents.
    assert set(opts.agents) == {"researcher", "data-analyst"}
    # the skill specs exist as docs (their behavior is embedded in code/prompts)
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


def test_render_pdf_from_markdown(tmp_path):
    from research_agent.render import render_report_pdf

    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    (files_dir / "research_notes" / "n.md").write_text("x")
    (files_dir / "reports" / "report.md").write_text(
        "# Test Report\n\n## Summary\nA **bold** finding: r = 0.42.\n\n- bullet one\n- bullet two\n"
    )
    out = render_report_pdf(
        files_dir / "reports" / "report.md",
        files_dir / "charts",
        files_dir / "reports" / "report.pdf",
        None,
    )
    assert out.exists() and out.stat().st_size > 1000
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


def test_strip_to_markdown_keeps_full_report_with_inner_fence():
    from research_agent.agent import _strip_to_markdown

    # A report containing an inner ``` calculation block must NOT be truncated to
    # that block (the original bug).
    report = (
        "# Title\n\n## Executive Summary\nThe recommendation.\n\n"
        "```\nROI = 90000 / 30000 = 300%\n```\n\n## Conclusion\nDone.\n"
    )
    out = _strip_to_markdown("Here is the report:\n\n" + report)
    assert out.startswith("# Title")
    assert "## Conclusion" in out  # not truncated at the inner fence
    # A fully fenced response is unwrapped.
    assert _strip_to_markdown("```markdown\n" + report + "\n```").startswith("# Title")


def test_cleanup_outputs_removes_strays(tmp_path):
    from research_agent.agent import cleanup_outputs

    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    reports = files_dir / "reports"
    # canonical
    (reports / "report.md").write_text("x")
    (reports / "report.pdf").write_bytes(b"%PDF")
    (reports / "qa_review.md").write_text("QA VERDICT: PASS")
    # strays
    (reports / "Multi_Method_Report.pdf").write_bytes(b"%PDF")
    (reports / "build_pdf.py").write_text("print(1)")
    (files_dir / "charts" / "01_chart.py").write_text("print(1)")
    (files_dir / "charts" / "01_chart.png").write_bytes(b"\x89PNG")

    cleanup_outputs(files_dir)

    assert {p.name for p in reports.iterdir() if p.is_file()} == {
        "report.md", "report.pdf", "qa_review.md",
    }
    assert not list(files_dir.rglob("*.py"))  # stray scripts gone
    assert (files_dir / "charts" / "01_chart.png").exists()  # real output kept


def test_reset_output_dirs_clears_artifacts_but_keeps_gitkeep(tmp_path):
    from research_agent.agent import ensure_output_dirs, reset_output_dirs

    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    (files_dir / "research_notes" / "a.md").write_text("x")
    (files_dir / "research_notes" / ".gitkeep").write_text("")
    (files_dir / "charts" / "c.png").write_bytes(b"\x89PNG")
    reset_output_dirs(files_dir)
    assert not (files_dir / "research_notes" / "a.md").exists()
    assert not (files_dir / "charts" / "c.png").exists()
    assert (files_dir / "research_notes" / ".gitkeep").exists()


def test_plan_from_notes_reconstructs_plan(tmp_path):
    from research_agent.agent import _plan_from_notes, ensure_output_dirs

    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    (files_dir / "research_notes" / "vendor_landscape.md").write_text("x")
    (files_dir / "research_notes" / "psychometrics.md").write_text("y")
    plan = _plan_from_notes(files_dir)
    assert [s["filename"] for s in plan] == ["psychometrics.md", "vendor_landscape.md"]
    assert plan[0]["title"] == "Psychometrics"


def test_max_qa_rounds_is_a_positive_cap():
    from research_agent.agent import MAX_QA_ROUNDS

    assert isinstance(MAX_QA_ROUNDS, int) and MAX_QA_ROUNDS >= 1


def test_qa_verdict_parsing(tmp_path):
    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    assert _qa_verdict(files_dir) == "UNKNOWN"
    qa = files_dir / "reports" / "qa_review.md"
    qa.write_text("## Summary\nlooks fine\n\nQA VERDICT: PASS\n")
    assert _qa_verdict(files_dir) == "PASS"
    qa.write_text("issues found\nQA VERDICT: REVISE")
    assert _qa_verdict(files_dir) == "REVISE"
