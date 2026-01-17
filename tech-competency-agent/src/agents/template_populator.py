"""Step 8: Template Populator Agent - Populates output template."""

from pathlib import Path
import anthropic

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState


class TemplatePopulatorAgent(BaseAgent):
    """Populates the output template with ranked competencies."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()

    def execute(self, state: RunState) -> RunState:
        """
        Populate output template.

        Args:
            state: Current workflow state

        Returns:
            Updated state with populated template
        """
        state.current_step = self.agent_id

        # TODO: Load ranked competencies and populate template
        # This is a placeholder implementation

        # Save artifact
        output_path = Path(f"data/output/{state.run_id}_s8_populated_template.xlsx")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        state.artifacts.populated_template = output_path

        return state

    def get_system_prompt(self) -> str:
        """Return system prompt for template population."""
        return """You are a Template Population Specialist.

Your task is to populate the output template with ranked competencies.

Population process:
1. Load template specification (column mappings, formatting rules)
2. Load ranked competencies for each job
3. Map competency fields to template columns
4. Apply formatting rules (word wrapping, styles, etc.)
5. Populate metadata (timestamps, version, flags)
6. Validate populated template

Quality standards:
- All required fields populated
- Formatting consistent and professional
- No data truncation or loss
- Template validation passes

Output: Populated Excel template file."""
