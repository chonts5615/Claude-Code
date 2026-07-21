"""Learning Optimizer Agent - Applies learnings to optimize the workflow."""

from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase
from src.schemas.feedback import (
    LearningInsight, OptimizationRecommendation, OptimizationType, LearningCategory
)


class LearningOptimizerAgent(BaseAgent):
    """
    Agent that applies learnings to optimize the workflow.

    This is the second core component of the learning feedback loop that:
    - Analyzes learning insights
    - Generates optimization recommendations
    - Applies approved optimizations
    - Tracks optimization effectiveness

    Responsibilities:
    - Convert insights to specific optimizations
    - Validate optimization safety
    - Apply threshold adjustments
    - Generate prompt refinements
    - Update agent configurations
    - Track optimization history and effectiveness
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="F2_LearningOptimizer",
            step_name="Learning Optimization",
            phase=WorkflowPhase.FEEDBACK,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are an expert in machine learning optimization and continuous improvement.

Your task is to convert learning insights into specific, safe optimizations that improve workflow quality.

**Optimization Types:**
1. **Threshold Adjustment**: Modify quality gate thresholds
2. **Prompt Refinement**: Improve agent prompts based on learnings
3. **Weight Tuning**: Adjust scoring/ranking weights
4. **Process Improvement**: Modify workflow steps or sequencing
5. **Template Update**: Improve output templates
6. **Rule Addition**: Add new validation rules
7. **Rule Removal**: Remove ineffective rules

**Optimization Principles:**
- Safety first: Changes should not break existing functionality
- Incremental: Make small, measurable changes
- Reversible: All changes should be rollbackable
- Evidence-based: Changes must be supported by data
- Conservative: Prefer smaller adjustments

**For each optimization:**
1. Clear specification of what to change
2. Current value and recommended value
3. Expected impact (quantified if possible)
4. Confidence level
5. Risk assessment
6. Implementation steps
7. Rollback procedure

Generate optimizations that are specific, safe, and impactful."""

    def get_required_inputs(self) -> list[str]:
        return ["learning_insights"]

    def get_output_keys(self) -> list[str]:
        return ["optimization_recommendations", "applied_optimizations", "learning_context_updates"]

    def execute(self, state: RunState) -> RunState:
        """Generate and apply optimizations based on learning insights."""

        insights = state.working_data.get("learning_insights", [])
        feedback_config = state.config.feedback

        if not insights:
            self.logger.info("No learning insights to process")
            return state

        if not feedback_config.enabled:
            self.logger.info("Feedback loop disabled")
            return state

        # Filter to actionable insights with sufficient confidence
        actionable_insights = [
            i for i in insights
            if i.get("is_actionable", True) and
            i.get("confidence", 0) >= feedback_config.learning_confidence_min
        ]

        if not actionable_insights:
            self.logger.info("No actionable insights meeting confidence threshold")
            return state

        user_prompt = f"""Generate optimization recommendations based on the following learning insights.

## Learning Insights ({len(actionable_insights)} actionable)
{actionable_insights}

## Current Configuration
Thresholds:
{state.config.thresholds.model_dump()}

Feedback Configuration:
- Learning rate: {feedback_config.learning_rate}
- Auto-optimize: {feedback_config.auto_optimize}
- Min improvement threshold: {feedback_config.min_improvement_threshold}

## Optimization History (from learning context)
{state.learning_context}

## Constraints
- Make conservative adjustments (max 10-15% change per optimization)
- Prefer threshold adjustments and prompt refinements
- Avoid changes that could cause failures
- All changes must be reversible

Generate specific optimizations for each actionable insight:

Return as valid JSON:
{{
    "optimization_recommendations": [
        {{
            "optimization_id": "OPT_001",
            "insight_id": "INS_001",
            "optimization_type": "threshold_adjustment",
            "target_component": "config.thresholds.goal_smart_score_min",
            "category": "quality",
            "title": "Increase SMART score threshold",
            "description": "Raise minimum SMART score to improve goal quality",
            "rationale": "Analysis shows goals with higher SMART scores lead to better outcomes",
            "current_value": 0.7,
            "recommended_value": 0.75,
            "change_specification": {{
                "path": "config.thresholds.goal_smart_score_min",
                "from": 0.7,
                "to": 0.75
            }},
            "expected_impact": 0.15,
            "confidence": 0.8,
            "risk_level": "low",
            "implementation_steps": [
                "Update threshold in configuration",
                "Monitor goal generation for increased rejections",
                "Track quality improvement"
            ],
            "rollback_steps": [
                "Revert threshold to 0.7",
                "Clear any cached configurations"
            ],
            "effectiveness_metric": "average_goal_quality_score",
            "measurement_period_days": 30
        }},
        {{
            "optimization_id": "OPT_002",
            "insight_id": "INS_001",
            "optimization_type": "prompt_refinement",
            "target_component": "agents.S4_GoalGenerator.system_prompt",
            "category": "quality",
            "title": "Add SMART goal examples to prompt",
            "description": "Include concrete examples of well-formed SMART goals",
            "rationale": "Examples improve LLM output consistency",
            "current_value": null,
            "recommended_value": "Additional prompt guidance with examples",
            "change_specification": {{
                "agent_id": "S4_GoalGenerator",
                "prompt_additions": [
                    "Always include specific numeric targets for each goal",
                    "Example of a well-formed SMART goal: 'Increase customer retention rate from 72% to 85% by Q4 2025 through implementation of loyalty program'"
                ]
            }},
            "expected_impact": 0.2,
            "confidence": 0.75,
            "risk_level": "low",
            "implementation_steps": [
                "Add examples to learning context",
                "Update prompt with additional guidance"
            ],
            "rollback_steps": [
                "Remove prompt additions from learning context"
            ],
            "effectiveness_metric": "goal_specificity_score",
            "measurement_period_days": 14
        }}
    ],
    "optimization_priority": ["OPT_002", "OPT_001"],
    "auto_apply_candidates": ["OPT_001"],
    "require_approval": ["OPT_002"],
    "risk_assessment": {{
        "overall_risk": "low",
        "max_impact_if_failure": "minor quality degradation",
        "combined_expected_improvement": 0.25
    }}
}}"""

        system_prompt = self.get_system_prompt()
        response = self.invoke_llm(user_prompt, system_prompt)

        try:
            result = self.extract_json_from_response(response)

            # Convert to OptimizationRecommendation objects
            recommendations = []
            for o in result.get("optimization_recommendations", []):
                recommendation = OptimizationRecommendation(
                    optimization_id=o.get("optimization_id", f"OPT_{uuid.uuid4().hex[:6]}"),
                    insight_id=o.get("insight_id", ""),
                    insight_ids=[o.get("insight_id", "")],
                    optimization_type=OptimizationType(o.get("optimization_type", "threshold_adjustment")),
                    target_component=o.get("target_component", ""),
                    category=LearningCategory(o.get("category", "process")),
                    title=o.get("title", ""),
                    description=o.get("description", ""),
                    rationale=o.get("rationale", ""),
                    current_value=o.get("current_value"),
                    recommended_value=o.get("recommended_value"),
                    change_specification=o.get("change_specification", {}),
                    expected_impact=o.get("expected_impact", 0),
                    confidence=o.get("confidence", 0.5),
                    risk_level=o.get("risk_level", "medium"),
                    implementation_steps=o.get("implementation_steps", []),
                    rollback_steps=o.get("rollback_steps", []),
                    status="proposed",
                )
                recommendations.append(recommendation)

            # Store recommendations
            state.working_data["optimization_recommendations"] = [r.model_dump() for r in recommendations]
            state.working_data["optimization_priority"] = result.get("optimization_priority", [])
            state.working_data["risk_assessment"] = result.get("risk_assessment", {})

            # Auto-apply if enabled and candidates identified
            applied = []
            if feedback_config.auto_optimize:
                auto_apply = result.get("auto_apply_candidates", [])
                for opt_id in auto_apply:
                    opt = next((r for r in recommendations if r.optimization_id == opt_id), None)
                    if opt and opt.risk_level == "low" and opt.expected_impact >= feedback_config.min_improvement_threshold:
                        self._apply_optimization(state, opt)
                        opt.status = "applied"
                        opt.applied_at = datetime.utcnow()
                        applied.append(opt_id)

            state.working_data["applied_optimizations"] = applied

            # Update learning context with prompt additions
            self._update_learning_context(state, recommendations)

            # Report on optimizations
            if recommendations:
                self.add_flag(
                    state,
                    SeverityLevel.INFO,
                    "OPTIMIZATIONS_GENERATED",
                    f"Generated {len(recommendations)} optimization recommendations, {len(applied)} auto-applied"
                )

            # Increment optimization round
            state.optimization_round += 1

            self.logger.info(
                f"Generated {len(recommendations)} optimizations, "
                f"auto-applied {len(applied)}"
            )

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.WARNING,
                "OPTIMIZATION_ERROR",
                f"Error generating optimizations: {str(e)}"
            )
            self.logger.error(f"Optimization failed: {e}")

        return state

    def _apply_optimization(self, state: RunState, opt: OptimizationRecommendation) -> bool:
        """Apply a specific optimization to the state/configuration."""
        try:
            if opt.optimization_type == OptimizationType.THRESHOLD_ADJUSTMENT:
                # Apply threshold change
                spec = opt.change_specification
                path = spec.get("path", "")
                new_value = spec.get("to")

                if path.startswith("config.thresholds."):
                    threshold_name = path.split(".")[-1]
                    if hasattr(state.config.thresholds, threshold_name):
                        setattr(state.config.thresholds, threshold_name, new_value)
                        self.logger.info(f"Applied threshold adjustment: {threshold_name} = {new_value}")
                        return True

            elif opt.optimization_type == OptimizationType.PROMPT_REFINEMENT:
                # Store prompt additions in learning context
                spec = opt.change_specification
                agent_id = spec.get("agent_id", "")
                additions = spec.get("prompt_additions", [])

                if agent_id and additions:
                    if agent_id not in state.learning_context:
                        state.learning_context[agent_id] = {}
                    existing = state.learning_context[agent_id].get("prompt_additions", [])
                    state.learning_context[agent_id]["prompt_additions"] = existing + additions
                    self.logger.info(f"Applied prompt refinement for {agent_id}")
                    return True

            elif opt.optimization_type == OptimizationType.WEIGHT_TUNING:
                # Store weight adjustments
                spec = opt.change_specification
                # Would apply to specific agent configurations
                self.logger.info(f"Weight tuning stored for future application")
                return True

            return False

        except Exception as e:
            self.logger.error(f"Failed to apply optimization {opt.optimization_id}: {e}")
            return False

    def _update_learning_context(
        self,
        state: RunState,
        recommendations: List[OptimizationRecommendation]
    ) -> None:
        """Update the learning context with optimization information."""
        # Track optimization history
        history = state.learning_context.get("optimization_history", [])
        for opt in recommendations:
            history.append({
                "optimization_id": opt.optimization_id,
                "type": opt.optimization_type.value,
                "target": opt.target_component,
                "status": opt.status,
                "timestamp": datetime.utcnow().isoformat(),
                "expected_impact": opt.expected_impact,
            })

        # Keep last 100 optimizations
        state.learning_context["optimization_history"] = history[-100:]

        # Track overall learning metrics
        state.learning_context["total_optimizations"] = len(history)
        state.learning_context["last_optimization_run"] = datetime.utcnow().isoformat()

        # Mark feedback as applied
        state.feedback_applied = True
