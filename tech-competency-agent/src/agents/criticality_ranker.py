"""Step 7: Criticality Ranker Agent - Ranks competencies by criticality."""

from datetime import datetime
from pathlib import Path

import anthropic

from src.agents.base import BaseAgent
from src.schemas.mapping import CompetencyMappingOutput
from src.schemas.ranking import (
    CoverageSummary,
    CriticalityFactors,
    JobRanking,
    RankedCompetency,
    RankingOutput,
)
from src.schemas.run_state import RunState


class CriticalityRankerAgent(BaseAgent):
    """Ranks competencies by criticality using multi-factor scoring."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()

    def execute(self, state: RunState) -> RunState:
        """
        Rank competencies by criticality.

        This deterministic fallback ranks mapped candidates by responsibility
        coverage so a complete R1 smoke run can exercise downstream gates even
        before the full LLM ranking implementation is connected.
        """
        state.current_step = self.agent_id

        job_rankings = []
        if state.artifacts.competency_map_v1 and Path(state.artifacts.competency_map_v1).exists():
            mapping = CompetencyMappingOutput.model_validate_json(
                Path(state.artifacts.competency_map_v1).read_text()
            )
            for job_mapping in mapping.job_mappings:
                coverage_by_comp: dict[str, dict] = {}
                total_responsibilities = len(job_mapping.responsibility_mappings)
                covered = 0
                for responsibility_mapping in job_mapping.responsibility_mappings:
                    candidate = responsibility_mapping.top_candidate()
                    if not candidate:
                        continue
                    covered += 1
                    bucket = coverage_by_comp.setdefault(
                        candidate.competency_id,
                        {
                            "name": candidate.competency_name,
                            "responsibilities": [],
                            "score": candidate.relevance_score,
                        },
                    )
                    bucket["responsibilities"].append(responsibility_mapping.responsibility_id)
                    bucket["score"] = max(bucket["score"], candidate.relevance_score)

                ranked = []
                sorted_items = sorted(
                    coverage_by_comp.items(),
                    key=lambda item: (len(item[1]["responsibilities"]), item[1]["score"]),
                    reverse=True,
                )[: state.config.top_n_competencies]
                for rank, (competency_id, data) in enumerate(sorted_items, start=1):
                    coverage = (
                        len(data["responsibilities"]) / total_responsibilities
                        if total_responsibilities else 0.0
                    )
                    factors = CriticalityFactors(
                        coverage=coverage,
                        impact_risk=0.6,
                        frequency=0.6,
                        complexity=0.6,
                        differentiation=0.5,
                        time_to_proficiency=0.5,
                    )
                    ranked.append(RankedCompetency(
                        competency_id=competency_id,
                        rank=rank,
                        criticality_score=factors.compute_total_score(),
                        criticality_factors=factors,
                        selection_rationale_paragraph=(
                            f"Selected through deterministic smoke ranking from mapped "
                            f"responsibilities for {data['name']}."
                        ),
                        responsibility_ids_covered=data["responsibilities"],
                    ))

                covered_ids = {
                    rid for item in ranked for rid in item.responsibility_ids_covered
                }
                all_ids = [rm.responsibility_id for rm in job_mapping.responsibility_mappings]
                coverage_rate = covered / total_responsibilities if total_responsibilities else 0.0
                job_rankings.append(JobRanking(
                    job_id=job_mapping.job_id,
                    ranked_competencies=ranked,
                    top_n=len(ranked),
                    coverage_summary=CoverageSummary(
                        responsibilities_total=total_responsibilities,
                        responsibilities_covered=covered,
                        coverage_rate=coverage_rate,
                        uncovered_responsibility_ids=[rid for rid in all_ids if rid not in covered_ids],
                    ),
                    ranking_timestamp=datetime.utcnow().isoformat(),
                ))

        average_coverage = (
            sum(j.coverage_summary.coverage_rate for j in job_rankings) / len(job_rankings)
            if job_rankings else 0.0
        )
        output = RankingOutput(
            jobs=job_rankings,
            total_jobs_ranked=len(job_rankings),
            average_coverage_rate=average_coverage,
            low_coverage_jobs=[
                j.job_id for j in job_rankings
                if j.coverage_summary.coverage_rate < state.config.thresholds.min_responsibility_coverage
            ],
        )

        output_path = Path(f"data/output/{state.run_id}_s7_ranked_top8_v5.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output.model_dump_json(indent=2))

        state.artifacts.ranked_top8_v5 = output_path
        return state

    def get_system_prompt(self) -> str:
        """Return system prompt for criticality ranking."""
        return """You are a Criticality Ranking Specialist with expertise in job analysis.

Your task is to rank technical competencies by criticality using a multi-factor model.

Criticality factors (weighted):
1. Coverage (25%): % of responsibilities enabled
2. Impact/Risk (20%): Consequence of failure
3. Frequency (15%): How often used
4. Complexity (15%): Cognitive/technical difficulty
5. Differentiation (15%): Distinguishes high performers
6. Time to Proficiency (10%): Development timeframe

Ranking process:
1. Score each competency on all six factors (0.0-1.0)
2. Compute weighted total criticality score
3. Rank competencies by score
4. Select top N
5. Verify responsibility coverage against threshold
6. Write selection rationale for each

Output structured JSON conforming to RankingOutput schema."""
