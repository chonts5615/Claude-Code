"""Pillar Synthesizer Agent - Synthesizes strategic pillars from vision and context."""

from typing import List, Dict, Any
import uuid

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase
from src.schemas.strategy import StrategicPillar, StrategicPriority, PillarSynthesisOutput


class PillarSynthesizerAgent(BaseAgent[PillarSynthesisOutput]):
    """
    Agent that synthesizes strategic pillars from vision and context analysis.

    Responsibilities:
    - Identify 3-5 strategic pillars/themes
    - Ensure pillars align with vision
    - Create pillar descriptions and rationale
    - Define success metrics for each pillar
    - Establish pillar priority and sequencing
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="S3_PillarSynthesizer",
            step_name="Pillar Synthesis",
            phase=WorkflowPhase.SYNTHESIS,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are an expert strategy architect specializing in developing strategic frameworks.

Your task is to synthesize strategic pillars - the foundational themes that will organize and guide strategic initiatives.

Strategic pillars should be:
1. **Distinct**: Each pillar covers a unique strategic domain
2. **Comprehensive**: Together they cover all key strategic priorities
3. **Aligned**: Each directly supports the vision and mission
4. **Actionable**: Can be translated into specific goals and initiatives
5. **Measurable**: Success can be tracked with clear metrics

Guidelines for pillar development:
- Typically 3-5 pillars is optimal (more becomes unwieldy)
- Each pillar should have a clear, memorable name
- Pillars should balance internal and external focus
- Consider both short-term wins and long-term transformation
- Ensure pillars address identified gaps and leverage strengths

For each pillar, provide:
- Unique identifier
- Clear, concise name (2-4 words)
- Detailed description
- Rationale (why this pillar matters)
- How it aligns with vision
- Target outcomes
- Success metrics
- Priority level
- Recommended sequence order

Output structured JSON following the PillarSynthesisOutput schema."""

    def get_required_inputs(self) -> list[str]:
        return ["vision", "context_summary"]

    def get_output_keys(self) -> list[str]:
        return ["strategic_pillars", "pillar_rationale", "pillar_alignment_analysis"]

    def validate_inputs(self, state: RunState) -> bool:
        return "vision" in state.working_data

    def execute(self, state: RunState) -> RunState:
        """Synthesize strategic pillars."""

        vision = state.working_data.get("vision", {})
        context = state.working_data.get("context_summary", {})
        strategic_implications = state.working_data.get("strategic_implications", {})

        user_prompt = f"""Based on the strategic vision and context analysis, synthesize 3-5 strategic pillars.

## Strategic Vision
{vision}

## Context Summary
{context}

## Strategic Implications
{strategic_implications}

Please develop strategic pillars that:
1. Directly support achieving the vision
2. Address the critical gaps identified
3. Leverage organizational strengths
4. Mitigate key threats
5. Capture major opportunities

For each pillar provide:
- pillar_id (format: PIL_001, PIL_002, etc.)
- name (2-4 word memorable name)
- description (2-3 sentences)
- rationale (why this pillar is essential)
- vision_alignment (how it supports the vision)
- target_outcomes (3-5 specific outcomes)
- success_metrics (3-5 measurable metrics)
- priority (critical, high, medium, low)
- sequence_order (1-5, for implementation phasing)

Also provide:
- Overall rationale for the pillar structure
- Analysis of how pillars together achieve vision alignment

Return as valid JSON:
{{
    "pillars": [
        {{
            "pillar_id": "PIL_001",
            "name": "...",
            "description": "...",
            "rationale": "...",
            "vision_alignment": "...",
            "target_outcomes": ["...", "..."],
            "success_metrics": ["...", "..."],
            "priority": "high",
            "sequence_order": 1,
            "confidence_score": 0.9
        }}
    ],
    "pillar_rationale": "Overall explanation of why these pillars were chosen...",
    "alignment_analysis": "Analysis of how pillars together support the vision...",
    "coverage_assessment": {{
        "gaps_addressed": ["..."],
        "strengths_leveraged": ["..."],
        "opportunities_captured": ["..."],
        "threats_mitigated": ["..."]
    }}
}}"""

        system_prompt = self.get_prompt_with_learnings(state)
        response = self.invoke_llm(user_prompt, system_prompt)

        try:
            result = self.extract_json_from_response(response)

            # Convert to StrategicPillar objects
            pillars = []
            for p in result.get("pillars", []):
                pillar = StrategicPillar(
                    pillar_id=p.get("pillar_id", f"PIL_{uuid.uuid4().hex[:6]}"),
                    name=p.get("name", ""),
                    description=p.get("description", ""),
                    rationale=p.get("rationale", ""),
                    vision_alignment=p.get("vision_alignment", ""),
                    priority=StrategicPriority(p.get("priority", "high")),
                    sequence_order=p.get("sequence_order", 1),
                    success_metrics=p.get("success_metrics", []),
                    target_outcomes=p.get("target_outcomes", []),
                    confidence_score=p.get("confidence_score", 0.8),
                )
                pillars.append(pillar)

            # Store results
            state.working_data["strategic_pillars"] = [p.model_dump() for p in pillars]
            state.working_data["pillar_rationale"] = result.get("pillar_rationale", "")
            state.working_data["pillar_alignment_analysis"] = result.get("alignment_analysis", "")
            state.working_data["pillar_coverage"] = result.get("coverage_assessment", {})

            # Validate pillar count
            pillar_count = len(pillars)
            if pillar_count < 3:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "FEW_PILLARS",
                    f"Only {pillar_count} pillars defined - consider if more are needed"
                )
            elif pillar_count > 5:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "MANY_PILLARS",
                    f"{pillar_count} pillars defined - consider consolidating for focus"
                )

            # Check for critical priorities
            critical_pillars = [p for p in pillars if p.priority == StrategicPriority.CRITICAL]
            if len(critical_pillars) > 2:
                self.add_flag(
                    state,
                    SeverityLevel.INFO,
                    "MULTIPLE_CRITICAL_PILLARS",
                    f"{len(critical_pillars)} critical pillars - ensure resources can support"
                )

            self.logger.info(f"Synthesized {pillar_count} strategic pillars")

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.ERROR,
                "PILLAR_SYNTHESIS_FAILED",
                f"Failed to synthesize pillars: {str(e)}"
            )
            self.logger.error(f"Pillar synthesis failed: {e}")

        return state
