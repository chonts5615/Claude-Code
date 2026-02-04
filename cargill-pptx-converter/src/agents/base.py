"""
Base agent interface for all pipeline agents.
"""

import logging
from abc import ABC, abstractmethod

from src.schemas.run_state import RunState

logger = logging.getLogger("cargill_pptx")


class BaseAgent(ABC):
    """Abstract base class for pipeline agents."""

    def __init__(self, agent_id: str, step_name: str):
        self.agent_id = agent_id
        self.step_name = step_name
        self.logger = logging.getLogger(f"cargill_pptx.{agent_id}")

    @abstractmethod
    def execute(self, state: RunState) -> RunState:
        """
        Execute the agent's processing step.

        Args:
            state: Current pipeline run state.

        Returns:
            Updated run state with this agent's outputs.
        """
        ...

    def validate_inputs(self, state: RunState) -> bool:
        """
        Validate that required inputs are present in state.

        Returns:
            True if inputs are valid, False otherwise.
        """
        return True

    def _add_flag(self, state: RunState, severity: str, message: str):
        """Add a flag to the run state from this agent."""
        state.add_flag(
            step_id=self.agent_id,
            severity=severity,
            message=message,
        )
        log_level = {
            "CRITICAL": logging.CRITICAL,
            "ERROR": logging.ERROR,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
        }.get(severity, logging.INFO)
        self.logger.log(log_level, f"[{self.agent_id}] {message}")
