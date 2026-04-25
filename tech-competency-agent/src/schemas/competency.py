"""v3.1 competency schemas.

Hard-cut migration from v3.0 (FOUNDATIONAL/WORKING/ADVANCED/EXPERT, flat
indicators) to v3.1 (L1-L4, exactly 3 indicators per level, single-sentence
definitions, boundary classification, source integrity tags).

No backward-compat shims — repo is internal and nothing in production runs the
v3.0 schema.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class LevelCode(str, Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"


IntegrityTag = Literal["CONFIRMED", "CORRECTED", "UNVERIFIABLE", "FLAGGED"]
BoundaryClass = Literal["V_AND_B", "COMMON", "TECHNICAL", "MIXED"]


class BehavioralIndicator(BaseModel):
    """One observable behavior at a specific proficiency level.

    Each indicator is tagged against the four Level Differentiation Rubric
    dimensions so QA can verify L3 indicators show stronger autonomy/scope
    than L1 indicators.
    """

    text: str = Field(..., min_length=1)
    autonomy: Optional[str] = None
    scope: Optional[str] = None
    complexity: Optional[str] = None
    contribution: Optional[str] = None
    integrity_tag: IntegrityTag = "CONFIRMED"


class ProficiencyLevel(BaseModel):
    """One of L1-L4. v3.1 requires exactly 3 indicators per level."""

    level: LevelCode
    description: str = Field(..., min_length=1)
    indicators: List[BehavioralIndicator]

    @field_validator("indicators")
    @classmethod
    def exactly_three_indicators(cls, v: List[BehavioralIndicator]) -> List[BehavioralIndicator]:
        if len(v) != 3:
            raise ValueError(f"v3.1 requires exactly 3 indicators per level; got {len(v)}")
        return v


class SourceEvidence(BaseModel):
    source_id: str
    source_type: Literal["EXCEL", "WORD", "PDF", "WEB", "ONET", "ESCO", "SFIA", "NICE", "OTHER"]
    source_title: str
    excerpt: str
    location: Optional[str] = None
    retrieval_date_utc: Optional[str] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    integrity_tag: IntegrityTag = "UNVERIFIABLE"


class CompetencyLibraryEntry(BaseModel):
    competency_id: str
    name: str
    definition: str
    indicators: List[str] = Field(default_factory=list)
    proficiency_levels: List[ProficiencyLevel] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    source_evidence: List[SourceEvidence] = Field(default_factory=list)


class CompetencyLibrary(BaseModel):
    competencies: List[CompetencyLibraryEntry]
    total_sources_processed: int
    ingestion_timestamp: str


class AppliedScope(BaseModel):
    tools_methods_tech: List[str] = Field(default_factory=list)
    standards_frameworks: List[str] = Field(default_factory=list)
    typical_outputs: List[str] = Field(default_factory=list)


class ResponsibilityTrace(BaseModel):
    responsibility_id: str
    contribution: Literal["PRIMARY", "SECONDARY", "SUPPORTING"]
    justification: str


class OverlapCheck(BaseModel):
    core_leadership_overlap: Literal["NONE", "MINOR", "MATERIAL"]
    overlap_domains: List[str] = Field(default_factory=list)
    similarity_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    remediation_notes: Optional[str] = None


class BenchmarkingRecord(BaseModel):
    benchmarked_against: List[str] = Field(default_factory=list)
    changes_made: Optional[str] = None
    evidence_refs: List[str] = Field(default_factory=list)
    benchmark_alignment_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class CriticalityBreakdown(BaseModel):
    """v3.1 four-factor criticality (Coverage 0.40, Criticality 0.30,
    Distinctiveness 0.20, Assessability 0.10)."""

    coverage: float = Field(..., ge=0.0, le=1.0)
    criticality: float = Field(..., ge=0.0, le=1.0)
    distinctiveness: float = Field(..., ge=0.0, le=1.0)
    assessability: float = Field(..., ge=0.0, le=1.0)

    @property
    def weighted_score(self) -> float:
        return (
            0.40 * self.coverage
            + 0.30 * self.criticality
            + 0.20 * self.distinctiveness
            + 0.10 * self.assessability
        )


def _word_count(text: str) -> int:
    return len([w for w in text.split() if w.strip()])


class TechnicalCompetency(BaseModel):
    """v3.1 technical competency.

    Invariants enforced:
    - title 3-6 words
    - definition 15-25 words, exactly one sentence (one terminal period)
    - exactly 4 ProficiencyLevels in order [L1, L2, L3, L4]
    - each level has exactly 3 indicators (enforced by ProficiencyLevel)
    - boundary_class is set explicitly
    """

    competency_id: str
    name: str
    definition: str
    why_it_matters: str
    proficiency_levels: List[ProficiencyLevel]
    boundary_class: BoundaryClass
    integrity_tag: IntegrityTag = "CONFIRMED"
    applied_scope: AppliedScope
    responsibility_trace: List[ResponsibilityTrace] = Field(default_factory=list)
    overlap_check: OverlapCheck
    benchmarking: BenchmarkingRecord
    criticality: Optional[CriticalityBreakdown] = None

    @field_validator("name")
    @classmethod
    def title_word_count(cls, v: str) -> str:
        n = _word_count(v)
        if not 3 <= n <= 6:
            raise ValueError(f"v3.1 title must be 3-6 words; got {n} ({v!r})")
        return v

    @field_validator("definition")
    @classmethod
    def definition_one_sentence_15_25(cls, v: str) -> str:
        n = _word_count(v)
        if not 15 <= n <= 25:
            raise ValueError(f"v3.1 definition must be 15-25 words; got {n}")
        # one terminal period — allow trailing whitespace but only one '.'
        if v.strip().count(".") != 1 or not v.strip().endswith("."):
            raise ValueError("v3.1 definition must be exactly one sentence ending with a period")
        return v

    @model_validator(mode="after")
    def four_levels_in_order(self) -> "TechnicalCompetency":
        codes = [p.level for p in self.proficiency_levels]
        expected = [LevelCode.L1, LevelCode.L2, LevelCode.L3, LevelCode.L4]
        if codes != expected:
            raise ValueError(
                f"v3.1 requires exactly 4 ProficiencyLevels in order L1-L4; got {codes}"
            )
        return self


class JobCompetencies(BaseModel):
    job_id: str
    technical_competencies: List[TechnicalCompetency]

    def competency_count(self) -> int:
        return len(self.technical_competencies)


class NormalizedCompetenciesOutput(BaseModel):
    jobs: List[JobCompetencies]
    processing_version: str = "v3.1"
    total_competencies: int
