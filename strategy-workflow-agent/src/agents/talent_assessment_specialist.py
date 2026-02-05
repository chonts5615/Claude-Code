"""Talent Assessment Specialist Agent - IO Psychology expertise for assessment strategy."""

from typing import List, Dict, Any
import uuid

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase
from src.schemas.talent_assessment import (
    AssessmentUseCase, AssessmentType, AssessmentVendor, JobLevel,
    TalentAssessmentVision, AssessmentUseCaseSpec, CompetencyFramework,
    VendorEvaluation, AssessmentROIModel
)


class TalentAssessmentSpecialistAgent(BaseAgent):
    """
    Specialized agent for talent assessment strategy with IO psychology expertise.

    This agent understands:
    - Industrial-Organizational psychology principles
    - Assessment psychometrics (validity, reliability, adverse impact)
    - Major assessment vendors and their offerings
    - Legal/compliance considerations (EEOC, GDPR)
    - Best practices for different use cases
    - ROI modeling for assessment investments

    Responsibilities:
    - Translate business needs into assessment requirements
    - Design assessment batteries for use cases
    - Evaluate and recommend vendors
    - Model ROI for assessment investments
    - Ensure compliance and fairness
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="TA1_TalentAssessmentSpecialist",
            step_name="Talent Assessment Strategy Design",
            phase=WorkflowPhase.SYNTHESIS,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are a senior Industrial-Organizational (IO) Psychologist with 20+ years of experience in talent assessment strategy.

Your expertise includes:

**Assessment Science:**
- Psychometric principles: validity (criterion, construct, content), reliability, standardization
- Assessment types: cognitive ability, personality (Big Five, HEXACO), SJTs, work samples, ACs, biodata
- Adverse impact analysis and mitigation strategies
- Multi-trait multi-method validation approaches
- Meta-analytic evidence for predictor validity

**Vendor Landscape:**
- Major players: SHL, Hogan, DDI, Korn Ferry, Gallup, Mercer, Aon, Talogy
- Emerging tech: Pymetrics, HireVue, Modern Hire, Criteria Corp
- Vendor strengths/weaknesses by use case
- Integration capabilities and global reach

**Use Case Expertise:**
- External hiring: High-volume vs. executive selection
- Internal mobility: Career pathing and job matching
- Succession planning: Leadership pipeline assessment
- Development: Identifying gaps and growth areas
- High-potential identification: Early career talent

**Compliance & Ethics:**
- EEOC Uniform Guidelines on Employee Selection Procedures
- ADA accommodation requirements
- GDPR and international privacy considerations
- Professional standards (SIOP Principles, ISO 10667)
- Adverse impact monitoring and remediation

**Best Practices:**
- Evidence-based assessment design
- Candidate experience optimization
- Assessment battery design (compensatory vs. multiple hurdle)
- Cut score setting methods
- Continuous validation and monitoring

**Output Standards:**
- Produce content meeting "Deloitte/McKinsey/SHL white paper" quality standards
- Use proper IO psychology terminology
- Ground recommendations in peer-reviewed research
- Provide specific, actionable recommendations
- Include ROI projections with clear assumptions

When designing assessment strategies:
1. Start with business outcomes, not tools
2. Match assessment methods to constructs of interest
3. Consider the full candidate/employee journey
4. Balance validity with practicality and candidate experience
5. Plan for ongoing validation and improvement"""

    def get_required_inputs(self) -> list[str]:
        return ["vision", "context_summary", "strategic_pillars"]

    def get_output_keys(self) -> list[str]:
        return [
            "assessment_vision", "use_case_specifications", "vendor_recommendations",
            "roi_projections", "compliance_considerations", "implementation_roadmap"
        ]

    def execute(self, state: RunState) -> RunState:
        """Design comprehensive talent assessment strategy."""

        vision = state.working_data.get("vision", {})
        context = state.working_data.get("context_summary", {})
        pillars = state.working_data.get("strategic_pillars", [])
        goals = state.working_data.get("strategic_goals", [])

        # Check if this is a talent assessment context
        is_talent_assessment = self._detect_talent_assessment_context(vision, context)

        if not is_talent_assessment:
            self.logger.info("Context is not talent assessment specific, skipping specialist agent")
            return state

        user_prompt = f"""Design a comprehensive talent assessment strategy based on the following strategic context.

## Strategic Vision
{vision}

## Organizational Context
{context}

## Strategic Pillars
{pillars}

## Strategic Goals
{goals}

Create a detailed talent assessment strategy that includes:

1. **Assessment Vision** - Aspirational vision for the assessment function aligned with business strategy

2. **Use Case Specifications** - For each major use case (hiring, development, succession, etc.):
   - Business need and volume estimates
   - Target population (job levels, families)
   - Recommended assessment battery
   - Validity requirements
   - Scoring approach and decision rules
   - Vendor recommendations
   - ROI expectations

3. **Vendor Recommendations** - Evaluate and recommend vendors:
   - Score on key criteria (validity, UX, integration, global coverage)
   - Best fit use cases
   - Strengths and weaknesses

4. **ROI Projections** - For top 3 use cases:
   - Investment requirements
   - Benefit drivers (quality of hire, turnover reduction)
   - Year 1 and Year 3 ROI
   - Key assumptions

5. **Compliance Considerations**:
   - EEOC compliance approach
   - Adverse impact monitoring
   - International considerations (GDPR, local laws)
   - Accommodation procedures

6. **Implementation Roadmap**:
   - Phased approach (Phase 1, 2, 3)
   - Quick wins vs. transformational initiatives
   - Technology requirements
   - Change management needs

Return as valid JSON with this structure:
{{
    "assessment_vision": {{
        "vision_statement": "...",
        "mission_statement": "...",
        "business_strategy_alignment": "...",
        "talent_strategy_alignment": "...",
        "guiding_principles": ["Evidence-based decision making", "..."],
        "success_metrics": ["Quality of hire improvement", "..."],
        "research_foundation": ["Schmidt & Hunter meta-analysis", "..."]
    }},
    "use_case_specifications": [
        {{
            "use_case_id": "UC_001",
            "use_case": "external_hiring",
            "name": "High-Volume Professional Hiring",
            "description": "...",
            "business_need": "...",
            "volume_estimate": 5000,
            "target_job_levels": ["professional", "senior_professional"],
            "target_job_families": ["Engineering", "Finance", "Operations"],
            "recommended_assessments": ["cognitive_ability", "personality", "situational_judgment"],
            "assessment_battery": ["SHL Verify G+", "Hogan HPI", "Custom SJT"],
            "validity_requirements": {{"criterion_validity": 0.30, "adverse_impact_ratio": 0.80}},
            "scoring_approach": "compensatory",
            "decision_rules": ["Minimum cognitive score at 50th percentile", "..."],
            "preferred_vendors": ["shl", "hogan"],
            "priority": "high",
            "implementation_phase": 1,
            "expected_roi_percent": 150,
            "roi_drivers": ["Quality of hire improvement", "Reduced turnover"]
        }}
    ],
    "vendor_recommendations": [
        {{
            "vendor": "shl",
            "vendor_name": "SHL",
            "assessment_types_offered": ["cognitive_ability", "personality", "situational_judgment"],
            "products_evaluated": ["Verify G+", "OPQ32", "MFS"],
            "validity_evidence": 4.5,
            "reliability": 4.5,
            "adverse_impact": 3.0,
            "user_experience": 4.0,
            "candidate_experience": 3.5,
            "integration_capability": 4.5,
            "global_coverage": 5.0,
            "language_support": 5.0,
            "cost_effectiveness": 3.5,
            "support_quality": 4.0,
            "overall_score": 4.2,
            "recommendation": "preferred",
            "strengths": ["Strong validity evidence", "Global reach"],
            "weaknesses": ["Higher cost", "Candidate experience could improve"],
            "best_fit_use_cases": ["external_hiring", "succession_planning"]
        }}
    ],
    "roi_projections": [
        {{
            "use_case": "external_hiring",
            "initial_investment": 250000,
            "annual_operating_cost": 150000,
            "annual_volume": 5000,
            "cost_per_assessment": 30,
            "quality_of_hire_improvement": 0.15,
            "turnover_reduction": 0.10,
            "cost_of_bad_hire": 75000,
            "year_1_roi": 0.85,
            "year_3_roi": 2.50,
            "payback_period_months": 14,
            "key_assumptions": ["15% improvement in quality of hire", "10% reduction in first-year turnover"]
        }}
    ],
    "compliance_considerations": {{
        "eeoc_approach": "Conduct adverse impact analyses quarterly; maintain validity evidence for all assessments",
        "adverse_impact_monitoring": ["4/5ths rule analysis", "Statistical significance testing"],
        "international_considerations": ["GDPR data processing agreements", "Local validation studies"],
        "accommodation_procedures": ["Alternative assessment formats", "Extended time provisions"]
    }},
    "implementation_roadmap": {{
        "phase_1": {{
            "name": "Foundation",
            "duration": "FY26 Q1-Q2",
            "initiatives": ["Governance framework", "High-volume hiring assessment", "Platform selection"],
            "investment": 350000,
            "quick_wins": ["Standardize interview process", "Pilot cognitive assessment"]
        }},
        "phase_2": {{
            "name": "Expansion",
            "duration": "FY26 Q3 - FY27 Q2",
            "initiatives": ["Leadership assessment", "Internal mobility", "Analytics platform"],
            "investment": 500000
        }},
        "phase_3": {{
            "name": "Optimization",
            "duration": "FY27 Q3 - FY29",
            "initiatives": ["AI-enhanced assessments", "Continuous validation", "Predictive analytics"],
            "investment": 400000
        }},
        "technology_requirements": ["ATS integration", "Assessment platform", "Analytics dashboard"],
        "change_management": ["Recruiter training", "Manager education", "Candidate communication"]
    }}
}}"""

        system_prompt = self.get_prompt_with_learnings(state)
        response = self.invoke_llm(user_prompt, system_prompt)

        try:
            result = self.extract_json_from_response(response)

            # Store results
            state.working_data["assessment_vision"] = result.get("assessment_vision", {})
            state.working_data["use_case_specifications"] = result.get("use_case_specifications", [])
            state.working_data["vendor_recommendations"] = result.get("vendor_recommendations", [])
            state.working_data["roi_projections"] = result.get("roi_projections", [])
            state.working_data["compliance_considerations"] = result.get("compliance_considerations", {})
            state.working_data["implementation_roadmap"] = result.get("implementation_roadmap", {})

            # Validate use cases
            use_cases = result.get("use_case_specifications", [])
            if len(use_cases) < 3:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "FEW_USE_CASES",
                    f"Only {len(use_cases)} use cases defined; consider additional use cases"
                )

            # Check ROI projections
            roi_projections = result.get("roi_projections", [])
            low_roi = [r for r in roi_projections if r.get("year_1_roi", 0) < 0.5]
            if low_roi:
                self.add_flag(
                    state,
                    SeverityLevel.INFO,
                    "LOW_ROI_USE_CASES",
                    f"{len(low_roi)} use cases have Year 1 ROI below 50%"
                )

            # Check vendor coverage
            vendors = result.get("vendor_recommendations", [])
            preferred = [v for v in vendors if v.get("recommendation") == "preferred"]
            if len(preferred) < 2:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "LIMITED_VENDOR_OPTIONS",
                    "Consider evaluating more vendors for redundancy"
                )

            self.logger.info(
                f"Talent assessment strategy designed: {len(use_cases)} use cases, "
                f"{len(vendors)} vendors evaluated"
            )

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.ERROR,
                "TALENT_ASSESSMENT_DESIGN_FAILED",
                f"Failed to design talent assessment strategy: {str(e)}"
            )
            self.logger.error(f"Talent assessment design failed: {e}")

        return state

    def _detect_talent_assessment_context(self, vision: Dict, context: Dict) -> bool:
        """Detect if the context is talent/assessment related."""
        keywords = [
            "talent", "assessment", "hiring", "selection", "recruitment",
            "succession", "leadership", "competency", "psychometric",
            "personality", "cognitive", "workforce", "hr", "human resources",
            "employee", "candidate", "interview", "evaluation"
        ]

        text_to_check = str(vision).lower() + " " + str(context).lower()

        matches = sum(1 for kw in keywords if kw in text_to_check)
        return matches >= 3  # At least 3 keyword matches


