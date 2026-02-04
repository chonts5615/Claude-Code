"""Timeline Optimizer Agent - Optimizes initiative timelines and sequencing."""

from typing import List, Dict, Any
import uuid
from datetime import date

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase
from src.schemas.strategy import Milestone, DependencyMap


class TimelineOptimizerAgent(BaseAgent):
    """
    Agent that optimizes initiative timelines and sequencing.

    Responsibilities:
    - Optimize initiative sequencing
    - Resolve scheduling conflicts
    - Identify critical path
    - Create milestone timeline
    - Balance workload distribution
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="S8_TimelineOptimizer",
            step_name="Timeline Optimization",
            phase=WorkflowPhase.OPTIMIZATION,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are an expert in strategic planning and project scheduling optimization.

Your task is to optimize the timeline for strategic initiatives:
1. Respect all dependencies
2. Balance resource utilization
3. Identify and optimize critical path
4. Create clear milestones
5. Build in appropriate buffers

**Timeline Optimization Principles:**
- Critical initiatives should start as early as dependencies allow
- Quick wins should be prioritized for early momentum
- Resource-intensive initiatives should be staggered
- Dependencies must be strictly respected
- Build in contingency for high-risk initiatives

**Optimization Goals:**
- Minimize overall program duration
- Balance resource loading across periods
- Maximize early value delivery
- Reduce risk through proper sequencing
- Ensure realistic, achievable timelines

**Outputs:**
- Optimized start/end dates for each initiative
- Milestone schedule with clear checkpoints
- Critical path identification
- Resource loading chart
- Key scheduling recommendations"""

    def get_required_inputs(self) -> list[str]:
        return ["initiatives", "initiative_dependencies", "resource_allocations"]

    def get_output_keys(self) -> list[str]:
        return ["optimized_timeline", "milestones", "critical_path", "dependency_map"]

    def validate_inputs(self, state: RunState) -> bool:
        return "initiatives" in state.working_data and len(state.working_data["initiatives"]) > 0

    def execute(self, state: RunState) -> RunState:
        """Optimize initiative timelines."""

        initiatives = state.working_data.get("initiatives", [])
        dependencies = state.working_data.get("initiative_dependencies", {})
        resource_allocations = state.working_data.get("resource_allocations", [])
        resource_plan = state.working_data.get("resource_plan_summary", {})

        user_prompt = f"""Optimize the timeline for the following strategic initiatives.

## Initiatives
{initiatives}

## Dependencies
{dependencies}

## Resource Allocations
{resource_allocations}

## Resource Plan Summary
{resource_plan}

Create an optimized timeline that:
1. Respects all dependencies
2. Balances resource utilization
3. Identifies critical path
4. Includes clear milestones
5. Builds in appropriate buffers

Return as valid JSON:
{{
    "optimized_initiatives": [
        {{
            "initiative_id": "INIT_GOAL001_001",
            "original_start": "2024-01-15",
            "original_end": "2024-06-30",
            "optimized_start": "2024-02-01",
            "optimized_end": "2024-07-15",
            "change_reason": "Shifted to allow dependency completion",
            "buffer_days": 15,
            "is_critical_path": true
        }}
    ],
    "milestones": [
        {{
            "milestone_id": "MS_001",
            "parent_id": "INIT_GOAL001_001",
            "parent_type": "initiative",
            "name": "Requirements Complete",
            "description": "All requirements documented and approved",
            "target_date": "2024-03-15",
            "acceptance_criteria": ["Requirements document approved", "Stakeholder sign-off"],
            "deliverables": ["Requirements Document v1.0"],
            "dependencies": [],
            "is_critical": true
        }}
    ],
    "critical_path": {{
        "path_initiatives": ["INIT_GOAL001_001", "INIT_GOAL001_002", "INIT_GOAL002_001"],
        "total_duration_days": 450,
        "critical_milestones": ["MS_001", "MS_005", "MS_010"],
        "bottlenecks": ["Resource constraint in Q3", "Dependency on external vendor"],
        "slack_analysis": {{
            "INIT_GOAL001_003": {{"slack_days": 30, "can_delay": true}},
            "INIT_GOAL002_002": {{"slack_days": 0, "can_delay": false}}
        }}
    }},
    "dependency_map": [
        {{
            "dependency_id": "DEP_001",
            "source_id": "INIT_GOAL001_002",
            "source_type": "initiative",
            "target_id": "INIT_GOAL001_001",
            "target_type": "initiative",
            "dependency_type": "finish-to-start",
            "is_critical": true,
            "lag_days": 5
        }}
    ],
    "resource_loading": {{
        "by_period": {{
            "2024Q1": {{"fte": 15, "utilization": 0.75, "status": "manageable"}},
            "2024Q2": {{"fte": 22, "utilization": 0.88, "status": "high"}},
            "2024Q3": {{"fte": 28, "utilization": 0.95, "status": "overloaded"}}
        }},
        "overload_periods": ["2024Q3"],
        "underutilized_periods": ["2024Q1"]
    }},
    "optimization_summary": {{
        "original_duration_days": 730,
        "optimized_duration_days": 680,
        "duration_savings_days": 50,
        "resource_conflicts_resolved": 3,
        "buffer_added_days": 45
    }},
    "recommendations": [
        "Consider starting Initiative X earlier to reduce Q3 peak",
        "Add resource buffer for critical path initiatives",
        "Plan quarterly review checkpoints for course correction"
    ]
}}"""

        system_prompt = self.get_prompt_with_learnings(state)
        response = self.invoke_llm(user_prompt, system_prompt)

        try:
            result = self.extract_json_from_response(response)

            # Convert milestones to objects
            milestones = []
            for m in result.get("milestones", []):
                milestone = Milestone(
                    milestone_id=m.get("milestone_id", f"MS_{uuid.uuid4().hex[:6]}"),
                    parent_id=m.get("parent_id", ""),
                    parent_type=m.get("parent_type", "initiative"),
                    name=m.get("name", ""),
                    description=m.get("description", ""),
                    target_date=date.fromisoformat(m.get("target_date")) if m.get("target_date") else date.today(),
                    acceptance_criteria=m.get("acceptance_criteria", []),
                    deliverables=m.get("deliverables", []),
                    dependencies=m.get("dependencies", []),
                )
                milestones.append(milestone)

            # Convert dependencies to objects
            dependency_map = []
            for d in result.get("dependency_map", []):
                dep = DependencyMap(
                    dependency_id=d.get("dependency_id", f"DEP_{uuid.uuid4().hex[:6]}"),
                    source_id=d.get("source_id", ""),
                    source_type=d.get("source_type", "initiative"),
                    target_id=d.get("target_id", ""),
                    target_type=d.get("target_type", "initiative"),
                    dependency_type=d.get("dependency_type", "finish-to-start"),
                    is_critical=d.get("is_critical", False),
                    lag_days=d.get("lag_days", 0),
                )
                dependency_map.append(dep)

            # Store results
            state.working_data["optimized_timeline"] = result.get("optimized_initiatives", [])
            state.working_data["milestones"] = [m.model_dump() for m in milestones]
            state.working_data["critical_path"] = result.get("critical_path", {})
            state.working_data["dependency_map"] = [d.model_dump() for d in dependency_map]
            state.working_data["resource_loading"] = result.get("resource_loading", {})
            state.working_data["optimization_summary"] = result.get("optimization_summary", {})
            state.working_data["timeline_recommendations"] = result.get("recommendations", [])

            # Check for overloaded periods
            resource_loading = result.get("resource_loading", {})
            overload_periods = resource_loading.get("overload_periods", [])
            if overload_periods:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "RESOURCE_OVERLOAD",
                    f"Resource overload in periods: {', '.join(overload_periods)}"
                )

            # Check critical path length
            critical_path = result.get("critical_path", {})
            critical_duration = critical_path.get("total_duration_days", 0)
            time_horizon_days = state.config.time_horizon_years * 365

            if critical_duration > time_horizon_days:
                self.add_flag(
                    state,
                    SeverityLevel.ERROR,
                    "CRITICAL_PATH_EXCEEDS_HORIZON",
                    f"Critical path ({critical_duration} days) exceeds planning horizon ({time_horizon_days} days)"
                )

            # Report optimization savings
            opt_summary = result.get("optimization_summary", {})
            savings = opt_summary.get("duration_savings_days", 0)
            if savings > 0:
                self.add_flag(
                    state,
                    SeverityLevel.INFO,
                    "TIMELINE_OPTIMIZED",
                    f"Timeline optimized: {savings} days saved through sequencing"
                )

            self.logger.info(
                f"Timeline optimized: {len(milestones)} milestones, "
                f"critical path {critical_duration} days"
            )

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.ERROR,
                "TIMELINE_OPTIMIZATION_FAILED",
                f"Failed to optimize timeline: {str(e)}"
            )
            self.logger.error(f"Timeline optimization failed: {e}")

        return state
