"""Pytest fixtures for testing."""

import pytest
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

from src.schemas.run_state import RunState, RunInputs, RunConfig, ThresholdConfig
from src.schemas.job import Job, Responsibility, JobSummary, SourceMetadata


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_job():
    """Sample job for testing."""
    return Job(
        job_id="JOB_0001",
        job_title="Data Scientist",
        job_family="Analytics",
        job_level="Senior",
        job_summary=JobSummary(
            raw_text="Analyzes data and builds models",
            normalized_text="Analyzes data and builds models"
        ),
        responsibilities=[
            Responsibility(
                responsibility_id="JOB_0001_R001",
                raw_text="Develop machine learning models",
                normalized_text="Develop machine learning models",
                priority_hint="HIGH"
            ),
            Responsibility(
                responsibility_id="JOB_0001_R002",
                raw_text="Analyze datasets",
                normalized_text="Analyze datasets",
                priority_hint="HIGH"
            ),
            Responsibility(
                responsibility_id="JOB_0001_R003",
                raw_text="Create visualizations",
                normalized_text="Create visualizations",
                priority_hint="MEDIUM"
            ),
            Responsibility(
                responsibility_id="JOB_0001_R004",
                raw_text="Present findings to stakeholders",
                normalized_text="Present findings to stakeholders",
                priority_hint="MEDIUM"
            ),
            Responsibility(
                responsibility_id="JOB_0001_R005",
                raw_text="Maintain documentation",
                normalized_text="Maintain documentation",
                priority_hint="LOW"
            ),
        ],
        source_metadata=SourceMetadata(
            sheet_name="Jobs",
            row_index=2,
            column_mapping={},
            extraction_timestamp=datetime.utcnow().isoformat()
        )
    )


@pytest.fixture
def sample_threshold_config():
    """Sample threshold configuration."""
    return ThresholdConfig(
        overlap_material=0.82,
        overlap_minor=0.72,
        distinctness_duplicate=0.88,
        min_responsibilities_per_job=5,
        top_n_competencies=8,
        min_responsibility_coverage=0.80
    )


@pytest.fixture
def sample_run_config(sample_threshold_config):
    """Sample run configuration."""
    return RunConfig(
        top_n_competencies=8,
        thresholds=sample_threshold_config
    )


@pytest.fixture
def sample_run_inputs(temp_dir):
    """Sample run inputs."""
    # Create dummy input files
    jobs_file = temp_dir / "jobs.xlsx"
    jobs_file.touch()

    tech_file = temp_dir / "tech_comps.xlsx"
    tech_file.touch()

    leadership_file = temp_dir / "leadership.xlsx"
    leadership_file.touch()

    template_file = temp_dir / "template.xlsx"
    template_file.touch()

    return RunInputs(
        jobs_file=jobs_file,
        tech_comp_source_files=[tech_file],
        core_leadership_file=leadership_file,
        output_template_file=template_file
    )


@pytest.fixture
def sample_run_state(sample_run_inputs, sample_run_config):
    """Sample run state."""
    return RunState(
        run_id="test_run_001",
        inputs=sample_run_inputs,
        config=sample_run_config
    )
