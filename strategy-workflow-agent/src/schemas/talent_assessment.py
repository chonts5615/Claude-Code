"""Talent Assessment domain-specific schemas for strategic planning."""

from datetime import date
from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


class AssessmentUseCase(str, Enum):
    """Primary use cases for talent assessment."""
    EXTERNAL_HIRING = "external_hiring"
    INTERNAL_MOBILITY = "internal_mobility"
    SUCCESSION_PLANNING = "succession_planning"
    LEADERSHIP_DEVELOPMENT = "leadership_development"
    HIGH_POTENTIAL_ID = "high_potential_identification"
    TEAM_COMPOSITION = "team_composition"
    PERFORMANCE_PREDICTION = "performance_prediction"
    CULTURE_FIT = "culture_fit"
    SKILL_GAP_ANALYSIS = "skill_gap_analysis"
    ONBOARDING = "onboarding"


class AssessmentType(str, Enum):
    """Types of talent assessments."""
    COGNITIVE_ABILITY = "cognitive_ability"
    PERSONALITY = "personality"
    SITUATIONAL_JUDGMENT = "situational_judgment"
    WORK_SAMPLE = "work_sample"
    STRUCTURED_INTERVIEW = "structured_interview"
    ASSESSMENT_CENTER = "assessment_center"
    BIODATA = "biodata"
    SIMULATION = "simulation"
    MULTI_RATER_360 = "multi_rater_360"
    ENGAGEMENT_SURVEY = "engagement_survey"
    VALUES_ASSESSMENT = "values_assessment"
    COMPETENCY_BASED = "competency_based"


class AssessmentVendor(str, Enum):
    """Major assessment vendors."""
    SHL = "shl"
    HOGAN = "hogan"
    DDI = "ddi"
    KORN_FERRY = "korn_ferry"
    GALLUP = "gallup"
    MERCER = "mercer"
    AON = "aon"
    TALOGY = "talogy"
    PYMETRICS = "pymetrics"
    HIREVUE = "hirevue"
    CRITERIA_CORP = "criteria_corp"
    WONDERLIC = "wonderlic"
    CUSTOM_INTERNAL = "custom_internal"
    OTHER = "other"


class JobLevel(str, Enum):
    """Organizational job levels."""
    ENTRY_LEVEL = "entry_level"
    INDIVIDUAL_CONTRIBUTOR = "individual_contributor"
    PROFESSIONAL = "professional"
    SENIOR_PROFESSIONAL = "senior_professional"
    MANAGER = "manager"
    SENIOR_MANAGER = "senior_manager"
    DIRECTOR = "director"
    SENIOR_DIRECTOR = "senior_director"
    VP = "vice_president"
    SVP = "senior_vice_president"
    C_SUITE = "c_suite"


class GovernanceLevel(str, Enum):
    """Governance and decision-making levels."""
    ENTERPRISE = "enterprise"
    BUSINESS_UNIT = "business_unit"
    FUNCTION = "function"
    REGION = "region"
    LOCAL = "local"


# Domain-specific schemas

class TalentAssessmentVision(BaseModel):
    """Strategic vision for talent assessment."""

    vision_statement: str = Field(..., description="Aspirational vision for assessment")
    mission_statement: str = Field(..., description="Purpose of assessment function")

    # Strategic alignment
    business_strategy_alignment: str = Field(..., description="How assessment supports business strategy")
    talent_strategy_alignment: str = Field(..., description="How assessment supports talent strategy")

    # Core principles
    guiding_principles: List[str] = Field(default_factory=list, description="IO psychology-grounded principles")
    core_values: List[str] = Field(default_factory=list)

    # Time horizon
    time_horizon_years: int = Field(3, ge=1, le=5)
    fiscal_year_start: str = Field("FY26", description="Starting fiscal year")
    fiscal_year_end: str = Field("FY29", description="Ending fiscal year")

    # Success criteria
    success_metrics: List[str] = Field(default_factory=list)
    key_outcomes: List[str] = Field(default_factory=list)

    # Evidence basis
    research_foundation: List[str] = Field(default_factory=list, description="IO psychology research grounding")


