"""Step 8: Template Populator Agent - Populates output template."""

from pathlib import Path
from zipfile import is_zipfile

import anthropic
from openpyxl import Workbook, load_workbook

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

        Args:
            state: Current workflow state

        Returns:
            Updated state with populated template
        """
        state.current_step = self.agent_id

        if not state.artifacts.ranked_top8_v5:
            self.add_flag(
                state,
                flag_type="MISSING_RANKING_ARTIFACT",
                message="Cannot populate template: ranked competencies artifact is missing.",
                severity="ERROR",
            )
            return state

        with open(state.artifacts.ranked_top8_v5, "r") as f:
            ranking_output = RankingOutput.parse_raw(f.read())

        template_path = state.inputs.output_template_file
        if template_path.exists() and is_zipfile(template_path):
            workbook = load_workbook(template_path)
        else:
            workbook = Workbook()

        if "RankedCompetencies" in workbook.sheetnames:
            sheet = workbook["RankedCompetencies"]
            if sheet.max_row > 1:
                sheet.delete_rows(2, sheet.max_row - 1)
        else:
            sheet = workbook.create_sheet("RankedCompetencies")
            headers = [
                "job_id",
                "rank",
                "competency_id",
                "criticality_score",
                "coverage_rate",
                "responsibility_ids_covered",
                "selection_rationale",
            ]
            sheet.append(headers)

        for job in ranking_output.jobs:
            for ranked in job.ranked_competencies:
                sheet.append(
                    [
                        job.job_id,
                        ranked.rank,
                        ranked.competency_id,
                        round(ranked.criticality_score, 4),
                        round(job.coverage_summary.coverage_rate, 4),
                        ";".join(ranked.responsibility_ids_covered),
                        ranked.selection_rationale_paragraph,
                    ]
                )

        # Save artifact
        output_path = Path(f"data/output/{state.run_id}_s8_populated_template.xlsx")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        workbook.save(output_path)

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
