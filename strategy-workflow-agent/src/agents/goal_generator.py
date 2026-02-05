"""Goal Generator Agent - Generates SMART goals for each strategic pillar."""

from typing import List, Dict, Any
import uuid
from datetime import date, timedelta

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase
from src.schemas.strategy import StrategicGoal, GoalStatus, StrategicPriority, GoalGenerationOutput


class GoalGeneratorAgent(BaseAgent[GoalGenerationOutput]):
    """
    Agent that generates SMART goals for each strategic pillar.

    Responsibilities:
    - Generate 2-5 goals per pillar
    - Ensure goals are SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
    - Score goal quality
    - Establish goal dependencies
    - Set realistic timelines
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="S4_GoalGenerator",
            step_name="Goal Generation",
            phase=WorkflowPhase.SYNTHESIS,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are an expert in strategic goal setting and the SMART framework.

Your task is to generate strategic goals for each pillar that are:

**SMART Criteria:**
- **Specific**: Clear and unambiguous, answering who, what, where, when, why
- **Measurable**: Quantifiable with concrete metrics or indicators
- **Achievable**: Realistic given resources and constraints
- **Relevant**: Aligned with pillar and vision, meaningful impact
- **Time-bound**: Clear timeline with deadlines

**Goal Quality Standards:**
- Each goal should represent a significant strategic outcome
- Goals should be outcome-focused, not activity-focused
- Avoid goals that are too vague or too narrow
- Consider dependencies between goals
- Balance quick wins with longer-term transformational goals

**For each goal, provide:**
1. Clear goal statement
2. SMART breakdown (each criterion explicitly addressed)
3. SMART compliance score (0-1)
4. Feasibility assessment
5. Impact assessment
6. Timeline (start and end dates)
7. Dependencies on other goals
8. Resource requirements
9. Key milestones

Aim for 2-4 goals per pillar. Quality over quantity."""

    def get_required_inputs(self) -> list[str]:
        return ["vision", "strategic_pillars", "context_summary"]

    def get_output_keys(self) -> list[str]:
        return ["strategic_goals", "goals_by_pillar", "goal_dependencies", "goal_quality_summary"]

    def validate_inputs(self, state: RunState) -> bool:
        return "strategic_pillars" in state.working_data and len(state.working_data["strategic_pillars"]) > 0

    def execute(self, state: RunState) -> RunState:
        """Generate SMART goals for each pillar."""

        vision = state.working_data.get("vision", {})
        pillars = state.working_data.get("strategic_pillars", [])
        context = state.working_data.get("context_summary", {})
        gap_analysis = state.working_data.get("gap_analysis", {})

        # Calculate timeline based on config
        time_horizon = state.config.time_horizon_years
        start_date = date.today()
        end_date = date.today() + timedelta(days=365 * time_horizon)

        user_prompt = f"""Generate SMART strategic goals for each of the following pillars.

## Strategic Vision
{vision}

## Strategic Pillars
{pillars}

## Context Summary
{context}

## Gap Analysis
{gap_analysis}

## Timeline Parameters
- Planning horizon: {time_horizon} years
- Start date: {start_date}
- End date: {end_date}

For each pillar, generate 2-4 strategic goals. For each goal provide:

- goal_id (format: GOAL_PIL001_001)
- pillar_id (parent pillar)
- name (concise goal name)
- description (detailed description)
- specific (what exactly will be achieved)
- measurable (how success will be measured)
- achievable (why this is realistic)
- relevant (why this matters for the pillar/vision)
- time_bound (timeline and milestones)
- smart_score (0-1 overall SMART compliance)
- feasibility_score (0-1)
- impact_score (0-1)
- priority (critical, high, medium, low)
- target_start (YYYY-MM-DD)
- target_end (YYYY-MM-DD)
- dependencies (list of goal_ids this depends on)
- resource_requirements (list of key resources needed)
- key_milestones (list of milestone descriptions)

Return as valid JSON:
{{
    "goals": [
        {{
            "goal_id": "GOAL_PIL001_001",
            "pillar_id": "PIL_001",
            "name": "...",
            "description": "...",
            "specific": "...",
            "measurable": "...",
            "achievable": "...",
            "relevant": "...",
            "time_bound": "...",
            "smart_score": 0.85,
            "feasibility_score": 0.8,
            "impact_score": 0.9,
            "priority": "high",
            "target_start": "2024-01-01",
            "target_end": "2025-12-31",
            "dependencies": [],
            "resource_requirements": ["..."],
            "key_milestones": ["..."]
        }}
    ],
    "goals_by_pillar": {{
        "PIL_001": ["GOAL_PIL001_001", "GOAL_PIL001_002"]
    }},
    "goal_dependencies_graph": {{
        "GOAL_PIL001_002": ["GOAL_PIL001_001"]
    }},
    "quality_summary": {{
        "total_goals": 8,
        "average_smart_score": 0.82,
        "average_feasibility": 0.78,
        "average_impact": 0.85,
        "goals_below_threshold": []
    }}
}}"""

        system_prompt = self.get_prompt_with_learnings(state)
        response = self.invoke_llm(user_prompt, system_prompt)

        try:
            result = self.extract_json_from_response(response)

            # Convert to StrategicGoal objects
            goals = []
            for g in result.get("goals", []):
                goal = StrategicGoal(
                    goal_id=g.get("goal_id", f"GOAL_{uuid.uuid4().hex[:8]}"),
                    pillar_id=g.get("pillar_id", ""),
                    name=g.get("name", ""),
                    description=g.get("description", ""),
                    specific=g.get("specific", ""),
                    measurable=g.get("measurable", ""),
                    achievable=g.get("achievable", ""),
                    relevant=g.get("relevant", ""),
                    time_bound=g.get("time_bound", ""),
                    smart_score=g.get("smart_score", 0.5),
                    feasibility_score=g.get("feasibility_score", 0.5),
                    impact_score=g.get("impact_score", 0.5),
                    status=GoalStatus.DRAFT,
                    priority=StrategicPriority(g.get("priority", "medium")),
                    target_start=date.fromisoformat(g.get("target_start", str(start_date))) if g.get("target_start") else start_date,
                    target_end=date.fromisoformat(g.get("target_end", str(end_date))) if g.get("target_end") else end_date,
                    dependencies=g.get("dependencies", []),
                    resource_requirements=g.get("resource_requirements", []),
                    milestones=g.get("key_milestones", []),
                )
                goals.append(goal)

            # Store results
            state.working_data["strategic_goals"] = [g.model_dump() for g in goals]
            state.working_data["goals_by_pillar"] = result.get("goals_by_pillar", {})
            state.working_data["goal_dependencies"] = result.get("goal_dependencies_graph", {})
            state.working_data["goal_quality_summary"] = result.get("quality_summary", {})

            # Validate goal counts
            goals_by_pillar = result.get("goals_by_pillar", {})
            thresholds = state.config.thresholds

            for pillar_id, pillar_goals in goals_by_pillar.items():
                goal_count = len(pillar_goals)
                if goal_count < thresholds.min_goals_per_pillar:
                    self.add_flag(
                        state,
                        SeverityLevel.WARNING,
                        "FEW_GOALS_PER_PILLAR",
                        f"Pillar {pillar_id} has only {goal_count} goals (minimum: {thresholds.min_goals_per_pillar})"
                    )
                elif goal_count > thresholds.max_goals_per_pillar:
                    self.add_flag(
                        state,
                        SeverityLevel.WARNING,
                        "MANY_GOALS_PER_PILLAR",
                        f"Pillar {pillar_id} has {goal_count} goals (maximum: {thresholds.max_goals_per_pillar})"
                    )

            # Check SMART scores
            quality_summary = result.get("quality_summary", {})
            avg_smart = quality_summary.get("average_smart_score", 0)
            if avg_smart < thresholds.goal_smart_score_min:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "LOW_SMART_SCORE",
                    f"Average SMART score ({avg_smart:.2f}) below threshold ({thresholds.goal_smart_score_min})"
                )

            # Flag low-scoring individual goals
            low_score_goals = [
                g for g in goals
                if g.smart_score < thresholds.goal_smart_score_min
            ]
            if low_score_goals:
                self.add_flag(
                    state,
                    SeverityLevel.INFO,
                    "GOALS_BELOW_THRESHOLD",
                    f"{len(low_score_goals)} goals have SMART scores below threshold"
                )

            self.logger.info(f"Generated {len(goals)} goals across {len(goals_by_pillar)} pillars")

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.ERROR,
                "GOAL_GENERATION_FAILED",
                f"Failed to generate goals: {str(e)}"
            )
            self.logger.error(f"Goal generation failed: {e}")

        return state
