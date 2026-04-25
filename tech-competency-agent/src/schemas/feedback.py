"""SME feedback ingestion (Phase 6 entry)."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

FeedbackDisposition = Literal["KEEP", "EDIT", "GAP", "DISCUSS", "REJECT"]


class FeedbackItem(BaseModel):
    """One verbatim SME comment, classified into disposition."""

    feedback_id: str
    sme_name: Optional[str] = None
    sme_role: Optional[str] = None
    target_competency_id: Optional[str] = None
    target_field: Optional[str] = None  # name | definition | indicators | proficiency_levels
    target_level: Optional[str] = None  # L1..L4 if applicable
    verbatim_comment: str  # never paraphrase
    disposition: FeedbackDisposition
    proposed_text: Optional[str] = None
    rationale: Optional[str] = None
    is_anchor_sme: bool = False  # anchor-SME edits propagate to shared competencies


class FeedbackBatch(BaseModel):
    run_id: str
    stage: Literal["R2", "FINAL"]
    family: str
    items: List[FeedbackItem]
    review_metadata: dict = Field(default_factory=dict)  # gate fields
    received_timestamp_utc: str
