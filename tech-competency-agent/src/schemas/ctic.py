"""CTIC — Character-level Text Integrity Check.

Phase 6F enforces no-drift on competencies NOT explicitly targeted by SME
feedback. Any character-level diff between pre- and post-feedback text on a
non-targeted competency is reverted and logged as drift.
"""

from typing import List

from pydantic import BaseModel, Field


class CTICDiff(BaseModel):
    competency_id: str
    field: str  # name | definition | why_it_matters | indicator_id
    before: str
    after: str
    char_diff_count: int
    is_targeted_by_feedback: bool
    reverted: bool
    rationale: str


class CTICReport(BaseModel):
    run_id: str
    diffs_detected: int
    diffs_reverted: int
    diffs_kept: int
    drift_rate: float = Field(..., ge=0.0, le=1.0)
    entries: List[CTICDiff] = Field(default_factory=list)
