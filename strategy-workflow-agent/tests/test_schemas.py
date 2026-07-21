"""Tests for Pydantic schemas."""

import pytest
from datetime import date, datetime
from pathlib import Path

from src.schemas.run_state import (
    RunState, RunInputs, RunConfig, ThresholdConfig, FeedbackConfig,
    ArtifactRegistry, RunFlag, QASummary, SeverityLevel, WorkflowPhase
)
from src.schemas.strategy import (
    StrategicVision, StrategicPillar, StrategicGoal, Initiative,
    Milestone, KPI, RiskAssessment, ResourceAllocation, ExecutionPlan,
    StrategicPriority, GoalStatus, RiskCategory, RiskSeverity
)
from src.schemas.feedback import (
    FeedbackEntry, LearningInsight, OptimizationRecommendation,
    FeedbackLoopState, FeedbackType, LearningCategory, OptimizationType
)
from src.schemas.talent_assessment import (
    TalentAssessmentVision, AssessmentUseCaseSpec, CompetencyFramework,
    VendorEvaluation, AssessmentROIModel, AssessmentUseCase, AssessmentType,
    AssessmentVendor, JobLevel
)


class TestRunStateSchemas:
    """Tests for run state schemas."""

    def test_run_state_creation(self):
        """Test creating a basic RunState."""
        state = RunState(run_id="test_run_001")
        assert state.run_id == "test_run_001"
        assert state.current_phase == WorkflowPhase.INGESTION
        assert len(state.completed_steps) == 0
        assert len(state.flags) == 0

    def test_run_state_with_inputs(self):
        """Test RunState with input configuration."""
        inputs = RunInputs(
            raw_vision_text="Our vision is to lead the industry",
            raw_goals_text="Increase market share by 20%"
        )
        state = RunState(run_id="test_run_002", inputs=inputs)
        assert state.inputs.raw_vision_text == "Our vision is to lead the industry"

    def test_threshold_config_defaults(self):
        """Test ThresholdConfig default values."""
        config = ThresholdConfig()
        assert config.goal_smart_score_min == 0.7
        assert config.initiative_feasibility_min == 0.6
        assert config.alignment_score_min == 0.75

    def test_threshold_config_validation(self):
        """Test ThresholdConfig value validation."""
        with pytest.raises(ValueError):
            ThresholdConfig(goal_smart_score_min=1.5)  # Must be <= 1.0

    def test_feedback_config(self):
        """Test FeedbackConfig creation."""
        config = FeedbackConfig(
            enabled=True,
            learning_rate=0.15,
            auto_optimize=True
        )
        assert config.enabled is True
        assert config.learning_rate == 0.15

    def test_run_flag_creation(self):
        """Test RunFlag creation."""
        flag = RunFlag(
            step_id="S1_VisionExtractor",
            phase=WorkflowPhase.INGESTION,
            severity=SeverityLevel.WARNING,
            flag_type="LOW_CONFIDENCE",
            message="Vision extraction confidence below threshold"
        )
        assert flag.resolved is False
        assert flag.severity == SeverityLevel.WARNING

    def test_add_flag_to_state(self):
        """Test adding flags to RunState."""
        state = RunState(run_id="test_run_003")
        state.add_flag(
            step_id="S1",
            severity=SeverityLevel.INFO,
            flag_type="TEST_FLAG",
            message="Test message"
        )
        assert len(state.flags) == 1
        assert state.flags[0].flag_type == "TEST_FLAG"

    def test_get_unresolved_flags(self):
        """Test filtering unresolved flags."""
        state = RunState(run_id="test_run_004")
        state.add_flag("S1", SeverityLevel.INFO, "INFO_FLAG", "Info")
        state.add_flag("S2", SeverityLevel.WARNING, "WARN_FLAG", "Warning")
        state.add_flag("S3", SeverityLevel.ERROR, "ERROR_FLAG", "Error")

        warnings_and_above = state.get_unresolved_flags(SeverityLevel.WARNING)
        assert len(warnings_and_above) == 2

    def test_mark_step_complete(self):
        """Test marking steps as complete."""
        state = RunState(run_id="test_run_005")
        state.mark_step_complete("S1_VisionExtractor")
        state.mark_step_complete("S2_ContextAnalyzer")
        assert "S1_VisionExtractor" in state.completed_steps
        assert len(state.completed_steps) == 2


