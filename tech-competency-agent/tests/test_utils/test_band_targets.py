"""Band -> proficiency target validator."""

from src.schemas.competency import LevelCode
from src.utils import band_targets


def test_get_target_levels_known_band():
    levels = band_targets.get_target_levels("Professional")
    assert LevelCode.L2 in levels


def test_get_target_levels_unknown_band():
    assert band_targets.get_target_levels("MadeUpBand") == []


def test_validate_match():
    ok, _ = band_targets.validate_job_band("Professional", [LevelCode.L2])
    assert ok is True


def test_validate_mismatch_warns():
    ok, msg = band_targets.validate_job_band("Associate", [LevelCode.L4])
    assert ok is False
    assert "L4" in msg or "associate" in msg.lower() or "outside" in msg.lower() or msg
