"""Strategic planning domain schemas."""

from datetime import date
from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


class StrategicPriority(str, Enum):
    """Priority levels for strategic elements."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class GoalStatus(str, Enum):
    """Status of goals and initiatives."""
    DRAFT = "draft"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    DELAYED = "delayed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RiskCategory(str, Enum):
    """Categories of strategic risks."""
    MARKET = "market"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    REGULATORY = "regulatory"
    TECHNOLOGY = "technology"
    TALENT = "talent"
    REPUTATION = "reputation"
    STRATEGIC = "strategic"


class RiskSeverity(str, Enum):
    """Risk severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StrategicVision(BaseModel):
    """Organization's strategic vision and mission."""

    vision_statement: str = Field(..., description="Long-term aspirational vision")
    mission_statement: str = Field(..., description="Organization's core purpose")
    core_values: List[str] = Field(default_factory=list, description="Guiding values")
    value_proposition: Optional[str] = Field(None, description="Unique value to stakeholders")

    # Time horizon
    time_horizon_years: int = Field(3, ge=1, le=10)
    target_end_date: Optional[date] = None

    # Context
    strategic_context: Optional[str] = Field(None, description="Key context and assumptions")
    success_criteria: List[str] = Field(default_factory=list, description="What success looks like")

    # Traceability
    source_document: Optional[str] = None
    extracted_from: Optional[str] = None
    confidence_score: float = Field(1.0, ge=0.0, le=1.0)


class StrategicPillar(BaseModel):
    """High-level strategic pillar or theme."""

    pillar_id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Pillar name")
    description: str = Field(..., description="Detailed description")
    rationale: str = Field(..., description="Why this pillar matters")

    # Relationships
    vision_alignment: str = Field(..., description="How pillar supports vision")
    priority: StrategicPriority = Field(StrategicPriority.HIGH)
    sequence_order: int = Field(1, ge=1)

    # Metrics
    success_metrics: List[str] = Field(default_factory=list)
    target_outcomes: List[str] = Field(default_factory=list)

    # Traceability
    source_text: Optional[str] = None
    confidence_score: float = Field(1.0, ge=0.0, le=1.0)


class StrategicGoal(BaseModel):
    """Strategic goal within a pillar."""

    goal_id: str = Field(..., description="Unique identifier")
    pillar_id: str = Field(..., description="Parent pillar ID")
    name: str = Field(..., description="Goal name")
    description: str = Field(..., description="Detailed description")

    # SMART criteria
    specific: str = Field(..., description="Specific target")
    measurable: str = Field(..., description="How it will be measured")
    achievable: str = Field(..., description="Why it's achievable")
    relevant: str = Field(..., description="Why it's relevant")
    time_bound: str = Field(..., description="Timeline")

    # Scoring
    smart_score: float = Field(0.0, ge=0.0, le=1.0, description="SMART compliance score")
    feasibility_score: float = Field(0.0, ge=0.0, le=1.0)
    impact_score: float = Field(0.0, ge=0.0, le=1.0)

    # Status
    status: GoalStatus = Field(GoalStatus.DRAFT)
    priority: StrategicPriority = Field(StrategicPriority.MEDIUM)

    # Timeline
    target_start: Optional[date] = None
    target_end: Optional[date] = None
    milestones: List[str] = Field(default_factory=list, description="Key milestone IDs")

    # Resources
    estimated_investment: Optional[float] = None
    resource_requirements: List[str] = Field(default_factory=list)

    # Traceability
    source_text: Optional[str] = None
    linked_initiatives: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)


class Initiative(BaseModel):
    """Specific initiative to achieve a goal."""

    initiative_id: str = Field(..., description="Unique identifier")
    goal_id: str = Field(..., description="Parent goal ID")
    name: str = Field(..., description="Initiative name")
    description: str = Field(..., description="Detailed description")
    objective: str = Field(..., description="What the initiative will achieve")

    # Classification
    initiative_type: str = Field("project", description="project, program, process, capability")
    priority: StrategicPriority = Field(StrategicPriority.MEDIUM)
    status: GoalStatus = Field(GoalStatus.DRAFT)

    # Timeline
    planned_start: Optional[date] = None
    planned_end: Optional[date] = None
    duration_months: Optional[int] = None

    # Resources
    estimated_budget: Optional[float] = None
    budget_currency: str = Field("USD")
    fte_required: Optional[float] = None
    key_roles: List[str] = Field(default_factory=list)
    required_capabilities: List[str] = Field(default_factory=list)

    # Success criteria
    success_criteria: List[str] = Field(default_factory=list)
    deliverables: List[str] = Field(default_factory=list)
    kpi_ids: List[str] = Field(default_factory=list)

    # Dependencies and risks
    dependencies: List[str] = Field(default_factory=list)
    prerequisite_initiatives: List[str] = Field(default_factory=list)
    risk_ids: List[str] = Field(default_factory=list)

    # Scores
    feasibility_score: float = Field(0.0, ge=0.0, le=1.0)
    impact_score: float = Field(0.0, ge=0.0, le=1.0)
    alignment_score: float = Field(0.0, ge=0.0, le=1.0)

    # Ownership
    sponsor: Optional[str] = None
    owner: Optional[str] = None
    team: List[str] = Field(default_factory=list)