class TestStrategySchemas:
    """Tests for strategy domain schemas."""

    def test_strategic_vision(self):
        """Test StrategicVision schema."""
        vision = StrategicVision(
            vision_statement="To be the world leader in sustainable energy",
            mission_statement="Providing clean energy solutions globally",
            core_values=["Innovation", "Sustainability", "Integrity"],
            time_horizon_years=3
        )
        assert vision.time_horizon_years == 3
        assert "Innovation" in vision.core_values

    def test_strategic_pillar(self):
        """Test StrategicPillar schema."""
        pillar = StrategicPillar(
            pillar_id="PIL_001",
            name="Digital Transformation",
            description="Modernize technology infrastructure",
            rationale="Enable competitive advantage through technology",
            vision_alignment="Supports vision of innovation leadership",
            priority=StrategicPriority.HIGH
        )
        assert pillar.priority == StrategicPriority.HIGH

    def test_strategic_goal_smart(self):
        """Test StrategicGoal with SMART criteria."""
        goal = StrategicGoal(
            goal_id="GOAL_001",
            pillar_id="PIL_001",
            name="Increase Cloud Adoption",
            description="Migrate 80% of applications to cloud",
            specific="Migrate 80% of tier-1 applications to AWS/Azure",
            measurable="Track migration percentage monthly",
            achievable="Based on industry benchmarks and team capacity",
            relevant="Supports digital transformation pillar",
            time_bound="Complete by Q4 2026",
            smart_score=0.85,
            feasibility_score=0.80,
            impact_score=0.90
        )
        assert goal.smart_score == 0.85
        assert goal.status == GoalStatus.DRAFT

    def test_initiative_creation(self):
        """Test Initiative schema."""
        initiative = Initiative(
            initiative_id="INIT_001",
            goal_id="GOAL_001",
            name="Cloud Migration Program",
            description="Phased migration to cloud infrastructure",
            objective="Migrate 50 applications in Year 1",
            estimated_budget=500000,
            fte_required=5.0,
            feasibility_score=0.75
        )
        assert initiative.estimated_budget == 500000

    def test_risk_assessment(self):
        """Test RiskAssessment schema."""
        risk = RiskAssessment(
            risk_id="RISK_001",
            name="Vendor Lock-in Risk",
            description="Dependency on single cloud provider",
            category=RiskCategory.TECHNOLOGY,
            severity=RiskSeverity.MEDIUM,
            likelihood=0.4,
            impact=0.6
        )
        risk.calculate_risk_score()
        assert risk.risk_score == 0.24

    def test_kpi_schema(self):
        """Test KPI schema."""
        kpi = KPI(
            kpi_id="KPI_001",
            name="Cloud Adoption Rate",
            description="Percentage of applications in cloud",
            unit="%",
            target_value=80.0,
            target_date=date(2026, 12, 31),
            baseline_value=20.0
        )
        assert kpi.target_value == 80.0


class TestFeedbackSchemas:
    """Tests for feedback loop schemas."""

    def test_feedback_entry(self):
        """Test FeedbackEntry schema."""
        entry = FeedbackEntry(
            feedback_id="FB_001",
            run_id="run_001",
            feedback_type=FeedbackType.USER_RATING,
            category=LearningCategory.QUALITY,
            rating=4.5,
            comment="Good goal clarity"
        )
        assert entry.rating == 4.5
        assert entry.processed is False

    def test_learning_insight(self):
        """Test LearningInsight schema."""
        insight = LearningInsight(
            insight_id="INS_001",
            category=LearningCategory.QUALITY,
            title="Goals need more specificity",
            description="Users frequently request more specific goals",
            pattern_type="quality_feedback",
            confidence=0.8,
            importance=0.7,
            evidence=["FB_001", "FB_002", "FB_003"],
            sample_size=3,
            is_actionable=True
        )
        assert insight.confidence == 0.8
        assert len(insight.evidence) == 3

    def test_optimization_recommendation(self):
        """Test OptimizationRecommendation schema."""
        opt = OptimizationRecommendation(
            optimization_id="OPT_001",
            insight_id="INS_001",
            optimization_type=OptimizationType.THRESHOLD_ADJUSTMENT,
            target_component="config.thresholds.goal_smart_score_min",
            category=LearningCategory.QUALITY,
            title="Increase SMART score threshold",
            description="Raise threshold from 0.7 to 0.75",
            rationale="Higher threshold improves goal quality",
            current_value=0.7,
            recommended_value=0.75,
            expected_impact=0.15,
            confidence=0.8,
            risk_level="low"
        )
        assert opt.optimization_type == OptimizationType.THRESHOLD_ADJUSTMENT

    def test_feedback_loop_state(self):
        """Test FeedbackLoopState schema."""
        loop_state = FeedbackLoopState(
            loop_id="LOOP_001",
            total_feedback_entries=100,
            total_insights=10,
            total_optimizations=5,
            applied_optimizations=3,
            optimization_success_rate=0.8
        )
        assert loop_state.total_feedback_entries == 100


