"""Tests for workflow orchestration and quality gates."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.schemas.run_state import RunState, RunConfig, ThresholdConfig, SeverityLevel
from src.orchestrator.gates import QualityGate, GateResult


class TestQualityGates:
    """Tests for quality gate validations."""

    @pytest.fixture
    def thresholds(self):
        """Create default thresholds."""
        return ThresholdConfig()

    @pytest.fixture
    def gate(self, thresholds):
        """Create QualityGate instance."""
        return QualityGate("TestGate", thresholds)

    def test_gate_initialization(self, gate):
        """Test gate initialization."""
        assert gate.gate_id == "TestGate"

    def test_validate_vision_extraction_pass(self, gate):
        """Test vision validation passes with valid data."""
        state = RunState(run_id="test_run")
        state.working_data["vision"] = {
            "vision_statement": "Be the industry leader",
            "mission_statement": "Deliver value to customers",
            "confidence_score": 0.9
        }

        results = gate.validate_vision_extraction(state)

        passing = [r for r in results if r.passed]
        assert len(passing) > 0

    def test_validate_vision_extraction_fail_missing(self, gate):
        """Test vision validation fails when missing."""
        state = RunState(run_id="test_run")
        state.working_data["vision"] = None

        results = gate.validate_vision_extraction(state)

        failed = [r for r in results if not r.passed]
        assert len(failed) > 0

    def test_validate_pillar_synthesis_pass(self, gate):
        """Test pillar validation passes with valid count."""
        state = RunState(run_id="test_run")
        state.working_data["strategic_pillars"] = [
            {"pillar_id": "P1", "name": "Growth"},
            {"pillar_id": "P2", "name": "Innovation"},
            {"pillar_id": "P3", "name": "Excellence"},
        ]

        results = gate.validate_pillar_synthesis(state)

        # Should have pillar count validation passing
        pillar_count_results = [r for r in results if "pillar" in r.rule_name.lower()]
        assert any(r.passed for r in pillar_count_results)

    def test_validate_pillar_synthesis_fail_few(self, gate):
        """Test pillar validation fails with too few pillars."""
        state = RunState(run_id="test_run")
        state.working_data["strategic_pillars"] = [
            {"pillar_id": "P1", "name": "Growth"},
        ]

        results = gate.validate_pillar_synthesis(state)

        # Should flag insufficient pillars
        failed = [r for r in results if not r.passed]
        assert len(failed) > 0

    def test_validate_goal_generation_pass(self, gate):
        """Test goal validation passes with valid goals."""
        state = RunState(run_id="test_run")
        state.working_data["strategic_goals"] = [
            {"goal_id": "G1", "smart_score": 0.85},
            {"goal_id": "G2", "smart_score": 0.80},
        ]
        state.working_data["goal_quality_summary"] = {
            "average_smart_score": 0.82
        }

        results = gate.validate_goal_generation(state)

        # Should validate SMART scores
        passing = [r for r in results if r.passed]
        assert len(passing) > 0

    def test_validate_goal_generation_fail_low_smart(self, gate):
        """Test goal validation fails with low SMART scores."""
        state = RunState(run_id="test_run")
        state.working_data["strategic_goals"] = [
            {"goal_id": "G1", "smart_score": 0.50},
        ]
        state.working_data["goal_quality_summary"] = {
            "average_smart_score": 0.50
        }

        results = gate.validate_goal_generation(state)

        # Should flag low SMART score
        failed = [r for r in results if not r.passed]
        assert any("smart" in r.rule_name.lower() for r in failed)

    def test_validate_initiative_design_pass(self, gate):
        """Test initiative validation passes with valid initiatives."""
        state = RunState(run_id="test_run")
        state.working_data["initiatives"] = [
            {"initiative_id": "I1", "feasibility_score": 0.75},
            {"initiative_id": "I2", "feasibility_score": 0.80},
        ]

        results = gate.validate_initiative_design(state)

        passing = [r for r in results if r.passed]
        assert len(passing) > 0

    def test_validate_risk_assessment_pass(self, gate):
        """Test risk validation passes with adequate coverage."""
        state = RunState(run_id="test_run")
        state.working_data["risks"] = [
            {"risk_id": "R1", "severity": "high", "mitigation_strategy": "Plan A"},
            {"risk_id": "R2", "severity": "medium", "mitigation_strategy": "Plan B"},
        ]
        state.working_data["risk_summary"] = {
            "mitigation_coverage": 0.85,
            "critical_risks_unmitigated": 0
        }

        results = gate.validate_risk_assessment(state)

        # Should validate risk coverage
        passing = [r for r in results if r.passed]
        assert len(passing) > 0

    def test_validate_risk_assessment_fail_low_coverage(self, gate):
        """Test risk validation fails with low mitigation coverage."""
        state = RunState(run_id="test_run")
        state.working_data["risks"] = [
            {"risk_id": "R1", "severity": "high", "mitigation_strategy": None},
        ]
        state.working_data["risk_summary"] = {
            "mitigation_coverage": 0.50,
            "critical_risks_unmitigated": 2
        }

        results = gate.validate_risk_assessment(state)

        failed = [r for r in results if not r.passed]
        assert len(failed) > 0

    def test_validate_strategy_quality_pass(self, gate):
        """Test final quality validation passes."""
        state = RunState(run_id="test_run")
        state.working_data["quality_scores"] = {
            "alignment_score": 0.85,
            "coherence_score": 0.90,
            "completeness_score": 0.88,
            "feasibility_score": 0.75
        }

        results = gate.validate_strategy_quality(state)

        passing = [r for r in results if r.passed]
        assert len(passing) >= 3


class TestGateResult:
    """Tests for GateResult class."""

    def test_gate_result_creation(self):
        """Test GateResult creation."""
        result = GateResult(
            rule_name="test_rule",
            passed=True,
            severity="INFO",
            message="Test passed",
            blocking=False
        )
        assert result.passed is True
        assert result.blocking is False

    def test_gate_result_blocking(self):
        """Test blocking GateResult."""
        result = GateResult(
            rule_name="critical_check",
            passed=False,
            severity="CRITICAL",
            message="Critical failure",
            blocking=True
        )
        assert result.passed is False
        assert result.blocking is True


class TestWorkflowOrchestrator:
    """Tests for StrategyWorkflowOrchestrator."""

    @pytest.fixture
    def mock_orchestrator(self):
        """Create orchestrator with mocked agents."""
        with patch('src.orchestrator.graph.VisionExtractorAgent'), \
             patch('src.orchestrator.graph.ContextAnalyzerAgent'), \
             patch('src.orchestrator.graph.PillarSynthesizerAgent'), \
             patch('src.orchestrator.graph.GoalGeneratorAgent'), \
             patch('src.orchestrator.graph.InitiativeDesignerAgent'), \
             patch('src.orchestrator.graph.RiskAssessorAgent'), \
             patch('src.orchestrator.graph.ResourcePlannerAgent'), \
             patch('src.orchestrator.graph.TimelineOptimizerAgent'), \
             patch('src.orchestrator.graph.ValidatorAgent'), \
             patch('src.orchestrator.graph.OutputGeneratorAgent'), \
             patch('src.orchestrator.graph.FeedbackProcessorAgent'), \
             patch('src.orchestrator.graph.LearningOptimizerAgent'):
            from src.orchestrator.graph import StrategyWorkflowOrchestrator
            return StrategyWorkflowOrchestrator()

    def test_orchestrator_initialization(self, mock_orchestrator):
        """Test orchestrator initialization."""
        assert mock_orchestrator.enable_feedback_loop is True
        assert mock_orchestrator.graph is not None

    def test_route_after_gate_continue(self, mock_orchestrator):
        """Test routing continues when no blocking failures."""
        state = RunState(run_id="test_run")
        state.current_step = "G1_Vision"
        state.working_data["G1_Vision_blocking_failures"] = 0

        result = mock_orchestrator._route_after_gate(state)
        assert result == "continue"

    def test_route_after_gate_fail(self, mock_orchestrator):
        """Test routing fails when blocking failures exist."""
        state = RunState(run_id="test_run")
        state.current_step = "G1_Vision"
        state.working_data["G1_Vision_blocking_failures"] = 1

        result = mock_orchestrator._route_after_gate(state)
        assert result == "fail"

    def test_route_after_gate_strict_mode(self, mock_orchestrator):
        """Test routing fails in strict mode with errors."""
        state = RunState(run_id="test_run")
        state.config.strict_mode = True
        state.current_step = "G1_Vision"
        state.working_data["G1_Vision_blocking_failures"] = 0
        state.add_flag("G1_Vision", SeverityLevel.ERROR, "ERROR", "Error message")

        result = mock_orchestrator._route_after_gate(state)
        assert result == "fail"

    def test_route_after_validation_continue(self, mock_orchestrator):
        """Test validation routing continues when ready."""
        state = RunState(run_id="test_run")
        state.working_data["G6_Validation_blocking_failures"] = 0
        state.working_data["validation_result"] = {
            "certification": {
                "ready_for_approval": True,
                "blocking_issues": []
            }
        }

        result = mock_orchestrator._route_after_validation(state)
        assert result == "continue"

    def test_route_after_validation_fail(self, mock_orchestrator):
        """Test validation routing fails with blocking issues."""
        state = RunState(run_id="test_run")
        state.working_data["G6_Validation_blocking_failures"] = 0
        state.working_data["validation_result"] = {
            "certification": {
                "ready_for_approval": False,
                "blocking_issues": ["Low alignment score"]
            }
        }

        result = mock_orchestrator._route_after_validation(state)
        assert result == "fail"


class TestCreateInitialState:
    """Tests for state initialization helper."""

    def test_create_initial_state_basic(self):
        """Test creating initial state with basic inputs."""
        from src.orchestrator import create_initial_state

        state = create_initial_state(
            vision_text="Our vision is excellence"
        )

        assert state.run_id is not None
        assert state.inputs.raw_vision_text == "Our vision is excellence"

    def test_create_initial_state_with_options(self):
        """Test creating initial state with all options."""
        from src.orchestrator import create_initial_state

        state = create_initial_state(
            vision_text="Our vision",
            goals_text="Our goals",
            context_text="Our context",
            time_horizon_years=5,
            output_format="executive",
            enable_feedback=True,
            auto_optimize=False,
            strict_mode=True
        )

        assert state.config.time_horizon_years == 5
        assert state.config.output_format == "executive"
        assert state.config.feedback.enabled is True
        assert state.config.feedback.auto_optimize is False
        assert state.config.strict_mode is True


class TestFeedbackLoopIntegration:
    """Tests for feedback loop integration."""

    def test_feedback_loop_disabled(self):
        """Test workflow runs without feedback when disabled."""
        state = RunState(run_id="test_run")
        state.config.feedback.enabled = False

        # Feedback processor should skip processing
        from src.agents.feedback_processor import FeedbackProcessorAgent
        agent = FeedbackProcessorAgent()

        # Should return early without processing
        result = agent.execute(state)
        assert "learning_insights" not in result.working_data

    def test_learning_context_persists(self):
        """Test learning context persists across optimization."""
        state = RunState(run_id="test_run")
        state.learning_context["S4_GoalGenerator"] = {
            "prompt_additions": ["Be more specific"]
        }

        # Verify learning context available to agent
        from src.agents.goal_generator import GoalGeneratorAgent
        agent = GoalGeneratorAgent()

        prompt = agent.get_prompt_with_learnings(state)
        assert "Be more specific" in prompt

    def test_optimization_round_increments(self):
        """Test optimization round increments correctly."""
        state = RunState(run_id="test_run")
        assert state.optimization_round == 0

        state.optimization_round += 1
        assert state.optimization_round == 1
