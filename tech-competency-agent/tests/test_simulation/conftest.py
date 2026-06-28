"""Shared fixtures for end-to-end simulation tests.

These fixtures build small, deterministic in-memory artifacts that exercise the
real code paths without requiring external services (Anthropic, sentence-
transformers, JDMS files).
"""

from __future__ import annotations

from typing import List

import pytest

from src.schemas.competency import (
    AppliedScope,
    BehavioralIndicator,
    BenchmarkingRecord,
    CriticalityBreakdown,
    LevelCode,
    OverlapCheck,
    ProficiencyLevel,
    TechnicalCompetency,
)
from src.skill_mapping.schemas import (
    SkillCompetencyMapping,
    TrainingItem,
)


def _levels(prefix: str) -> List[ProficiencyLevel]:
    return [
        ProficiencyLevel(
            level=code,
            description=f"{prefix} {code.value} description.",
            indicators=[
                BehavioralIndicator(text=f"{prefix} {code.value} indicator {i+1}")
                for i in range(3)
            ],
        )
        for code in (LevelCode.L1, LevelCode.L2, LevelCode.L3, LevelCode.L4)
    ]


def _competency(cid: str, name: str, definition: str, criticality: float = 0.85) -> TechnicalCompetency:
    return TechnicalCompetency(
        competency_id=cid,
        name=name,
        definition=definition,
        why_it_matters="Supports business outcomes.",
        proficiency_levels=_levels(name.split()[0]),
        boundary_class="TECHNICAL",
        integrity_tag="CONFIRMED",
        applied_scope=AppliedScope(
            tools_methods_tech=["openpyxl", "pandas"],
            standards_frameworks=["ISO 9001"],
            typical_outputs=["report"],
        ),
        responsibility_trace=[],
        overlap_check=OverlapCheck(core_leadership_overlap="NONE"),
        benchmarking=BenchmarkingRecord(benchmarked_against=["O*NET"]),
        criticality=CriticalityBreakdown(
            coverage=0.95,
            criticality=criticality,
            distinctiveness=0.80,
            assessability=0.70,
            weighted_total=0.40 * 0.95 + 0.30 * criticality + 0.20 * 0.80 + 0.10 * 0.70,
        ),
    )


@pytest.fixture
def synthetic_competencies() -> List[TechnicalCompetency]:
    """Three deterministic v3.1 competencies — used by simulation tests."""
    return [
        _competency(
            "TC-FIN-001",
            "Financial Risk Modeling",
            "Builds quantitative models to forecast credit and market risk across "
            "trading and portfolio decisions daily.",
            criticality=0.90,
        ),
        _competency(
            "TC-FIN-002",
            "Regulatory Reporting Compliance",
            "Prepares accurate regulatory filings under U.S. GAAP and IFRS standards "
            "within statutory deadlines each reporting period.",
            criticality=0.85,
        ),
        _competency(
            "TC-FIN-003",
            "Treasury Cash Forecasting",
            "Forecasts enterprise cash position and liquidity needs across all global "
            "regions using rolling thirteen-week treasury models on a weekly basis.",
            criticality=0.78,
        ),
    ]


@pytest.fixture
def synthetic_catalog() -> List[TrainingItem]:
    """Five fixture L&D courses spanning L1-L4 verbs."""
    return [
        TrainingItem(
            course_id="LDN-FIN-1001",
            title="Intro to Financial Risk",
            description="Recognize and list common credit and market risk metrics used across desks.",
            learning_objectives=["Recognize key risk metrics", "List common risk frameworks", "Describe the trade lifecycle"],
            duration_hours=2.0,
            modality="ELEARNING",
            audience_band="Associate",
            prerequisites=[],
            vendor="Vendor A",
        ),
        TrainingItem(
            course_id="LDN-FIN-1002",
            title="Apply IFRS Reporting Practice",
            description="Apply IFRS rules to prepare standard quarterly filings under supervision.",
            learning_objectives=["Apply IFRS rules to filings", "Demonstrate disclosure controls", "Implement reconciliation steps"],
            duration_hours=8.0,
            modality="ILT",
            audience_band="Professional",
            prerequisites=[],
            vendor="Vendor A",
        ),
        TrainingItem(
            course_id="LDN-FIN-1003",
            title="Advanced Risk Modeling Coaching",
            description="Analyze portfolio risk drivers; design stress-test scenarios for complex books.",
            learning_objectives=["Analyze portfolio risk drivers", "Design stress-test scenarios", "Evaluate model performance"],
            duration_hours=24.0,
            modality="COACHING",
            audience_band="SeniorAdvisor",
            prerequisites=["LDN-FIN-1002"],
            vendor="Vendor B",
        ),
        TrainingItem(
            course_id="LDN-FIN-1004",
            title="Treasury Cash Mastery",
            description="Lead enterprise cash strategy; mentor advanced practitioners across regions.",
            learning_objectives=["Lead enterprise cash strategy", "Mentor advanced practitioners", "Set standards for liquidity governance"],
            duration_hours=60.0,
            modality="OJT",
            audience_band="SeniorManagerI",
            prerequisites=["LDN-FIN-1003"],
            vendor="Vendor B",
        ),
        TrainingItem(
            course_id="LDN-COMMON-9001",
            title="Code of Conduct & Ethics Training",
            description="Recognize ethics principles and harassment policies; commit to acting with integrity.",
            learning_objectives=["Recognize ethics policies", "Identify harassment scenarios"],
            duration_hours=1.0,
            modality="ELEARNING",
            audience_band=None,
            prerequisites=[],
            vendor="Vendor A",
        ),
    ]


@pytest.fixture
def synthetic_mappings(synthetic_competencies, synthetic_catalog) -> List[SkillCompetencyMapping]:
    """Four high-confidence mappings; one auto-V&B route."""
    return [
        SkillCompetencyMapping(
            course_id="LDN-FIN-1001",
            competency_id="TC-FIN-001",
            competency_name="Financial Risk Modeling",
            level=LevelCode.L1,
            confidence=0.72,
            rationale="L1 verbs + financial risk semantic match.",
            bloom_evidence=["recognize", "list", "describe"],
            similarity_score=0.78,
            integrity_tag="CONFIRMED",
            mismatch_flags=[],
        ),
        SkillCompetencyMapping(
            course_id="LDN-FIN-1002",
            competency_id="TC-FIN-002",
            competency_name="Regulatory Reporting Compliance",
            level=LevelCode.L2,
            confidence=0.81,
            rationale="L2 verbs + IFRS regulatory match.",
            bloom_evidence=["apply", "demonstrate", "implement"],
            similarity_score=0.84,
            integrity_tag="CONFIRMED",
            mismatch_flags=[],
        ),
        SkillCompetencyMapping(
            course_id="LDN-FIN-1003",
            competency_id="TC-FIN-001",
            competency_name="Financial Risk Modeling",
            level=LevelCode.L3,
            confidence=0.88,
            rationale="L3 verbs + coaching modality + risk semantic match.",
            bloom_evidence=["analyze", "design", "evaluate"],
            similarity_score=0.90,
            integrity_tag="CONFIRMED",
            mismatch_flags=[],
        ),
        SkillCompetencyMapping(
            course_id="LDN-FIN-1004",
            competency_id="TC-FIN-003",
            competency_name="Treasury Cash Forecasting",
            level=LevelCode.L4,
            confidence=0.91,
            rationale="L4 verbs + OJT modality + treasury cash semantic match.",
            bloom_evidence=["lead", "mentor", "set"],
            similarity_score=0.93,
            integrity_tag="CONFIRMED",
            mismatch_flags=[],
        ),
    ]
