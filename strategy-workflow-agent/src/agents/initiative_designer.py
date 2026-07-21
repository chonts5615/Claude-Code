"""Initiative Designer Agent - Designs specific initiatives to achieve goals."""

from typing import List, Dict, Any
import uuid
from datetime import date, timedelta

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase
from src.schemas.strategy import Initiative, GoalStatus, StrategicPriority, InitiativeDesignOutput


class InitiativeDesignerAgent(BaseAgent[InitiativeDesignOutput]):
    """
    Agent that designs specific initiatives to achieve strategic goals.

    Responsibilities:
    - Create 1-3 initiatives per goal
    - Define initiative scope and deliverables
    - Estimate resources and budget
    - Identify dependencies and prerequisites
    - Assess feasibility and alignment
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="S5_InitiativeDesigner",
            step_name="Initiative Design",
            phase=WorkflowPhase.PLANNING,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are an expert in strategic initiative design and program management.

Your task is to design specific initiatives that will achieve strategic goals.

**Initiative Design Principles:**
1. Each initiative should have a clear, bounded scope
2. Deliverables should be concrete and verifiable
3. Resource estimates should be realistic
4. Dependencies should be clearly identified
5. Success criteria should be measurable

**Initiative Types:**
- **Project**: Time-bound effort with specific deliverables
- **Program**: Collection of related projects
- **Process**: Ongoing operational improvement
- **Capability**: Building new organizational capability

**For each initiative, provide:**
1. Clear name and description
2. Objective (what it will achieve)
3. Type classification
4. Timeline (start/end dates, duration)
5. Budget estimate with breakdown
6. FTE requirements
7. Key roles needed
8. Deliverables and success criteria
9. Dependencies (goals, other initiatives)
10. Risks specific to this initiative
11. Feasibility, impact, and alignment scores

Design 1-3 initiatives per goal. Focus on initiatives that are:
- Necessary and sufficient to achieve the goal
- Appropriately scoped (not too large or too small)
- Realistically resourced"""

    def get_required_inputs(self) -> list[str]:
        return ["strategic_goals", "strategic_pillars", "context_summary"]

    def get_output_keys(self) -> list[str]:
        return ["initiatives", "initiatives_by_goal", "initiative_dependencies", "resource_summary"]

    def validate_inputs(self, state: RunState) -> bool:
        return "strategic_goals" in state.working_data and len(state.working_data["strategic_goals"]) > 0

    def execute(self, state: RunState) -> RunState:
        """Design initiatives for strategic goals."""

        goals = state.working_data.get("strategic_goals", [])
        pillars = state.working_data.get("strategic_pillars", [])
        context = state.working_data.get("context_summary", {})
        gap_analysis = state.working_data.get("gap_analysis", {})

        user_prompt = f"""Design specific initiatives to achieve the following strategic goals.

## Strategic Goals
{goals}

## Strategic Pillars
{pillars}

## Context Summary
{context}

## Gap Analysis (capabilities needed)
{gap_analysis}

For each goal, design 1-3 initiatives. For each initiative provide:

- initiative_id (format: INIT_GOAL001_001)
- goal_id (parent goal)
- name (concise initiative name)
- description (detailed description)
- objective (what this initiative will achieve)
- initiative_type (project, program, process, capability)
- priority (critical, high, medium, low)
- planned_start (YYYY-MM-DD)
- planned_end (YYYY-MM-DD)
- duration_months
- estimated_budget (in USD)
- fte_required (total FTE needed)
- key_roles (list of roles required)
- required_capabilities (skills/capabilities needed)
- deliverables (list of concrete deliverables)
- success_criteria (list of measurable criteria)
- dependencies (list of initiative_ids this depends on)
- prerequisite_initiatives (must complete before this)
- risks (list of key risks)
- feasibility_score (0-1)
- impact_score (0-1)
- alignment_score (0-1)
- sponsor (recommended sponsor role)
- owner (recommended owner role)

Return as valid JSON:
{{
    "initiatives": [
        {{
            "initiative_id": "INIT_GOAL001_001",
            "goal_id": "GOAL_PIL001_001",
            "name": "...",
            "description": "...",
            "objective": "...",
            "initiative_type": "project",
            "priority": "high",
            "planned_start": "2024-01-15",
            "planned_end": "2024-06-30",
            "duration_months": 6,
            "estimated_budget": 150000,
            "fte_required": 3.5,
            "key_roles": ["Project Manager", "..."],
            "required_capabilities": ["..."],
            "deliverables": ["..."],
            "success_criteria": ["..."],
            "dependencies": [],
            "prerequisite_initiatives": [],
            "risks": ["..."],
            "feasibility_score": 0.85,
            "impact_score": 0.9,
            "alignment_score": 0.95,
            "sponsor": "CTO",
            "owner": "Director of Engineering"
        }}
    ],
    "initiatives_by_goal": {{
        "GOAL_PIL001_001": ["INIT_GOAL001_001", "INIT_GOAL001_002"]
    }},
    "initiative_dependencies": {{
        "INIT_GOAL001_002": ["INIT_GOAL001_001"]
    }},
    "resource_summary": {{
        "total_budget": 1500000,
        "total_fte": 25.5,
        "budget_by_year": {{"2024": 800000, "2025": 700000}},
        "fte_by_quarter": {{"Q1_2024": 15, "Q2_2024": 20}},
        "resource_conflicts": []
    }}
}}"""

        system_prompt = self.get_prompt_with_learnings(state)
        response = self.invoke_llm(user_prompt, system_prompt)

        try:
            result = self.extract_json_from_response(response)

            # Convert to Initiative objects
            initiatives = []
            for i in result.get("initiatives", []):
                initiative = Initiative(
                    initiative_id=i.get("initiative_id", f"INIT_{uuid.uuid4().hex[:8]}"),
                    goal_id=i.get("goal_id", ""),
                    name=i.get("name", ""),
                    description=i.get("description", ""),
                    objective=i.get("objective", ""),
                    initiative_type=i.get("initiative_type", "project"),
                    priority=StrategicPriority(i.get("priority", "medium")),
                    status=GoalStatus.DRAFT,
                    planned_start=date.fromisoformat(i.get("planned_start")) if i.get("planned_start") else None,
                    planned_end=date.fromisoformat(i.get("planned_end")) if i.get("planned_end") else None,
                    duration_months=i.get("duration_months"),
                    estimated_budget=i.get("estimated_budget"),
                    fte_required=i.get("fte_required"),
                    key_roles=i.get("key_roles", []),
                    required_capabilities=i.get("required_capabilities", []),
                    deliverables=i.get("deliverables", []),
                    success_criteria=i.get("success_criteria", []),
                    dependencies=i.get("dependencies", []),
                    prerequisite_initiatives=i.get("prerequisite_initiatives", []),
                    feasibility_score=i.get("feasibility_score", 0.5),
                    impact_score=i.get("impact_score", 0.5),
                    alignment_score=i.get("alignment_score", 0.5),
                    sponsor=i.get("sponsor"),
                    owner=i.get("owner"),
                )
                initiatives.append(initiative)

            # Store results
            state.working_data["initiatives"] = [i.model_dump() for i in initiatives]
            state.working_data["initiatives_by_goal"] = result.get("initiatives_by_goal", {})
            state.working_data["initiative_dependencies"] = result.get("initiative_dependencies", {})
            state.working_data["resource_summary"] = result.get("resource_summary", {})

            # Validate initiative counts
            initiatives_by_goal = result.get("initiatives_by_goal", {})
            thresholds = state.config.thresholds

            for goal_id, goal_inits in initiatives_by_goal.items():
                init_count = len(goal_inits)
                if init_count < thresholds.min_initiatives_per_goal:
                    self.add_flag(
                        state,
                        SeverityLevel.WARNING,
                        "FEW_INITIATIVES_PER_GOAL",
                        f"Goal {goal_id} has only {init_count} initiatives"
                    )
                elif init_count > thresholds.max_initiatives_per_goal:
                    self.add_flag(
                        state,
                        SeverityLevel.WARNING,
                        "MANY_INITIATIVES_PER_GOAL",
                        f"Goal {goal_id} has {init_count} initiatives - consider consolidating"
                    )

            # Check feasibility scores
            low_feasibility = [
                i for i in initiatives
                if i.feasibility_score < thresholds.initiative_feasibility_min
            ]
            if low_feasibility:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "LOW_FEASIBILITY_INITIATIVES",
                    f"{len(low_feasibility)} initiatives have low feasibility scores"
                )

            # Check for resource conflicts
            resource_conflicts = result.get("resource_summary", {}).get("resource_conflicts", [])
            if resource_conflicts:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "RESOURCE_CONFLICTS",
                    f"Identified {len(resource_conflicts)} resource conflicts"
                )

            self.logger.info(f"Designed {len(initiatives)} initiatives for {len(initiatives_by_goal)} goals")

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.ERROR,
                "INITIATIVE_DESIGN_FAILED",
                f"Failed to design initiatives: {str(e)}"
            )
            self.logger.error(f"Initiative design failed: {e}")

        return state