class TestTalentAssessmentSchemas:
    """Tests for talent assessment domain schemas."""

    def test_talent_assessment_vision(self):
        """Test TalentAssessmentVision schema."""
        vision = TalentAssessmentVision(
            vision_statement="World-class talent assessment driving business outcomes",
            mission_statement="Enable evidence-based talent decisions globally",
            business_strategy_alignment="Supports growth through talent quality",
            talent_strategy_alignment="Backbone of talent management lifecycle",
            guiding_principles=["Evidence-based", "Fair and unbiased", "Candidate-centric"],
            fiscal_year_start="FY26",
            fiscal_year_end="FY29"
        )
        assert vision.fiscal_year_start == "FY26"

    def test_assessment_use_case_spec(self):
        """Test AssessmentUseCaseSpec schema."""
        use_case = AssessmentUseCaseSpec(
            use_case_id="UC_001",
            use_case=AssessmentUseCase.EXTERNAL_HIRING,
            name="Professional Hiring Assessment",
            description="Assessment battery for professional-level hiring",
            business_need="Improve quality of hire for professional roles",
            volume_estimate=5000,
            target_job_levels=[JobLevel.PROFESSIONAL, JobLevel.SENIOR_PROFESSIONAL],
            recommended_assessments=[AssessmentType.COGNITIVE_ABILITY, AssessmentType.PERSONALITY],
            preferred_vendors=[AssessmentVendor.SHL, AssessmentVendor.HOGAN],
            priority="high",
            implementation_phase=1
        )
        assert use_case.volume_estimate == 5000
        assert AssessmentType.COGNITIVE_ABILITY in use_case.recommended_assessments

    def test_vendor_evaluation(self):
        """Test VendorEvaluation schema."""
        evaluation = VendorEvaluation(
            vendor=AssessmentVendor.SHL,
            vendor_name="SHL",
            assessment_types_offered=[AssessmentType.COGNITIVE_ABILITY, AssessmentType.PERSONALITY],
            validity_evidence=4.5,
            reliability=4.5,
            adverse_impact=3.0,
            user_experience=4.0,
            global_coverage=5.0,
            overall_score=4.2,
            recommendation="preferred",
            strengths=["Strong validity", "Global reach"],
            weaknesses=["Higher cost"]
        )
        assert evaluation.overall_score == 4.2
        assert evaluation.recommendation == "preferred"

    def test_assessment_roi_model(self):
        """Test AssessmentROIModel schema."""
        roi = AssessmentROIModel(
            model_id="ROI_001",
            use_case=AssessmentUseCase.EXTERNAL_HIRING,
            initial_investment=250000,
            annual_operating_cost=150000,
            annual_volume=5000,
            cost_per_assessment=30,
            quality_of_hire_improvement=0.15,
            turnover_reduction=0.10,
            cost_of_bad_hire=75000,
            year_1_roi=0.85,
            year_3_roi=2.50,
            payback_period_months=14
        )
        assert roi.year_1_roi == 0.85
        assert roi.payback_period_months == 14


class TestSchemasSerialization:
    """Tests for schema serialization and deserialization."""

    def test_run_state_to_json(self):
        """Test RunState serialization to JSON."""
        state = RunState(run_id="test_run")
        state.add_flag("S1", SeverityLevel.INFO, "TEST", "Test message")
        json_data = state.model_dump_json()
        assert "test_run" in json_data
        assert "TEST" in json_data

    def test_run_state_from_json(self):
        """Test RunState deserialization from JSON."""
        state = RunState(run_id="test_run")
        json_data = state.model_dump_json()
        restored = RunState.model_validate_json(json_data)
        assert restored.run_id == "test_run"

    def test_complex_nested_serialization(self):
        """Test serialization of nested schemas."""
        config = RunConfig(
            output_format="comprehensive",
            time_horizon_years=3,
            thresholds=ThresholdConfig(goal_smart_score_min=0.75),
            feedback=FeedbackConfig(enabled=True, auto_optimize=True)
        )
        json_data = config.model_dump_json()
        assert "0.75" in json_data

        restored = RunConfig.model_validate_json(json_data)
        assert restored.thresholds.goal_smart_score_min == 0.75
