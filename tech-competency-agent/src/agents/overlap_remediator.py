"""Step 5: Overlap Remediator Agent - Fixes overlap issues."""

from pathlib import Path
from typing import List
import anthropic

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.audit import (
    OverlapRemediationOutput,
    JobRemediationLog,
    RemediationAction
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

        # TODO: Load audit results and remediate issues
        # This is a placeholder implementation
        remediation_logs = []

        # Create output
        output = OverlapRemediationOutput(
            job_remediation_logs=remediation_logs,
            total_remediations=sum(
                len(log.remediation_actions) for log in remediation_logs
            ),
            reaudit_required=False
        )

        # Save artifact
        output_path = Path(f"data/output/{state.run_id}_s5_remediation_log.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(output.json(indent=2))

        # Save cleaned competencies (v3)
        clean_output_path = Path(f"data/output/{state.run_id}_s5_clean_v3.json")
        state.artifacts.clean_v3 = clean_output_path

        return state

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
