"""
Compliance report schemas for brand and quality verification.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class IssueSeverity(str, Enum):
    """Severity levels for compliance issues."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ComplianceIssue(BaseModel):
    """A single compliance issue found during QA."""
    issue_id: str
    category: str  # "color", "typography", "logo", "spacing", "terminology", "accessibility"
    severity: IssueSeverity
    slide_number: Optional[int] = None
    element: Optional[str] = None
    description: str
    recommendation: Optional[str] = None
    auto_fixed: bool = False


class ToneAnalysis(BaseModel):
    """Analysis of content tone against brand personality."""
    optimistic: dict = Field(default_factory=dict)
    curious: dict = Field(default_factory=dict)
    courageous: dict = Field(default_factory=dict)
    compassionate: dict = Field(default_factory=dict)
    humble: dict = Field(default_factory=dict)
    overall_score: float = 0.0


class ComplianceReport(BaseModel):
    """Complete brand compliance report."""
    overall_score: float = 0.0
    status: str = "PENDING"  # "APPROVED", "APPROVED_WITH_RECOMMENDATIONS", "NEEDS_REVISION"
    issues: list[ComplianceIssue] = Field(default_factory=list)
    tone_analysis: Optional[ToneAnalysis] = None
    terminology_corrections: list[dict] = Field(default_factory=list)
    category_scores: dict[str, float] = Field(default_factory=dict)
    recommendations: list[str] = Field(default_factory=list)
    checks_passed: int = 0
    checks_failed: int = 0
    checks_total: int = 0

    def add_issue(self, issue: ComplianceIssue):
        """Add a compliance issue."""
        self.issues.append(issue)
        if issue.severity in (IssueSeverity.CRITICAL, IssueSeverity.HIGH):
            self.checks_failed += 1
        self.checks_total += 1

    def add_pass(self, category: str):
        """Record a passed check."""
        self.checks_passed += 1
        self.checks_total += 1

    @property
    def has_critical_issues(self) -> bool:
        return any(i.severity == IssueSeverity.CRITICAL for i in self.issues)

    @property
    def high_severity_count(self) -> int:
        return sum(1 for i in self.issues if i.severity in (IssueSeverity.CRITICAL, IssueSeverity.HIGH))
