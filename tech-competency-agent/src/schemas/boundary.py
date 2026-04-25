"""Boundary classification for v3.1 (V&B / Common / Technical / Mixed)."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

BoundaryClass = Literal["V_AND_B", "COMMON", "TECHNICAL", "MIXED"]


class BoundaryClassification(BaseModel):
    """Result of running a competency through the boundary classifier."""

    competency_id: str
    classification: BoundaryClass
    confidence: float = Field(..., ge=0.0, le=1.0)
    matched_terms: List[str] = Field(default_factory=list)
    domain_noun_test_passed: Optional[bool] = None  # for COMMON test
    rationale: str
