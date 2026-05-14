"""Contract parity checks for quality gate documentation and threshold config."""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
THRESHOLDS_PATH = REPO_ROOT / "config" / "thresholds.yaml"
GATES_DOC_PATH = REPO_ROOT / "docs" / "validation_rules" / "quality_gates.md"


def test_ranking_threshold_values_match_v32_contract():
    """Ensure ranking thresholds are pinned to the v3.2 contract values."""
    with THRESHOLDS_PATH.open("r", encoding="utf-8") as f:
        thresholds = yaml.safe_load(f)

    ranking = thresholds["ranking"]
    assert ranking["top_n_competencies"] == 6
    assert ranking["min_responsibility_coverage"] == 0.90
    assert ranking["min_competencies_per_job"] == 6
    assert ranking["max_competencies_per_job"] == 6


def test_quality_gate_doc_mentions_current_ranking_contract():
    """Ensure quality gate doc reflects configured ranking thresholds."""
    text = GATES_DOC_PATH.read_text(encoding="utf-8")

    assert "Average coverage <90% of responsibilities" in text
    assert "Top N Must Equal 6" in text
    assert "count different from 6 ranked competencies" in text
