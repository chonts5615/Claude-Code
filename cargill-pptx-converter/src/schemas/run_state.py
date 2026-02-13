"""
Run state schema - central state object passed through the pipeline.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from src.schemas.compliance import ComplianceReport
from src.schemas.content import ExtractedContent
from src.schemas.slide import PresentationPlan


class RunInputs(BaseModel):
    """Input configuration for a conversion run."""
    input_file: str
    output_path: Optional[str] = None
    template_file: Optional[str] = None


class RunConfig(BaseModel):
    """Configuration for the conversion pipeline."""
    max_words_per_slide: int = 150
    max_bullets_per_slide: int = 7
    max_slides: int = 50
    min_slides: int = 3
    include_speaker_notes: bool = False
    chart_dpi: int = 150
    slide_width: str = "widescreen"  # "widescreen" or "standard"
    use_brand_fonts: bool = True
    include_footer: bool = True
    include_logo: bool = True


class RunFlag(BaseModel):
    """A flag raised during pipeline execution."""
    flag_id: str = Field(default_factory=lambda: str(uuid4())[:8])
    step_id: str
    severity: str  # "CRITICAL", "ERROR", "WARNING", "INFO"
    message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ArtifactRegistry(BaseModel):
    """Registry of generated artifacts."""
    extracted_content_path: Optional[str] = None
    compliance_report_path: Optional[str] = None
    slide_plan_path: Optional[str] = None
    output_pptx_path: Optional[str] = None
    qa_report_path: Optional[str] = None


class RunState(BaseModel):
    """Central state object passed through the conversion pipeline."""
    run_id: str = Field(default_factory=lambda: str(uuid4())[:12])
    run_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    inputs: RunInputs
    config: RunConfig = Field(default_factory=RunConfig)
    artifacts: ArtifactRegistry = Field(default_factory=ArtifactRegistry)
    flags: list[RunFlag] = Field(default_factory=list)

    # In-memory state passed between agents
    extracted_content: Optional[ExtractedContent] = None
    presentation_plan: Optional[PresentationPlan] = None
    compliance_report: Optional[ComplianceReport] = None
    qa_report: Optional[ComplianceReport] = None
    current_step: Optional[str] = None
    output_file: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    def add_flag(self, step_id: str, severity: str, message: str):
        """Add a flag to the run state."""
        self.flags.append(RunFlag(
            step_id=step_id,
            severity=severity,
            message=message,
        ))

    @property
    def has_critical_flags(self) -> bool:
        return any(f.severity == "CRITICAL" for f in self.flags)

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.flags if f.severity == "WARNING")
