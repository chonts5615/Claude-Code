from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from pathlib import Path


class RunInputs(BaseModel):
    """Input files for a workflow run."""
    jobs_file: Path
    tech_comp_source_files: List[Path]
    core_leadership_file: Path
    output_template_file: Path


class ThresholdConfig(BaseModel):
    """Configurable thresholds for quality gates."""
    overlap_material: float = Field(0.82, ge=0.0, le=1.0)
    overlap_minor: float = Field(0.72, ge=0.0, le=1.0)
    distinctness_duplicate: float = Field(0.88, ge=0.0, le=1.0)
    min_responsibilities_per_job: int = Field(5, ge=1)
    top_n_competencies: int = Field(8, ge=1, le=12)
    min_responsibility_coverage: float = Field(0.80, ge=0.0, le=1.0)


class RunConfig(BaseModel):
    """Configuration for workflow execution."""
    top_n_competencies: int = 8
    thresholds: ThresholdConfig = Field(default_factory=ThresholdConfig)
    template_spec_path: Optional[Path] = None
    competency_format_spec_path: Optional[Path] = None


class ArtifactRegistry(BaseModel):
    """Registry of generated artifacts."""
    jobs_extracted: Optional[Path] = None
    competency_library: Optional[Path] = None
    competency_map_v1: Optional[Path] = None
    normalized_v2: Optional[Path] = None
    overlap_audit_v1: Optional[Path] = None
    clean_v3: Optional[Path] = None
    benchmarked_v4: Optional[Path] = None
    ranked_top8_v5: Optional[Path] = None
    populated_template: Optional[Path] = None
    final_review_package: Optional[Path] = None


class RunFlag(BaseModel):
    """Quality flag or warning."""
    step_id: str
    job_id: Optional[str] = None
    severity: str = Field(..., pattern="^(INFO|WARNING|ERROR|CRITICAL)$")
    flag_type: str
    message: str
    metadata: Dict = Field(default_factory=dict)


class QASummary(BaseModel):
    """Quality assurance summary for run."""
    total_jobs_processed: int
    total_competencies_identified: int
    flags_by_severity: Dict[str, int] = Field(default_factory=dict)
    coverage_metrics: Dict[str, float] = Field(default_factory=dict)
    unresolved_issues: List[str] = Field(default_factory=list)


class RunState(BaseModel):
    """Complete state of workflow run - passed between agents."""
    run_id: str
    run_timestamp_utc: datetime = Field(default_factory=datetime.utcnow)
    inputs: RunInputs
    config: RunConfig
    artifacts: ArtifactRegistry = Field(default_factory=ArtifactRegistry)
    flags: List[RunFlag] = Field(default_factory=list)
    qa_summary: Optional[QASummary] = None
    current_step: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Path: lambda v: str(v)
        }
