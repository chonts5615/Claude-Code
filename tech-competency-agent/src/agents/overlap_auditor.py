"""Step 4: Overlap Auditor Agent - Detects overlap with core/leadership competencies."""

from pathlib import Path
from typing import List, Dict
import anthropic

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.audit import (
    OverlapAuditOutput,
    JobOverlapAudit,
    OverlapFlag,
    DistinctnessFlag
)
from src.schemas.competency import (
    NormalizedCompetenciesOutput,
    JobCompetencies,
    TechnicalCompetency,
    CompetencyLibraryEntry
)
from src.utils.similarity import compute_similarity
from src.utils.file_parsers import parse_competency_library


class OverlapAuditorAgent(BaseAgent):
    """Audits competencies for overlap with core/leadership competencies."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()

    def execute(self, state: RunState) -> RunState:
        """
        Audit competencies for overlap.

        Args:
            state: Current workflow state

        Returns:
            Updated state with audit results
        """
        state.current_step = self.agent_id

        # Load normalized competencies from Step 3
        jobs_competencies = self._load_normalized_competencies(state)

        # Load core/leadership competency library
        leadership_library = self._load_leadership_library(state)

        # Audit each job for overlaps
        job_audits = []
        for job_comps in jobs_competencies.jobs:
            audit = self._audit_job(job_comps, leadership_library, state)
            job_audits.append(audit)

        # Create output
        output = OverlapAuditOutput(
            job_audits=job_audits,
            total_material_overlaps=sum(ja.material_overlap_count for ja in job_audits),
            total_distinctness_conflicts=sum(ja.distinctness_conflict_count for ja in job_audits),
            jobs_requiring_remediation=[ja.job_id for ja in job_audits if not ja.audit_passed],
            audit_timestamp=str(state.run_timestamp_utc)
        )

        # Save artifact
        output_path = Path(f"data/output/{state.run_id}_s4_overlap_audit_v1.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(output.json(indent=2))

        state.artifacts.overlap_audit_v1 = output_path

        # Add quality flags for blocking issues
        for audit in job_audits:
            if not audit.audit_passed:
                for issue in audit.blocking_issues:
                    self.add_flag(
                        state,
                        severity="ERROR",
                        flag_type="OVERLAP_DETECTED",
                        message=issue,
                        job_id=audit.job_id,
                        metadata={}
                    )

        return state

    def _load_normalized_competencies(self, state: RunState) -> NormalizedCompetenciesOutput:
        """Load normalized competencies from Step 3."""
        if not state.artifacts.normalized_v2:
            raise ValueError("Normalized competencies not available - Step 3 must run first")

        with open(state.artifacts.normalized_v2, 'r') as f:
            return NormalizedCompetenciesOutput.parse_raw(f.read())

    def _load_leadership_library(self, state: RunState) -> List[CompetencyLibraryEntry]:
        """Load core/leadership competency library."""
        return parse_competency_library(state.inputs.core_leadership_file)

    def _audit_job(
        self,
        job_comps: JobCompetencies,
        leadership_library: List[CompetencyLibraryEntry],
        state: RunState
    ) -> JobOverlapAudit:
        """Audit a single job for overlaps."""

        overlap_flags = []
        distinctness_flags = []

        # Get thresholds from config
        overlap_material_threshold = state.config.thresholds.overlap_material
        overlap_minor_threshold = state.config.thresholds.overlap_minor
        distinctness_duplicate_threshold = state.config.thresholds.distinctness_duplicate

        # Check each technical competency against leadership library
        for tech_comp in job_comps.technical_competencies:
            overlap_flag = self._check_leadership_overlap(
                tech_comp,
                leadership_library,
                overlap_material_threshold,
                overlap_minor_threshold
            )
            if overlap_flag:
                overlap_flags.append(overlap_flag)

        # Check for within-job distinctness conflicts
        for i, comp1 in enumerate(job_comps.technical_competencies):
            for comp2 in job_comps.technical_competencies[i+1:]:
                distinctness_flag = self._check_distinctness(
                    comp1,
                    comp2,
                    distinctness_duplicate_threshold
                )
                if distinctness_flag:
                    distinctness_flags.append(distinctness_flag)

        # Count overlaps
        material_overlap_count = sum(1 for f in overlap_flags if f.overlap_severity == "MATERIAL")
        minor_overlap_count = sum(1 for f in overlap_flags if f.overlap_severity == "MINOR")
        distinctness_conflict_count = len(distinctness_flags)

        # Determine if audit passed (no material overlaps or duplicate conflicts)
        audit_passed = material_overlap_count == 0 and distinctness_conflict_count == 0

        # Create blocking issues list
        blocking_issues = []
        if material_overlap_count > 0:
            blocking_issues.append(f"{material_overlap_count} material overlap(s) with leadership competencies")
        if distinctness_conflict_count > 0:
            blocking_issues.append(f"{distinctness_conflict_count} distinctness conflict(s) within job")

        return JobOverlapAudit(
            job_id=job_comps.job_id,
            overlap_flags=overlap_flags,
            distinctness_flags=distinctness_flags,
            material_overlap_count=material_overlap_count,
            minor_overlap_count=minor_overlap_count,
            distinctness_conflict_count=distinctness_conflict_count,
            audit_passed=audit_passed,
            blocking_issues=blocking_issues
        )

    def _check_leadership_overlap(
        self,
        tech_comp: TechnicalCompetency,
        leadership_library: List[CompetencyLibraryEntry],
        material_threshold: float,
        minor_threshold: float
    ) -> OverlapFlag | None:
        """Check if technical competency overlaps with leadership competencies."""

        max_similarity = 0.0
        most_similar_comp = None

        # Compare against each leadership competency
        for leader_comp in leadership_library:
            similarity = compute_similarity(tech_comp.definition, leader_comp.definition)
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_comp = leader_comp

        # Determine overlap severity
        if max_similarity >= material_threshold:
            severity = "MATERIAL"
            action = "REMOVE"
            rationale = f"Material overlap ({max_similarity:.2f}) with leadership competency '{most_similar_comp.name}'. Technical competency should be removed."
        elif max_similarity >= minor_threshold:
            severity = "MINOR"
            action = "REVISE"
            rationale = f"Minor overlap ({max_similarity:.2f}) with leadership competency '{most_similar_comp.name}'. Consider revising to focus on technical aspects."
        else:
            return None  # No significant overlap

        domain = "leadership" if most_similar_comp else "unknown"

        return OverlapFlag(
            competency_id=tech_comp.competency_id,
            competency_name=tech_comp.name,
            overlap_severity=severity,
            overlap_target_domain=domain,
            similarity_score=max_similarity,
            rationale=rationale,
            suggested_action=action
        )

    def _check_distinctness(
        self,
        comp1: TechnicalCompetency,
        comp2: TechnicalCompetency,
        duplicate_threshold: float
    ) -> DistinctnessFlag | None:
        """Check if two competencies are too similar (lack distinctness)."""

        similarity = compute_similarity(comp1.definition, comp2.definition)

        if similarity >= duplicate_threshold:
            conflict_type = "DUPLICATE" if similarity >= 0.95 else "NEAR_DUPLICATE"
            recommendation = f"Merge or differentiate: '{comp1.name}' and '{comp2.name}' have {similarity:.2f} similarity"

            return DistinctnessFlag(
                competency_id_1=comp1.competency_id,
                competency_id_2=comp2.competency_id,
                similarity_score=similarity,
                conflict_type=conflict_type,
                resolution_recommendation=recommendation
            )

        return None

    def get_system_prompt(self) -> str:
        """Return system prompt for overlap auditing."""
        return """You are an Overlap Detection Specialist with expertise in competency frameworks.

Your task is to identify overlaps between technical and core/leadership competencies.

Overlap detection criteria:
1. Material overlap (≥0.82 similarity): Substantial conceptual overlap
2. Minor overlap (0.72-0.82): Partial overlap, may need revision
3. Distinctness conflicts: Near-duplicates within same job

Analysis process:
1. Compare each technical competency against core/leadership library
2. Compute semantic similarity scores
3. Identify overlap domains (e.g., "leadership", "communication")
4. Suggest remediation actions (KEEP, REVISE, REMOVE, REPLACE)
5. Check within-job distinctness

Quality standards:
- Flag all material overlaps as blocking issues
- Provide clear rationale for each flag
- Suggest specific remediation actions

Output structured JSON conforming to OverlapAuditOutput schema."""
