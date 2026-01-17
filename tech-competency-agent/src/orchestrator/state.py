"""State management for workflow orchestration."""

from typing import TypedDict, Annotated
from operator import add

from src.schemas.run_state import RunState, RunFlag


class WorkflowState(TypedDict):
    """State passed through LangGraph workflow."""
    run_state: RunState
    flags: Annotated[list[RunFlag], add]  # Accumulate flags


def update_state(current: WorkflowState, update: dict) -> WorkflowState:
    """Update workflow state with new values."""
    new_state = current.copy()
    new_state.update(update)
    return new_state
