"""BCO Ledger — system of record for Boundary, Coverage, Overlap tracking."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from src.schemas.boundary import BoundaryClass


class BoundaryEntry(BaseModel):
    competency_id: str
    competency_name: str
    classification: BoundaryClass
    confidence: float = Field(..., ge=0.0, le=1.0)
    rationale: str


class CoverageEntry(BaseModel):
    job_id: str
    job_title: str
    family: str
    technical_ef_count: int
    technical_ef_covered: int
    coverage_rate: float = Field(..., ge=0.0, le=1.0)
    uncovered_ef_ids: List[str] = Field(default_factory=list)
    meets_90_threshold: bool


class OverlapEntry(BaseModel):
    competency_id_a: str
    competency_id_b: str
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    severity: Literal["NONE", "MINOR", "MATERIAL"]
    resolution: Optional[str] = None


class BCOLedger(BaseModel):
    run_id: str
    stage: str
    boundary: List[BoundaryEntry] = Field(default_factory=list)
    coverage: List[CoverageEntry] = Field(default_factory=list)
    overlap: List[OverlapEntry] = Field(default_factory=list)
    timestamp_utc: str
