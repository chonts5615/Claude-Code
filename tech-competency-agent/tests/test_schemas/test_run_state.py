"""Tests for run state schemas."""

from src.schemas.run_state import RunFlag, ThresholdConfig


def test_run_state_creation(sample_run_state):
    """Test run state creation."""
    assert sample_run_state.run_id == "test_run_001"
    assert len(sample_run_state.flags) == 0
    assert sample_run_state.config.top_n_competencies == 6


def test_threshold_config_defaults():
    """Test threshold config with defaults."""
    config = ThresholdConfig()
    assert config.overlap_material == 0.82
    assert config.overlap_minor == 0.72
    assert config.min_responsibilities_per_job == 5
    assert config.top_n_competencies == 6
    assert config.min_responsibility_coverage == 0.90
    assert config.min_competencies_per_job == 6
    assert config.max_competencies_per_job == 6


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
