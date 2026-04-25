"""SM4 — Semantic matching of a training item to library competencies."""

from __future__ import annotations

from src.skill_mapping.library_loader import competency_match_text
from src.skill_mapping.schemas import TrainingItem
from src.utils.similarity import compute_similarity_batch


def _course_text(item: TrainingItem) -> str:
    objectives = " ".join(item.learning_objectives or [])
    return f"{item.title}. {item.description} Objectives: {objectives}".strip()


def match(
    item: TrainingItem,
    library: list[dict],
    top_k: int = 5,
    threshold: float = 0.55,
) -> list[tuple[dict, float]]:
    """Return library entries with similarity ≥ threshold, sorted desc, ≤top_k."""
    if not library:
        return []

    course_text = _course_text(item)
    candidate_texts = [competency_match_text(entry) for entry in library]

    # Pull *all* indices ranked, then filter by threshold and slice.
    ranked = compute_similarity_batch(course_text, candidate_texts, top_k=len(library))
    results: list[tuple[dict, float]] = []
    for idx, score in ranked:
        if score >= threshold:
            results.append((library[idx], score))
        if len(results) >= top_k:
            break
    return results
