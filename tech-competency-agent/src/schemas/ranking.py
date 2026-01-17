from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class CriticalityFactors(BaseModel):
    """Scoring factors for criticality ranking."""
    coverage: float = Field(..., ge=0.0, le=1.0,
                           description="% of responsibilities enabled")
    impact_risk: float = Field(..., ge=0.0, le=1.0,
                               description="Consequence of failure")
    frequency: float = Field(..., ge=0.0, le=1.0,
                            description="How often used")
    complexity: float = Field(..., ge=0.0, le=1.0,
                             description="Cognitive/technical difficulty")
    differentiation: float = Field(..., ge=0.0, le=1.0,
                                  description="Distinguishes high performers")
    time_to_proficiency: float = Field(..., ge=0.0, le=1.0,
                                       description="Development timeframe")

    # Weights for aggregation (should sum to 1.0)
    weights: Dict[str, float] = Field(default_factory=lambda: {
        "coverage": 0.25,
        "impact_risk": 0.20,
        "frequency": 0.15,
        "complexity": 0.15,
        "differentiation": 0.15,
        "time_to_proficiency": 0.10
    })

    def compute_total_score(self) -> float:
        """Weighted criticality score."""
        return (
            self.coverage * self.weights["coverage"] +
            self.impact_risk * self.weights["impact_risk"] +
            self.frequency * self.weights["frequency"] +
            self.complexity * self.weights["complexity"] +
            self.differentiation * self.weights["differentiation"] +
            self.time_to_proficiency * self.weights["time_to_proficiency"]
        )


class RankedCompetency(BaseModel):
    """Competency with ranking metadata."""
    competency_id: str
    rank: int = Field(..., ge=1)
    criticality_score: float = Field(..., ge=0.0, le=1.0)
    criticality_factors: CriticalityFactors
    selection_rationale_paragraph: str

    # For traceability
    responsibility_ids_covered: List[str] = Field(default_factory=list)


class CoverageSummary(BaseModel):
    """Responsibility coverage metrics."""
    responsibilities_total: int
    responsibilities_covered: int
    coverage_rate: float = Field(..., ge=0.0, le=1.0)
    uncovered_responsibility_ids: List[str] = Field(default_factory=list)


class JobRanking(BaseModel):
    """Ranked competencies for single job."""
    job_id: str
    ranked_competencies: List[RankedCompetency]
    top_n: int
    coverage_summary: CoverageSummary

    ranking_methodology: str = "weighted_criticality_factors"
    ranking_timestamp: Optional[str] = None


class RankingOutput(BaseModel):
    """Output from Step 7 - Criticality Ranking."""
    jobs: List[JobRanking]
    total_jobs_ranked: int
    average_coverage_rate: float
    low_coverage_jobs: List[str] = Field(default_factory=list)
