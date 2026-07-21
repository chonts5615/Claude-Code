"""Context Analyzer Agent - Analyzes strategic context including SWOT and market analysis."""

from typing import Dict, List, Any
from src.agents.base import BaseAgent
from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase


class ContextAnalyzerAgent(BaseAgent):
    """
    Agent that performs comprehensive strategic context analysis.

    Responsibilities:
    - SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
    - Market and competitive analysis
    - Stakeholder analysis
    - Gap analysis between current and desired state
    - Trend identification
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="S2_ContextAnalyzer",
            step_name="Context Analysis",
            phase=WorkflowPhase.ANALYSIS,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are an expert strategic analyst specializing in organizational context analysis.

Your task is to perform comprehensive strategic analysis including:

1. **SWOT Analysis**:
   - Strengths: Internal capabilities and advantages
   - Weaknesses: Internal limitations and disadvantages
   - Opportunities: External factors that could be leveraged
   - Threats: External factors that could cause problems

2. **Market Analysis**:
   - Industry trends and dynamics
   - Competitive landscape
   - Market opportunities and challenges
   - Customer/stakeholder needs

3. **Gap Analysis**:
   - Current state assessment
   - Desired future state
   - Critical gaps to address
   - Capability requirements

4. **Trend Analysis**:
   - Technology trends
   - Market trends
   - Regulatory trends
   - Social/demographic trends

Guidelines:
- Be specific and evidence-based
- Identify the most impactful factors
- Consider interdependencies between factors
- Prioritize findings by strategic importance
- Maintain objectivity in assessment

Output structured JSON with clear categorization and prioritization."""

    def get_required_inputs(self) -> list[str]:
        return ["vision"]

    def get_output_keys(self) -> list[str]:
        return ["swot_analysis", "market_analysis", "gap_analysis", "trend_analysis", "context_summary"]

    def validate_inputs(self, state: RunState) -> bool:
        return "vision" in state.working_data

    def execute(self, state: RunState) -> RunState:
        """Perform comprehensive context analysis."""

        vision = state.working_data.get("vision", {})
        additional_context = self._gather_context(state)

        user_prompt = f"""Perform a comprehensive strategic context analysis based on the following inputs:

## Strategic Vision
{vision}

## Additional Context
{additional_context}

Please provide:

1. **SWOT Analysis** with 3-5 items in each category, prioritized by impact:
   - Strengths (internal positives)
   - Weaknesses (internal negatives)
   - Opportunities (external positives)
   - Threats (external negatives)

2. **Market Analysis**:
   - Key industry trends
   - Competitive dynamics
   - Market opportunities
   - Customer/stakeholder needs

3. **Gap Analysis**:
   - Current state summary
   - Desired state summary
   - Critical gaps (prioritized)
   - Required capabilities

4. **Trend Analysis**:
   - Technology trends affecting strategy
   - Market/industry trends
   - Regulatory considerations
   - Social/demographic factors

5. **Strategic Implications**:
   - Key insights for strategy
   - Critical success factors
   - Major risks to address
   - Recommended focus areas

Return as valid JSON:
{{
    "swot_analysis": {{
        "strengths": [{{"item": "...", "impact": "high/medium/low", "evidence": "..."}}],
        "weaknesses": [{{"item": "...", "impact": "high/medium/low", "evidence": "..."}}],
        "opportunities": [{{"item": "...", "impact": "high/medium/low", "evidence": "..."}}],
        "threats": [{{"item": "...", "impact": "high/medium/low", "evidence": "..."}}]
    }},
    "market_analysis": {{
        "industry_trends": [...],
        "competitive_dynamics": [...],
        "market_opportunities": [...],
        "stakeholder_needs": [...]
    }},
    "gap_analysis": {{
        "current_state": "...",
        "desired_state": "...",
        "critical_gaps": [{{"gap": "...", "priority": "high/medium/low", "impact": "..."}}],
        "required_capabilities": [...]
    }},
    "trend_analysis": {{
        "technology": [...],
        "market": [...],
        "regulatory": [...],
        "social": [...]
    }},
    "strategic_implications": {{
        "key_insights": [...],
        "critical_success_factors": [...],
        "major_risks": [...],
        "recommended_focus_areas": [...]
    }},
    "analysis_confidence": 0.85
}}"""

        system_prompt = self.get_prompt_with_learnings(state)
        response = self.invoke_llm(user_prompt, system_prompt)

        try:
            result = self.extract_json_from_response(response)

            # Store all analysis results
            state.working_data["swot_analysis"] = result.get("swot_analysis", {})
            state.working_data["market_analysis"] = result.get("market_analysis", {})
            state.working_data["gap_analysis"] = result.get("gap_analysis", {})
            state.working_data["trend_analysis"] = result.get("trend_analysis", {})
            state.working_data["strategic_implications"] = result.get("strategic_implications", {})
            state.working_data["context_analysis_confidence"] = result.get("analysis_confidence", 0.5)

            # Create summary for downstream agents
            state.working_data["context_summary"] = self._create_summary(result)

            # Flag high-impact threats
            threats = result.get("swot_analysis", {}).get("threats", [])
            high_threats = [t for t in threats if t.get("impact") == "high"]
            if len(high_threats) >= 3:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "HIGH_THREAT_COUNT",
                    f"Identified {len(high_threats)} high-impact threats requiring attention"
                )

            # Flag critical gaps
            gaps = result.get("gap_analysis", {}).get("critical_gaps", [])
            critical_gaps = [g for g in gaps if g.get("priority") == "high"]
            if critical_gaps:
                self.add_flag(
                    state,
                    SeverityLevel.INFO,
                    "CRITICAL_GAPS_IDENTIFIED",
                    f"Identified {len(critical_gaps)} high-priority gaps to address"
                )

            self.logger.info(f"Context analysis completed with confidence {result.get('analysis_confidence', 0):.2f}")

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.ERROR,
                "CONTEXT_ANALYSIS_FAILED",
                f"Failed to parse context analysis: {str(e)}"
            )
            self.logger.error(f"Context analysis failed: {e}")

        return state

    def _gather_context(self, state: RunState) -> str:
        """Gather additional context from inputs."""
        parts = []

        if state.inputs.raw_context_text:
            parts.append(f"User-provided context:\n{state.inputs.raw_context_text}")

        if state.inputs.market_analysis and state.inputs.market_analysis.exists():
            try:
                content = state.inputs.market_analysis.read_text()
                parts.append(f"Market analysis document:\n{content}")
            except Exception:
                pass

        if state.inputs.current_state_analysis and state.inputs.current_state_analysis.exists():
            try:
                content = state.inputs.current_state_analysis.read_text()
                parts.append(f"Current state analysis:\n{content}")
            except Exception:
                pass

        return "\n\n".join(parts) if parts else "No additional context provided."

    def _create_summary(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Create a concise summary for downstream agents."""
        return {
            "key_strengths": [
                s.get("item") for s in result.get("swot_analysis", {}).get("strengths", [])[:3]
            ],
            "key_weaknesses": [
                w.get("item") for w in result.get("swot_analysis", {}).get("weaknesses", [])[:3]
            ],
            "key_opportunities": [
                o.get("item") for o in result.get("swot_analysis", {}).get("opportunities", [])[:3]
            ],
            "key_threats": [
                t.get("item") for t in result.get("swot_analysis", {}).get("threats", [])[:3]
            ],
            "critical_gaps": [
                g.get("gap") for g in result.get("gap_analysis", {}).get("critical_gaps", [])[:5]
            ],
            "focus_areas": result.get("strategic_implications", {}).get("recommended_focus_areas", [])[:5],
            "success_factors": result.get("strategic_implications", {}).get("critical_success_factors", [])[:5],
        }
