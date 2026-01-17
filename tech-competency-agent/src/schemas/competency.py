from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class ProficiencyLevel(BaseModel):
    """Proficiency level definition."""
    level: str = Field(..., pattern="^(FOUNDATIONAL|WORKING|ADVANCED|EXPERT)$")
    description: str
    observable_examples: List[str] = Field(default_factory=list)


class SourceEvidence(BaseModel):
    """Evidence/citation for competency."""
    source_id: str
    source_type: str = Field(..., pattern="^(EXCEL|WORD|PDF|WEB|ONET|SFIA|NICE|OTHER)$")
    source_title: str
    excerpt: str
    location: Optional[str] = None  # page, section, sheet
    retrieval_date_utc: Optional[str] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class CompetencyLibraryEntry(BaseModel):
    """Raw competency from source ingestion (Step 2)."""
    competency_id: str
    name: str
    definition: str
    indicators: List[str] = Field(default_factory=list)
    proficiency_levels: List[ProficiencyLevel] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    source_evidence: List[SourceEvidence]


class CompetencyLibrary(BaseModel):
    """Collection of competencies from all sources."""
    competencies: List[CompetencyLibraryEntry]
    total_sources_processed: int
    ingestion_timestamp: str


class AppliedScope(BaseModel):
    """Technical application context."""
    tools_methods_tech: List[str] = Field(default_factory=list)
    standards_frameworks: List[str] = Field(default_factory=list)
    typical_outputs: List[str] = Field(default_factory=list)


class ResponsibilityTrace(BaseModel):
    """Trace to specific responsibility."""
    responsibility_id: str
    contribution: str = Field(..., pattern="^(PRIMARY|SECONDARY|SUPPORTING)$")
    justification: str


class OverlapCheck(BaseModel):
    """Overlap audit result."""
    core_leadership_overlap: str = Field(..., pattern="^(NONE|MINOR|MATERIAL)$")
    overlap_domains: List[str] = Field(default_factory=list)
    similarity_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    remediation_notes: Optional[str] = None


class BenchmarkingRecord(BaseModel):
    """Benchmarking/validation record."""
    benchmarked_against: List[str] = Field(default_factory=list)
    changes_made: Optional[str] = None
    evidence_refs: List[str] = Field(default_factory=list)
    benchmark_alignment_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class TechnicalCompetency(BaseModel):
    """Normalized technical competency (Steps 3-6)."""
    competency_id: str
    name: str
    definition: str
    why_it_matters: str
    behavioral_indicators: List[str]
    applied_scope: AppliedScope
    responsibility_trace: List[ResponsibilityTrace]
    overlap_check: OverlapCheck
    benchmarking: BenchmarkingRecord

    # Quality metadata
    word_count_definition: Optional[int] = None
    indicator_count: Optional[int] = None


class JobCompetencies(BaseModel):
    """All competencies for a single job."""
    job_id: str
    technical_competencies: List[TechnicalCompetency]

    def competency_count(self) -> int:
        return len(self.technical_competencies)


class NormalizedCompetenciesOutput(BaseModel):
    """Output from Steps 3/5/6."""
    jobs: List[JobCompetencies]
    processing_version: str  # v2, v3, v4
    total_competencies: int