class Milestone(BaseModel):
    """Key milestone for tracking progress."""

    milestone_id: str = Field(..., description="Unique identifier")
    parent_id: str = Field(..., description="Parent goal or initiative ID")
    parent_type: str = Field("initiative", description="goal or initiative")
    name: str = Field(..., description="Milestone name")
    description: str = Field(..., description="What this milestone represents")

    # Timeline
    target_date: date = Field(..., description="Target completion date")
    actual_date: Optional[date] = None

    # Status
    status: GoalStatus = Field(GoalStatus.DRAFT)
    completion_percentage: float = Field(0.0, ge=0.0, le=100.0)

    # Criteria
    acceptance_criteria: List[str] = Field(default_factory=list)
    deliverables: List[str] = Field(default_factory=list)

    # Dependencies
    dependencies: List[str] = Field(default_factory=list)
    blocking_risks: List[str] = Field(default_factory=list)


class KPI(BaseModel):
    """Key Performance Indicator for measuring success."""

    kpi_id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="KPI name")
    description: str = Field(..., description="What this KPI measures")

    # Linkage
    linked_goals: List[str] = Field(default_factory=list)
    linked_initiatives: List[str] = Field(default_factory=list)

    # Measurement
    metric_type: str = Field("quantitative", description="quantitative or qualitative")
    unit: str = Field(..., description="Unit of measurement")
    calculation_method: Optional[str] = None
    data_source: Optional[str] = None
    measurement_frequency: str = Field("monthly", description="daily, weekly, monthly, quarterly, annually")

    # Targets
    baseline_value: Optional[float] = None
    baseline_date: Optional[date] = None
    target_value: float = Field(..., description="Target value")
    target_date: date = Field(..., description="Target date")

    # Thresholds
    threshold_red: Optional[float] = Field(None, description="Critical threshold")
    threshold_amber: Optional[float] = Field(None, description="Warning threshold")
    threshold_green: Optional[float] = Field(None, description="On-track threshold")

    # Current state
    current_value: Optional[float] = None
    current_date: Optional[date] = None
    trend: Optional[str] = Field(None, description="improving, stable, declining")

    # Ownership
    owner: Optional[str] = None
    reporting_to: Optional[str] = None


class RiskAssessment(BaseModel):
    """Strategic risk assessment."""

    risk_id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Risk name")
    description: str = Field(..., description="Detailed risk description")

    # Classification
    category: RiskCategory = Field(...)
    severity: RiskSeverity = Field(...)

    # Assessment
    likelihood: float = Field(..., ge=0.0, le=1.0, description="Probability (0-1)")
    impact: float = Field(..., ge=0.0, le=1.0, description="Impact if occurs (0-1)")
    risk_score: float = Field(0.0, ge=0.0, le=1.0, description="Combined risk score")

    # Context
    triggers: List[str] = Field(default_factory=list, description="What could trigger this risk")
    affected_goals: List[str] = Field(default_factory=list)
    affected_initiatives: List[str] = Field(default_factory=list)

    # Mitigation
    mitigation_strategy: Optional[str] = None
    mitigation_actions: List[str] = Field(default_factory=list)
    contingency_plan: Optional[str] = None
    residual_risk: Optional[float] = Field(None, ge=0.0, le=1.0)

    # Status
    status: str = Field("identified", description="identified, assessing, mitigating, monitoring, closed")
    owner: Optional[str] = None
    review_date: Optional[date] = None

    def calculate_risk_score(self) -> float:
        """Calculate combined risk score."""
        self.risk_score = self.likelihood * self.impact
        return self.risk_score


