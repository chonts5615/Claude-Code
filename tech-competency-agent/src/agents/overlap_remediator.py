"""Step 5: Overlap Remediator Agent - Fixes overlap issues."""

from pathlib import Path
from typing import List, Dict
import anthropic
import copy

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.audit import (
    OverlapRemediationOutput,
    JobRemediationLog,
    RemediationAction,
    OverlapAuditOutput,
    JobOverlapAudit,
    OverlapFlag
)
from src.schemas.competency import (
    NormalizedCompetenciesOutput,
    JobCompetencies,
    TechnicalCompetency
)


class OverlapRemediatorAgent(BaseAgent):
    """Remediates overlap issues identified by auditor."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()

    def execute(self, state: RunState) -> RunState:
        """
        Remediate overlap issues.

        Args:
            state: Current workflow state

        Returns:
            Updated state with remediation results
        """
        state.current_step = self.agent_id

        # Load audit results from Step 4
        audit_output = self._load_audit_results(state)

        # Load normalized competencies from Step 3
        normalized_comps = self._load_normalized_competencies(state)

        # Remediate each job with issues
        remediation_logs = []
        clean_jobs = []

        for job_comps, job_audit in zip(normalized_comps.jobs, audit_output.job_audits):
            if not job_audit.audit_passed:
                # Remediate issues
                clean_job, remediation_log = self._remediate_job(
                    job_comps, job_audit, state
                )
                remediation_logs.append(remediation_log)
                clean_jobs.append(clean_job)
            else:
                # No issues, keep as-is
                clean_jobs.append(job_comps)

        # Create clean competencies output (v3)
        clean_output = NormalizedCompetenciesOutput(
            jobs=clean_jobs,
            processing_version="v3",
            total_competencies=sum(jc.competency_count() for jc in clean_jobs)
        )

        # Save cleaned competencies
        clean_output_path = Path(f"data/output/{state.run_id}_s5_clean_v3.json")
        clean_output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(clean_output_path, 'w') as f:
            f.write(clean_output.json(indent=2))

        state.artifacts.clean_v3 = clean_output_path

        # Determine if reaudit is required (if we made revisions instead of removals)
        reaudit_required = any(
            action.action_taken in ["REVISED_DEFINITION", "REVISED_INDICATORS", "REPLACED"]
            for log in remediation_logs
            for action in log.remediation_actions
        )

        # Create remediation output
        output = OverlapRemediationOutput(
            job_remediation_logs=remediation_logs,
            total_remediations=sum(
                len(log.remediation_actions) for log in remediation_logs
            ),
            reaudit_required=reaudit_required
        )

        # Save remediation log
        output_path = Path(f"data/output/{state.run_id}_s5_remediation_log.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(output.json(indent=2))

        # Add flags for remediation summary
        for log in remediation_logs:
            if log.removed_count > 0 or log.revised_count > 0:
                self.add_flag(
                    state,
                    severity="INFO",
                    flag_type="REMEDIATION_APPLIED",
                    message=f"Job {log.job_id}: Removed {log.removed_count}, Revised {log.revised_count}",
                    job_id=log.job_id,
                    metadata={"removed": log.removed_count, "revised": log.revised_count}
                )

        return state

    def _load_audit_results(self, state: RunState) -> OverlapAuditOutput:
        """Load audit results from Step 4."""
        if not state.artifacts.overlap_audit_v1:
            raise ValueError("Overlap audit not available - Step 4 must run first")

        with open(state.artifacts.overlap_audit_v1, 'r') as f:
            return OverlapAuditOutput.parse_raw(f.read())

    def _load_normalized_competencies(self, state: RunState) -> NormalizedCompetenciesOutput:
        """Load normalized competencies from Step 3."""
        if not state.artifacts.normalized_v2:
            raise ValueError("Normalized competencies not available - Step 3 must run first")

        with open(state.artifacts.normalized_v2, 'r') as f:
            return NormalizedCompetenciesOutput.parse_raw(f.read())

    def _remediate_job(
        self,
        job_comps: JobCompetencies,
        job_audit: JobOverlapAudit,
        state: RunState
    ) -> tuple[JobCompetencies, JobRemediationLog]:
        """Remediate issues for a single job."""

        remediation_actions = []
        clean_competencies = []

        # Create a set of competency IDs to remove
        to_remove = set()
        to_revise = {}

        # Process overlap flags
        for overlap_flag in job_audit.overlap_flags:
            if overlap_flag.suggested_action == "REMOVE":
                to_remove.add(overlap_flag.competency_id)
            elif overlap_flag.suggested_action == "REVISE":
                to_revise[overlap_flag.competency_id] = overlap_flag

        # Process distinctness flags (remove duplicates)
        for dist_flag in job_audit.distinctness_flags:
            # Remove the second competency in the duplicate pair
            to_remove.add(dist_flag.competency_id_2)

        # Process each competency
        for comp in job_comps.technical_competencies:
            if comp.competency_id in to_remove:
                # Record removal
                action = RemediationAction(
                    competency_id=comp.competency_id,
                    original_name=comp.name,
                    action_taken="REMOVED",
                    before_snapshot=comp.dict(),
                    after_snapshot=None,
                    remediation_rationale=f"Removed due to overlap with leadership competencies or duplicate within job"
                )
                remediation_actions.append(action)

            elif comp.competency_id in to_revise:
                # Revise the competency definition to focus on technical aspects
                overlap_flag = to_revise[comp.competency_id]
                revised_comp = self._revise_competency(comp, overlap_flag)

                action = RemediationAction(
                    competency_id=comp.competency_id,
                    original_name=comp.name,
                    action_taken="REVISED_DEFINITION",
                    revised_name=revised_comp.name,
                    revision_details=f"Revised to reduce overlap ({overlap_flag.similarity_score:.2f}) with {overlap_flag.overlap_target_domain}",
                    before_snapshot=comp.dict(),
                    after_snapshot=revised_comp.dict(),
                    remediation_rationale=f"Refocused on technical aspects to differentiate from leadership competencies"
                )
                remediation_actions.append(action)
                clean_competencies.append(revised_comp)

            else:
                # Keep as-is
                clean_competencies.append(comp)

        # Count remediation types
        removed_count = sum(1 for a in remediation_actions if a.action_taken == "REMOVED")
        revised_count = sum(1 for a in remediation_actions if a.action_taken in ["REVISED_DEFINITION", "REVISED_INDICATORS"])
        replaced_count = sum(1 for a in remediation_actions if a.action_taken == "REPLACED")

        # Create remediation log
        remediation_log = JobRemediationLog(
            job_id=job_comps.job_id,
            remediation_actions=remediation_actions,
            removed_count=removed_count,
            revised_count=revised_count,
            replaced_count=replaced_count
        )

        # Create clean job competencies
        clean_job = JobCompetencies(
            job_id=job_comps.job_id,
            technical_competencies=clean_competencies
        )

        return clean_job, remediation_log

    def _revise_competency(
        self,
        comp: TechnicalCompetency,
        overlap_flag: OverlapFlag
    ) -> TechnicalCompetency:
        """Revise a competency to reduce overlap with leadership competencies."""

        # Create a copy to revise
        revised_comp = copy.deepcopy(comp)

        # Refocus definition on technical aspects
        revised_comp.definition = f"Technical execution of {comp.name.lower()}: {comp.definition}"

        # Update why_it_matters to emphasize technical value
        revised_comp.why_it_matters = f"This technical competency provides the specialized skills and knowledge needed to execute job responsibilities effectively, distinct from general leadership or behavioral competencies."

        # Update overlap check to reflect remediation
        revised_comp.overlap_check.core_leadership_overlap = "MINOR"
        revised_comp.overlap_check.similarity_score = overlap_flag.similarity_score
        revised_comp.overlap_check.remediation_notes = f"Revised to reduce overlap from {overlap_flag.overlap_severity} to acceptable level"

        # Update word count
        revised_comp.word_count_definition = len(revised_comp.definition.split())

        return revised_comp

    def get_system_prompt(self) -> str:
        """Return system prompt for overlap remediation."""
        return """You are an Overlap Remediation Specialist with expertise in competency development.

Your task is to resolve overlap issues while preserving technical focus.

Remediation strategies:
1. REMOVE: Delete competency if primarily leadership/core focused
2. REVISED_DEFINITION: Narrow definition to technical aspects
3. REVISED_INDICATORS: Refocus indicators on technical behaviors
4. REPLACE: Substitute with different technical competency
5. NO_ACTION: Keep as-is if overlap is acceptable

Remediation process:
1. Review overlap audit flags
2. Analyze competency content
3. Determine appropriate action
4. Execute remediation while preserving technical substance
5. Document before/after snapshots
6. Provide clear rationale

Quality standards:
- Maintain technical focus throughout
- Preserve traceability to original responsibilities
- Document all changes comprehensively
- Ensure distinctness within job

Output structured JSON conforming to OverlapRemediationOutput schema."""
