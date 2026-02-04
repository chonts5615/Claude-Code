"""State management utilities for the workflow."""

from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
import uuid

from src.schemas.run_state import RunState, RunInputs, RunConfig, ThresholdConfig, FeedbackConfig


def create_initial_state(
    vision_text: Optional[str] = None,
    goals_text: Optional[str] = None,
    context_text: Optional[str] = None,
    vision_document: Optional[Path] = None,
    time_horizon_years: int = 3,
    output_format: str = "comprehensive",
    enable_feedback: bool = True,
    auto_optimize: bool = True,
    strict_mode: bool = False,
    **kwargs
) -> RunState:
    """
    Create an initial run state with the given inputs.

    Args:
        vision_text: Raw text containing vision/strategy content
        goals_text: Raw text containing goals
        context_text: Additional context text
        vision_document: Path to vision document file
        time_horizon_years: Planning horizon (1-10 years)
        output_format: Output format (comprehensive, executive, minimal)
        enable_feedback: Enable the learning feedback loop
        auto_optimize: Automatically apply optimizations
        strict_mode: Fail on any quality gate violation
        **kwargs: Additional configuration overrides

    Returns:
        Initialized RunState ready for workflow execution
    """
    # Create run ID
    run_id = f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

    # Build inputs
    inputs = RunInputs(
        raw_vision_text=vision_text,
        raw_goals_text=goals_text,
        raw_context_text=context_text,
        vision_document=vision_document,
    )

    # Build thresholds (can be overridden via kwargs)
    threshold_overrides = {k: v for k, v in kwargs.items() if hasattr(ThresholdConfig, k)}
    thresholds = ThresholdConfig(**threshold_overrides)

    # Build feedback config
    feedback_config = FeedbackConfig(
        enabled=enable_feedback,
        auto_optimize=auto_optimize,
    )

    # Build run config
    config = RunConfig(
        time_horizon_years=time_horizon_years,
        output_format=output_format,
        thresholds=thresholds,
        feedback=feedback_config,
        strict_mode=strict_mode,
    )

    # Create and return state
    return RunState(
        run_id=run_id,
        inputs=inputs,
        config=config,
    )


def load_state_from_checkpoint(checkpoint_path: Path) -> RunState:
    """
    Load a run state from a checkpoint file.

    Args:
        checkpoint_path: Path to the checkpoint JSON file

    Returns:
        Restored RunState
    """
    import json

    with open(checkpoint_path, 'r') as f:
        data = json.load(f)

    return RunState.model_validate(data)


def save_state_checkpoint(state: RunState, output_dir: Path) -> Path:
    """
    Save the current state to a checkpoint file.

    Args:
        state: Current run state
        output_dir: Directory to save checkpoint

    Returns:
        Path to saved checkpoint file
    """
    import json

    output_dir.mkdir(parents=True, exist_ok=True)

    checkpoint_name = f"{state.run_id}_checkpoint_{state.current_step or 'init'}.json"
    checkpoint_path = output_dir / checkpoint_name

    with open(checkpoint_path, 'w') as f:
        json.dump(state.model_dump(mode='json'), f, indent=2, default=str)

    return checkpoint_path


def save_final_state(state: RunState, output_dir: Path) -> Path:
    """
    Save the final state after workflow completion.

    Args:
        state: Final run state
        output_dir: Directory to save output

    Returns:
        Path to saved state file
    """
    import json

    output_dir.mkdir(parents=True, exist_ok=True)

    output_name = f"{state.run_id}_final_state.json"
    output_path = output_dir / output_name

    with open(output_path, 'w') as f:
        json.dump(state.model_dump(mode='json'), f, indent=2, default=str)

    return output_path


def extract_working_data(state: RunState, keys: Optional[list[str]] = None) -> Dict[str, Any]:
    """
    Extract specific working data from state.

    Args:
        state: Current run state
        keys: Specific keys to extract (all if None)

    Returns:
        Dictionary of extracted data
    """
    if keys is None:
        return dict(state.working_data)

    return {k: state.working_data.get(k) for k in keys if k in state.working_data}
