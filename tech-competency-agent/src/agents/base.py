from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from pydantic import BaseModel
from src.schemas.run_state import RunState, RunFlag

InputT = TypeVar('InputT', bound=BaseModel)
OutputT = TypeVar('OutputT', bound=BaseModel)


class BaseAgent(ABC, Generic[InputT, OutputT]):
    """Base class for all agents in the workflow."""

    def __init__(self, agent_id: str, step_name: str):
        self.agent_id = agent_id
        self.step_name = step_name

    @abstractmethod
    def execute(self, state: RunState) -> OutputT:
        """
        Execute agent logic.

        Args:
            state: Current workflow state

        Returns:
            Agent-specific output conforming to schema
        """
        pass

    def add_flag(
        self,
        state: RunState,
        severity: str,
        flag_type: str,
        message: str,
        job_id: str = None,
        metadata: dict = None
    ):
        """Add flag to run state."""
        flag = RunFlag(
            step_id=self.agent_id,
            job_id=job_id,
            severity=severity,
            flag_type=flag_type,
            message=message,
            metadata=metadata or {}
        )
        state.flags.append(flag)

    def validate_inputs(self, state: RunState) -> bool:
        """
        Validate required inputs exist in state.

        Override in subclasses to add specific validation.
        """
        return True

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return agent-specific system prompt."""
        pass
