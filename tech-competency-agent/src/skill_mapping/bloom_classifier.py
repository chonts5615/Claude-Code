"""SM3 — Bloom-aligned proficiency-level classifier for training items.

Heuristic-first: count verb hits per L1..L4 lexicon, then apply rule-based
adjustments for duration / modality / prerequisites / audience band. LLM
tie-break is *flagged* (adjustments_applied) but not invoked here — call sites
handle the actual model dispatch.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import yaml
from rapidfuzz import fuzz

from src.schemas.competency import LevelCode
from src.skill_mapping.schemas import BloomLevelEstimate, TrainingItem
from src.utils.band_targets import get_target_levels

_DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[2] / "config" / "bloom_verbs.yaml"
)

_LEVEL_ORDER: list[LevelCode] = [
    LevelCode.L1,
    LevelCode.L2,
    LevelCode.L3,
    LevelCode.L4,
]
_TOKEN_RE = re.compile(r"\b([a-zA-Z]{3,})\b")


@lru_cache(maxsize=1)
def _load_lexicon(path: str | None = None) -> dict[LevelCode, list[str]]:
    cfg_path = Path(path) if path else _DEFAULT_CONFIG_PATH
    if not cfg_path.exists():
        return {lvl: [] for lvl in _LEVEL_ORDER}
    with cfg_path.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}
    lexicon: dict[LevelCode, list[str]] = {}
    for lvl in _LEVEL_ORDER:
        lexicon[lvl] = [v.lower().strip() for v in (raw.get(lvl.value) or [])]
    return lexicon


def _tokens(text: str) -> list[str]:
    return [m.group(1).lower() for m in _TOKEN_RE.finditer(text or "")]


def _matches(token: str, lexicon: list[str]) -> str | None:
    """Return the matched lexicon verb (or None) for one token."""
    # Stem-trim trailing common inflections to widen lexical hits.
    candidates = {token}
    for suffix in ("ing", "ed", "es", "s"):
        if token.endswith(suffix) and len(token) > len(suffix) + 2:
            candidates.add(token[: -len(suffix)])
    for cand in candidates:
        if cand in lexicon:
            return cand
    # Fuzzy fallback (catches typos like "analize" → "analyze").
    for verb in lexicon:
        if fuzz.ratio(token, verb) >= 85:
            return verb
    return None


def _shift(level: LevelCode, delta: int) -> LevelCode:
    idx = _LEVEL_ORDER.index(level)
    new_idx = max(0, min(len(_LEVEL_ORDER) - 1, idx + delta))
    return _LEVEL_ORDER[new_idx]


def _snap_to_band(level: LevelCode, targets: list[LevelCode]) -> LevelCode:
    if not targets:
        return level
    target_idxs = sorted(_LEVEL_ORDER.index(t) for t in targets)
    cur = _LEVEL_ORDER.index(level)
    if target_idxs[0] <= cur <= target_idxs[-1]:
        return level
    if cur < target_idxs[0]:
        return _LEVEL_ORDER[target_idxs[0]]
    return _LEVEL_ORDER[target_idxs[-1]]


def classify(item: TrainingItem, llm_tiebreak: bool = True) -> BloomLevelEstimate:
    lexicon = _load_lexicon()

    text_chunks = [item.description] + list(item.learning_objectives)
    tokens = []
    for chunk in text_chunks:
        tokens.extend(_tokens(chunk))

    counts: dict[LevelCode, int] = {lvl: 0 for lvl in _LEVEL_ORDER}
    evidence: list[str] = []
    for tok in tokens:
        for lvl in _LEVEL_ORDER:
            hit = _matches(tok, lexicon[lvl])
            if hit:
                counts[lvl] += 1
                if hit not in evidence:
                    evidence.append(hit)
                break  # one verb counts at one level only

    total_hits = sum(counts.values())
    if total_hits == 0:
        base = LevelCode.L2
    else:
        max_count = max(counts.values())
        leaders = [lvl for lvl in _LEVEL_ORDER if counts[lvl] == max_count]
        # Default to L2 on a flat tie; otherwise pick the lowest leader so we
        # don't over-claim seniority on noisy inputs.
        if len(leaders) > 1 and counts[LevelCode.L2] == max_count:
            base = LevelCode.L2
        else:
            base = leaders[0]

    adjustments: list[str] = []
    level = base

    # Duration × modality nudges.
    if item.duration_hours and item.duration_hours < 2 and item.modality == "ELEARNING":
        new_level = _shift(level, -1)
        if new_level != level:
            adjustments.append("DURATION_SHORT_ELEARNING_DOWNSHIFT")
            level = new_level
    if item.modality in ("COACHING", "OJT") and item.duration_hours > 16:
        new_level = _shift(level, +1)
        if new_level != level:
            adjustments.append("LONG_COACHING_OJT_UPSHIFT")
            level = new_level
    if item.prerequisites:
        new_level = _shift(level, +1)
        if new_level != level:
            adjustments.append("PREREQUISITES_UPSHIFT")
            level = new_level

    # Audience-band snap.
    if item.audience_band:
        targets = get_target_levels(item.audience_band)
        snapped = _snap_to_band(level, targets)
        if snapped != level:
            adjustments.append("AUDIENCE_BAND_SNAP")
            level = snapped

    # Tie-break flag (no LLM call yet — caller handles dispatch).
    sorted_counts = sorted(counts.values(), reverse=True)
    needs_tiebreak = (
        total_hits > 0
        and len(sorted_counts) >= 2
        and (sorted_counts[0] - sorted_counts[1]) <= 1
        and llm_tiebreak
    )
    if needs_tiebreak:
        adjustments.append("LLM_TIEBREAK_NEEDED")

    # Confidence assembly.
    verb_signal = (max(counts.values()) / total_hits) if total_hits else 0.0
    verb_signal = max(0.0, min(1.0, verb_signal))
    duration_signal = 0.7
    modality_signal = 0.7
    llm_agreement = 0.5 if needs_tiebreak else 1.0
    confidence = (
        0.4 * verb_signal
        + 0.2 * duration_signal
        + 0.2 * modality_signal
        + 0.2 * llm_agreement
    )
    confidence = max(0.0, min(1.0, confidence))

    return BloomLevelEstimate(
        level=level,
        confidence=confidence,
        evidence_verbs=evidence,
        verb_counts={lvl.value: counts[lvl] for lvl in _LEVEL_ORDER},
        adjustments_applied=adjustments,
    )
