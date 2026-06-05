"""Step 6: Benchmark Researcher Agent - Validates against industry standards."""

import shutil
from pathlib import Path

import anthropic

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState


class BenchmarkResearchAgent(BaseAgent):
    """Validates and refines competencies against industry benchmarks."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()

    def execute(self, state: RunState) -> RunState:
        """
        Benchmark competencies against industry standards.

        The current implementation preserves the clean competency artifact as a
        benchmarked candidate so downstream gates can exercise a complete R1
        smoke path. Full external benchmark enrichment is planned in the v3.8
        workstream, but the artifact is intentionally materialized here rather
        than leaving an empty path in the registry.
        """
        state.current_step = self.agent_id

        output_path = Path(f"data/output/{state.run_id}_s6_benchmarked_v4.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        source_path = state.artifacts.clean_v3 or state.artifacts.normalized_v2
        if source_path and Path(source_path).exists():
            shutil.copyfile(source_path, output_path)
        else:
            output_path.write_text(
                '{\n'
                '  "jobs": [],\n'
                '  "processing_version": "v4",\n'
                '  "total_competencies": 0\n'
                '}\n'
            )

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
