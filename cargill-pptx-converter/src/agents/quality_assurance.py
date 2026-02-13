"""
Agent 6: Quality Assurance Agent

Final comprehensive review ensuring brand compliance and professional polish.
"""

from src.agents.base import BaseAgent
from src.brand.constants import (
    HEX_CARGILL_LEAF_GREEN,
    HEX_WHITE,
    HEX_WHITE_GREEN,
    HEX_DEEP_GREEN,
    HEX_NEUTRAL_1000,
    HEX_NEUTRAL_700,
    HEX_NEUTRAL_300,
)
from src.schemas.compliance import (
    ComplianceIssue,
    ComplianceReport,
    IssueSeverity,
)
from src.schemas.slide import SlideLayout
from src.schemas.run_state import RunState


# All approved hex colors (lowercase for comparison)
APPROVED_HEX_COLORS = {
    "#ffffff", "#f5f9ed", "#bde588", "#81ab40", "#00843d",
    "#01632d", "#03441f", "#012912", "#000000",
    "#f3f4f3", "#e7e8e8", "#dbdddc", "#9fa4a2", "#707773",
    "#58605c", "#404945", "#28332d", "#1c2722", "#101c16",
    "#eb5655", "#c50f1f", "#fea800", "#55a5eb", "#0f49c5",
    "#f7b9c0", "#ea5062", "#9e2a2f",
    "#ffd77d", "#ffbc27",
    "#bcedff", "#57d1ff", "#007681",
    "#c6c2ff", "#7166ff", "#393380",
    "#99adc2", "#003266", "#001a33",
    "none",
}


