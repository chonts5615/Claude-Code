"""Step 8: Template Populator Agent - Populates output template."""

from pathlib import Path

import anthropic

from src.agents.base import BaseAgent
from src.schemas.ranking import RankingOutput
from src.schemas.run_state import RunState


class TemplatePopulatorAgent(BaseAgent):
    """Populates the output template with ranked competencies."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()

    def execute(self, state: RunState) -> RunState:
        """
        Populate output template.

        Writes a minimal workbook with run, job, competency, rank, score, and
        covered-responsibility metadata so end-to-end smoke runs generate a real
        artifact instead of a dangling workbook path.
        """
        state.current_step = self.agent_id

        output_path = Path(f"data/output/{state.run_id}_s8_populated_template.xlsx")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            from openpyxl import Workbook
        except ImportError as exc:  # pragma: no cover - dependency is installed in project env
            raise RuntimeError("openpyxl is required to populate template workbooks") from exc

        wb = Workbook()
        ws = wb.active
        ws.title = "Ranked Competencies"
        ws.append([
            "run_id", "family", "job_id", "rank", "competency_id",
            "criticality_score", "responsibilities_covered",
        ])

        if state.artifacts.ranked_top8_v5 and Path(state.artifacts.ranked_top8_v5).exists():
            ranking = RankingOutput.model_validate_json(Path(state.artifacts.ranked_top8_v5).read_text())
            for job in ranking.jobs:
                for competency in job.ranked_competencies:
                    ws.append([
                        state.run_id,
                        state.config.family,
                        job.job_id,
                        competency.rank,
                        competency.competency_id,
                        competency.criticality_score,
                        ",".join(competency.responsibility_ids_covered),
                    ])

        wb.save(output_path)
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

Output: Populated Excel template file."""