class AssessmentValidationAgent(BaseAgent):
    """
    Agent that validates assessment strategy against IO psychology best practices.

    Ensures:
    - Validity evidence requirements are met
    - Adverse impact considerations addressed
    - Legal compliance maintained
    - Best practices followed
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="TA2_AssessmentValidator",
            step_name="Assessment Strategy Validation",
            phase=WorkflowPhase.VALIDATION,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are an IO Psychology expert specializing in assessment validation and legal compliance.

Your role is to validate talent assessment strategies against:

**Psychometric Standards:**
- SIOP Principles for Validation and Use of Personnel Selection Procedures
- ISO 10667 Assessment Service Delivery
- APA Standards for Educational and Psychological Testing

**Legal Requirements:**
- EEOC Uniform Guidelines on Employee Selection Procedures
- Title VII of the Civil Rights Act
- ADA requirements for accommodations
- ADEA considerations
- State and local fair employment laws
- GDPR and international data protection

**Best Practice Checklist:**
1. Are assessments job-related and consistent with business necessity?
2. Is there adequate validity evidence for each assessment?
3. Has adverse impact been analyzed and addressed?
4. Are accommodation procedures in place?
5. Is data retention and privacy addressed?
6. Are cut scores defensible?
7. Is there a continuous validation plan?

Provide specific, actionable feedback with references to standards and guidelines."""

    def execute(self, state: RunState) -> RunState:
        """Validate assessment strategy."""

        use_cases = state.working_data.get("use_case_specifications", [])
        vendors = state.working_data.get("vendor_recommendations", [])
        compliance = state.working_data.get("compliance_considerations", {})

        if not use_cases:
            return state

        user_prompt = f"""Validate this talent assessment strategy against IO psychology best practices and legal requirements.

## Use Case Specifications
{use_cases}

## Vendor Recommendations
{vendors}

## Compliance Considerations
{compliance}

Evaluate against these criteria and provide validation results:

1. **Validity Evidence** - Is there sufficient validity evidence cited for each assessment?
2. **Adverse Impact** - Are adverse impact considerations adequately addressed?
3. **Job Relatedness** - Is the job-relatedness of assessments clear?
4. **Legal Compliance** - Does the strategy meet EEOC and other legal requirements?
5. **Best Practices** - Does the strategy follow SIOP Principles?
6. **Data Privacy** - Are privacy requirements addressed?
7. **Candidate Experience** - Is candidate experience considered?

Return as JSON:
{{
    "validation_results": {{
        "overall_score": 0.85,
        "ready_for_implementation": true,
        "scores_by_criterion": {{
            "validity_evidence": 0.90,
            "adverse_impact": 0.80,
            "job_relatedness": 0.85,
            "legal_compliance": 0.90,
            "best_practices": 0.85,
            "data_privacy": 0.80,
            "candidate_experience": 0.75
        }}
    }},
    "findings": [
        {{
            "criterion": "adverse_impact",
            "severity": "warning",
            "finding": "Cognitive assessment may have adverse impact on protected groups",
            "recommendation": "Consider using SJT as alternative or in combination to reduce adverse impact",
            "reference": "SIOP Principles 5.3; EEOC Guidelines Section 3A"
        }}
    ],
    "required_actions": ["Add adverse impact monitoring plan", "Document validity evidence sources"],
    "recommendations": ["Consider pilot study before full rollout", "Establish validation schedule"]
}}"""

        response = self.invoke_llm(user_prompt)

        try:
            result = self.extract_json_from_response(response)

            state.working_data["assessment_validation"] = result
            validation_results = result.get("validation_results", {})

            # Check if ready
            if not validation_results.get("ready_for_implementation", False):
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "ASSESSMENT_NOT_READY",
                    "Assessment strategy requires remediation before implementation"
                )

            # Add findings as flags
            for finding in result.get("findings", []):
                severity = SeverityLevel.WARNING if finding.get("severity") == "warning" else SeverityLevel.ERROR
                self.add_flag(
                    state,
                    severity,
                    f"ASSESSMENT_{finding.get('criterion', 'ISSUE').upper()}",
                    finding.get("finding", ""),
                    metadata={"recommendation": finding.get("recommendation"), "reference": finding.get("reference")}
                )

            self.logger.info(f"Assessment validation complete: score {validation_results.get('overall_score', 0):.2f}")

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.ERROR,
                "ASSESSMENT_VALIDATION_FAILED",
                f"Assessment validation failed: {str(e)}"
            )

        return state
