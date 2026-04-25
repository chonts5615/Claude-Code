"""SM5 — Resolve final SkillCompetencyMapping rows from candidates + bloom."""

from __future__ import annotations

from src.schemas.competency import IntegrityTag
from src.skill_mapping.schemas import (
    BloomLevelEstimate,
    SkillCompetencyMapping,
    TrainingItem,
)
from src.utils.band_targets import get_target_levels


def _integrity(similarity: float, bloom_conf: float) -> IntegrityTag:
    if similarity >= 0.70 and bloom_conf >= 0.6:
        return "CONFIRMED"
    if 0.55 <= similarity < 0.70:
        return "UNVERIFIABLE"
    return "FLAGGED"


def _band_mismatch(item: TrainingItem, course_level) -> bool:
    if not item.audience_band:
        return False
    targets = get_target_levels(item.audience_band)
    if not targets:
        return False
    return course_level not in targets


def resolve(
    item: TrainingItem,
    candidates: list[tuple[dict, float]],
    bloom: BloomLevelEstimate,
    llm_tiebreak: bool = True,
) -> list[SkillCompetencyMapping]:
    mappings: list[SkillCompetencyMapping] = []
    needs_tiebreak = "LLM_TIEBREAK_NEEDED" in bloom.adjustments_applied
    llm_agreement = 0.5 if (needs_tiebreak and llm_tiebreak) else 1.0

    for entry, similarity in candidates:
        mapping_conf = 0.5 * similarity + 0.3 * bloom.confidence + 0.2 * llm_agreement
        mapping_conf = max(0.0, min(1.0, mapping_conf))

        integrity = _integrity(similarity, bloom.confidence)

        flags: list[str] = []
        if _band_mismatch(item, bloom.level):
            flags.append("AUDIENCE_BAND_LEVEL_MISMATCH")
        if needs_tiebreak:
            flags.append("BLOOM_LLM_TIEBREAK_NEEDED")

        evidence_str = ", ".join(bloom.evidence_verbs) if bloom.evidence_verbs else "—"
        rationale = (
            f"Course objectives use [{evidence_str}] ({bloom.level.value}); "
            f"competency definition matched with {similarity:.2f} cosine similarity."
        )

        mappings.append(
            SkillCompetencyMapping(
                course_id=item.course_id,
                competency_id=entry.get("competency_id", ""),
                competency_name=entry.get("name", ""),
                level=bloom.level,
                confidence=mapping_conf,
                rationale=rationale,
                bloom_evidence=list(bloom.evidence_verbs),
                similarity_score=similarity,
                integrity_tag=integrity,
                mismatch_flags=flags,
            )
        )
    return mappings
