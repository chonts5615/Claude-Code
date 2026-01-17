"""Step 6: Benchmark Researcher Agent - Validates against industry standards."""

from pathlib import Path
from typing import List
import anthropic

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.competency import NormalizedCompetenciesOutput


class BenchmarkResearchAgent(BaseAgent):
    """Validates and refines competencies against industry benchmarks."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()

    def execute(self, state: RunState) -> RunState:
        """
        Benchmark competencies against industry standards.

        Args:
            state: Current workflow state

        Returns:
            Updated state with benchmarked competencies
        """
        state.current_step = self.agent_id

        # TODO: Load clean competencies and benchmark
        # This is a placeholder implementation

        # Save artifact
        output_path = Path(f"data/output/{state.run_id}_s6_benchmarked_v4.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        state.artifacts.benchmarked_v4 = output_path

        return state

    def get_system_prompt(self) -> str:
        """Return system prompt for benchmarking."""
        return """You are a Competency Benchmarking Specialist with access to industry frameworks.

Your task is to validate and refine competencies against established standards.

Benchmark sources (priority order):
1. O*NET (Occupational Information Network)
2. SFIA (Skills Framework for the Information Age)
3. NICE (National Initiative for Cybersecurity Education)
4. Industry-specific frameworks

Benchmarking process:
1. Search relevant frameworks for each competency
2. Compare definitions, indicators, and proficiency levels
3. Identify gaps or misalignments
4. Refine competency content to align with standards
5. Document evidence and changes made
6. Assign alignment score

Quality standards:
- All competencies benchmarked against ≥1 source
- Clear documentation of changes
- Evidence references included
- Alignment scores >= 0.7

Output structured JSON conforming to NormalizedCompetenciesOutput schema (v4)."""
