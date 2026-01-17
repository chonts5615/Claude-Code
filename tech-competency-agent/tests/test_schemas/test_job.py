"""Tests for job schemas."""

import pytest
from src.schemas.job import Job, Responsibility, JobSummary, SourceMetadata


def test_job_creation(sample_job):
    """Test job creation with valid data."""
    assert sample_job.job_id == "JOB_0001"
    assert sample_job.job_title == "Data Scientist"
    assert sample_job.responsibility_count() == 5


def test_responsibility_creation():
    """Test responsibility creation."""
    resp = Responsibility(
        responsibility_id="TEST_R001",
        raw_text="Test responsibility",
        normalized_text="test responsibility",
        priority_hint="HIGH"
    )
    assert resp.responsibility_id == "TEST_R001"
    assert resp.priority_hint == "HIGH"


def test_invalid_priority_hint():
    """Test that invalid priority hint raises error."""
    with pytest.raises(ValueError):
        Responsibility(
            responsibility_id="TEST_R001",
            raw_text="Test",
            normalized_text="test",
            priority_hint="INVALID"
        )


def test_job_summary():
    """Test job summary creation."""
    summary = JobSummary(
        raw_text="Original summary text",
        normalized_text="Normalized summary text"
    )
    assert summary.raw_text == "Original summary text"
    assert summary.normalized_text == "Normalized summary text"
