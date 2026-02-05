"""Validator Agent - Validates strategy quality and completeness."""

from typing import List, Dict, Any

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase
from src.schemas.strategy import ValidationOutput


class ValidatorAgent(BaseAgent[ValidationOutput]):
    """
    Agent that validates strategy quality, alignment, and completeness.

    Responsibilities:
    - Validate strategic alignment (vision -> pillars -> goals -> initiatives)
    - Check completeness of all elements
    - Assess coherence and consistency
    - Verify feasibility
    - Generate quality scores
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="S9_Validator",
            step_name="Strategy Validation",
            phase=WorkflowPhase.VALIDATION,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are an expert strategy reviewer and quality assessor.

Your task is to validate the strategic plan for quality, alignment, and completeness.

**Validation Dimensions:**

1. **Alignment Score (0-1)**:
   - Vision -> Pillars alignment
   - Pillars -> Goals alignment
   - Goals -> Initiatives alignment
   - Overall strategic coherence

2. **Coherence Score (0-1)**:
   - Logical consistency between elements
   - No contradictory goals or initiatives
   - Dependencies make sense
   - Timing and sequencing logical

3. **Completeness Score (0-1)**:
   - All required elements present
   - Sufficient detail provided
   - Success criteria defined
   - Resources allocated
   - Risks identified and mitigated

4. **Feasibility Score (0-1)**:
   - Resource requirements realistic
   - Timelines achievable
   - Dependencies manageable
   - Risk level acceptable

**Validation Checks:**
- Each pillar has sufficient goals
- Each goal has initiatives to achieve it
- All initiatives have resources
- All critical risks have mitigation
- Timeline is achievable
- KPIs defined for measurement

Provide specific issues found and recommendations for improvement."""

    def get_required_inputs(self) -> list[str]:
        return ["vision", "strategic_pillars", "strategic_goals", "initiatives", "risks"]

    def get_output_keys(self) -> list[str]:
        return ["validation_result", "quality_scores", "validation_issues", "recommendations"]

    def validate_inputs(self, state: RunState) -> bool:
        required = ["vision", "strategic_pillars", "strategic_goals", "initiatives"]
        return all(key in state.working_data for key in required)

    def execute(self, state: RunState) -> RunState:
        """Validate the strategic plan."""

        vision = state.working_data.get("vision", {})
        pillars = state.working_data.get("strategic_pillars", [])
        goals = state.working_data.get("strategic_goals", [])
        initiatives = state.working_data.get("initiatives", [])
        risks = state.working_data.get("risks", [])
        milestones = state.working_data.get("milestones", [])
        resource_plan = state.working_data.get("resource_plan_summary", {})
        critical_path = state.working_data.get("critical_path", {})

        user_prompt = f"""Perform a comprehensive validation of the following strategic plan.

## Vision
{vision}

## Strategic Pillars ({len(pillars)} pillars)
{pillars}

## Strategic Goals ({len(goals)} goals)
{goals}

## Initiatives ({len(initiatives)} initiatives)
{initiatives}

## Risks ({len(risks)} risks)
{risks}

## Milestones ({len(milestones)} milestones)
{milestones}

## Resource Plan
{resource_plan}

## Critical Path
{critical_path}

## Validation Thresholds
- Minimum alignment score: {state.config.thresholds.alignment_score_min}
- Minimum coherence score: {state.config.thresholds.coherence_score_min}
- Minimum completeness score: {state.config.thresholds.completeness_score_min}

Validate and score the strategic plan. Return as valid JSON:
{{
    "is_valid": true,
    "overall_score": 0.85,
    "scores": {{
        "alignment_score": 0.88,
        "coherence_score": 0.85,
        "completeness_score": 0.82,
        "feasibility_score": 0.80
    }},
    "alignment_analysis": {{
        "vision_to_pillars": 0.90,
        "pillars_to_goals": 0.85,
        "goals_to_initiatives": 0.88,
        "gaps": ["Goal X lacks clear initiative coverage"]
    }},
    "coherence_analysis": {{
        "consistency_issues": [],
        "dependency_issues": [],
        "timing_issues": [],
        "contradictions": []
    }},
    "completeness_analysis": {{
        "missing_elements": ["KPIs for Goal Y"],
        "insufficient_detail": ["Initiative Z needs success criteria"],
        "unallocated_resources": [],
        "unmitigated_risks": []
    }},
    "feasibility_analysis": {{
        "resource_feasibility": 0.85,
        "timeline_feasibility": 0.80,
        "risk_feasibility": 0.75,
        "concerns": ["Q3 resource peak may be challenging"]
    }},
    "issues": [
        {{
            "severity": "warning",
            "category": "completeness",
            "element_id": "GOAL_PIL001_002",
            "issue": "No KPIs defined",
            "recommendation": "Add 2-3 measurable KPIs"
        }}
    ],
    "recommendations": [
        "Add KPIs for 3 goals that are missing measurement criteria",
        "Consider adding buffer to Q3 timeline due to resource constraints",
        "Review Risk_003 mitigation strategy - may be insufficient"
    ],
    "certification": {{
        "ready_for_approval": true,
        "blocking_issues": [],
        "conditional_issues": ["Pending KPI definition"],
        "reviewer_notes": "Overall solid strategic plan with minor gaps to address"
    }}
}}"""

        system_prompt = self.get_prompt_with_learnings(state)
        response = self.invoke_llm(user_prompt, system_prompt)

        try:
            result = self.extract_json_from_response(response)

            # Store validation results
            state.working_data["validation_result"] = result
            state.working_data["quality_scores"] = result.get("scores", {})
            state.working_data["validation_issues"] = result.get("issues", [])
            state.working_data["validation_recommendations"] = result.get("recommendations", [])

            # Check scores against thresholds
            scores = result.get("scores", {})
            thresholds = state.config.thresholds

            if scores.get("alignment_score", 0) < thresholds.alignment_score_min:
                self.add_flag(
                    state,
                    SeverityLevel.ERROR,
                    "LOW_ALIGNMENT_SCORE",
                    f"Alignment score ({scores.get('alignment_score', 0):.2f}) below threshold ({thresholds.alignment_score_min})"
                )

            if scores.get("coherence_score", 0) < thresholds.coherence_score_min:
                self.add_flag(
                    state,
                    SeverityLevel.ERROR,
                    "LOW_COHERENCE_SCORE",
                    f"Coherence score ({scores.get('coherence_score', 0):.2f}) below threshold ({thresholds.coherence_score_min})"
                )

            if scores.get("completeness_score", 0) < thresholds.completeness_score_min:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "LOW_COMPLETENESS_SCORE",
                    f"Completeness score ({scores.get('completeness_score', 0):.2f}) below threshold ({thresholds.completeness_score_min})"
                )

            # Flag specific issues
            issues = result.get("issues", [])
            error_issues = [i for i in issues if i.get("severity") == "error"]
            if error_issues:
                self.add_flag(
                    state,
                    SeverityLevel.ERROR,
                    "VALIDATION_ERRORS",
                    f"Found {len(error_issues)} validation errors that must be resolved"
                )

            # Check if ready for approval
            certification = result.get("certification", {})
            if certification.get("ready_for_approval", False):
                self.add_flag(
                    state,
                    SeverityLevel.INFO,
                    "READY_FOR_APPROVAL",
                    "Strategic plan passes validation and is ready for approval"
                )
            else:
                blocking = certification.get("blocking_issues", [])
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "NOT_READY_FOR_APPROVAL",
                    f"Strategic plan has {len(blocking)} blocking issues"
                )

            # Update QA summary
            self._update_qa_summary(state, result)

            self.logger.info(
                f"Validation complete: overall score {result.get('overall_score', 0):.2f}, "
                f"ready={certification.get('ready_for_approval', False)}"
            )

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.ERROR,
                "VALIDATION_FAILED",
                f"Failed to validate strategy: {str(e)}"
            )
            self.logger.error(f"Validation failed: {e}")

        return state

    def _update_qa_summary(self, state: RunState, validation_result: Dict[str, Any]) -> None:
        """Update QA summary with validation results."""
        from src.schemas.run_state import QASummary

        scores = validation_result.get("scores", {})

        # Count elements
        pillars = state.working_data.get("strategic_pillars", [])
        goals = state.working_data.get("strategic_goals", [])
        initiatives = state.working_data.get("initiatives", [])
        milestones = state.working_data.get("milestones", [])
        risks = state.working_data.get("risks", [])

        # Count flags by severity
        flags_by_severity = {}
        for flag in state.flags:
            severity = flag.severity.value
            flags_by_severity[severity] = flags_by_severity.get(severity, 0) + 1

        # Unresolved issues
        unresolved = [
            f.message for f in state.flags
            if not f.resolved and f.severity in [SeverityLevel.ERROR, SeverityLevel.CRITICAL]
        ]

        state.qa_summary = QASummary(
            total_goals_defined=len(goals),
            total_initiatives_defined=len(initiatives),
            total_milestones_defined=len(milestones),
            total_kpis_defined=0,  # Would need to count from goals/initiatives
            alignment_score=scores.get("alignment_score", 0),
            coherence_score=scores.get("coherence_score", 0),
            completeness_score=scores.get("completeness_score", 0),
            feasibility_score=scores.get("feasibility_score", 0),
            smart_compliance_score=state.working_data.get("goal_quality_summary", {}).get("average_smart_score", 0),
            risks_identified=len(risks),
            risks_mitigated=len([r for r in risks if r.get("mitigation_strategy")]),
            critical_risks_remaining=len(state.working_data.get("critical_risks", [])),
            flags_by_severity=flags_by_severity,
            unresolved_issues=unresolved[:10],  # Limit to top 10
        )
