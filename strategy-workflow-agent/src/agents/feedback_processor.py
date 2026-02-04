"""Feedback Processor Agent - Processes feedback and extracts learning insights."""

from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase
from src.schemas.feedback import (
    FeedbackEntry, FeedbackType, FeedbackSentiment, LearningCategory,
    LearningInsight, FeedbackLoopState, FeedbackSummary
)


class FeedbackProcessorAgent(BaseAgent):
    """
    Agent that processes feedback and extracts learning insights.

    This is a core component of the learning feedback loop that:
    - Collects feedback from multiple sources
    - Analyzes patterns in feedback
    - Extracts actionable insights
    - Prepares data for optimization

    Responsibilities:
    - Process user feedback (ratings, comments, corrections)
    - Analyze quality metrics from runs
    - Track outcome data
    - Identify patterns and themes
    - Generate learning insights
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="F1_FeedbackProcessor",
            step_name="Feedback Processing",
            phase=WorkflowPhase.FEEDBACK,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are an expert in feedback analysis and organizational learning.

Your task is to process feedback from multiple sources and extract actionable learning insights.

**Feedback Sources:**
1. User feedback (ratings, comments, corrections)
2. Quality metrics from workflow execution
3. Outcome tracking data
4. Execution performance metrics

**Analysis Goals:**
1. Identify patterns across feedback
2. Extract root causes of issues
3. Recognize successful patterns to reinforce
4. Generate specific, actionable insights
5. Prioritize by impact and confidence

**Learning Categories:**
- Process: Workflow and execution improvements
- Quality: Output quality enhancements
- Content: Strategy content improvements
- Timing: Timeline and scheduling insights
- Resource: Resource allocation learnings
- Risk: Risk identification and mitigation
- Stakeholder: Communication and engagement
- Communication: Presentation and documentation

**Insight Requirements:**
- Supported by specific evidence (feedback entries)
- Confidence score based on sample size and consistency
- Specific affected agents/steps identified
- Clear recommended actions
- Impact assessment

Generate insights that can be directly used to improve the workflow."""

    def get_required_inputs(self) -> list[str]:
        return []  # Can work with any available feedback

    def get_output_keys(self) -> list[str]:
        return ["feedback_summary", "learning_insights", "feedback_loop_state"]

    def execute(self, state: RunState) -> RunState:
        """Process feedback and extract insights."""

        # Gather all feedback sources
        feedback_entries = self._collect_feedback(state)

        if not feedback_entries:
            self.logger.info("No feedback to process")
            state.working_data["feedback_summary"] = {"total_feedback": 0}
            return state

        # Prepare feedback for analysis
        feedback_text = self._format_feedback_for_analysis(feedback_entries)

        user_prompt = f"""Analyze the following feedback and extract learning insights.

## Feedback Entries ({len(feedback_entries)} total)
{feedback_text}

## Current Run Quality Scores
{state.working_data.get('quality_scores', {})}

## Run Flags (issues identified)
{[{'severity': f.severity.value, 'type': f.flag_type, 'message': f.message} for f in state.flags[:20]]}

## Previous Learning Context
{state.learning_context}

Analyze this feedback and:
1. Identify patterns and themes
2. Extract root causes of issues
3. Recognize successful patterns
4. Generate specific learning insights
5. Recommend improvements

Return as valid JSON:
{{
    "feedback_analysis": {{
        "total_entries_analyzed": {len(feedback_entries)},
        "positive_patterns": [
            {{
                "pattern": "...",
                "frequency": 0.8,
                "affected_areas": ["S3_PillarSynthesizer"],
                "evidence": ["feedback_id_1", "feedback_id_2"]
            }}
        ],
        "negative_patterns": [
            {{
                "pattern": "...",
                "frequency": 0.3,
                "affected_areas": ["S4_GoalGenerator"],
                "root_cause": "...",
                "evidence": ["feedback_id_3"]
            }}
        ],
        "theme_distribution": {{
            "quality": 0.4,
            "process": 0.3,
            "content": 0.2,
            "timing": 0.1
        }}
    }},
    "learning_insights": [
        {{
            "insight_id": "INS_001",
            "category": "quality",
            "importance": 0.85,
            "title": "Improve SMART Goal Specificity",
            "description": "Goals generated often lack specific measurable targets...",
            "pattern_type": "quality_gap",
            "affected_agents": ["S4_GoalGenerator"],
            "affected_steps": ["Goal Generation"],
            "evidence": ["FB_001", "FB_003", "FB_007"],
            "sample_size": 3,
            "confidence": 0.82,
            "frequency": 0.45,
            "impact": 0.7,
            "is_actionable": true,
            "recommended_actions": [
                "Add explicit prompt guidance for numeric targets",
                "Include examples of well-formed SMART goals",
                "Add validation check for measurability"
            ]
        }}
    ],
    "feedback_summary": {{
        "total_feedback": {len(feedback_entries)},
        "positive_feedback": 0,
        "negative_feedback": 0,
        "neutral_feedback": 0,
        "average_rating": null,
        "positive_themes": ["..."],
        "improvement_areas": ["..."],
        "corrections_made": 0,
        "suggestions_received": 0
    }},
    "optimization_triggers": [
        {{
            "trigger_type": "threshold_violation",
            "metric": "goal_smart_score",
            "current_value": 0.72,
            "threshold": 0.8,
            "recommended_action": "Adjust goal generation prompt"
        }}
    ]
}}"""

        system_prompt = self.get_system_prompt()
        response = self.invoke_llm(user_prompt, system_prompt)

        try:
            result = self.extract_json_from_response(response)

            # Process learning insights
            insights = []
            for i in result.get("learning_insights", []):
                insight = LearningInsight(
                    insight_id=i.get("insight_id", f"INS_{uuid.uuid4().hex[:6]}"),
                    category=LearningCategory(i.get("category", "process")),
                    importance=i.get("importance", 0.5),
                    title=i.get("title", ""),
                    description=i.get("description", ""),
                    evidence=i.get("evidence", []),
                    sample_size=i.get("sample_size", 1),
                    pattern_type=i.get("pattern_type", ""),
                    affected_agents=i.get("affected_agents", []),
                    affected_steps=i.get("affected_steps", []),
                    confidence=i.get("confidence", 0.5),
                    frequency=i.get("frequency", 0),
                    impact=i.get("impact", 0),
                    is_actionable=i.get("is_actionable", True),
                    recommended_actions=i.get("recommended_actions", []),
                    status="new",
                )
                insights.append(insight)

            # Store results
            state.working_data["feedback_analysis"] = result.get("feedback_analysis", {})
            state.working_data["learning_insights"] = [i.model_dump() for i in insights]
            state.working_data["feedback_summary"] = result.get("feedback_summary", {})
            state.working_data["optimization_triggers"] = result.get("optimization_triggers", [])

            # Update feedback loop state
            self._update_feedback_loop_state(state, feedback_entries, insights)

            # Flag high-importance insights
            high_importance = [i for i in insights if i.importance > 0.8]
            if high_importance:
                self.add_flag(
                    state,
                    SeverityLevel.INFO,
                    "HIGH_IMPORTANCE_INSIGHTS",
                    f"Identified {len(high_importance)} high-importance learning insights"
                )

            self.logger.info(f"Processed {len(feedback_entries)} feedback entries, extracted {len(insights)} insights")

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.WARNING,
                "FEEDBACK_PROCESSING_ERROR",
                f"Error processing feedback: {str(e)}"
            )
            self.logger.error(f"Feedback processing failed: {e}")

        return state

    def _collect_feedback(self, state: RunState) -> List[Dict[str, Any]]:
        """Collect feedback from all available sources."""
        feedback = []

        # Collect from working data (if feedback was provided)
        user_feedback = state.working_data.get("user_feedback", [])
        feedback.extend(user_feedback)

        # Collect quality metrics as feedback
        quality_scores = state.working_data.get("quality_scores", {})
        if quality_scores:
            for metric, value in quality_scores.items():
                feedback.append({
                    "feedback_id": f"METRIC_{metric}",
                    "type": "quality_metric",
                    "category": "quality",
                    "metric": metric,
                    "value": value,
                    "sentiment": "positive" if value >= 0.8 else "neutral" if value >= 0.6 else "negative"
                })

        # Collect flags as feedback
        for flag in state.flags:
            feedback.append({
                "feedback_id": f"FLAG_{flag.step_id}_{flag.flag_type}",
                "type": "system_flag",
                "category": self._flag_to_category(flag.flag_type),
                "severity": flag.severity.value,
                "message": flag.message,
                "agent": flag.step_id,
                "sentiment": "negative" if flag.severity.value in ["ERROR", "CRITICAL"] else "neutral"
            })

        return feedback

    def _flag_to_category(self, flag_type: str) -> str:
        """Map flag type to learning category."""
        mappings = {
            "SMART": "quality",
            "ALIGNMENT": "quality",
            "COMPLETENESS": "quality",
            "COHERENCE": "quality",
            "RESOURCE": "resource",
            "TIMELINE": "timing",
            "RISK": "risk",
            "VALIDATION": "quality",
        }
        for key, category in mappings.items():
            if key in flag_type.upper():
                return category
        return "process"

    def _format_feedback_for_analysis(self, feedback: List[Dict[str, Any]]) -> str:
        """Format feedback entries for LLM analysis."""
        formatted = []
        for i, fb in enumerate(feedback[:50]):  # Limit to 50 for context size
            formatted.append(f"{i+1}. [{fb.get('type', 'unknown')}] {fb.get('sentiment', 'neutral')}: {fb}")
        return "\n".join(formatted)

    def _update_feedback_loop_state(
        self,
        state: RunState,
        feedback: List[Dict[str, Any]],
        insights: List[LearningInsight]
    ) -> None:
        """Update the feedback loop state."""
        # Get or create feedback loop state
        loop_state = state.working_data.get("feedback_loop_state", {})

        loop_state.update({
            "last_updated": datetime.utcnow().isoformat(),
            "total_feedback_entries": loop_state.get("total_feedback_entries", 0) + len(feedback),
            "total_insights": loop_state.get("total_insights", 0) + len(insights),
            "active_insights": len([i for i in insights if i.status == "new"]),
            "recent_insight_ids": [i.insight_id for i in insights],
        })

        # Track by category
        insights_by_category = loop_state.get("insights_by_category", {})
        for insight in insights:
            cat = insight.category.value
            insights_by_category[cat] = insights_by_category.get(cat, 0) + 1
        loop_state["insights_by_category"] = insights_by_category

        state.working_data["feedback_loop_state"] = loop_state
