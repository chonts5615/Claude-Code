"""Tests for agent implementations."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import date

from src.schemas.run_state import RunState, RunConfig, SeverityLevel, WorkflowPhase
from src.agents.base import BaseAgent, AgentChain


class MockAgent(BaseAgent):
    """Mock agent for testing."""

    def __init__(self):
        super().__init__(
            agent_id="TEST_Agent",
            step_name="Test Agent",
            phase=WorkflowPhase.ANALYSIS,
            model_name="test-model"
        )
        self.execute_called = False

    def get_system_prompt(self) -> str:
        return "You are a test agent."

    def execute(self, state: RunState) -> RunState:
        self.execute_called = True
        state.working_data["test_output"] = "test_value"
        return state


class TestBaseAgent:
    """Tests for BaseAgent class."""

    def test_agent_initialization(self):
        """Test agent initialization."""
        agent = MockAgent()
        assert agent.agent_id == "TEST_Agent"
        assert agent.step_name == "Test Agent"
        assert agent.phase == WorkflowPhase.ANALYSIS

    def test_pre_execute_updates_state(self):
        """Test pre_execute updates state tracking."""
        agent = MockAgent()
        state = RunState(run_id="test_run")

        state = agent.pre_execute(state)

        assert state.current_step == "TEST_Agent"
        assert state.current_phase == WorkflowPhase.ANALYSIS

    def test_post_execute_marks_complete(self):
        """Test post_execute marks step as complete."""
        agent = MockAgent()
        state = RunState(run_id="test_run")
        state.current_step = "TEST_Agent"

        state = agent.post_execute(state)

        assert "TEST_Agent" in state.completed_steps

    def test_add_flag(self):
        """Test adding flags through agent."""
        agent = MockAgent()
        state = RunState(run_id="test_run")
        state.current_phase = WorkflowPhase.ANALYSIS

        agent.add_flag(
            state,
            SeverityLevel.WARNING,
            "TEST_WARNING",
            "This is a test warning",
            metadata={"test_key": "test_value"}
        )

        assert len(state.flags) == 1
        assert state.flags[0].flag_type == "TEST_WARNING"
        assert state.flags[0].metadata["test_key"] == "test_value"

    def test_validate_inputs_default(self):
        """Test default input validation returns True."""
        agent = MockAgent()
        state = RunState(run_id="test_run")
        assert agent.validate_inputs(state) is True

    def test_get_required_inputs(self):
        """Test get_required_inputs returns empty list by default."""
        agent = MockAgent()
        assert agent.get_required_inputs() == []

    def test_get_output_keys(self):
        """Test get_output_keys returns empty list by default."""
        agent = MockAgent()
        assert agent.get_output_keys() == []

    def test_extract_json_from_response_code_block(self):
        """Test JSON extraction from markdown code blocks."""
        agent = MockAgent()
        response = '''Here is the result:
```json
{"key": "value", "number": 42}
```
That's the output.'''

        result = agent.extract_json_from_response(response)
        assert result["key"] == "value"
        assert result["number"] == 42

    def test_extract_json_from_response_plain(self):
        """Test JSON extraction from plain text."""
        agent = MockAgent()
        response = '{"key": "value"}'

        result = agent.extract_json_from_response(response)
        assert result["key"] == "value"

    def test_apply_learning_context_empty(self):
        """Test apply_learning_context with no learnings."""
        agent = MockAgent()
        state = RunState(run_id="test_run")

        learnings = agent.apply_learning_context(state)
        assert learnings == {}

    def test_apply_learning_context_with_data(self):
        """Test apply_learning_context with existing learnings."""
        agent = MockAgent()
        state = RunState(run_id="test_run")
        state.learning_context["TEST_Agent"] = {
            "prompt_additions": ["Additional guidance"]
        }

        learnings = agent.apply_learning_context(state)
        assert "prompt_additions" in learnings

    def test_get_prompt_with_learnings_no_learnings(self):
        """Test prompt generation without learnings."""
        agent = MockAgent()
        state = RunState(run_id="test_run")

        prompt = agent.get_prompt_with_learnings(state)
        assert prompt == "You are a test agent."

    def test_get_prompt_with_learnings_with_additions(self):
        """Test prompt generation with learning additions."""
        agent = MockAgent()
        state = RunState(run_id="test_run")
        state.learning_context["TEST_Agent"] = {
            "prompt_additions": ["Be more specific", "Include examples"]
        }

        prompt = agent.get_prompt_with_learnings(state)
        assert "Additional guidance from system learning" in prompt
        assert "Be more specific" in prompt


class TestAgentChain:
    """Tests for AgentChain class."""

    def test_chain_execution(self):
        """Test executing a chain of agents."""
        agent1 = MockAgent()
        agent1.agent_id = "Agent1"
        agent2 = MockAgent()
        agent2.agent_id = "Agent2"

        chain = AgentChain([agent1, agent2])
        state = RunState(run_id="test_run")

        result = chain.execute(state)

        assert agent1.execute_called
        assert agent2.execute_called
        assert "Agent1" in result.completed_steps
        assert "Agent2" in result.completed_steps

    def test_chain_stops_on_critical_flag(self):
        """Test chain stops when critical flag is raised."""
        class CriticalAgent(MockAgent):
            def execute(self, state):
                self.add_flag(
                    state,
                    SeverityLevel.CRITICAL,
                    "CRITICAL_ERROR",
                    "Critical error occurred"
                )
                return state

        agent1 = CriticalAgent()
        agent1.agent_id = "Agent1"
        agent2 = MockAgent()
        agent2.agent_id = "Agent2"

        chain = AgentChain([agent1, agent2])
        state = RunState(run_id="test_run")

        result = chain.execute(state)

        # Agent2 should not execute after critical flag
        assert not agent2.execute_called


class TestGoalGeneratorAgent:
    """Tests for GoalGeneratorAgent."""

    @pytest.fixture
    def goal_agent(self):
        """Create GoalGeneratorAgent instance."""
        from src.agents.goal_generator import GoalGeneratorAgent
        return GoalGeneratorAgent()

    def test_goal_agent_initialization(self, goal_agent):
        """Test GoalGeneratorAgent initialization."""
        assert goal_agent.agent_id == "S4_GoalGenerator"
        assert goal_agent.phase == WorkflowPhase.SYNTHESIS

    def test_goal_agent_required_inputs(self, goal_agent):
        """Test required inputs for goal generation."""
        required = goal_agent.get_required_inputs()
        assert "vision" in required
        assert "strategic_pillars" in required

    def test_goal_agent_validate_inputs_missing_pillars(self, goal_agent):
        """Test validation fails without pillars."""
        state = RunState(run_id="test_run")
        state.working_data["strategic_pillars"] = []

        assert goal_agent.validate_inputs(state) is False

    def test_goal_agent_validate_inputs_with_pillars(self, goal_agent):
        """Test validation passes with pillars."""
        state = RunState(run_id="test_run")
        state.working_data["strategic_pillars"] = [{"pillar_id": "PIL_001"}]

        assert goal_agent.validate_inputs(state) is True


class TestValidatorAgent:
    """Tests for ValidatorAgent."""

    @pytest.fixture
    def validator_agent(self):
        """Create ValidatorAgent instance."""
        from src.agents.validator import ValidatorAgent
        return ValidatorAgent()

    def test_validator_initialization(self, validator_agent):
        """Test ValidatorAgent initialization."""
        assert validator_agent.agent_id == "S9_Validator"
        assert validator_agent.phase == WorkflowPhase.VALIDATION

    def test_validator_required_inputs(self, validator_agent):
        """Test required inputs for validation."""
        required = validator_agent.get_required_inputs()
        assert "strategic_pillars" in required
        assert "strategic_goals" in required


class TestFeedbackProcessorAgent:
    """Tests for FeedbackProcessorAgent."""

    @pytest.fixture
    def feedback_agent(self):
        """Create FeedbackProcessorAgent instance."""
        from src.agents.feedback_processor import FeedbackProcessorAgent
        return FeedbackProcessorAgent()

    def test_feedback_processor_initialization(self, feedback_agent):
        """Test FeedbackProcessorAgent initialization."""
        assert feedback_agent.agent_id == "F1_FeedbackProcessor"
        assert feedback_agent.phase == WorkflowPhase.FEEDBACK

    def test_feedback_processor_system_prompt(self, feedback_agent):
        """Test system prompt contains key concepts."""
        prompt = feedback_agent.get_system_prompt()
        assert "feedback" in prompt.lower()
        assert "learning" in prompt.lower()


class TestLearningOptimizerAgent:
    """Tests for LearningOptimizerAgent."""

    @pytest.fixture
    def learning_agent(self):
        """Create LearningOptimizerAgent instance."""
        from src.agents.learning_optimizer import LearningOptimizerAgent
        return LearningOptimizerAgent()

    def test_learning_optimizer_initialization(self, learning_agent):
        """Test LearningOptimizerAgent initialization."""
        assert learning_agent.agent_id == "F2_LearningOptimizer"
        assert learning_agent.phase == WorkflowPhase.FEEDBACK

    def test_learning_optimizer_skips_without_insights(self, learning_agent):
        """Test optimizer skips when no insights available."""
        state = RunState(run_id="test_run")
        state.working_data["learning_insights"] = []

        result = learning_agent.execute(state)

        # Should return state unchanged (no optimizations)
        assert "optimization_recommendations" not in result.working_data


class TestTalentAssessmentSpecialistAgent:
    """Tests for TalentAssessmentSpecialistAgent."""

    @pytest.fixture
    def ta_agent(self):
        """Create TalentAssessmentSpecialistAgent instance."""
        from src.agents.talent_assessment_specialist import TalentAssessmentSpecialistAgent
        return TalentAssessmentSpecialistAgent()

    def test_ta_specialist_initialization(self, ta_agent):
        """Test TalentAssessmentSpecialistAgent initialization."""
        assert ta_agent.agent_id == "TA1_TalentAssessmentSpecialist"
        assert ta_agent.phase == WorkflowPhase.SYNTHESIS

    def test_ta_specialist_system_prompt(self, ta_agent):
        """Test system prompt contains IO psychology terms."""
        prompt = ta_agent.get_system_prompt()
        assert "Industrial-Organizational" in prompt or "IO" in prompt
        assert "validity" in prompt.lower()
        assert "psychometric" in prompt.lower()

    def test_detect_talent_context_positive(self, ta_agent):
        """Test context detection identifies talent assessment."""
        vision = {"vision_statement": "World-class talent assessment"}
        context = {"summary": "Improve hiring quality and selection"}

        result = ta_agent._detect_talent_assessment_context(vision, context)
        assert result is True

    def test_detect_talent_context_negative(self, ta_agent):
        """Test context detection for non-talent context."""
        vision = {"vision_statement": "Be the market leader in widgets"}
        context = {"summary": "Expand manufacturing capacity"}

        result = ta_agent._detect_talent_assessment_context(vision, context)
        assert result is False
