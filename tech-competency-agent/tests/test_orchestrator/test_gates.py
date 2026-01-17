"""Tests for quality gates."""

from src.orchestrator.gates import QualityGate, ValidationResult


def test_validation_result_creation():
    """Test validation result creation."""
    result = ValidationResult(
        rule_name="test_rule",
        passed=True,
        severity="INFO",
        message="Test passed",
        metadata={"key": "value"}
    )
    assert result.rule_name == "test_rule"
    assert result.passed is True
    assert result.severity == "INFO"


def test_quality_gate_initialization(sample_threshold_config):
    """Test quality gate initialization."""
    gate = QualityGate("TEST_GATE", sample_threshold_config)
    assert gate.gate_id == "TEST_GATE"
    assert gate.thresholds.overlap_material == 0.82
