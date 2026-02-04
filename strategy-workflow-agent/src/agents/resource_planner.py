"""Resource Planner Agent - Plans resource allocation across initiatives."""

from typing import List, Dict, Any
import uuid

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase
from src.schemas.strategy import ResourceAllocation, ResourcePlanOutput


class ResourcePlannerAgent(BaseAgent[ResourcePlanOutput]):
    """
    Agent that plans resource allocation across strategic initiatives.

    Responsibilities:
    - Allocate budget across initiatives
    - Plan FTE allocation
    - Identify resource constraints
    - Optimize resource utilization
    - Flag resource conflicts
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="S7_ResourcePlanner",
            step_name="Resource Planning",
            phase=WorkflowPhase.PLANNING,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are an expert in strategic resource planning and portfolio management.

Your task is to create a comprehensive resource allocation plan that:
1. Aligns resources with strategic priorities
2. Ensures feasible execution
3. Identifies and resolves conflicts
4. Optimizes utilization
5. Maintains flexibility for adjustments

**Resource Planning Principles:**
- Prioritize critical and high-priority initiatives
- Consider dependencies when sequencing
- Build in contingency for uncertainties
- Balance short-term and long-term investments
- Ensure sustainable workload for teams

**Resource Types:**
- **Financial**: Budget allocation by period
- **Human**: FTE allocation by role and skill
- **Technology**: Systems, tools, infrastructure
- **External**: Vendors, consultants, partners

**For each allocation:**
1. Link to specific initiative
2. Specify amounts by period
3. Identify role/skill requirements
4. Note constraints and assumptions
5. Calculate utilization rates
6. Flag conflicts or gaps

Provide detailed allocation plan with period-by-period breakdown."""

    def get_required_inputs(self) -> list[str]:
        return ["initiatives", "strategic_goals"]

    def get_output_keys(self) -> list[str]:
        return ["resource_allocations", "resource_plan_summary", "resource_gaps", "resource_timeline"]

    def validate_inputs(self, state: RunState) -> bool:
        return "initiatives" in state.working_data and len(state.working_data["initiatives"]) > 0

    def execute(self, state: RunState) -> RunState:
        """Plan resource allocation."""

        initiatives = state.working_data.get("initiatives", [])
        goals = state.working_data.get("strategic_goals", [])
        resource_summary = state.working_data.get("resource_summary", {})
        time_horizon = state.config.time_horizon_years

        user_prompt = f"""Create a detailed resource allocation plan for the following initiatives.

## Initiatives
{initiatives}

## Strategic Goals
{goals}

## Initial Resource Summary
{resource_summary}

## Planning Parameters
- Time horizon: {time_horizon} years
- Planning granularity: {state.config.planning_granularity}

For each initiative, create resource allocations by period. Include:

- allocation_id (format: ALLOC_INIT001_2024Q1)
- initiative_id
- budget_allocated (in USD)
- budget_currency
- budget_year
- budget_quarter (1-4)
- fte_allocated
- roles_allocated (dict of role -> FTE)
- technology_resources (list)
- external_resources (list)
- utilization_rate (0-1)
- allocation_confidence (0-1)
- allocation_rationale
- constraints (list)

Return as valid JSON:
{{
    "allocations": [
        {{
            "allocation_id": "ALLOC_INIT001_2024Q1",
            "initiative_id": "INIT_GOAL001_001",
            "budget_allocated": 75000,
            "budget_currency": "USD",
            "budget_year": 2024,
            "budget_quarter": 1,
            "fte_allocated": 2.5,
            "roles_allocated": {{
                "Project Manager": 0.5,
                "Developer": 1.5,
                "Analyst": 0.5
            }},
            "technology_resources": ["Cloud infrastructure", "Analytics platform"],
            "external_resources": ["Implementation consultant"],
            "utilization_rate": 0.85,
            "allocation_confidence": 0.9,
            "allocation_rationale": "...",
            "constraints": ["Dependent on Q4 hiring"]
        }}
    ],
    "plan_summary": {{
        "total_budget": 2500000,
        "total_fte_peak": 30,
        "budget_by_year": {{"2024": 1200000, "2025": 1000000, "2026": 300000}},
        "fte_by_quarter": {{
            "2024Q1": 15, "2024Q2": 22, "2024Q3": 28, "2024Q4": 30,
            "2025Q1": 28, "2025Q2": 25, "2025Q3": 20, "2025Q4": 15
        }},
        "budget_by_pillar": {{"PIL_001": 1000000, "PIL_002": 900000}},
        "utilization_by_quarter": {{"2024Q1": 0.75, "2024Q2": 0.85}}
    }},
    "resource_gaps": [
        {{
            "gap_type": "skill",
            "description": "Need 2 additional data engineers",
            "impact": "May delay analytics initiative",
            "mitigation": "Consider external contractors",
            "urgency": "high"
        }}
    ],
    "resource_timeline": {{
        "hiring_needs": [{{"role": "Data Engineer", "count": 2, "by_date": "2024-03-01"}}],
        "budget_milestones": [{{"amount": 500000, "by_date": "2024-01-01", "purpose": "Q1 allocation"}}],
        "capacity_constraints": [{{"period": "2024Q3", "constraint": "Peak utilization - limited flexibility"}}]
    }},
    "optimization_recommendations": [
        "Consider phasing Initiative X to reduce Q2 peak load",
        "Bundle vendor contracts for 15% cost savings"
    ]
}}"""

        system_prompt = self.get_prompt_with_learnings(state)
        response = self.invoke_llm(user_prompt, system_prompt)

        try:
            result = self.extract_json_from_response(response)

            # Convert to ResourceAllocation objects
            allocations = []
            for a in result.get("allocations", []):
                allocation = ResourceAllocation(
                    allocation_id=a.get("allocation_id", f"ALLOC_{uuid.uuid4().hex[:8]}"),
                    initiative_id=a.get("initiative_id", ""),
                    budget_allocated=a.get("budget_allocated", 0),
                    budget_currency=a.get("budget_currency", "USD"),
                    budget_year=a.get("budget_year", 2024),
                    budget_quarter=a.get("budget_quarter"),
                    fte_allocated=a.get("fte_allocated", 0),
                    roles_allocated=a.get("roles_allocated", {}),
                    technology_resources=a.get("technology_resources", []),
                    external_resources=a.get("external_resources", []),
                    utilization_rate=a.get("utilization_rate", 0),
                    allocation_confidence=a.get("allocation_confidence", 0.8),
                    allocation_rationale=a.get("allocation_rationale"),
                    constraints=a.get("constraints", []),
                )
                allocations.append(allocation)

            # Store results
            state.working_data["resource_allocations"] = [a.model_dump() for a in allocations]
            state.working_data["resource_plan_summary"] = result.get("plan_summary", {})
            state.working_data["resource_gaps"] = result.get("resource_gaps", [])
            state.working_data["resource_timeline"] = result.get("resource_timeline", {})
            state.working_data["optimization_recommendations"] = result.get("optimization_recommendations", [])

            # Validate resource plan
            thresholds = state.config.thresholds
            plan_summary = result.get("plan_summary", {})

            # Check utilization rates
            utilization = plan_summary.get("utilization_by_quarter", {})
            low_utilization_periods = [
                period for period, rate in utilization.items()
                if rate < thresholds.resource_utilization_min
            ]
            if low_utilization_periods:
                self.add_flag(
                    state,
                    SeverityLevel.INFO,
                    "LOW_UTILIZATION_PERIODS",
                    f"Low utilization in periods: {', '.join(low_utilization_periods)}"
                )

            # Check for resource gaps
            gaps = result.get("resource_gaps", [])
            high_urgency_gaps = [g for g in gaps if g.get("urgency") == "high"]
            if high_urgency_gaps:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "URGENT_RESOURCE_GAPS",
                    f"{len(high_urgency_gaps)} high-urgency resource gaps identified"
                )

            # Store total budget and FTE for QA
            state.working_data["total_budget"] = plan_summary.get("total_budget", 0)
            state.working_data["total_fte_peak"] = plan_summary.get("total_fte_peak", 0)

            self.logger.info(
                f"Resource plan: ${plan_summary.get('total_budget', 0):,.0f} budget, "
                f"{plan_summary.get('total_fte_peak', 0)} peak FTE"
            )

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.ERROR,
                "RESOURCE_PLANNING_FAILED",
                f"Failed to plan resources: {str(e)}"
            )
            self.logger.error(f"Resource planning failed: {e}")

        return state