class ResourceAllocation(BaseModel):
    """Resource allocation plan."""

    allocation_id: str = Field(..., description="Unique identifier")
    initiative_id: str = Field(..., description="Linked initiative")

    # Financial resources
    budget_allocated: float = Field(0.0, ge=0.0)
    budget_currency: str = Field("USD")
    budget_year: int = Field(...)
    budget_quarter: Optional[int] = Field(None, ge=1, le=4)

    # Human resources
    fte_allocated: float = Field(0.0, ge=0.0)
    roles_allocated: Dict[str, float] = Field(default_factory=dict)  # role -> FTE

    # Other resources
    technology_resources: List[str] = Field(default_factory=list)
    external_resources: List[str] = Field(default_factory=list)

    # Utilization
    utilization_rate: float = Field(0.0, ge=0.0, le=1.0)
    allocation_confidence: float = Field(1.0, ge=0.0, le=1.0)

    # Notes
    allocation_rationale: Optional[str] = None
    constraints: List[str] = Field(default_factory=list)


class DependencyMap(BaseModel):
    """Map of dependencies between strategic elements."""

    dependency_id: str = Field(..., description="Unique identifier")
    source_id: str = Field(..., description="Dependent element ID")
    source_type: str = Field(..., description="goal, initiative, milestone")
    target_id: str = Field(..., description="Dependency target ID")
    target_type: str = Field(..., description="goal, initiative, milestone, external")

    # Dependency details
    dependency_type: str = Field("finish-to-start", description="finish-to-start, start-to-start, etc.")
    is_critical: bool = Field(False, description="Is this on critical path")
    lag_days: int = Field(0, description="Lag between elements")

    # Status
    status: str = Field("active", description="active, resolved, removed")
    notes: Optional[str] = None


class ExecutionPlan(BaseModel):
    """Complete execution plan for strategy."""

    plan_id: str = Field(..., description="Unique identifier")
    plan_name: str = Field(..., description="Plan name")
    plan_version: str = Field("1.0")
    created_date: date = Field(default_factory=date.today)
    last_updated: date = Field(default_factory=date.today)

    # Strategic elements
    vision: StrategicVision = Field(...)
    pillars: List[StrategicPillar] = Field(default_factory=list)
    goals: List[StrategicGoal] = Field(default_factory=list)
    initiatives: List[Initiative] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)
    kpis: List[KPI] = Field(default_factory=list)

    # Risk and resources
    risks: List[RiskAssessment] = Field(default_factory=list)
    resource_allocations: List[ResourceAllocation] = Field(default_factory=list)
    dependencies: List[DependencyMap] = Field(default_factory=list)

    # Summary metrics
    total_budget: float = Field(0.0, ge=0.0)
    total_fte: float = Field(0.0, ge=0.0)
    critical_path_length_months: Optional[int] = None

    # Quality scores
    overall_feasibility: float = Field(0.0, ge=0.0, le=1.0)
    overall_alignment: float = Field(0.0, ge=0.0, le=1.0)
    overall_completeness: float = Field(0.0, ge=0.0, le=1.0)

    # Approval
    status: str = Field("draft", description="draft, review, approved, active")
    approved_by: Optional[str] = None
    approval_date: Optional[date] = None


# Output schemas for agents

class VisionExtractionOutput(BaseModel):
    """Output from vision extraction agent."""
    vision: StrategicVision
    extraction_confidence: float
    warnings: List[str] = Field(default_factory=list)


class PillarSynthesisOutput(BaseModel):
    """Output from pillar synthesis agent."""
    pillars: List[StrategicPillar]
    pillar_rationale: str
    alignment_analysis: str


class GoalGenerationOutput(BaseModel):
    """Output from goal generation agent."""
    goals: List[StrategicGoal]
    goals_by_pillar: Dict[str, List[str]]
    smart_analysis: Dict[str, Dict[str, float]]


class InitiativeDesignOutput(BaseModel):
    """Output from initiative design agent."""
    initiatives: List[Initiative]
    initiatives_by_goal: Dict[str, List[str]]
    resource_summary: Dict[str, float]


class RiskAnalysisOutput(BaseModel):
    """Output from risk analysis agent."""
    risks: List[RiskAssessment]
    risk_matrix: Dict[str, List[str]]
    critical_risks: List[str]
    mitigation_coverage: float


class ResourcePlanOutput(BaseModel):
    """Output from resource planning agent."""
    allocations: List[ResourceAllocation]
    total_budget: float
    total_fte: float
    resource_gaps: List[str]
    utilization_forecast: Dict[str, float]


class ValidationOutput(BaseModel):
    """Output from validation agent."""
    is_valid: bool
    alignment_score: float
    coherence_score: float
    completeness_score: float
    feasibility_score: float
    issues: List[str]
    recommendations: List[str]
