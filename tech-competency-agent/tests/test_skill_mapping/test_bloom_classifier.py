"""Bloom-classifier heuristic + adjustments."""

from __future__ import annotations

from src.schemas.competency import LevelCode
from src.skill_mapping.bloom_classifier import classify
from src.skill_mapping.schemas import TrainingItem


def _item(**overrides):
    base = dict(
        course_id="C1",
        title="Test course",
        description="",
        learning_objectives=[],
        duration_hours=8.0,
        modality="ILT",
        audience_band=None,
        prerequisites=[],
        vendor=None,
    )
    base.update(overrides)
    return TrainingItem(**base)


def test_l1_verbs_yield_l1():
    est = classify(_item(learning_objectives=["Recognize basic terms", "Describe the process", "List standard fields"]))
    assert est.level == LevelCode.L1


def test_l3_verbs_yield_l3():
    est = classify(_item(learning_objectives=[
        "Analyze production data",
        "Evaluate root causes",
        "Diagnose recurring failures",
    ]))
    assert est.level == LevelCode.L3


def test_l4_verbs_yield_l4():
    est = classify(_item(learning_objectives=[
        "Design enterprise data architecture",
        "Lead transformation initiatives",
        "Mentor advanced practitioners",
    ]))
    assert est.level == LevelCode.L4


def test_short_elearning_downshift():
    long_est = classify(_item(
        learning_objectives=["Apply techniques", "Implement controls"],
        duration_hours=8.0, modality="ELEARNING",
    ))
    short_est = classify(_item(
        learning_objectives=["Apply techniques", "Implement controls"],
        duration_hours=1.0, modality="ELEARNING",
    ))
    short_idx = [LevelCode.L1, LevelCode.L2, LevelCode.L3, LevelCode.L4].index(short_est.level)
    long_idx = [LevelCode.L1, LevelCode.L2, LevelCode.L3, LevelCode.L4].index(long_est.level)
    assert short_idx <= long_idx


def test_long_coaching_upshift():
    base = classify(_item(
        learning_objectives=["Apply techniques", "Implement controls"],
        duration_hours=8.0, modality="ILT",
    ))
    coached = classify(_item(
        learning_objectives=["Apply techniques", "Implement controls"],
        duration_hours=20.0, modality="COACHING",
    ))
    levels = [LevelCode.L1, LevelCode.L2, LevelCode.L3, LevelCode.L4]
    assert levels.index(coached.level) >= levels.index(base.level)


def test_prerequisites_upshift():
    base = classify(_item(learning_objectives=["Apply", "Implement"]))
    with_pre = classify(_item(learning_objectives=["Apply", "Implement"], prerequisites=["Intro Course"]))
    levels = [LevelCode.L1, LevelCode.L2, LevelCode.L3, LevelCode.L4]
    assert levels.index(with_pre.level) >= levels.index(base.level)


def test_no_verbs_defaults_to_l2():
    est = classify(_item(description="A course on widgets.", learning_objectives=["Widgets matter."]))
    assert est.level == LevelCode.L2


def test_confidence_in_range():
    est = classify(_item(learning_objectives=["Recognize, list, describe"]))
    assert 0.0 <= est.confidence <= 1.0
