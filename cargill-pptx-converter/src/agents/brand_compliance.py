"""
Agent 2: Brand Compliance Agent

Ensures all content aligns with Cargill brand guidelines before design begins.
Checks tone, terminology, and personality alignment.
"""

from src.agents.base import BaseAgent
from src.brand.terminology import (
    analyze_personality,
    apply_corrections,
    check_terminology,
)
from src.schemas.compliance import (
    ComplianceIssue,
    ComplianceReport,
    IssueSeverity,
    ToneAnalysis,
)
from src.schemas.content import ContentType
from src.schemas.run_state import RunState


class BrandComplianceAgent(BaseAgent):
    """Assess content for brand alignment and apply terminology corrections."""

    def __init__(self):
        super().__init__("S2", "Brand Compliance")

    def execute(self, state: RunState) -> RunState:
        state.current_step = self.agent_id
        self.logger.info("Assessing brand compliance")

        if not state.extracted_content:
            self._add_flag(state, "CRITICAL", "No extracted content available for compliance check")
            return state

        report = ComplianceReport()
        content = state.extracted_content

        # 1. Terminology check on all text content
        all_text = content.get_all_text()
        corrections = check_terminology(all_text)

        for correction in corrections:
            report.add_issue(ComplianceIssue(
                issue_id=f"term_{len(report.issues)}",
                category="terminology",
                severity=IssueSeverity.MEDIUM if correction.severity == "medium" else IssueSeverity.LOW,
                description=correction.context,
                recommendation=f"Replace '{correction.original}' with '{correction.replacement}'",
            ))

        # Apply corrections to content blocks
        if corrections:
            for block in content.blocks:
                if block.text:
                    block.text = apply_corrections(block.text, corrections)
                if block.items:
                    block.items = [apply_corrections(item, corrections) for item in block.items]

            report.terminology_corrections = [
                {"original": c.original, "replacement": c.replacement, "severity": c.severity}
                for c in corrections
            ]
            self.logger.info(f"Applied {len(corrections)} terminology corrections")

        # 2. Tone and personality analysis
        personality_results = analyze_personality(all_text)
        tone_analysis = ToneAnalysis(
            optimistic=personality_results.get("optimistic", {}),
            curious=personality_results.get("curious", {}),
            courageous=personality_results.get("courageous", {}),
            compassionate=personality_results.get("compassionate", {}),
            humble=personality_results.get("humble", {}),
        )

        # Calculate overall tone score
        total_score = 0
        total_weight = 0
        for trait, data in personality_results.items():
            score = data.get("score", 0.5)
            weight = data.get("weight", 0.2)
            total_score += score * weight
            total_weight += weight

        tone_analysis.overall_score = round(total_score / total_weight, 2) if total_weight > 0 else 0.5
        report.tone_analysis = tone_analysis

        # Flag low personality scores
        for trait, data in personality_results.items():
            if data.get("score", 1.0) < 0.5:
                report.add_issue(ComplianceIssue(
                    issue_id=f"tone_{trait}",
                    category="tone",
                    severity=IssueSeverity.LOW,
                    description=f"'{trait}' personality trait score is low ({data['score']})",
                    recommendation=f"Consider adding more {trait} language to the content",
                ))
            else:
                report.add_pass("tone")

        # 3. Check for purpose alignment
        purpose_keywords = ["nourish", "safe", "responsible", "sustainable", "partner"]
        purpose_score = sum(1 for kw in purpose_keywords if kw in all_text.lower())
        if purpose_score < 2:
            report.add_issue(ComplianceIssue(
                issue_id="purpose_alignment",
                category="message",
                severity=IssueSeverity.INFO,
                description="Content could better align with Cargill's purpose statement",
                recommendation="Consider incorporating themes of nourishment, safety, responsibility, and sustainability",
            ))
        else:
            report.add_pass("message")

        # 4. Check content length suitability
        word_count = content.get_word_count()
        if word_count < 50:
            report.add_issue(ComplianceIssue(
                issue_id="content_short",
                category="content",
                severity=IssueSeverity.INFO,
                description=f"Content is brief ({word_count} words), presentation may have limited slides",
            ))
        elif word_count > 5000:
            report.add_issue(ComplianceIssue(
                issue_id="content_long",
                category="content",
                severity=IssueSeverity.INFO,
                description=f"Content is lengthy ({word_count} words), consider summarizing for presentation",
            ))
        else:
            report.add_pass("content")

        # Calculate overall compliance score
        if report.checks_total > 0:
            report.overall_score = round(
                report.checks_passed / report.checks_total * 100, 1
            )
        else:
            report.overall_score = 100.0

        # Set status
        if report.has_critical_issues:
            report.status = "NEEDS_REVISION"
        elif report.high_severity_count > 0:
            report.status = "APPROVED_WITH_RECOMMENDATIONS"
        else:
            report.status = "APPROVED"

        # Generate recommendations
        report.recommendations = self._generate_recommendations(report, personality_results)

        report.category_scores = {
            "terminology": 100 - len(corrections) * 5,
            "tone": round(tone_analysis.overall_score * 100, 1),
            "purpose": min(purpose_score * 20, 100),
        }

        state.compliance_report = report
        self.logger.info(
            f"Compliance score: {report.overall_score}, status: {report.status}"
        )

        return state

    def _generate_recommendations(self, report, personality_results) -> list[str]:
        """Generate actionable recommendations."""
        recs = []

        for trait, data in personality_results.items():
            if data.get("assessment") == "Needs improvement":
                recs.append(
                    f"Enhance '{trait}' trait: Add more {trait} language and framing"
                )
            elif data.get("assessment") == "Moderate":
                recs.append(
                    f"Consider strengthening '{trait}' trait in messaging"
                )

        if report.terminology_corrections:
            recs.append(
                f"{len(report.terminology_corrections)} terminology corrections applied automatically"
            )

        return recs