class AssessmentUseCaseSpec(BaseModel):
    """Specification for a talent assessment use case."""

    use_case_id: str = Field(...)
    use_case: AssessmentUseCase = Field(...)
    name: str = Field(...)
    description: str = Field(...)

    # Business context
    business_need: str = Field(..., description="Why this use case matters")
    volume_estimate: Optional[int] = Field(None, description="Annual volume estimate")

    # Target population
    target_job_levels: List[JobLevel] = Field(default_factory=list)
    target_job_families: List[str] = Field(default_factory=list)
    geographic_scope: List[str] = Field(default_factory=list)

    # Assessment design
    recommended_assessments: List[AssessmentType] = Field(default_factory=list)
    assessment_battery: List[str] = Field(default_factory=list, description="Specific assessment names")
    validity_requirements: Dict[str, float] = Field(default_factory=dict)

    # Timing
    assessment_timing: str = Field("pre-hire", description="When in process")
    turnaround_time_days: int = Field(3, ge=1)

    # Scoring and decisions
    scoring_approach: str = Field("compensatory", description="compensatory, multiple_hurdle, or hybrid")
    decision_rules: List[str] = Field(default_factory=list)
    cut_score_approach: Optional[str] = None

    # Vendors
    preferred_vendors: List[AssessmentVendor] = Field(default_factory=list)
    vendor_rationale: Optional[str] = None

    # Priority
    priority: str = Field("medium", description="high, medium, low")
    implementation_phase: int = Field(1, ge=1, le=3)

    # ROI expectations
    expected_roi_percent: Optional[float] = None
    roi_drivers: List[str] = Field(default_factory=list)


class CompetencyFramework(BaseModel):
    """Competency framework for assessment."""

    framework_id: str = Field(...)
    framework_name: str = Field(...)
    description: str = Field(...)

    # Framework structure
    competency_categories: List[str] = Field(default_factory=list)
    total_competencies: int = Field(0)

    # Competency details
    competencies: List[Dict[str, Any]] = Field(default_factory=list)

    # Level definitions
    proficiency_levels: List[str] = Field(
        default_factory=lambda: ["Foundational", "Developing", "Proficient", "Advanced", "Expert"]
    )

    # Alignment
    aligned_to_job_levels: Dict[str, List[str]] = Field(default_factory=dict)

    # Source
    source: str = Field("internal", description="internal, vendor, hybrid")
    last_validated: Optional[date] = None


class AssessmentGovernance(BaseModel):
    """Governance model for talent assessment."""

    governance_id: str = Field(...)
    governance_level: GovernanceLevel = Field(...)

    # Structure
    governance_body: str = Field(..., description="Name of governing body")
    charter: str = Field(..., description="Governance charter/scope")

    # Roles
    roles: List[Dict[str, str]] = Field(default_factory=list)
    decision_rights: Dict[str, List[str]] = Field(default_factory=dict)
    escalation_path: List[str] = Field(default_factory=list)

    # Policies
    key_policies: List[str] = Field(default_factory=list)
    compliance_requirements: List[str] = Field(default_factory=list)

    # Cadence
    meeting_frequency: str = Field("quarterly")
    review_cycle: str = Field("annual")

    # Metrics
    governance_kpis: List[str] = Field(default_factory=list)


class VendorEvaluation(BaseModel):
    """Vendor evaluation for assessment tools."""

    vendor: AssessmentVendor = Field(...)
    vendor_name: str = Field(...)

    # Assessment offerings
    assessment_types_offered: List[AssessmentType] = Field(default_factory=list)
    products_evaluated: List[str] = Field(default_factory=list)

    # Evaluation criteria scores (0-5 scale)
    validity_evidence: float = Field(0.0, ge=0.0, le=5.0)
    reliability: float = Field(0.0, ge=0.0, le=5.0)
    adverse_impact: float = Field(0.0, ge=0.0, le=5.0, description="Lower is better")
    user_experience: float = Field(0.0, ge=0.0, le=5.0)
    candidate_experience: float = Field(0.0, ge=0.0, le=5.0)
    integration_capability: float = Field(0.0, ge=0.0, le=5.0)
    global_coverage: float = Field(0.0, ge=0.0, le=5.0)
    language_support: float = Field(0.0, ge=0.0, le=5.0)
    cost_effectiveness: float = Field(0.0, ge=0.0, le=5.0)
    support_quality: float = Field(0.0, ge=0.0, le=5.0)

    # Overall
    overall_score: float = Field(0.0, ge=0.0, le=5.0)
    recommendation: str = Field("consider", description="preferred, consider, not_recommended")

    # Notes
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    best_fit_use_cases: List[AssessmentUseCase] = Field(default_factory=list)


