"""Tests for base agent."""

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState


class MockAgent(BaseAgent):
    """Mock agent for testing."""

    def execute(self, state: RunState) -> RunState:
        """Mock execute."""
        state.current_step = self.agent_id
        return state

    def get_system_prompt(self) -> str:
        """Mock system prompt."""
        return "Mock system prompt"


def test_base_agent_initialization():
    """Test base agent initialization."""
    agent = MockAgent("TEST", "Test Agent")
    assert agent.agent_id == "TEST"
    assert agent.step_name == "Test Agent"


def test_base_agent_execute(sample_run_state):
    """Test base agent execute."""
    agent = MockAgent("TEST", "Test Agent")
    result = agent.execute(sample_run_state)
    assert result.current_step == "TEST"


def test_add_flag(sample_run_state):
    """Test adding flag to state."""
    agent = MockAgent("TEST", "Test Agent")
    agent.add_flag(
        sample_run_state,
        severity="WARNING",
        flag_type="TEST_FLAG",
        message="Test message"
    )
    assert len(sample_run_state.flags) == 1
    assert sample_run_state.flags[0].severity == "WARNING"


def test_get_system_prompt():
    """Test get system prompt."""
    agent = MockAgent("TEST", "Test Agent")
    prompt = agent.get_system_prompt()
    assert prompt == "Mock system prompt"
