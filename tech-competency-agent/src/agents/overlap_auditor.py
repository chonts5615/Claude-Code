"""Step 4: Overlap Auditor Agent - Detects overlap with core/leadership competencies."""

from pathlib import Path
from typing import List
import anthropic

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.audit import (
    OverlapAuditOutput,
    JobOverlapAudit,
    OverlapFlag,
    DistinctnessFlag
)


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

        # TODO: Load competencies and check for overlaps
        # This is a placeholder implementation
        job_audits = []

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

        return state

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