class AssessmentROIModel(BaseModel):
    """ROI model for talent assessment investment."""

    model_id: str = Field(...)
    use_case: AssessmentUseCase = Field(...)

    # Investment
    initial_investment: float = Field(0.0, ge=0.0)
    annual_operating_cost: float = Field(0.0, ge=0.0)
    implementation_cost: float = Field(0.0, ge=0.0)

    # Volume assumptions
    annual_volume: int = Field(0, ge=0)
    cost_per_assessment: float = Field(0.0, ge=0.0)

    # Benefit drivers
    quality_of_hire_improvement: float = Field(0.0, ge=0.0, le=1.0)
    turnover_reduction: float = Field(0.0, ge=0.0, le=1.0)
    time_to_productivity_reduction_days: int = Field(0, ge=0)
    bad_hire_avoidance_rate: float = Field(0.0, ge=0.0, le=1.0)

    # Value calculations
    cost_of_bad_hire: float = Field(0.0, ge=0.0)
    average_salary: float = Field(0.0, ge=0.0)

    # Results
    year_1_roi: float = Field(0.0)
    year_3_roi: float = Field(0.0)
    payback_period_months: int = Field(0, ge=0)
    npv: float = Field(0.0)

    # Assumptions
    key_assumptions: List[str] = Field(default_factory=list)
    sensitivity_factors: List[str] = Field(default_factory=list)


class ChangeManagementPlan(BaseModel):
    """Change management plan for assessment implementation."""

    plan_id: str = Field(...)
    initiative_name: str = Field(...)

    # Stakeholder analysis
    stakeholder_groups: List[Dict[str, Any]] = Field(default_factory=list)
    change_impact_by_group: Dict[str, str] = Field(default_factory=dict)

    # Communication
    communication_strategy: str = Field(...)
    key_messages: List[str] = Field(default_factory=list)
    communication_channels: List[str] = Field(default_factory=list)

    # Training
    training_needs: List[str] = Field(default_factory=list)
    training_approach: str = Field(...)
    training_timeline: Dict[str, str] = Field(default_factory=dict)

    # Adoption
    adoption_metrics: List[str] = Field(default_factory=list)
    resistance_mitigation: List[str] = Field(default_factory=list)

    # Support
    support_model: str = Field(...)
    go_live_support: str = Field(...)


class TalentAssessmentStrategy(BaseModel):
    """Complete talent assessment strategy document."""

    strategy_id: str = Field(...)
    strategy_name: str = Field(...)
    version: str = Field("1.0")

    # Core elements
    vision: TalentAssessmentVision = Field(...)
    competency_framework: Optional[CompetencyFramework] = None
    governance: Optional[AssessmentGovernance] = None

    # Use cases
    use_cases: List[AssessmentUseCaseSpec] = Field(default_factory=list)
    use_case_priority_matrix: Dict[str, str] = Field(default_factory=dict)

    # Vendors
    vendor_evaluations: List[VendorEvaluation] = Field(default_factory=list)
    preferred_vendor_stack: List[AssessmentVendor] = Field(default_factory=list)

    # Investment
    roi_models: List[AssessmentROIModel] = Field(default_factory=list)
    total_investment_year_1: float = Field(0.0)
    total_investment_3_year: float = Field(0.0)

    # Implementation
    implementation_phases: List[Dict[str, Any]] = Field(default_factory=list)
    change_management: Optional[ChangeManagementPlan] = None

    # Technology
    technology_requirements: List[str] = Field(default_factory=list)
    integration_requirements: List[str] = Field(default_factory=list)

    # Compliance
    legal_compliance: List[str] = Field(default_factory=list)
    eeoc_considerations: List[str] = Field(default_factory=list)
    gdpr_considerations: List[str] = Field(default_factory=list)

    # Success metrics
    strategy_kpis: List[str] = Field(default_factory=list)
    measurement_approach: str = Field(...)

    # Document metadata
    created_date: date = Field(default_factory=date.today)
    last_updated: date = Field(default_factory=date.today)
    owner: Optional[str] = None
    approvers: List[str] = Field(default_factory=list)
