from typing import List, Optional
from pydantic import BaseModel, Field


class CompetencyCandidate(BaseModel):
    """Candidate competency for a responsibility."""
    competency_id: str
    competency_name: str
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    mapping_rationale: str
    evidence_refs: List[str] = Field(default_factory=list)

    # Scoring breakdown
    lexical_match_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    semantic_similarity_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    llm_relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class ResponsibilityMapping(BaseModel):
    """Mapping from one responsibility to candidate competencies."""
    responsibility_id: str
    candidates: List[CompetencyCandidate]

    def top_candidate(self) -> Optional[CompetencyCandidate]:
        """Return highest-scored candidate."""
        if not self.candidates:
            return None
        return max(self.candidates, key=lambda c: c.relevance_score)


class JobMapping(BaseModel):
    """All mappings for a single job."""
    job_id: str
    responsibility_mappings: List[ResponsibilityMapping]

    def unmapped_responsibilities(self) -> List[str]:
        """Return IDs of responsibilities with no candidates."""
        return [
            rm.responsibility_id
            for rm in self.responsibility_mappings
            if not rm.candidates
        ]


class CompetencyMappingOutput(BaseModel):
    """Output from Step 2 - Competency Mapping."""
    job_mappings: List[JobMapping]
    total_mappings_created: int
    average_candidates_per_responsibility: float
    unmapped_responsibility_rate: float
