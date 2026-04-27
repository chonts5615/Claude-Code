import re
from typing import Iterable, List

from src.schemas.tcb_builder import (
    CompetencyValidationResult,
    JobFamilyCompetencySet,
    JobFamilyValidationResult,
    TCBValidationIssue,
    TCBValidationReport,
)

TITLE_WORD_MIN = 3
TITLE_WORD_MAX = 6
DEFINITION_WORD_MIN = 15
DEFINITION_WORD_MAX = 25
EXPECTED_LEVELS = ("L1", "L2", "L3", "L4")
BOUNDARY_TERMS_VB = {
    "integrity",
    "ethics",
    "transparency",
    "inclusion",
    "diversity",
    "wellbeing",
    "continuous improvement",
    "growth mindset",
    "accountability",
    "ownership",
    "decisiveness",
    "urgency",
    "collaboration",
    "teamwork",
}
BOUNDARY_TERMS_COMMON = {
    "change acumen",
    "technology & data acumen",
    "business acumen",
    "financial acumen",
    "partner with impact",
}


class TCBStandardsValidator:
    """Validates competency packages against Technical Competency Builder standards."""

    def validate(self, job_families: Iterable[JobFamilyCompetencySet]) -> TCBValidationReport:
        family_results: List[JobFamilyValidationResult] = []
        total_competencies = 0
        valid_competencies = 0

        for family in job_families:
            competency_results: List[CompetencyValidationResult] = []
            efs_covered: set[str] = set()

            for competency in family.competencies:
                total_competencies += 1
                efs_covered.update(competency.technical_efs_covered)
                issues = self._validate_competency(competency)
                is_valid = len([issue for issue in issues if issue.severity == "ERROR"]) == 0
                if is_valid:
                    valid_competencies += 1
                competency_results.append(
                    CompetencyValidationResult(
                        competency_id=competency.competency_id,
                        is_valid=is_valid,
                        issues=issues,
                    )
                )

            total_efs = len(family.technical_efs_total)
            coverage_rate = len(efs_covered) / total_efs if total_efs else 0.0
            package_issues = self._validate_package(family, coverage_rate)
            if package_issues:
                competency_results.append(
                    CompetencyValidationResult(
                        competency_id="_PACKAGE_",
                        is_valid=False,
                        issues=package_issues,
                    )
                )

            family_valid = all(result.is_valid for result in competency_results)
            family_results.append(
                JobFamilyValidationResult(
                    job_family=family.job_family,
                    competency_results=competency_results,
                    package_coverage_rate=coverage_rate,
                    package_is_valid=family_valid,
                )
            )

        return TCBValidationReport(
            total_job_families=len(family_results),
            total_competencies=total_competencies,
            valid_competencies=valid_competencies,
            report_is_valid=all(result.package_is_valid for result in family_results),
            results=family_results,
        )

    def _validate_competency(self, competency) -> List[TCBValidationIssue]:
        issues: List[TCBValidationIssue] = []

        title_words = _word_count(competency.title)
        if not TITLE_WORD_MIN <= title_words <= TITLE_WORD_MAX:
            issues.append(
                TCBValidationIssue(
                    severity="ERROR",
                    code="TITLE_WORD_COUNT",
                    field="title",
                    message=f"Title must be {TITLE_WORD_MIN}-{TITLE_WORD_MAX} words; got {title_words}.",
                )
            )

        definition_words = _word_count(competency.definition)
        if not DEFINITION_WORD_MIN <= definition_words <= DEFINITION_WORD_MAX:
            issues.append(
                TCBValidationIssue(
                    severity="ERROR",
                    code="DEFINITION_WORD_COUNT",
                    field="definition",
                    message=(
                        f"Definition must be {DEFINITION_WORD_MIN}-{DEFINITION_WORD_MAX} words; "
                        f"got {definition_words}."
                    ),
                )
            )

        sentence_count = _sentence_count(competency.definition)
        if sentence_count != 1:
            issues.append(
                TCBValidationIssue(
                    severity="ERROR",
                    code="DEFINITION_SENTENCE_COUNT",
                    field="definition",
                    message=f"Definition must be exactly one sentence; got {sentence_count}.",
                )
            )

        first_word = competency.definition.strip().split(" ")[0].lower()
        if first_word.endswith("ing"):
            issues.append(
                TCBValidationIssue(
                    severity="WARNING",
                    code="DEFINITION_VERB_LED",
                    field="definition",
                    message="Definition should begin with a clear action verb instead of a gerund form.",
                )
            )

        lower_text = f"{competency.title} {competency.definition}".lower()
        if any(term in lower_text for term in BOUNDARY_TERMS_VB):
            issues.append(
                TCBValidationIssue(
                    severity="WARNING",
                    code="VB_BOUNDARY_TERM",
                    field="title/definition",
                    message="Contains generic V&B boundary language that may not be technical.",
                )
            )
        if any(term in lower_text for term in BOUNDARY_TERMS_COMMON):
            issues.append(
                TCBValidationIssue(
                    severity="WARNING",
                    code="COMMON_BOUNDARY_TERM",
                    field="title/definition",
                    message="Contains Common Competency boundary language; confirm domain specificity.",
                )
            )

        for level in EXPECTED_LEVELS:
            indicators = competency.level_indicators.get(level, [])
            if len(indicators) != 3:
                issues.append(
                    TCBValidationIssue(
                        severity="ERROR",
                        code="LEVEL_INDICATOR_COUNT",
                        field=f"level_indicators.{level}",
                        message=f"{level} must contain exactly 3 indicators; got {len(indicators)}.",
                    )
                )

        return issues

    @staticmethod
    def _validate_package(
        family: JobFamilyCompetencySet,
        coverage_rate: float,
    ) -> List[TCBValidationIssue]:
        issues: List[TCBValidationIssue] = []

        if len(family.competencies) > 6:
            issues.append(
                TCBValidationIssue(
                    severity="ERROR",
                    code="MAX_COMPETENCY_COUNT",
                    field="competencies",
                    message=f"Max 6 competencies per job family; got {len(family.competencies)}.",
                )
            )

        if coverage_rate < 0.90:
            issues.append(
                TCBValidationIssue(
                    severity="ERROR",
                    code="EF_COVERAGE",
                    field="technical_efs_total",
                    message=f"Technical EF coverage must be >= 0.90; got {coverage_rate:.2f}.",
                )
            )

        return issues


def _word_count(text: str) -> int:
    return len([token for token in re.findall(r"\b[\w'-]+\b", text) if token])


def _sentence_count(text: str) -> int:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return len([segment for segment in sentences if segment])
