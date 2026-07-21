"""Quality gates for workflow validation."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel

from src.schemas.run_state import RunState, SeverityLevel, ThresholdConfig


class ValidationResult(BaseModel):
    """Result of a validation check."""
    rule_name: str
    passed: bool
    severity: str  # INFO, WARNING, ERROR, CRITICAL
    message: str
    metadata: Dict[str, Any] = {}
    blocking: bool = False


class QualityGate:
    """Quality gate validator for workflow steps."""

    def __init__(self, gate_id: str, thresholds: ThresholdConfig):
        self.gate_id = gate_id
        self.thresholds = thresholds

    def validate_vision_extraction(self, state: RunState) -> List[ValidationResult]:
        """Validate vision extraction output."""
        results = []

        vision = state.working_data.get("vision", {})
        confidence = state.working_data.get("vision_extraction_confidence", 0)

        # Check vision statement exists
        if not vision.get("vision_statement"):
            results.append(ValidationResult(
                rule_name="vision_statement_required",
                passed=False,
                severity="ERROR",
                message="Vision statement is required but not extracted",
                blocking=True
            ))
        else:
            results.append(ValidationResult(
                rule_name="vision_statement_required",
                passed=True,
                severity="INFO",
                message="Vision statement extracted successfully"
            ))

        # Check extraction confidence
        if confidence < 0.5:
            results.append(ValidationResult(
                rule_name="extraction_confidence",
                passed=False,
                severity="WARNING",
                message=f"Low extraction confidence ({confidence:.2f})",
                metadata={"confidence": confidence}
            ))

        return results

    def validate_pillar_synthesis(self, state: RunState) -> List[ValidationResult]:
        """Validate pillar synthesis output."""
        results = []

        pillars = state.working_data.get("strategic_pillars", [])

        # Check pillar count
        if len(pillars) < 2:
            results.append(ValidationResult(
                rule_name="min_pillars",
                passed=False,
                severity="ERROR",
                message=f"At least 2 strategic pillars required, found {len(pillars)}",
                blocking=True
            ))
        elif len(pillars) > 6:
            results.append(ValidationResult(
                rule_name="max_pillars",
                passed=False,
                severity="WARNING",
                message=f"More than 6 pillars may reduce focus, found {len(pillars)}"
            ))
        else:
            results.append(ValidationResult(
                rule_name="pillar_count",
                passed=True,
                severity="INFO",
                message=f"Synthesized {len(pillars)} strategic pillars"
            ))

        return results

    def validate_goal_generation(self, state: RunState) -> List[ValidationResult]:
        """Validate goal generation output."""
        results = []

        goals = state.working_data.get("strategic_goals", [])
        goals_by_pillar = state.working_data.get("goals_by_pillar", {})
        quality_summary = state.working_data.get("goal_quality_summary", {})

        # Check total goals
        if len(goals) == 0:
            results.append(ValidationResult(
                rule_name="goals_required",
                passed=False,
                severity="CRITICAL",
                message="No strategic goals generated",
                blocking=True
            ))
            return results

        # Check goals per pillar
        for pillar_id, pillar_goals in goals_by_pillar.items():
            if len(pillar_goals) < self.thresholds.min_goals_per_pillar:
                results.append(ValidationResult(
                    rule_name="min_goals_per_pillar",
                    passed=False,
                    severity="WARNING",
                    message=f"Pillar {pillar_id} has {len(pillar_goals)} goals (min: {self.thresholds.min_goals_per_pillar})",
                    metadata={"pillar_id": pillar_id, "goal_count": len(pillar_goals)}
                ))

        # Check SMART score
        avg_smart = quality_summary.get("average_smart_score", 0)
        if avg_smart < self.thresholds.goal_smart_score_min:
            results.append(ValidationResult(
                rule_name="smart_score_threshold",
                passed=False,
                severity="WARNING",
                message=f"Average SMART score ({avg_smart:.2f}) below threshold ({self.thresholds.goal_smart_score_min})",
                metadata={"average_smart_score": avg_smart}
            ))
        else:
            results.append(ValidationResult(
                rule_name="smart_score_threshold",
                passed=True,
                severity="INFO",
                message=f"SMART score meets threshold ({avg_smart:.2f})"
            ))

        return results

    def validate_initiative_design(self, state: RunState) -> List[ValidationResult]:
        """Validate initiative design output."""
        results = []

        initiatives = state.working_data.get("initiatives", [])

        if len(initiatives) == 0:
            results.append(ValidationResult(
                rule_name="initiatives_required",
                passed=False,
                severity="CRITICAL",
                message="No initiatives designed",
                blocking=True
            ))
            return results

        # Check feasibility scores
        low_feasibility = [
            i for i in initiatives
            if i.get("feasibility_score", 1) < self.thresholds.initiative_feasibility_min
        ]
        if low_feasibility:
            results.append(ValidationResult(
                rule_name="initiative_feasibility",
                passed=False,
                severity="WARNING",
                message=f"{len(low_feasibility)} initiatives have low feasibility scores",
                metadata={"count": len(low_feasibility)}
            ))

        results.append(ValidationResult(
            rule_name="initiatives_generated",
            passed=True,
            severity="INFO",
            message=f"Designed {len(initiatives)} strategic initiatives"
        ))

        return results

    def validate_risk_assessment(self, state: RunState) -> List[ValidationResult]:
        """Validate risk assessment output."""
        results = []

        risks = state.working_data.get("risks", [])
        critical_risks = state.working_data.get("critical_risks", [])
        mitigation_summary = state.working_data.get("mitigation_summary", {})

        # Check critical risk count
        if len(critical_risks) > self.thresholds.max_critical_risks:
            results.append(ValidationResult(
                rule_name="max_critical_risks",
                passed=False,
                severity="ERROR",
                message=f"Too many critical risks ({len(critical_risks)}) - max {self.thresholds.max_critical_risks}",
                metadata={"critical_count": len(critical_risks)}
            ))

        # Check mitigation coverage
        coverage = mitigation_summary.get("mitigation_coverage", 0)
        if coverage < self.thresholds.risk_mitigation_coverage:
            results.append(ValidationResult(
                rule_name="mitigation_coverage",
                passed=False,
                severity="WARNING",
                message=f"Mitigation coverage ({coverage:.0%}) below threshold ({self.thresholds.risk_mitigation_coverage:.0%})",
                metadata={"coverage": coverage}
            ))
        else:
            results.append(ValidationResult(
                rule_name="mitigation_coverage",
                passed=True,
                severity="INFO",
                message=f"Risk mitigation coverage adequate ({coverage:.0%})"
            ))

        return results

    def validate_strategy_quality(self, state: RunState) -> List[ValidationResult]:
        """Validate overall strategy quality."""
        results = []

        quality_scores = state.working_data.get("quality_scores", {})

        # Alignment score
        alignment = quality_scores.get("alignment_score", 0)
        if alignment < self.thresholds.alignment_score_min:
            results.append(ValidationResult(
                rule_name="alignment_score",
                passed=False,
                severity="ERROR",
                message=f"Alignment score ({alignment:.2f}) below threshold ({self.thresholds.alignment_score_min})",
                blocking=state.config.strict_mode if hasattr(state, 'config') else False
            ))

        # Coherence score
        coherence = quality_scores.get("coherence_score", 0)
        if coherence < self.thresholds.coherence_score_min:
            results.append(ValidationResult(
                rule_name="coherence_score",
                passed=False,
                severity="ERROR",
                message=f"Coherence score ({coherence:.2f}) below threshold ({self.thresholds.coherence_score_min})"
            ))

        # Completeness score
        completeness = quality_scores.get("completeness_score", 0)
        if completeness < self.thresholds.completeness_score_min:
            results.append(ValidationResult(
                rule_name="completeness_score",
                passed=False,
                severity="WARNING",
                message=f"Completeness score ({completeness:.2f}) below threshold ({self.thresholds.completeness_score_min})"
            ))

        # All passing
        if alignment >= self.thresholds.alignment_score_min and \
           coherence >= self.thresholds.coherence_score_min and \
           completeness >= self.thresholds.completeness_score_min:
            results.append(ValidationResult(
                rule_name="quality_threshold",
                passed=True,
                severity="INFO",
                message="Strategy meets all quality thresholds"
            ))

        return results


class GateResult(BaseModel):
    """Result of running a quality gate."""
    gate_id: str
    passed: bool
    blocking_failures: int
    warnings: int
    validation_results: List[ValidationResult]

    @property
    def should_continue(self) -> bool:
        """Whether workflow should continue after this gate."""
        return self.blocking_failures == 0
