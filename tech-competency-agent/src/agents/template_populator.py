"""Step 8: Template Populator Agent - Populates output template."""

from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import anthropic
import json

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.ranking import RankingOutput, JobRanking, RankedCompetency
from src.schemas.competency import NormalizedCompetenciesOutput


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

        # Load ranked competencies from Step 7
        ranking_output = self._load_ranking_output(state)

        # Load benchmarked competencies for full details
        benchmarked_comps = self._load_benchmarked_competencies(state)

        # Create populated output data
        populated_data = self._create_populated_data(
            ranking_output, benchmarked_comps, state
        )

        # Save as JSON (Excel generation would require openpyxl)
        output_path = Path(f"data/output/{state.run_id}_s8_populated_template.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(populated_data, f, indent=2, default=str)

        state.artifacts.populated_template = output_path

        # Create final review package
        review_package = self._create_review_package(
            state, ranking_output, populated_data
        )

        review_path = Path(f"data/output/{state.run_id}_s9_final_review_package.json")
        review_path.parent.mkdir(parents=True, exist_ok=True)
        with open(review_path, 'w') as f:
            json.dump(review_package, f, indent=2, default=str)

        state.artifacts.final_review_package = review_path

        # Add completion flag
        self.add_flag(
            state,
            severity="INFO",
            flag_type="WORKFLOW_COMPLETE",
            message=f"Successfully processed {len(ranking_output.jobs)} jobs with {sum(len(jr.ranked_competencies) for jr in ranking_output.jobs)} total ranked competencies",
            metadata={"total_jobs": len(ranking_output.jobs)}
        )

        return state

    def _load_ranking_output(self, state: RunState) -> RankingOutput:
        """Load ranking output from Step 7."""
        if not state.artifacts.ranked_top8_v5:
            raise ValueError("Ranking output not available - Step 7 must run first")

        with open(state.artifacts.ranked_top8_v5, 'r') as f:
            return RankingOutput.parse_raw(f.read())

    def _load_benchmarked_competencies(self, state: RunState) -> NormalizedCompetenciesOutput:
        """Load benchmarked competencies for full details."""
        if not state.artifacts.benchmarked_v4:
            raise ValueError("Benchmarked competencies not available - Step 6 must run first")

        with open(state.artifacts.benchmarked_v4, 'r') as f:
            return NormalizedCompetenciesOutput.parse_raw(f.read())

    def _create_populated_data(
        self,
        ranking_output: RankingOutput,
        benchmarked_comps: NormalizedCompetenciesOutput,
        state: RunState
    ) -> Dict[str, Any]:
        """Create populated template data."""

        # Create a lookup for full competency details
        comp_lookup = {}
        for job_comps in benchmarked_comps.jobs:
            for comp in job_comps.technical_competencies:
                comp_lookup[comp.competency_id] = comp

        # Build populated data structure
        jobs_data = []

        for job_ranking in ranking_output.jobs:
            job_data = {
                "job_id": job_ranking.job_id,
                "top_n": job_ranking.top_n,
                "coverage_rate": job_ranking.coverage_summary.coverage_rate,
                "competencies": []
            }

            for ranked_comp in job_ranking.ranked_competencies:
                # Get full competency details
                full_comp = comp_lookup.get(ranked_comp.competency_id)

                comp_data = {
                    "rank": ranked_comp.rank,
                    "competency_id": ranked_comp.competency_id,
                    "name": full_comp.name if full_comp else "Unknown",
                    "definition": full_comp.definition if full_comp else "",
                    "why_it_matters": full_comp.why_it_matters if full_comp else "",
                    "behavioral_indicators": full_comp.behavioral_indicators if full_comp else [],
                    "criticality_score": ranked_comp.criticality_score,
                    "criticality_factors": {
                        "coverage": ranked_comp.criticality_factors.coverage,
                        "impact_risk": ranked_comp.criticality_factors.impact_risk,
                        "frequency": ranked_comp.criticality_factors.frequency,
                        "complexity": ranked_comp.criticality_factors.complexity,
                        "differentiation": ranked_comp.criticality_factors.differentiation,
                        "time_to_proficiency": ranked_comp.criticality_factors.time_to_proficiency
                    },
                    "selection_rationale": ranked_comp.selection_rationale_paragraph,
                    "tools_methods": full_comp.applied_scope.tools_methods_tech if full_comp else [],
                    "standards_frameworks": full_comp.applied_scope.standards_frameworks if full_comp else [],
                    "benchmarked_against": full_comp.benchmarking.benchmarked_against if full_comp else [],
                    "benchmark_alignment_score": full_comp.benchmarking.benchmark_alignment_score if full_comp else None,
                    "responsibilities_covered": ranked_comp.responsibility_ids_covered
                }

                job_data["competencies"].append(comp_data)

            jobs_data.append(job_data)

        return {
            "workflow_id": state.run_id,
            "generation_timestamp": datetime.utcnow().isoformat(),
            "processing_version": "v5_final",
            "total_jobs": len(jobs_data),
            "average_coverage_rate": ranking_output.average_coverage_rate,
            "jobs": jobs_data
        }

    def _create_review_package(
        self,
        state: RunState,
        ranking_output: RankingOutput,
        populated_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create final review package with workflow summary."""

        # Summarize flags by severity
        flags_by_severity = {}
        for flag in state.flags:
            flags_by_severity[flag.severity] = flags_by_severity.get(flag.severity, 0) + 1

        # Create review package
        return {
            "workflow_summary": {
                "run_id": state.run_id,
                "run_timestamp": state.run_timestamp_utc.isoformat(),
                "total_jobs_processed": len(ranking_output.jobs),
                "average_coverage_rate": ranking_output.average_coverage_rate,
                "low_coverage_jobs": ranking_output.low_coverage_jobs,
                "workflow_status": "COMPLETE"
            },
            "quality_summary": {
                "flags_by_severity": flags_by_severity,
                "total_flags": len(state.flags),
                "blocking_issues": [f for f in state.flags if f.severity in ["ERROR", "CRITICAL"]],
                "warnings": [f for f in state.flags if f.severity == "WARNING"]
            },
            "artifacts": {
                "jobs_extracted": str(state.artifacts.jobs_extracted) if state.artifacts.jobs_extracted else None,
                "competency_map_v1": str(state.artifacts.competency_map_v1) if state.artifacts.competency_map_v1 else None,
                "normalized_v2": str(state.artifacts.normalized_v2) if state.artifacts.normalized_v2 else None,
                "overlap_audit_v1": str(state.artifacts.overlap_audit_v1) if state.artifacts.overlap_audit_v1 else None,
                "clean_v3": str(state.artifacts.clean_v3) if state.artifacts.clean_v3 else None,
                "benchmarked_v4": str(state.artifacts.benchmarked_v4) if state.artifacts.benchmarked_v4 else None,
                "ranked_top8_v5": str(state.artifacts.ranked_top8_v5) if state.artifacts.ranked_top8_v5 else None,
                "populated_template": str(state.artifacts.populated_template) if state.artifacts.populated_template else None
            },
            "populated_data": populated_data,
            "next_steps": [
                "Review populated template for accuracy",
                "Validate competency definitions with subject matter experts",
                "Apply to target population for assessment",
                "Monitor for effectiveness and refine as needed"
            ]
        }

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
