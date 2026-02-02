"""Step 7: Criticality Ranker Agent - Ranks competencies by criticality."""

from pathlib import Path
from typing import List, Set
from datetime import datetime
import anthropic

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.ranking import (
    RankingOutput,
    JobRanking,
    RankedCompetency,
    CriticalityFactors,
    CoverageSummary
)
from src.schemas.competency import NormalizedCompetenciesOutput, TechnicalCompetency, JobCompetencies


class CriticalityRankerAgent(BaseAgent):
    """Ranks competencies by criticality using multi-factor scoring."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()

    def execute(self, state: RunState) -> RunState:
        """
        Rank competencies by criticality.

        Args:
            state: Current workflow state

        Returns:
            Updated state with ranked competencies
        """
        state.current_step = self.agent_id

        # Load benchmarked competencies from Step 6
        benchmarked_comps = self._load_benchmarked_competencies(state)

        # Get top N from config
        top_n = state.config.top_n_competencies

        # Rank each job's competencies
        job_rankings = []
        for job_comps in benchmarked_comps.jobs:
            job_ranking = self._rank_job_competencies(job_comps, top_n, state)
            job_rankings.append(job_ranking)

        # Calculate overall statistics
        total_jobs = len(job_rankings)
        avg_coverage = sum(jr.coverage_summary.coverage_rate for jr in job_rankings) / total_jobs if total_jobs > 0 else 0
        low_coverage_jobs = [
            jr.job_id for jr in job_rankings
            if jr.coverage_summary.coverage_rate < state.config.thresholds.min_responsibility_coverage
        ]

        # Create ranking output
        output = RankingOutput(
            jobs=job_rankings,
            total_jobs_ranked=total_jobs,
            average_coverage_rate=avg_coverage,
            low_coverage_jobs=low_coverage_jobs
        )

        # Save artifact
        output_path = Path(f"data/output/{state.run_id}_s7_ranked_top{top_n}_v5.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(output.json(indent=2))

        state.artifacts.ranked_top8_v5 = output_path

        # Add quality flags for low coverage
        for job_id in low_coverage_jobs:
            job_ranking = next(jr for jr in job_rankings if jr.job_id == job_id)
            self.add_flag(
                state,
                severity="WARNING",
                flag_type="LOW_COVERAGE",
                message=f"Job {job_id} coverage rate ({job_ranking.coverage_summary.coverage_rate:.1%}) below threshold",
                job_id=job_id,
                metadata={"coverage_rate": job_ranking.coverage_summary.coverage_rate}
            )

        return state

    def _load_benchmarked_competencies(self, state: RunState) -> NormalizedCompetenciesOutput:
        """Load benchmarked competencies from Step 6."""
        if not state.artifacts.benchmarked_v4:
            raise ValueError("Benchmarked competencies not available - Step 6 must run first")

        with open(state.artifacts.benchmarked_v4, 'r') as f:
            return NormalizedCompetenciesOutput.parse_raw(f.read())

    def _rank_job_competencies(
        self,
        job_comps: JobCompetencies,
        top_n: int,
        state: RunState
    ) -> JobRanking:
        """Rank and select top N competencies for a job."""

        # Score each competency
        scored_competencies = []
        for comp in job_comps.technical_competencies:
            factors = self._compute_criticality_factors(comp, job_comps)
            score = factors.compute_total_score()
            scored_competencies.append((comp, factors, score))

        # Sort by score (descending)
        scored_competencies.sort(key=lambda x: x[2], reverse=True)

        # Select top N
        top_competencies = scored_competencies[:top_n]

        # Create ranked competency objects
        ranked_comps = []
        for rank, (comp, factors, score) in enumerate(top_competencies, start=1):
            rationale = self._generate_rationale(comp, factors, rank)

            ranked_comp = RankedCompetency(
                competency_id=comp.competency_id,
                rank=rank,
                criticality_score=score,
                criticality_factors=factors,
                selection_rationale_paragraph=rationale,
                responsibility_ids_covered=[rt.responsibility_id for rt in comp.responsibility_trace]
            )
            ranked_comps.append(ranked_comp)

        # Calculate coverage summary
        coverage_summary = self._calculate_coverage(ranked_comps, job_comps)

        return JobRanking(
            job_id=job_comps.job_id,
            ranked_competencies=ranked_comps,
            top_n=top_n,
            coverage_summary=coverage_summary,
            ranking_timestamp=datetime.utcnow().isoformat()
        )

    def _compute_criticality_factors(
        self,
        comp: TechnicalCompetency,
        job_comps: JobCompetencies
    ) -> CriticalityFactors:
        """Compute criticality factors for a competency."""

        # Coverage: % of job's responsibilities covered by this competency
        total_responsibilities = sum(
            len(c.responsibility_trace)
            for c in job_comps.technical_competencies
        )
        comp_responsibilities = len(comp.responsibility_trace)
        coverage = comp_responsibilities / total_responsibilities if total_responsibilities > 0 else 0.5

        # Impact/Risk: Based on PRIMARY vs SECONDARY contributions
        primary_count = sum(1 for rt in comp.responsibility_trace if rt.contribution == "PRIMARY")
        impact_risk = 0.8 if primary_count > 0 else 0.5

        # Frequency: Estimate based on number of responsibilities (more = more frequent)
        frequency = min(1.0, comp_responsibilities / 5.0)  # Normalize to 0-1

        # Complexity: Based on definition word count and indicator count
        complexity_score = 0.0
        if comp.word_count_definition and comp.word_count_definition >= 100:
            complexity_score += 0.5
        if comp.indicator_count and comp.indicator_count >= 5:
            complexity_score += 0.5
        complexity = min(1.0, complexity_score)

        # Differentiation: Based on benchmark alignment (well-benchmarked = distinguishes performers)
        if comp.benchmarking.benchmark_alignment_score:
            differentiation = comp.benchmarking.benchmark_alignment_score
        else:
            differentiation = 0.5

        # Time to Proficiency: Based on complexity (higher complexity = longer time)
        time_to_proficiency = complexity

        return CriticalityFactors(
            coverage=min(1.0, coverage),
            impact_risk=impact_risk,
            frequency=frequency,
            complexity=complexity,
            differentiation=differentiation,
            time_to_proficiency=time_to_proficiency
        )

    def _generate_rationale(
        self,
        comp: TechnicalCompetency,
        factors: CriticalityFactors,
        rank: int
    ) -> str:
        """Generate selection rationale for a ranked competency."""

        rationale_parts = [
            f"Ranked #{rank} based on criticality analysis.",
            f"Covers {len(comp.responsibility_trace)} key job responsibilities.",
        ]

        # Highlight top factors
        scores = {
            "coverage": factors.coverage,
            "impact": factors.impact_risk,
            "frequency": factors.frequency,
            "complexity": factors.complexity,
            "differentiation": factors.differentiation,
        }
        top_factor = max(scores.items(), key=lambda x: x[1])

        if top_factor[1] >= 0.7:
            rationale_parts.append(
                f"High {top_factor[0]} score ({top_factor[1]:.2f}) indicates this competency is essential for job success."
            )

        # Mention benchmarking
        if comp.benchmarking.benchmarked_against:
            rationale_parts.append(
                f"Validated against industry standards ({', '.join(comp.benchmarking.benchmarked_against[:2])})."
            )

        return " ".join(rationale_parts)

    def _calculate_coverage(
        self,
        ranked_comps: List[RankedCompetency],
        job_comps: JobCompetencies
    ) -> CoverageSummary:
        """Calculate responsibility coverage for selected competencies."""

        # Get all unique responsibility IDs from the original job
        all_responsibility_ids: Set[str] = set()
        for comp in job_comps.technical_competencies:
            for rt in comp.responsibility_trace:
                all_responsibility_ids.add(rt.responsibility_id)

        # Get covered responsibility IDs from ranked competencies
        covered_ids: Set[str] = set()
        for ranked_comp in ranked_comps:
            covered_ids.update(ranked_comp.responsibility_ids_covered)

        # Calculate coverage
        total = len(all_responsibility_ids)
        covered = len(covered_ids)
        coverage_rate = covered / total if total > 0 else 0.0
        uncovered = list(all_responsibility_ids - covered_ids)

        return CoverageSummary(
            responsibilities_total=total,
            responsibilities_covered=covered,
            coverage_rate=coverage_rate,
            uncovered_responsibility_ids=uncovered
        )

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
4. Select top N (typically 8)
5. Verify responsibility coverage ≥ threshold (80%)
6. Write selection rationale for each

Quality standards:
- Coverage rate ≥ 80% of responsibilities
- Clear, evidence-based rationale for each selection
- Explicit scoring for all factors
- Top N count within configured range (6-10)

Output structured JSON conforming to RankingOutput schema."""
