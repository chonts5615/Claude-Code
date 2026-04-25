from datetime import datetime
from pathlib import Path
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class RunInputs(BaseModel):
    """Input files for a workflow run.

    `jobs_file` is required for stage R1 (enforced at the CLI / orchestrator
    boundary) but may be omitted for R2/FINAL/RESUME runs that operate on
    artifacts from an earlier run.
    """
    jobs_file: Optional[Path] = None
    tech_comp_source_files: List[Path] = Field(default_factory=list)
    core_leadership_file: Optional[Path] = None
    output_template_file: Optional[Path] = None
    feedback_file: Optional[Path] = None  # R2/FINAL stages


class ThresholdConfig(BaseModel):
    """v3.1 quality gate thresholds."""
    overlap_material: float = Field(0.82, ge=0.0, le=1.0)
    overlap_minor: float = Field(0.72, ge=0.0, le=1.0)
    distinctness_duplicate: float = Field(0.88, ge=0.0, le=1.0)
    min_responsibilities_per_job: int = Field(3, ge=1)        # v3.1: 3
    top_n_competencies: int = Field(6, ge=1, le=6)             # v3.1: hard cap 6
    min_responsibility_coverage: float = Field(0.90, ge=0.0, le=1.0)  # v3.1: 90%
    max_drift_rate: float = Field(0.05, ge=0.0, le=1.0)
    max_qa_cycles: int = Field(3, ge=1)


class RunConfig(BaseModel):
    """Configuration for workflow execution."""
    stage: Literal["R1", "R2", "FINAL", "RESUME"] = "R1"
    family: Optional[str] = None
    top_n_competencies: int = 6
    thresholds: ThresholdConfig = Field(default_factory=ThresholdConfig)
    template_spec_path: Optional[Path] = None
    competency_format_spec_path: Optional[Path] = None


class ArtifactRegistry(BaseModel):
    """Registry of generated artifacts."""
    # R1 pipeline
    jobs_extracted: Optional[Path] = None
    competency_library: Optional[Path] = None
    competency_map_v1: Optional[Path] = None
    normalized_v2: Optional[Path] = None
    overlap_audit_v1: Optional[Path] = None
    clean_v3: Optional[Path] = None
    benchmarked_v4: Optional[Path] = None
    ranked_top8_v5: Optional[Path] = None
    normalized_competencies_v2: Optional[Path] = None  # alias for gate validator
    normalized_competencies_v3: Optional[Path] = None
    populated_template: Optional[Path] = None
    final_review_package: Optional[Path] = None

    # v3.1 deliverables
    library_master: Optional[Path] = None
    job_family_package: Optional[Path] = None
    sme_package: Optional[Path] = None
    bco_ledger: Optional[Path] = None
    hrlt_summary: Optional[Path] = None
    change_log: Optional[Path] = None
    rosetta_stone: Optional[Path] = None

    # v3.1 R2/FINAL phase artifacts
    pre_feedback_snapshot: Optional[Path] = None
    feedback_batch: Optional[Path] = None
    coverage_refresh: Optional[Path] = None      # 6E-bis
    boundary_rescan: Optional[Path] = None       # 6E-ter
    overlap_reaudit: Optional[Path] = None       # 6E-quater
    ctic_report: Optional[Path] = None           # 6F
    post_ctic_state: Optional[Path] = None       # 6F: post-feedback state after non-targeted drift reverts
    focus_group_package: Optional[Path] = None   # 6G
    learning_synthesis: Optional[Path] = None    # Phase 7


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
    # Pydantic v2 serializes datetime/Path natively via model_dump_json; no
    # legacy json_encoders needed. arbitrary_types_allowed kept for safety on
    # any future field additions.
    model_config = ConfigDict(arbitrary_types_allowed=True)

    run_id: str
    run_timestamp_utc: datetime = Field(default_factory=datetime.utcnow)
    inputs: RunInputs
    config: RunConfig
    artifacts: ArtifactRegistry = Field(default_factory=ArtifactRegistry)
    flags: List[RunFlag] = Field(default_factory=list)
    qa_summary: Optional[QASummary] = None
    current_step: Optional[str] = None
