"""Step 7: Criticality Ranker Agent - Ranks competencies by criticality."""

from pathlib import Path
from typing import List
import anthropic

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.ranking import RankingOutput


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

        # TODO: Load benchmarked competencies and rank
        # This is a placeholder implementation

        # Save artifact
        output_path = Path(f"data/output/{state.run_id}_s7_ranked_top8_v5.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)

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
4. Select top N (typically 8)
5. Verify responsibility coverage ≥ threshold (80%)
6. Write selection rationale for each

Quality standards:
- Coverage rate ≥ 80% of responsibilities
- Clear, evidence-based rationale for each selection
- Explicit scoring for all factors
- Top N count within configured range (6-10)

Output structured JSON conforming to RankingOutput schema."""
