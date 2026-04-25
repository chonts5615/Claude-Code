"""Source integrity tagging (CONFIRMED / CORRECTED / UNVERIFIABLE / FLAGGED)."""

from __future__ import annotations

from src.schemas.competency import IntegrityTag

_CONFIRMED_THRESHOLD = 0.85
_UNVERIFIABLE_THRESHOLD = 0.50


def tag_from_confidence(
    confidence: float,
    was_corrected: bool = False,
    was_flagged: bool = False,
) -> IntegrityTag:
    if was_flagged:
        return "FLAGGED"
    if was_corrected:
        return "CORRECTED"
    if confidence >= _CONFIRMED_THRESHOLD:
        return "CONFIRMED"
    if confidence >= _UNVERIFIABLE_THRESHOLD:
        return "UNVERIFIABLE"
    return "FLAGGED"
