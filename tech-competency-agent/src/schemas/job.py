from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class Responsibility(BaseModel):
    """Individual job responsibility."""
    responsibility_id: str
    raw_text: str
    normalized_text: str
    category: Optional[str] = None
    priority_hint: str = Field("UNKNOWN", pattern="^(LOW|MEDIUM|HIGH|UNKNOWN)$")
    importance_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class JobSummary(BaseModel):
    """Job summary/overview."""
    raw_text: str
    normalized_text: str


class SourceMetadata(BaseModel):
    """Tracking where job data came from."""
    sheet_name: Optional[str] = None
    row_index: Optional[int] = None
    column_mapping: Dict[str, str] = Field(default_factory=dict)
    extraction_timestamp: Optional[str] = None


class Job(BaseModel):
    """Normalized job structure."""
    job_id: str
    job_title: str
    job_family: Optional[str] = None
    job_level: Optional[str] = None
    job_summary: JobSummary
    responsibilities: List[Responsibility]
    source_metadata: SourceMetadata

    def responsibility_count(self) -> int:
        return len(self.responsibilities)


class ExtractionWarning(BaseModel):
    """Warning during job extraction."""
    job_id: Optional[str] = None
    warning_type: str = Field(
        ...,
        pattern="^(MISSING_SUMMARY|NO_RESPONSIBILITIES|MERGED_CELLS|DUPLICATE_RESPONSIBILITIES|OTHER)$"
    )
    message: str
    severity: str = Field("WARNING", pattern="^(INFO|WARNING|ERROR)$")


class JobExtractionOutput(BaseModel):
    """Output from Step 1 - Job Ingestion."""
    jobs: List[Job]
    extraction_warnings: List[ExtractionWarning] = Field(default_factory=list)
    total_jobs_extracted: int
    total_responsibilities_extracted: int
