"""Tests for TemplatePopulatorAgent."""

from src.agents.template_populator import TemplatePopulatorAgent

RANKING_FIXTURE = {
    "jobs": [
        {
            "job_id": "JOB_001",
            "ranked_competencies": [
                {
                    "competency_id": "COMP_001",
                    "rank": 1,
                    "criticality_score": 0.91,
                    "criticality_factors": {
                        "coverage": 0.9,
                        "impact_risk": 0.9,
                        "frequency": 0.9,
                        "complexity": 0.9,
                        "differentiation": 0.9,
                        "time_to_proficiency": 0.9,
                        "weights": {
                            "coverage": 0.25,
                            "impact_risk": 0.2,
                            "frequency": 0.15,
                            "complexity": 0.15,
                            "differentiation": 0.15,
                            "time_to_proficiency": 0.1,
                        },
                    },
                    "selection_rationale_paragraph": "Critical for role outcomes.",
                    "responsibility_ids_covered": ["R1", "R2"],
                }
            ],
            "top_n": 1,
            "coverage_summary": {
                "responsibilities_total": 2,
                "responsibilities_covered": 2,
                "coverage_rate": 1.0,
                "uncovered_responsibility_ids": [],
            },
            "ranking_methodology": "weighted_criticality_factors",
            "ranking_timestamp": "2026-01-01T00:00:00Z",
        }
    ],
    "total_jobs_ranked": 1,
    "average_coverage_rate": 1.0,
    "low_coverage_jobs": [],
}


def test_template_populator_writes_workbook(sample_run_state, tmp_path):
    ranking_path = tmp_path / "ranking.json"
    ranking_path.write_text(__import__("json").dumps(RANKING_FIXTURE), encoding="utf-8")
    sample_run_state.artifacts.ranked_top8_v5 = ranking_path

    agent = TemplatePopulatorAgent(agent_id="S8", step_name="Template Populator")
    updated = agent.execute(sample_run_state)

    assert updated.artifacts.populated_template is not None
    assert updated.artifacts.populated_template.exists()
