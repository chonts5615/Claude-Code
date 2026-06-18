"""Tests for deterministic output-location handling in agent.py.

Importing agent.py requires the claude_agent_sdk package; skip cleanly if it is
not installed (these are the only tests that need it).
"""

import pytest

pytest.importorskip("claude_agent_sdk")

from research_agent.agent import (  # noqa: E402
    OUTPUT_SUBDIRS,
    _continuation_prompt,
    _final_report_exists,
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


def test_continuation_prompt_reflects_state(tmp_path):
    files_dir = tmp_path / "files"
    ensure_output_dirs(files_dir)
    # Nothing yet.
    assert "NONE" in _continuation_prompt(files_dir)
    # Add a note; it should be listed and .gitkeep ignored.
    (files_dir / "research_notes" / "sub1.md").write_text("x")
    prompt = _continuation_prompt(files_dir)
    assert "sub1.md" in prompt
    assert ".gitkeep" not in prompt
