"""Skill mapping data contracts."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from src.schemas.competency import IntegrityTag, LevelCode

Modality = Literal["ELEARNING", "ILT", "COACHING", "OJT", "BLENDED"]
GapSeverity = Literal["INFO", "WARNING", "CRITICAL"]


class TrainingItem(BaseModel):
    course_id: str
    title: str
    description: str = ""
    learning_objectives: List[str] = Field(default_factory=list)
    duration_hours: float = 0.0
    modality: Modality = "ELEARNING"
    audience_band: Optional[str] = None
    prerequisites: List[str] = Field(default_factory=list)
    vendor: Optional[str] = None


class BloomLevelEstimate(BaseModel):
    level: LevelCode
    confidence: float = Field(..., ge=0.0, le=1.0)
    evidence_verbs: List[str] = Field(default_factory=list)
    verb_counts: dict = Field(default_factory=dict)  # {L1: int, ...}
    adjustments_applied: List[str] = Field(default_factory=list)


class SkillCompetencyMapping(BaseModel):
    course_id: str
    competency_id: str
    competency_name: str
    level: LevelCode
    confidence: float = Field(..., ge=0.0, le=1.0)
    rationale: str
    bloom_evidence: List[str] = Field(default_factory=list)
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    integrity_tag: IntegrityTag
    mismatch_flags: List[str] = Field(default_factory=list)


class CoverageCell(BaseModel):
    competency_id: str
    competency_name: str
    level: LevelCode
    course_ids: List[str] = Field(default_factory=list)
    count: int = 0
    has_gap: bool = False


class GapFinding(BaseModel):
    competency_id: str
    competency_name: str
    level: LevelCode
    severity: GapSeverity
    recommendation: str


class SurplusFinding(BaseModel):
    course_id: str
    title: str
    reason: str  # NO_TECHNICAL_MATCH | LIKELY_VB_OR_COMMON | AUDIENCE_LEVEL_MISMATCH
    max_similarity: float
