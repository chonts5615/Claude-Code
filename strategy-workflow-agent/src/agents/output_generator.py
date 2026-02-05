"""Output Generator Agent - Generates final strategy documents and outputs."""

from typing import List, Dict, Any
from datetime import datetime

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase
from src.schemas.strategy import ExecutionPlan


class OutputGeneratorAgent(BaseAgent):
    """
    Agent that generates final strategy documents and outputs.

    Responsibilities:
    - Generate comprehensive strategy document
    - Create executive summary
    - Produce presentation materials
    - Define KPI dashboard specifications
    - Package all deliverables
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="S10_OutputGenerator",
            step_name="Output Generation",
            phase=WorkflowPhase.OUTPUT,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are an expert in strategic communication and documentation.

Your task is to generate polished, professional strategy outputs including:

1. **Executive Summary**: 1-2 page overview for leadership
2. **Strategy Document**: Comprehensive strategic plan
3. **Presentation Deck Outline**: Key slides for stakeholder presentation
4. **KPI Dashboard Specification**: Metrics tracking requirements
5. **Implementation Roadmap**: Visual timeline summary

**Document Quality Standards:**
- Clear, concise language
- Logical flow and structure
- Consistent terminology
- Visual-ready formatting
- Actionable content

**Executive Summary Structure:**
- Strategic context and opportunity
- Vision and strategic direction
- Key pillars and priorities
- Critical success factors
- Resource requirements
- Key risks and mitigation
- Implementation timeline
- Call to action

Generate content ready for professional presentation."""

    def get_required_inputs(self) -> list[str]:
        return ["vision", "strategic_pillars", "strategic_goals", "initiatives", "validation_result"]

    def get_output_keys(self) -> list[str]:
        return ["executive_summary", "strategy_document", "presentation_outline", "kpi_dashboard_spec"]

    def validate_inputs(self, state: RunState) -> bool:
        required = ["vision", "strategic_pillars", "strategic_goals", "initiatives"]
        return all(key in state.working_data for key in required)

    def execute(self, state: RunState) -> RunState:
        """Generate strategy outputs."""

        vision = state.working_data.get("vision", {})
        pillars = state.working_data.get("strategic_pillars", [])
        goals = state.working_data.get("strategic_goals", [])
        initiatives = state.working_data.get("initiatives", [])
        risks = state.working_data.get("risks", [])
        resource_plan = state.working_data.get("resource_plan_summary", {})
        milestones = state.working_data.get("milestones", [])
        validation = state.working_data.get("validation_result", {})
        qa_summary = state.qa_summary

        output_format = state.config.output_format

        user_prompt = f"""Generate comprehensive strategy outputs based on the following validated strategic plan.

## Vision
{vision}

## Strategic Pillars
{pillars}

## Goals
{goals}

## Initiatives
{initiatives}

## Risks
{risks}

## Resource Plan
{resource_plan}

## Key Milestones
{milestones[:20]}  # Top 20 milestones

## Validation Summary
{validation.get('certification', {})}

## QA Summary
{qa_summary}

## Output Format Requested: {output_format}

Generate the following outputs:

1. **Executive Summary** (1-2 pages worth of content)
2. **Strategy Document Outline** with key section content
3. **Presentation Deck Outline** (10-15 slides)
4. **KPI Dashboard Specification**
5. **Implementation Roadmap Summary**

Return as valid JSON:
{{
    "executive_summary": {{
        "title": "Strategic Plan Executive Summary",
        "subtitle": "[Organization] {state.config.time_horizon_years}-Year Strategy",
        "date": "{datetime.utcnow().strftime('%B %Y')}",
        "sections": [
            {{
                "heading": "Strategic Context",
                "content": "..."
            }},
            {{
                "heading": "Vision & Direction",
                "content": "..."
            }},
            {{
                "heading": "Strategic Pillars",
                "content": "...",
                "bullets": ["Pillar 1: ...", "Pillar 2: ..."]
            }},
            {{
                "heading": "Key Initiatives",
                "content": "...",
                "bullets": ["..."]
            }},
            {{
                "heading": "Resource Requirements",
                "content": "...",
                "key_figures": {{"total_budget": "...", "peak_fte": "..."}}
            }},
            {{
                "heading": "Risk Management",
                "content": "...",
                "bullets": ["..."]
            }},
            {{
                "heading": "Implementation Timeline",
                "content": "...",
                "key_dates": ["..."]
            }},
            {{
                "heading": "Call to Action",
                "content": "..."
            }}
        ]
    }},
    "strategy_document": {{
        "title": "Strategic Plan",
        "version": "1.0",
        "sections": [
            {{"title": "Executive Summary", "content_summary": "..."}},
            {{"title": "Strategic Context", "subsections": ["Current State", "Market Analysis", "SWOT"]}},
            {{"title": "Strategic Direction", "subsections": ["Vision", "Mission", "Values"]}},
            {{"title": "Strategic Pillars", "subsections": ["Pillar 1", "Pillar 2", "..."]}},
            {{"title": "Goals & Objectives", "subsections": ["By Pillar"]}},
            {{"title": "Strategic Initiatives", "subsections": ["Initiative Portfolio", "Dependencies"]}},
            {{"title": "Resource Plan", "subsections": ["Budget", "Staffing", "Technology"]}},
            {{"title": "Risk Management", "subsections": ["Risk Register", "Mitigation"]}},
            {{"title": "Implementation Roadmap", "subsections": ["Timeline", "Milestones"]}},
            {{"title": "Governance", "subsections": ["Roles", "Review Process"]}},
            {{"title": "Appendices", "subsections": ["Detailed Data", "Glossary"]}}
        ]
    }},
    "presentation_outline": {{
        "title": "Strategic Plan Overview",
        "slides": [
            {{"number": 1, "title": "Title Slide", "content": "Strategic Plan [Year Range]"}},
            {{"number": 2, "title": "Agenda", "content": "Overview of presentation"}},
            {{"number": 3, "title": "Strategic Context", "content": "Key context points", "visual": "timeline or context diagram"}},
            {{"number": 4, "title": "Vision & Mission", "content": "Vision and mission statements", "visual": "large text"}},
            {{"number": 5, "title": "Strategic Pillars Overview", "content": "Pillar names and brief descriptions", "visual": "pillar diagram"}},
            {{"number": 6, "title": "Pillar 1 Deep Dive", "content": "Goals and key initiatives", "visual": "hierarchy"}},
            {{"number": 7, "title": "Pillar 2 Deep Dive", "content": "Goals and key initiatives", "visual": "hierarchy"}},
            {{"number": 8, "title": "Key Initiatives Portfolio", "content": "Top initiatives", "visual": "portfolio matrix"}},
            {{"number": 9, "title": "Resource Requirements", "content": "Budget and staffing", "visual": "bar chart"}},
            {{"number": 10, "title": "Implementation Timeline", "content": "Key phases", "visual": "Gantt chart"}},
            {{"number": 11, "title": "Risk Summary", "content": "Top risks and mitigation", "visual": "risk matrix"}},
            {{"number": 12, "title": "Success Metrics", "content": "KPIs and targets", "visual": "dashboard mockup"}},
            {{"number": 13, "title": "Next Steps", "content": "Immediate actions", "visual": "checklist"}},
            {{"number": 14, "title": "Q&A", "content": "Discussion", "visual": "none"}}
        ]
    }},
    "kpi_dashboard_spec": {{
        "dashboard_name": "Strategic KPI Dashboard",
        "refresh_frequency": "monthly",
        "sections": [
            {{
                "name": "Executive Overview",
                "metrics": [
                    {{"name": "Overall Strategy Progress", "type": "progress_bar", "target": 100}},
                    {{"name": "Goals On Track", "type": "ratio", "format": "X/Y"}},
                    {{"name": "Budget Utilization", "type": "gauge", "target": "planned"}}
                ]
            }},
            {{
                "name": "Pillar Performance",
                "metrics": [
                    {{"name": "Pillar 1 Progress", "type": "progress_bar"}},
                    {{"name": "Pillar 2 Progress", "type": "progress_bar"}}
                ]
            }},
            {{
                "name": "Initiative Status",
                "metrics": [
                    {{"name": "Initiatives by Status", "type": "donut_chart"}},
                    {{"name": "Milestone Completion", "type": "timeline"}}
                ]
            }},
            {{
                "name": "Risk Monitor",
                "metrics": [
                    {{"name": "Open Risks by Severity", "type": "stacked_bar"}},
                    {{"name": "Risk Trend", "type": "line_chart"}}
                ]
            }}
        ],
        "data_sources": ["Initiative tracking system", "Financial system", "Risk register"],
        "access_levels": ["Executive", "Manager", "Team Lead"]
    }},
    "roadmap_summary": {{
        "phases": [
            {{
                "name": "Phase 1: Foundation",
                "duration": "Q1-Q2 Year 1",
                "focus": "...",
                "key_deliverables": ["..."]
            }}
        ],
        "critical_milestones": ["..."],
        "key_decision_points": ["..."]
    }}
}}"""

        system_prompt = self.get_prompt_with_learnings(state)
        response = self.invoke_llm(user_prompt, system_prompt)

        try:
            result = self.extract_json_from_response(response)

            # Store all outputs
            state.working_data["executive_summary"] = result.get("executive_summary", {})
            state.working_data["strategy_document"] = result.get("strategy_document", {})
            state.working_data["presentation_outline"] = result.get("presentation_outline", {})
            state.working_data["kpi_dashboard_spec"] = result.get("kpi_dashboard_spec", {})
            state.working_data["roadmap_summary"] = result.get("roadmap_summary", {})

            # Create execution plan object
            self._create_execution_plan(state)

            self.add_flag(
                state,
                SeverityLevel.INFO,
                "OUTPUTS_GENERATED",
                "All strategy outputs generated successfully"
            )

            self.logger.info("Strategy outputs generated successfully")

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.ERROR,
                "OUTPUT_GENERATION_FAILED",
                f"Failed to generate outputs: {str(e)}"
            )
            self.logger.error(f"Output generation failed: {e}")

        return state

    def _create_execution_plan(self, state: RunState) -> None:
        """Create the final execution plan object."""
        from datetime import date
        from src.schemas.strategy import (
            ExecutionPlan, StrategicVision, StrategicPillar, StrategicGoal,
            Initiative, Milestone, KPI, RiskAssessment, ResourceAllocation, DependencyMap
        )

        vision_data = state.working_data.get("vision", {})
        vision = StrategicVision(**vision_data) if vision_data else None

        execution_plan = ExecutionPlan(
            plan_id=f"PLAN_{state.run_id}",
            plan_name=f"Strategic Plan {state.config.time_horizon_years}-Year",
            plan_version="1.0",
            created_date=date.today(),
            last_updated=date.today(),
            vision=vision,
            pillars=[],  # Would convert from working_data
            goals=[],
            initiatives=[],
            milestones=[],
            kpis=[],
            risks=[],
            resource_allocations=[],
            dependencies=[],
            total_budget=state.working_data.get("total_budget", 0),
            total_fte=state.working_data.get("total_fte_peak", 0),
            overall_feasibility=state.working_data.get("quality_scores", {}).get("feasibility_score", 0),
            overall_alignment=state.working_data.get("quality_scores", {}).get("alignment_score", 0),
            overall_completeness=state.working_data.get("quality_scores", {}).get("completeness_score", 0),
            status="draft",
        )

        state.working_data["execution_plan"] = execution_plan.model_dump()
