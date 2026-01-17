from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class OverlapFlag(BaseModel):
    """Individual overlap detection."""
    competency_id: str
    competency_name: str
    overlap_severity: str = Field(..., pattern="^(NONE|MINOR|MATERIAL)$")
    overlap_target_domain: Optional[str] = None
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    rationale: str
    suggested_action: str = Field(
        ...,
        pattern="^(KEEP|REVISE|REMOVE|REPLACE|REVIEW)$"
    )


class DistinctnessFlag(BaseModel):
    """Competency distinctness issue within job."""
    competency_id_1: str
    competency_id_2: str
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    conflict_type: str = Field(
        ...,
        pattern="^(DUPLICATE|NEAR_DUPLICATE|SEMANTIC_OVERLAP|OTHER)$"
    )
    resolution_recommendation: str


class JobOverlapAudit(BaseModel):
    """Overlap audit for single job."""
    job_id: str
    overlap_flags: List[OverlapFlag] = Field(default_factory=list)
    distinctness_flags: List[DistinctnessFlag] = Field(default_factory=list)

    material_overlap_count: int = 0
    minor_overlap_count: int = 0
    distinctness_conflict_count: int = 0

    audit_passed: bool
    blocking_issues: List[str] = Field(default_factory=list)


class OverlapAuditOutput(BaseModel):
    """Output from Step 4 - Overlap Audit."""
    job_audits: List[JobOverlapAudit]
    total_material_overlaps: int
    total_distinctness_conflicts: int
    jobs_requiring_remediation: List[str]
    audit_timestamp: str


class RemediationAction(BaseModel):
    """Action taken to resolve overlap."""
    competency_id: str
    original_name: str
    action_taken: str = Field(
        ...,
        pattern="^(REMOVED|REVISED_DEFINITION|REVISED_INDICATORS|REPLACED|NO_ACTION)$"
    )
    revised_name: Optional[str] = None
    revision_details: Optional[str] = None
    before_snapshot: Optional[Dict] = None
    after_snapshot: Optional[Dict] = None
    remediation_rationale: str


class JobRemediationLog(BaseModel):
    """Remediation log for single job."""
    job_id: str
    remediation_actions: List[RemediationAction]

    removed_count: int = 0
    revised_count: int = 0
    replaced_count: int = 0


class OverlapRemediationOutput(BaseModel):
    """Output from Step 5 - Overlap Remediation."""
    job_remediation_logs: List[JobRemediationLog]
    total_remediations: int
    reaudit_required: bool
