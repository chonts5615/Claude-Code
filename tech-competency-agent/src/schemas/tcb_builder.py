from typing import Dict, List, Literal

from pydantic import BaseModel, Field

LevelKey = Literal["L1", "L2", "L3", "L4"]


class LevelIndicators(BaseModel):
    """Behavioral indicators grouped by level."""

    indicators: List[str] = Field(default_factory=list)


class BuilderCompetency(BaseModel):
    """Competency format expected by the TCB standards validator."""

    competency_id: str
    title: str
    definition: str
    technical_efs_covered: List[str] = Field(default_factory=list)
    level_indicators: Dict[LevelKey, List[str]]


class JobFamilyCompetencySet(BaseModel):
    """Job-family package containing technical competencies."""

    job_family: str
    technical_efs_total: List[str] = Field(default_factory=list)
    competencies: List[BuilderCompetency]


class TCBValidationIssue(BaseModel):
    """A single validation issue raised by standards checks."""

    severity: Literal["ERROR", "WARNING"]
    code: str
    field: str
    message: str


class CompetencyValidationResult(BaseModel):
    """Validation output for one competency."""

    competency_id: str
    is_valid: bool
    issues: List[TCBValidationIssue] = Field(default_factory=list)


class JobFamilyValidationResult(BaseModel):
    """Validation output for one job family package."""

    job_family: str
    competency_results: List[CompetencyValidationResult]
    package_coverage_rate: float = Field(ge=0.0, le=1.0)
    package_is_valid: bool


class TCBValidationReport(BaseModel):
    """Top-level standards validation report."""

    total_job_families: int
    total_competencies: int
    valid_competencies: int
    report_is_valid: bool
    results: List[JobFamilyValidationResult]