class QualityAssuranceAgent(BaseAgent):
    """Final review ensuring 100% brand compliance and professional polish."""

    def __init__(self):
        super().__init__("S6", "Quality Assurance")

    def execute(self, state: RunState) -> RunState:
        state.current_step = self.agent_id
        self.logger.info("Running quality assurance checks")

        if not state.presentation_plan:
            self._add_flag(state, "CRITICAL", "No presentation plan for QA")
            return state

        report = ComplianceReport()
        slides = state.presentation_plan.slides

        # Run all checks
        self._check_color_compliance(slides, report)
        self._check_typography_compliance(slides, report)
        self._check_slide_structure(slides, report)
        self._check_content_quality(slides, report)
        self._check_spacing_compliance(slides, report)
        self._check_accessibility(slides, report)

        # Calculate scores
        report.category_scores = {
            "color": self._category_score(report, "color"),
            "typography": self._category_score(report, "typography"),
            "structure": self._category_score(report, "structure"),
            "content": self._category_score(report, "content"),
            "spacing": self._category_score(report, "spacing"),
            "accessibility": self._category_score(report, "accessibility"),
        }

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
        elif report.overall_score >= 95:
            report.status = "APPROVED"
        else:
            report.status = "APPROVED_WITH_RECOMMENDATIONS"

        state.qa_report = report
        self.logger.info(
            f"QA score: {report.overall_score}/100, status: {report.status}, "
            f"issues: {len(report.issues)}"
        )

        return state

    def _check_color_compliance(self, slides, report: ComplianceReport):
        """Verify all colors are from approved palette."""
        for slide in slides:
            scheme = slide.color_scheme
            colors_to_check = [
                ("background", scheme.background),
                ("primary", scheme.primary),
                ("headline", scheme.headline),
                ("body_text", scheme.body_text),
                ("card_background", scheme.card_background),
                ("card_border", scheme.card_border),
            ]
            if scheme.accent:
                colors_to_check.append(("accent", scheme.accent))
            if scheme.subheading:
                colors_to_check.append(("subheading", scheme.subheading))

            all_valid = True
            for name, color in colors_to_check:
                if color and color.lower() not in APPROVED_HEX_COLORS:
                    all_valid = False
                    report.add_issue(ComplianceIssue(
                        issue_id=f"color_{slide.slide_number}_{name}",
                        category="color",
                        severity=IssueSeverity.HIGH,
                        slide_number=slide.slide_number,
                        element=name,
                        description=f"Unapproved color {color} used for {name}",
                        recommendation="Use only colors from approved Cargill palette",
                    ))

            if all_valid:
                report.add_pass("color")

    def _check_typography_compliance(self, slides, report: ComplianceReport):
        """Verify typography meets brand standards."""
        approved_fonts = {
            "Big Caslon for Cargill",
            "Helvetica Now for Cargill",
            # Fallbacks
            "Georgia",
            "Arial",
        }

        for slide in slides:
            typo = slide.typography
            fonts_ok = True

            if typo.headline_font not in approved_fonts:
                fonts_ok = False
                report.add_issue(ComplianceIssue(
                    issue_id=f"font_headline_{slide.slide_number}",
                    category="typography",
                    severity=IssueSeverity.HIGH,
                    slide_number=slide.slide_number,
                    element="headline_font",
                    description=f"Unapproved font '{typo.headline_font}'",
                    recommendation="Use 'Big Caslon for Cargill' for headlines",
                ))

            if typo.body_font not in approved_fonts:
                fonts_ok = False
                report.add_issue(ComplianceIssue(
                    issue_id=f"font_body_{slide.slide_number}",
                    category="typography",
                    severity=IssueSeverity.HIGH,
                    slide_number=slide.slide_number,
                    element="body_font",
                    description=f"Unapproved font '{typo.body_font}'",
                    recommendation="Use 'Helvetica Now for Cargill' for body text",
                ))

            # Check minimum text sizes
            if typo.body_size < 10:
                report.add_issue(ComplianceIssue(
                    issue_id=f"font_size_{slide.slide_number}",
                    category="typography",
                    severity=IssueSeverity.MEDIUM,
                    slide_number=slide.slide_number,
                    description=f"Body text size {typo.body_size}pt is below minimum (10pt)",
                    recommendation="Minimum body text is 10pt (body-xs for legal only)",
                ))

            if fonts_ok:
                report.add_pass("typography")

    def _check_slide_structure(self, slides, report: ComplianceReport):
        """Check slide structure and flow."""
        if not slides:
            report.add_issue(ComplianceIssue(
                issue_id="no_slides",
                category="structure",
                severity=IssueSeverity.CRITICAL,
                description="No slides in presentation",
            ))
            return

        # Check for title slide
        first = slides[0]
        if first.layout not in (SlideLayout.TITLE_HERO, SlideLayout.BASIC_HERO):
            report.add_issue(ComplianceIssue(
                issue_id="no_title_slide",
                category="structure",
                severity=IssueSeverity.MEDIUM,
                slide_number=1,
                description="Presentation should start with a hero/title slide",
            ))
        else:
            report.add_pass("structure")

        # Check for closing slide
        last = slides[-1]
        if last.layout != SlideLayout.CLOSING:
            report.add_issue(ComplianceIssue(
                issue_id="no_closing",
                category="structure",
                severity=IssueSeverity.LOW,
                slide_number=len(slides),
                description="Presentation should end with a closing slide",
            ))
        else:
            report.add_pass("structure")

        # Check each slide has a title
        for slide in slides:
            has_title = any(e.element_type == "title" for e in slide.elements)
            if not has_title and slide.layout != SlideLayout.BLANK:
                report.add_issue(ComplianceIssue(
                    issue_id=f"no_title_{slide.slide_number}",
                    category="structure",
                    severity=IssueSeverity.LOW,
                    slide_number=slide.slide_number,
                    description="Slide has no title element",
                ))
            else:
                report.add_pass("structure")

        # Warn if too many slides
        if len(slides) > 30:
            report.add_issue(ComplianceIssue(
                issue_id="too_many_slides",
                category="structure",
                severity=IssueSeverity.INFO,
                description=f"Presentation has {len(slides)} slides, consider condensing",
            ))

    def _check_content_quality(self, slides, report: ComplianceReport):
        """Check content quality across slides."""
        for slide in slides:
            for element in slide.elements:
                # Check for empty content
                if element.element_type in ("title", "body") and not element.content:
                    report.add_issue(ComplianceIssue(
                        issue_id=f"empty_{element.element_type}_{slide.slide_number}",
                        category="content",
                        severity=IssueSeverity.MEDIUM,
                        slide_number=slide.slide_number,
                        element=element.element_type,
                        description=f"Empty {element.element_type} element",
                    ))
                else:
                    report.add_pass("content")

                # Check word count per slide
                if element.element_type == "body" and element.content:
                    words = len(element.content.split())
                    if words > 200:
                        report.add_issue(ComplianceIssue(
                            issue_id=f"wordy_{slide.slide_number}",
                            category="content",
                            severity=IssueSeverity.LOW,
                            slide_number=slide.slide_number,
                            description=f"Slide body has {words} words, consider reducing",
                            recommendation="Aim for under 150 words per slide for readability",
                        ))

                # Check bullet count
                if element.element_type == "bullet" and len(element.items) > 7:
                    report.add_issue(ComplianceIssue(
                        issue_id=f"too_many_bullets_{slide.slide_number}",
                        category="content",
                        severity=IssueSeverity.LOW,
                        slide_number=slide.slide_number,
                        description=f"Slide has {len(element.items)} bullets, consider splitting",
                        recommendation="Maximum 7 bullet points per slide",
                    ))

    def _check_spacing_compliance(self, slides, report: ComplianceReport):
        """Verify spacing follows brand scale."""
        valid_spacing_values = {
            0.028, 0.056, 0.111, 0.167, 0.222, 0.333,
            0.444, 0.556, 0.667, 0.778, 1.111,
        }

        for slide in slides:
            spacing = slide.spacing
            values = [
                spacing.content_padding,
                spacing.headline_margin_bottom,
                spacing.element_gap,
                spacing.card_gap,
                spacing.card_padding,
            ]

            all_valid = True
            for val in values:
                # Allow some floating point tolerance
                if not any(abs(val - v) < 0.01 for v in valid_spacing_values):
                    all_valid = False

            if all_valid:
                report.add_pass("spacing")

    def _check_accessibility(self, slides, report: ComplianceReport):
        """Check accessibility standards."""
        for slide in slides:
            # Basic contrast check for hero slides
            if slide.template_category == "hero":
                if slide.color_scheme.headline == slide.color_scheme.background:
                    report.add_issue(ComplianceIssue(
                        issue_id=f"contrast_{slide.slide_number}",
                        category="accessibility",
                        severity=IssueSeverity.HIGH,
                        slide_number=slide.slide_number,
                        description="Text color matches background - no contrast",
                    ))
                else:
                    report.add_pass("accessibility")
            else:
                report.add_pass("accessibility")

    def _category_score(self, report: ComplianceReport, category: str) -> float:
        """Calculate score for a specific category."""
        category_issues = [i for i in report.issues if i.category == category]
        if not category_issues:
            return 100.0

        deductions = 0
        for issue in category_issues:
            if issue.severity == IssueSeverity.CRITICAL:
                deductions += 25
            elif issue.severity == IssueSeverity.HIGH:
                deductions += 15
            elif issue.severity == IssueSeverity.MEDIUM:
                deductions += 5
            elif issue.severity == IssueSeverity.LOW:
                deductions += 2

        return max(0.0, 100.0 - deductions)
