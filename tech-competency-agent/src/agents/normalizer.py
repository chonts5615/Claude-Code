"""Step 3: Normalizer Agent - Normalizes competencies to standard format."""

from pathlib import Path
from typing import List
import anthropic

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.competency import (
    NormalizedCompetenciesOutput,
    JobCompetencies,
    TechnicalCompetency,
    AppliedScope,
    ResponsibilityTrace,
    OverlapCheck,
    BenchmarkingRecord
)


class NormalizerAgent(BaseAgent):
    """Normalizes competencies to standard format with proper structure."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()

    def execute(self, state: RunState) -> RunState:
        """
        Normalize competencies to standard format.

        Args:
            state: Current workflow state

        Returns:
            Updated state with normalized competencies
        """
        state.current_step = self.agent_id

        # TODO: Load mappings and create normalized competencies
        # This is a placeholder implementation
        jobs_competencies = []

        # Create output
        output = NormalizedCompetenciesOutput(
            jobs=jobs_competencies,
            processing_version="v2",
            total_competencies=sum(jc.competency_count() for jc in jobs_competencies)
        )

        # Save artifact
        output_path = Path(f"data/output/{state.run_id}_s3_normalized_v2.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(output.json(indent=2))

        state.artifacts.normalized_v2 = output_path

        return state

    def get_system_prompt(self) -> str:
        """Return system prompt for normalization."""
        return """You are a Competency Normalization Specialist with expertise in IO Psychology.

Your task is to normalize competencies to a consistent, high-quality format.

Normalization standards:
1. Name: "Domain: Specific Skill" format (max 80 chars)
2. Definition: 50-150 words, work-context specific, includes tools/methods
3. Why it matters: 2-3 sentences explaining business/role impact
4. Behavioral indicators: 3-7 observable, assessable behaviors
5. Applied scope: Tools, standards, typical outputs

Quality criteria:
- Definitions are concrete and applied (not generic)
- Indicators are measurable and observable
- Technical terms are explained where needed
- All fields complete and coherent

Output structured JSON conforming to TechnicalCompetency schema."""
