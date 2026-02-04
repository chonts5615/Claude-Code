"""Risk Assessor Agent - Identifies and assesses strategic risks."""

from typing import List, Dict, Any
import uuid

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase
from src.schemas.strategy import RiskAssessment, RiskCategory, RiskSeverity, RiskAnalysisOutput


class RiskAssessorAgent(BaseAgent[RiskAnalysisOutput]):
    """
    Agent that identifies and assesses strategic risks.

    Responsibilities:
    - Identify risks across all categories
    - Assess likelihood and impact
    - Develop mitigation strategies
    - Create contingency plans
    - Track risk coverage
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="S6_RiskAssessor",
            step_name="Risk Assessment",
            phase=WorkflowPhase.PLANNING,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are an expert in strategic risk management and assessment.

Your task is to identify, assess, and develop mitigation strategies for strategic risks.

**Risk Categories:**
- **Market**: Market changes, competition, customer shifts
- **Operational**: Execution risks, process failures, capacity
- **Financial**: Funding, cash flow, cost overruns
- **Regulatory**: Compliance, legal, policy changes
- **Technology**: Technical failures, obsolescence, integration
- **Talent**: Skills gaps, retention, succession
- **Reputation**: Brand, public perception, stakeholder trust
- **Strategic**: Strategy misalignment, scope, timing

**Risk Assessment Framework:**
1. **Identification**: What could go wrong?
2. **Likelihood**: Probability of occurrence (0-1)
3. **Impact**: Severity if it occurs (0-1)
4. **Risk Score**: Likelihood × Impact
5. **Triggers**: What would cause this risk to materialize?
6. **Mitigation**: Actions to reduce likelihood or impact
7. **Contingency**: Plan if risk materializes
8. **Residual Risk**: Remaining risk after mitigation

**Risk Severity Classification:**
- Critical: Risk score > 0.64 (high likelihood, high impact)
- High: Risk score 0.36-0.64
- Medium: Risk score 0.16-0.36
- Low: Risk score < 0.16

For each identified risk, provide comprehensive assessment and actionable mitigation."""

    def get_required_inputs(self) -> list[str]:
        return ["strategic_goals", "initiatives", "swot_analysis"]

    def get_output_keys(self) -> list[str]:
        return ["risks", "risk_matrix", "critical_risks", "mitigation_coverage"]

    def validate_inputs(self, state: RunState) -> bool:
        return "initiatives" in state.working_data and len(state.working_data["initiatives"]) > 0

    def execute(self, state: RunState) -> RunState:
        """Assess strategic risks."""

        goals = state.working_data.get("strategic_goals", [])
        initiatives = state.working_data.get("initiatives", [])
        swot = state.working_data.get("swot_analysis", {})
        context = state.working_data.get("context_summary", {})

        user_prompt = f"""Perform a comprehensive strategic risk assessment.

## Strategic Goals
{goals}

## Initiatives
{initiatives}

## SWOT Analysis
{swot}

## Context Summary
{context}

Identify and assess risks across all categories. For each risk provide:

- risk_id (format: RISK_001)
- name (concise risk name)
- description (detailed description of the risk)
- category (market, operational, financial, regulatory, technology, talent, reputation, strategic)
- severity (low, medium, high, critical - based on risk score)
- likelihood (0-1 probability)
- impact (0-1 severity)
- risk_score (likelihood × impact)
- triggers (list of what could cause this risk)
- affected_goals (list of goal_ids affected)
- affected_initiatives (list of initiative_ids affected)
- mitigation_strategy (overall approach)
- mitigation_actions (specific actions to take)
- contingency_plan (what to do if risk materializes)
- residual_risk (0-1 risk remaining after mitigation)
- owner (recommended risk owner role)
- review_frequency (how often to review)

Return as valid JSON:
{{
    "risks": [
        {{
            "risk_id": "RISK_001",
            "name": "...",
            "description": "...",
            "category": "market",
            "severity": "high",
            "likelihood": 0.6,
            "impact": 0.8,
            "risk_score": 0.48,
            "triggers": ["..."],
            "affected_goals": ["GOAL_PIL001_001"],
            "affected_initiatives": ["INIT_GOAL001_001"],
            "mitigation_strategy": "...",
            "mitigation_actions": ["..."],
            "contingency_plan": "...",
            "residual_risk": 0.15,
            "owner": "CRO",
            "review_frequency": "monthly"
        }}
    ],
    "risk_matrix": {{
        "critical": ["RISK_001"],
        "high": ["RISK_002", "RISK_003"],
        "medium": ["RISK_004"],
        "low": ["RISK_005"]
    }},
    "risks_by_category": {{
        "market": ["RISK_001"],
        "operational": ["RISK_002"]
    }},
    "mitigation_summary": {{
        "total_risks": 10,
        "risks_with_mitigation": 10,
        "mitigation_coverage": 1.0,
        "average_residual_risk": 0.18,
        "top_residual_risks": ["RISK_001"]
    }},
    "risk_recommendations": [
        "Key recommendation 1...",
        "Key recommendation 2..."
    ]
}}"""

        system_prompt = self.get_prompt_with_learnings(state)
        response = self.invoke_llm(user_prompt, system_prompt)

        try:
            result = self.extract_json_from_response(response)

            # Convert to RiskAssessment objects
            risks = []
            for r in result.get("risks", []):
                risk = RiskAssessment(
                    risk_id=r.get("risk_id", f"RISK_{uuid.uuid4().hex[:6]}"),
                    name=r.get("name", ""),
                    description=r.get("description", ""),
                    category=RiskCategory(r.get("category", "strategic")),
                    severity=RiskSeverity(r.get("severity", "medium")),
                    likelihood=r.get("likelihood", 0.5),
                    impact=r.get("impact", 0.5),
                    risk_score=r.get("risk_score", 0.25),
                    triggers=r.get("triggers", []),
                    affected_goals=r.get("affected_goals", []),
                    affected_initiatives=r.get("affected_initiatives", []),
                    mitigation_strategy=r.get("mitigation_strategy"),
                    mitigation_actions=r.get("mitigation_actions", []),
                    contingency_plan=r.get("contingency_plan"),
                    residual_risk=r.get("residual_risk"),
                    owner=r.get("owner"),
                    status="identified",
                )
                risks.append(risk)

            # Store results
            state.working_data["risks"] = [r.model_dump() for r in risks]
            state.working_data["risk_matrix"] = result.get("risk_matrix", {})
            state.working_data["risks_by_category"] = result.get("risks_by_category", {})
            state.working_data["mitigation_summary"] = result.get("mitigation_summary", {})
            state.working_data["risk_recommendations"] = result.get("risk_recommendations", [])

            # Validate risk assessment
            risk_matrix = result.get("risk_matrix", {})
            critical_risks = risk_matrix.get("critical", [])
            thresholds = state.config.thresholds

            if len(critical_risks) > thresholds.max_critical_risks:
                self.add_flag(
                    state,
                    SeverityLevel.ERROR,
                    "TOO_MANY_CRITICAL_RISKS",
                    f"{len(critical_risks)} critical risks identified (max: {thresholds.max_critical_risks})"
                )
            elif critical_risks:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "CRITICAL_RISKS_PRESENT",
                    f"{len(critical_risks)} critical risks require immediate attention"
                )

            # Check mitigation coverage
            mitigation_summary = result.get("mitigation_summary", {})
            coverage = mitigation_summary.get("mitigation_coverage", 0)
            if coverage < thresholds.risk_mitigation_coverage:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "LOW_MITIGATION_COVERAGE",
                    f"Mitigation coverage ({coverage:.0%}) below threshold ({thresholds.risk_mitigation_coverage:.0%})"
                )

            # Store critical risks for easy access
            state.working_data["critical_risks"] = critical_risks

            self.logger.info(f"Assessed {len(risks)} risks, {len(critical_risks)} critical")

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.ERROR,
                "RISK_ASSESSMENT_FAILED",
                f"Failed to assess risks: {str(e)}"
            )
            self.logger.error(f"Risk assessment failed: {e}")

        return state
