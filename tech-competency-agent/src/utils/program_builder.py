from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Dict, Iterable, List, Optional

from src.schemas.ranking import JobRanking, RankedCompetency


@dataclass
class ProgramModule:
    """A scheduled learning module for one competency."""

    competency_id: str
    competency_name: str
    rank: int
    criticality_score: float
    intensity: str
    start_week: int
    end_week: int
    outcomes: List[str]


@dataclass
class CompetencyBuilderProgram:
    """Structured development plan built from ranked competencies."""

    job_id: str
    total_weeks: int
    modules: List[ProgramModule]


class TechnicalCompetencyProgramBuilder:
    """Builds a competency development program from ranked competencies."""

    def __init__(
        self,
        total_weeks: int = 12,
        max_competencies: int = 8,
        competency_names: Optional[Dict[str, str]] = None,
    ) -> None:
        if total_weeks < 4:
            raise ValueError("total_weeks must be at least 4")
        if max_competencies < 1:
            raise ValueError("max_competencies must be at least 1")

        self.total_weeks = total_weeks
        self.max_competencies = max_competencies
        self.competency_names = competency_names or {}

    def build_for_job(self, ranking: JobRanking) -> CompetencyBuilderProgram:
        top_competencies = ranking.ranked_competencies[: self.max_competencies]
        if not top_competencies:
            return CompetencyBuilderProgram(job_id=ranking.job_id, total_weeks=self.total_weeks, modules=[])

        week_allocations = self._allocate_weeks(top_competencies)
        modules: List[ProgramModule] = []

        cursor = 1
        for competency, weeks in zip(top_competencies, week_allocations):
            start_week = cursor
            end_week = min(self.total_weeks, cursor + weeks - 1)
            cursor = end_week + 1
            modules.append(
                ProgramModule(
                    competency_id=competency.competency_id,
                    competency_name=self.competency_names.get(
                        competency.competency_id, competency.competency_id
                    ),
                    rank=competency.rank,
                    criticality_score=competency.criticality_score,
                    intensity=self._intensity(competency),
                    start_week=start_week,
                    end_week=end_week,
                    outcomes=self._default_outcomes(competency),
                )
            )

        return CompetencyBuilderProgram(
            job_id=ranking.job_id,
            total_weeks=self.total_weeks,
            modules=modules,
        )

    def _allocate_weeks(self, competencies: Iterable[RankedCompetency]) -> List[int]:
        competency_list = list(competencies)
        scores = [c.criticality_score for c in competency_list]
        total_score = sum(scores)

        if total_score <= 0:
            equal_slice = max(1, self.total_weeks // len(competency_list))
            weeks = [equal_slice for _ in competency_list]
        else:
            weeks = [max(1, ceil((score / total_score) * self.total_weeks)) for score in scores]

        while sum(weeks) > self.total_weeks:
            idx = max(range(len(weeks)), key=lambda i: weeks[i])
            if weeks[idx] > 1:
                weeks[idx] -= 1
            else:
                break

        while sum(weeks) < self.total_weeks:
            idx = min(range(len(weeks)), key=lambda i: weeks[i])
            weeks[idx] += 1

        return weeks

    @staticmethod
    def _intensity(competency: RankedCompetency) -> str:
        if competency.criticality_score >= 0.85:
            return "High"
        if competency.criticality_score >= 0.70:
            return "Medium"
        return "Foundational"

    @staticmethod
    def _default_outcomes(competency: RankedCompetency) -> List[str]:
        return [
            f"Demonstrate applied proficiency in {competency.competency_id}.",
            "Complete one practical artifact tied to job responsibilities.",
            "Pass checkpoint review with manager or SME.",
        ]


def render_program_markdown(program: CompetencyBuilderProgram) -> str:
    """Render a competency builder program into a markdown report."""
    lines = [
        f"# Technical Competency Builder Program: {program.job_id}",
        "",
        f"**Total Duration:** {program.total_weeks} weeks",
        "",
        "## Module Schedule",
        "",
        "| Module | Competency | Intensity | Timeline |",
        "|---|---|---|---|",
    ]

    for module in program.modules:
        lines.append(
            f"| {module.rank} | {module.competency_name} | {module.intensity} | "
            f"Week {module.start_week}-{module.end_week} |"
        )

    lines.append("")
    lines.append("## Expected Outcomes")
    lines.append("")

    for module in program.modules:
        lines.append(
            f"### Module {module.rank}: {module.competency_name} "
            f"(Week {module.start_week}-{module.end_week})"
        )
        for outcome in module.outcomes:
            lines.append(f"- {outcome}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
