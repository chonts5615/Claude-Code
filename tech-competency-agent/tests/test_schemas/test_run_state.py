"""Tests for run state schemas."""

from src.schemas.run_state import RunFlag, ThresholdConfig


def test_run_state_creation(sample_run_state):
    """Test run state creation."""
    assert sample_run_state.run_id == "test_run_001"
    assert len(sample_run_state.flags) == 0
    assert sample_run_state.config.top_n_competencies == 6  # v3.1


def test_threshold_config_defaults():
    """v3.1 threshold defaults."""
    config = ThresholdConfig()
    assert config.overlap_material == 0.82
    assert config.overlap_minor == 0.72
    assert config.min_responsibilities_per_job == 3
    assert config.top_n_competencies == 6
    assert config.min_responsibility_coverage == 0.90
    assert config.max_drift_rate == 0.05


def test_run_flag_creation():
    """Test run flag creation."""
    flag = RunFlag(
        step_id="S1",
        severity="WARNING",
        flag_type="MISSING_SUMMARY",
        message="Job missing summary",
        metadata={"job_id": "JOB_001"}
    )
    assert flag.step_id == "S1"
    assert flag.severity == "WARNING"


def test_invalid_severity():
    """Test that invalid severity raises error."""
    import pytest
    with pytest.raises(ValueError):
        RunFlag(
            step_id="S1",
            severity="INVALID",
            flag_type="TEST",
            message="Test message"
        )


def test_run_inputs_jobs_file_optional():
    """R2/FINAL/RESUME runs may omit jobs_file (consume artifacts instead)."""
    from pathlib import Path

    from src.schemas.run_state import RunInputs

    inputs = RunInputs(jobs_file=None, feedback_file=Path("data/feedback.json"))
    assert inputs.jobs_file is None
    assert inputs.feedback_file == Path("data/feedback.json")


def test_run_state_serializes_path_and_datetime():
    """Verify Pydantic v2 ConfigDict (no legacy json_encoders) still serializes
    Path and datetime cleanly."""
    import json
    from pathlib import Path

    from src.schemas.run_state import RunConfig, RunInputs, RunState

    state = RunState(
        run_id="t",
        inputs=RunInputs(jobs_file=Path("x.xlsx")),
        config=RunConfig(),
    )
    payload = json.loads(state.model_dump_json())
    assert payload["run_id"] == "t"
    assert payload["inputs"]["jobs_file"] == "x.xlsx"
    assert "T" in payload["run_timestamp_utc"]  # ISO format


def test_artifact_registry_has_post_ctic_state():
    """6F revert path requires a dedicated artifact pointer."""
    from src.schemas.run_state import ArtifactRegistry

    reg = ArtifactRegistry()
    assert hasattr(reg, "post_ctic_state")
    assert reg.post_ctic_state is None
