"""v3.1 structural invariants on TechnicalCompetency / ProficiencyLevel."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.schemas.competency import (
    AppliedScope,
    BehavioralIndicator,
    BenchmarkingRecord,
    LevelCode,
    OverlapCheck,
    ProficiencyLevel,
    TechnicalCompetency,
)


def _levels(num_indicators: int = 3):
    return [
        ProficiencyLevel(
            level=code,
            description=f"Level {code.value} description.",
            indicators=[BehavioralIndicator(text=f"i{i}-{code.value}") for i in range(num_indicators)],
        )
        for code in (LevelCode.L1, LevelCode.L2, LevelCode.L3, LevelCode.L4)
    ]


def _valid_competency(**overrides):
    base = dict(
        competency_id="c1",
        name="Process Hazard Analysis",
        definition=(
            "Systematically identifies and evaluates process hazards using HAZOP "
            "methodology, recommends safeguards, and verifies their effective ongoing implementation."
        ),
        why_it_matters="Reduces incident risk in chemical operations.",
        proficiency_levels=_levels(),
        boundary_class="TECHNICAL",
        integrity_tag="CONFIRMED",
        applied_scope=AppliedScope(),
        overlap_check=OverlapCheck(core_leadership_overlap="NONE"),
        benchmarking=BenchmarkingRecord(),
    )
    base.update(overrides)
    return TechnicalCompetency(**base)


def test_valid_competency_constructs():
    c = _valid_competency()
    assert len(c.name.split()) == 3
    assert 15 <= len(c.definition.split()) <= 25
    assert [p.level for p in c.proficiency_levels] == [
        LevelCode.L1, LevelCode.L2, LevelCode.L3, LevelCode.L4
    ]
    assert all(len(p.indicators) == 3 for p in c.proficiency_levels)


@pytest.mark.parametrize("name", ["one two", "one two three four five six seven", ""])
def test_title_word_count_rejected(name):
    with pytest.raises(ValidationError):
        _valid_competency(name=name)


def test_definition_under_15_words_rejected():
    with pytest.raises(ValidationError):
        _valid_competency(definition="Short definition with too few words to satisfy v3.1.")


def test_definition_over_25_words_rejected():
    long = " ".join(["word"] * 30) + "."
    with pytest.raises(ValidationError):
        _valid_competency(definition=long)


def test_definition_multiple_sentences_rejected():
    bad = "First sentence ending here. Second sentence here for testing the validator behavior properly today."
    with pytest.raises(ValidationError):
        _valid_competency(definition=bad)


def test_indicators_count_must_be_three():
    with pytest.raises(ValidationError):
        ProficiencyLevel(level=LevelCode.L1, description="x",
                         indicators=[BehavioralIndicator(text="a"), BehavioralIndicator(text="b")])


def test_proficiency_levels_must_be_l1_through_l4_in_order():
    out_of_order = [
        ProficiencyLevel(level=LevelCode.L2, description="x",
                         indicators=[BehavioralIndicator(text=f"i{i}") for i in range(3)]),
        ProficiencyLevel(level=LevelCode.L1, description="x",
                         indicators=[BehavioralIndicator(text=f"i{i}") for i in range(3)]),
        ProficiencyLevel(level=LevelCode.L3, description="x",
                         indicators=[BehavioralIndicator(text=f"i{i}") for i in range(3)]),
        ProficiencyLevel(level=LevelCode.L4, description="x",
                         indicators=[BehavioralIndicator(text=f"i{i}") for i in range(3)]),
    ]
    with pytest.raises(ValidationError):
        _valid_competency(proficiency_levels=out_of_order)


def test_boundary_class_enum():
    for cls in ("V_AND_B", "COMMON", "TECHNICAL", "MIXED"):
        c = _valid_competency(boundary_class=cls)
        assert c.boundary_class == cls
    with pytest.raises(ValidationError):
        _valid_competency(boundary_class="OTHER")


def test_integrity_tag_enum():
    for tag in ("CONFIRMED", "CORRECTED", "UNVERIFIABLE", "FLAGGED"):
        c = _valid_competency(integrity_tag=tag)
        assert c.integrity_tag == tag
    with pytest.raises(ValidationError):
        _valid_competency(integrity_tag="UNKNOWN")
