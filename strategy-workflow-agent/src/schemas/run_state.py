"""Run state schemas for strategy workflow."""

from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field
from pathlib import Path


class WorkflowPhase(str, Enum):
    """Phases of the strategic planning workflow."""
    INGESTION = "ingestion"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    PLANNING = "planning"
    OPTIMIZATION = "optimization"
    VALIDATION = "validation"
    OUTPUT = "output"
    FEEDBACK = "feedback"


class SeverityLevel(str, Enum):
    """Severity levels for flags and alerts."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class RunInputs(BaseModel):
    """Input files and sources for a workflow run."""

    # Primary strategy documents
    vision_document: Optional[Path] = Field(None, description="Path to vision/mission document")
    current_state_analysis: Optional[Path] = Field(None, description="Current state assessment")
    market_analysis: Optional[Path] = Field(None, description="Market/competitive analysis")
    financial_projections: Optional[Path] = Field(None, description="Financial data/projections")

    # Organizational context
    org_structure: Optional[Path] = Field(None, description="Organization structure data")
    resource_inventory: Optional[Path] = Field(None, description="Available resources/capabilities")
    stakeholder_map: Optional[Path] = Field(None, description="Key stakeholders and interests")

    # Constraints and guidelines
    constraints_file: Optional[Path] = Field(None, description="Business/regulatory constraints")
    brand_guidelines: Optional[Path] = Field(None, description="Brand/communication guidelines")

    # Historical data for learning
    historical_strategies: Optional[Path] = Field(None, description="Past strategy documents")
    performance_history: Optional[Path] = Field(None, description="Historical performance data")
    lessons_learned: Optional[Path] = Field(None, description="Previous lessons learned")

    # Raw text inputs (for direct input without files)
    raw_vision_text: Optional[str] = Field(None, description="Vision text if no file provided")
    raw_goals_text: Optional[str] = Field(None, description="Goals text if no file provided")
    raw_context_text: Optional[str] = Field(None, description="Additional context text")

    class Config:
        json_encoders = {Path: lambda v: str(v) if v else None}


class ThresholdConfig(BaseModel):
    """Configurable thresholds for quality gates."""

    # Goal quality thresholds
    min_goals_per_pillar: int = Field(2, ge=1, description="Minimum goals per strategic pillar")
    max_goals_per_pillar: int = Field(5, le=10, description="Maximum goals per strategic pillar")
    goal_smart_score_min: float = Field(0.7, ge=0.0, le=1.0, description="Minimum SMART score for goals")

    # Initiative thresholds
    min_initiatives_per_goal: int = Field(1, ge=1)
    max_initiatives_per_goal: int = Field(5, le=10)
    initiative_feasibility_min: float = Field(0.6, ge=0.0, le=1.0)

    # Risk thresholds
    max_critical_risks: int = Field(3, ge=0, description="Max unmitigated critical risks")
    risk_mitigation_coverage: float = Field(0.8, ge=0.0, le=1.0)

    # Resource thresholds
    budget_variance_max: float = Field(0.15, ge=0.0, le=0.5, description="Max budget variance allowed")
    resource_utilization_min: float = Field(0.6, ge=0.0, le=1.0)

    # Quality thresholds
    alignment_score_min: float = Field(0.75, ge=0.0, le=1.0)
    coherence_score_min: float = Field(0.8, ge=0.0, le=1.0)
    completeness_score_min: float = Field(0.85, ge=0.0, le=1.0)

    # Feedback loop thresholds
    learning_confidence_min: float = Field(0.7, ge=0.0, le=1.0)
    optimization_impact_min: float = Field(0.1, ge=0.0, le=1.0)


class FeedbackConfig(BaseModel):
    """Configuration for the learning feedback loop."""

    enabled: bool = Field(True, description="Enable feedback loop")

    # Learning parameters
    learning_rate: float = Field(0.1, ge=0.01, le=1.0, description="Rate of incorporating learnings")
    memory_decay: float = Field(0.95, ge=0.5, le=1.0, description="Decay rate for older learnings")
    min_samples_for_learning: int = Field(3, ge=1, description="Min samples before applying learnings")

    # Feedback sources
    include_user_feedback: bool = Field(True)
    include_outcome_tracking: bool = Field(True)
    include_quality_metrics: bool = Field(True)
    include_execution_metrics: bool = Field(True)

    # Optimization triggers
    auto_optimize: bool = Field(True, description="Automatically apply optimizations")
    optimization_frequency: str = Field("per_run", description="per_run, daily, weekly")
    min_improvement_threshold: float = Field(0.05, ge=0.0, le=0.5)

    # Storage
    feedback_log_path: Optional[Path] = Field(None)
    max_feedback_history: int = Field(1000, ge=100)


class RunConfig(BaseModel):
    """Configuration for workflow execution."""

    # Output settings
    output_format: str = Field("comprehensive", description="comprehensive, executive, or minimal")
    time_horizon_years: int = Field(3, ge=1, le=10, description="Strategic planning horizon")
    planning_granularity: str = Field("quarterly", description="annual, quarterly, monthly")

    # Processing settings
    parallel_processing: bool = Field(True)
    max_retries: int = Field(2, ge=0, le=5)
    checkpoint_enabled: bool = Field(True)

    # Quality settings
    thresholds: ThresholdConfig = Field(default_factory=ThresholdConfig)
    strict_mode: bool = Field(False, description="Fail on any quality gate violation")

    # Feedback settings
    feedback: FeedbackConfig = Field(default_factory=FeedbackConfig)

    # Model settings
    primary_model: str = Field("claude-sonnet-4-20250514", description="Primary LLM model")
    reasoning_model: str = Field("claude-sonnet-4-20250514", description="Model for complex reasoning")
    temperature: float = Field(0.3, ge=0.0, le=1.0)

    class Config:
        json_encoders = {Path: lambda v: str(v) if v else None}


class ArtifactRegistry(BaseModel):
    """Registry of generated artifacts during workflow."""

    # Ingestion outputs
    parsed_vision: Optional[Path] = None
    parsed_context: Optional[Path] = None
    stakeholder_analysis: Optional[Path] = None

    # Analysis outputs
    swot_analysis: Optional[Path] = None
    gap_analysis: Optional[Path] = None
    trend_analysis: Optional[Path] = None
    competitive_analysis: Optional[Path] = None

    # Synthesis outputs
    strategic_pillars: Optional[Path] = None
    goal_hierarchy: Optional[Path] = None
    initiative_map: Optional[Path] = None

    # Planning outputs
    execution_plan: Optional[Path] = None
    resource_allocation: Optional[Path] = None
    timeline: Optional[Path] = None
    risk_register: Optional[Path] = None

    # Validation outputs
    alignment_report: Optional[Path] = None
    feasibility_report: Optional[Path] = None
    quality_report: Optional[Path] = None

    # Final outputs
    strategy_document: Optional[Path] = None
    executive_summary: Optional[Path] = None
    presentation_deck: Optional[Path] = None
    kpi_dashboard_spec: Optional[Path] = None

    # Feedback artifacts
    feedback_summary: Optional[Path] = None
    optimization_log: Optional[Path] = None
    learning_insights: Optional[Path] = None

    class Config:
        json_encoders = {Path: lambda v: str(v) if v else None}


class RunFlag(BaseModel):
    """Quality flag or warning during workflow execution."""

    step_id: str = Field(..., description="ID of the step that raised the flag")
    phase: WorkflowPhase = Field(..., description="Phase where flag was raised")
    severity: SeverityLevel = Field(..., description="Severity level")
    flag_type: str = Field(..., description="Type/category of the flag")
    message: str = Field(..., description="Human-readable message")
    artifact_id: Optional[str] = Field(None, description="Related artifact if any")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    resolved: bool = Field(False, description="Whether flag has been resolved")
    resolution_note: Optional[str] = None


class QASummary(BaseModel):
    """Quality assurance summary for the workflow run."""

    # Completeness metrics
    total_goals_defined: int = 0
    total_initiatives_defined: int = 0
    total_milestones_defined: int = 0
    total_kpis_defined: int = 0

    # Quality scores (0-1)
    alignment_score: float = 0.0
    coherence_score: float = 0.0
    completeness_score: float = 0.0
    feasibility_score: float = 0.0
    smart_compliance_score: float = 0.0

    # Risk metrics
    risks_identified: int = 0
    risks_mitigated: int = 0
    critical_risks_remaining: int = 0

    # Flag summary
    flags_by_severity: Dict[str, int] = Field(default_factory=dict)
    unresolved_issues: List[str] = Field(default_factory=list)

    # Feedback metrics
    learning_insights_applied: int = 0
    optimizations_applied: int = 0
    feedback_confidence: float = 0.0


class RunState(BaseModel):
    """Complete state of workflow run - passed between agents."""

    # Run identification
    run_id: str = Field(..., description="Unique run identifier")
    run_timestamp_utc: datetime = Field(default_factory=datetime.utcnow)

    # Configuration
    inputs: RunInputs = Field(default_factory=RunInputs)
    config: RunConfig = Field(default_factory=RunConfig)

    # Workflow tracking
    current_phase: WorkflowPhase = Field(WorkflowPhase.INGESTION)
    current_step: Optional[str] = None
    completed_steps: List[str] = Field(default_factory=list)

    # Artifacts and data
    artifacts: ArtifactRegistry = Field(default_factory=ArtifactRegistry)
    working_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="In-memory working data passed between agents"
    )

    # Quality tracking
    flags: List[RunFlag] = Field(default_factory=list)
    qa_summary: Optional[QASummary] = None

    # Feedback loop state
    feedback_applied: bool = Field(False)
    optimization_round: int = Field(0)
    learning_context: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Path: lambda v: str(v) if v else None,
        }

    def add_flag(
        self,
        step_id: str,
        severity: SeverityLevel,
        flag_type: str,
        message: str,
        metadata: Optional[Dict] = None
    ) -> None:
        """Add a flag to the run state."""
        flag = RunFlag(
            step_id=step_id,
            phase=self.current_phase,
            severity=severity,
            flag_type=flag_type,
            message=message,
            metadata=metadata or {}
        )
        self.flags.append(flag)

    def get_unresolved_flags(self, min_severity: SeverityLevel = SeverityLevel.WARNING) -> List[RunFlag]:
        """Get unresolved flags at or above a severity level."""
        severity_order = [SeverityLevel.INFO, SeverityLevel.WARNING, SeverityLevel.ERROR, SeverityLevel.CRITICAL]
        min_index = severity_order.index(min_severity)
        return [
            f for f in self.flags
            if not f.resolved and severity_order.index(f.severity) >= min_index
        ]

    def mark_step_complete(self, step_id: str) -> None:
        """Mark a step as completed."""
        if step_id not in self.completed_steps:
            self.completed_steps.append(step_id)
