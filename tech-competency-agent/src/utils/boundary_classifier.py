"""v3.1 boundary classifier (V&B / Common / Technical / Mixed)."""

from __future__ import annotations

import re
from typing import Iterable

from rapidfuzz import fuzz

from src.schemas.boundary import BoundaryClassification

_FUZZ_THRESHOLD = 85
_TOKEN_RETENTION_THRESHOLD = 0.7

# Heuristic seed list of domain-specific nouns. Used to detect "technical
# specificity" — extended via boundary_terms["common"] family terms at runtime.
_DOMAIN_NOUNS_SEED: tuple[str, ...] = (
    "regression", "pipeline", "centrifuge", "kubernetes", "kafka", "spark",
    "tensorflow", "pytorch", "sql", "etl", "elt", "airflow", "snowflake",
    "redshift", "hadoop", "kubernetes", "docker", "terraform", "ansible",
    "fermenter", "bioreactor", "chromatography", "spectrometer", "plc",
    "scada", "hvac", "siemens", "rockwell", "matlab", "simulink", "ansys",
    "solidworks", "autocad", "revit", "primavera", "sap", "oracle", "salesforce",
    "tableau", "powerbi", "looker", "dbt", "fivetran", "segment",
)

_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_\-]*")


def _tokens(text: str) -> list[str]:
    return _WORD_RE.findall(text)


def _join_text(name: str, definition: str, indicators: list[str]) -> str:
    return " ".join([name, definition, *indicators]).strip()


def _fuzzy_keyword_hits(text: str, keywords: Iterable[str]) -> list[str]:
    text_l = text.lower()
    hits: list[str] = []
    for kw in keywords:
        kw_l = kw.lower()
        if kw_l in text_l:
            hits.append(kw)
            continue
        if fuzz.partial_ratio(kw_l, text_l) >= _FUZZ_THRESHOLD:
            hits.append(kw)
    return hits


def _detect_domain_nouns(text: str, extra_nouns: Iterable[str]) -> list[str]:
    text_l = text.lower()
    found: list[str] = []
    candidates = set(n.lower() for n in _DOMAIN_NOUNS_SEED) | set(n.lower() for n in extra_nouns)
    for noun in candidates:
        if re.search(rf"\b{re.escape(noun)}\b", text_l):
            found.append(noun)
    return found


def _strip_nouns(text: str, nouns: Iterable[str]) -> str:
    out = text
    for n in nouns:
        out = re.sub(rf"\b{re.escape(n)}\b", " ", out, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", out).strip()


def _confidence(n_matches: int, scale: int = 5) -> float:
    if n_matches <= 0:
        return 0.0
    return min(1.0, 0.4 + 0.12 * n_matches) if n_matches < scale else 1.0


def classify_boundary(
    name: str,
    definition: str,
    indicators: list[str],
    boundary_terms: dict,
) -> BoundaryClassification:
    text = _join_text(name, definition, indicators)
    if not text:
        return BoundaryClassification(
            competency_id="",
            classification="TECHNICAL",
            confidence=0.0,
            matched_terms=[],
            domain_noun_test_passed=None,
            rationale="Empty input — defaulted to TECHNICAL with zero confidence.",
        )

    vb_terms = boundary_terms.get("v_and_b", {}) or {}
    common_terms = boundary_terms.get("common", {}) or {}

    vb_keywords: list[str] = []
    for kws in vb_terms.values():
        vb_keywords.extend(kws or [])

    common_keywords: list[str] = []
    common_family_terms: list[str] = []
    for family, kws in common_terms.items():
        common_family_terms.append(family)
        common_keywords.extend(kws or [])

    vb_hits = _fuzzy_keyword_hits(text, vb_keywords)
    common_hits = _fuzzy_keyword_hits(text, common_keywords)

    domain_nouns = _detect_domain_nouns(text, common_family_terms)
    has_domain_specificity = bool(domain_nouns)

    original_tokens = _tokens(text)
    stripped_text = _strip_nouns(text, domain_nouns)
    stripped_tokens = _tokens(stripped_text)
    retention_ratio = (
        len(stripped_tokens) / len(original_tokens) if original_tokens else 0.0
    )
    domain_noun_test_passed = retention_ratio >= _TOKEN_RETENTION_THRESHOLD

    matched: list[str] = list(dict.fromkeys(vb_hits + common_hits))

    if vb_hits and not has_domain_specificity:
        return BoundaryClassification(
            competency_id="",
            classification="V_AND_B",
            confidence=_confidence(len(vb_hits)),
            matched_terms=matched,
            domain_noun_test_passed=domain_noun_test_passed,
            rationale=(
                f"V&B keywords matched ({len(vb_hits)}) and no domain-specific noun "
                "detected; classified as V_AND_B."
            ),
        )

    if (vb_hits or common_hits) and has_domain_specificity:
        return BoundaryClassification(
            competency_id="",
            classification="MIXED",
            confidence=_confidence(len(vb_hits) + len(common_hits)),
            matched_terms=matched,
            domain_noun_test_passed=domain_noun_test_passed,
            rationale=(
                f"Both boundary keywords ({len(vb_hits) + len(common_hits)}) and domain "
                f"nouns ({domain_nouns}) present; classified as MIXED."
            ),
        )

    if common_hits and domain_noun_test_passed:
        return BoundaryClassification(
            competency_id="",
            classification="COMMON",
            confidence=_confidence(len(common_hits)),
            matched_terms=matched,
            domain_noun_test_passed=True,
            rationale=(
                f"Common keywords matched ({len(common_hits)}); after removing domain "
                f"nouns {domain_nouns} text retains {retention_ratio:.0%} of tokens — "
                "parses generically."
            ),
        )

    return BoundaryClassification(
        competency_id="",
        classification="TECHNICAL",
        confidence=_confidence(len(domain_nouns) or 1),
        matched_terms=matched,
        domain_noun_test_passed=domain_noun_test_passed,
        rationale=(
            f"Domain-specific nouns present ({domain_nouns or 'inferred'}); "
            "classified as TECHNICAL."
        ),
    )
