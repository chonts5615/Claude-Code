from src.schemas.ranking import CoverageSummary, CriticalityFactors, JobRanking, RankedCompetency
from src.utils.program_builder import TechnicalCompetencyProgramBuilder, render_program_markdown


def _ranked_competency(competency_id: str, rank: int, score: float) -> RankedCompetency:
    return RankedCompetency(
        competency_id=competency_id,
        rank=rank,
        criticality_score=score,
        criticality_factors=CriticalityFactors(
            coverage=score,
            impact_risk=score,
            frequency=score,
            complexity=score,
            differentiation=score,
            time_to_proficiency=score,
        ),
        selection_rationale_paragraph="test rationale",
        responsibility_ids_covered=["r1"],
    )


def test_build_program_allocates_timeline_and_modules():
    ranking = JobRanking(
        job_id="job-1",
        ranked_competencies=[
            _ranked_competency("comp-a", 1, 0.9),
            _ranked_competency("comp-b", 2, 0.8),
            _ranked_competency("comp-c", 3, 0.6),
        ],
        top_n=3,
        coverage_summary=CoverageSummary(
            responsibilities_total=10,
            responsibilities_covered=9,
            coverage_rate=0.9,
        ),
    )

    builder = TechnicalCompetencyProgramBuilder(total_weeks=12, max_competencies=3)
    program = builder.build_for_job(ranking)

    assert len(program.modules) == 3
    assert program.modules[0].start_week == 1
    assert program.modules[-1].end_week == 12
    assert sum(module.end_week - module.start_week + 1 for module in program.modules) == 12


def test_render_markdown_includes_job_and_schedule():
    ranking = JobRanking(
        job_id="job-2",
        ranked_competencies=[_ranked_competency("comp-x", 1, 0.85)],
        top_n=1,
        coverage_summary=CoverageSummary(
            responsibilities_total=5,
            responsibilities_covered=5,
            coverage_rate=1.0,
        ),
    )

    program = TechnicalCompetencyProgramBuilder(total_weeks=6).build_for_job(ranking)
    markdown = render_program_markdown(program)

    assert "Technical Competency Builder Program: job-2" in markdown
    assert "| 1 | comp-x |" in markdown
    assert "## Expected Outcomes" in markdown
