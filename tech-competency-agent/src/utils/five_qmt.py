"""5-Question Match Test for Library reuse decisions (v3.1)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from src.schemas.competency import (
    AppliedScope,
    CompetencyLibraryEntry,
    TechnicalCompetency,
)
from src.utils.similarity import compute_similarity

_DEFINITION_SIM_THRESHOLD = 0.75
_SCOPE_OVERLAP_THRESHOLD = 0.5
_MAX_LEVEL_REWRITES = 1

Decision = Literal["REUSE", "ADAPT", "VARIANT", "NEW"]


class FiveQMTResult(BaseModel):
    score: int
    decision: Decision
    answers: dict
    rationale: str


def _norm(s: str) -> str:
    return s.strip().lower()


def _set(items: list[str]) -> set[str]:
    return {_norm(x) for x in items if x and x.strip()}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 0.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def _q1_same_domain(candidate: TechnicalCompetency, entry: CompetencyLibraryEntry, target_family: str) -> bool:
    entry_tags = _set(entry.tags)
    family_l = _norm(target_family)
    if family_l and family_l in entry_tags:
        return True
    cand_tokens = _set(candidate.applied_scope.tools_methods_tech)
    return bool(cand_tokens & entry_tags)


def _q2_same_scope(candidate: TechnicalCompetency, entry: CompetencyLibraryEntry, target_scope: AppliedScope) -> bool:
    target_tools = _set(target_scope.tools_methods_tech)
    entry_tools: set[str] = set()
    for lvl in entry.proficiency_levels:
        for ind in lvl.indicators:
            for token in ind.text.split():
                entry_tools.add(_norm(token))
    entry_tools |= _set(entry.tags)
    if not target_tools:
        return False
    overlap = _jaccard(target_tools, entry_tools)
    return overlap >= _SCOPE_OVERLAP_THRESHOLD


def _q3_levels_transfer(candidate: TechnicalCompetency, entry: CompetencyLibraryEntry) -> bool:
    if not entry.proficiency_levels:
        return False
    rewrites = 0
    by_level = {p.level: p for p in entry.proficiency_levels}
    for cand_level in candidate.proficiency_levels:
        entry_level = by_level.get(cand_level.level)
        if entry_level is None:
            rewrites += 1
            continue
        sim = compute_similarity(cand_level.description, entry_level.description)
        if sim < _DEFINITION_SIM_THRESHOLD:
            rewrites += 1
    return rewrites <= _MAX_LEVEL_REWRITES


def _q4_descriptor_transfers(candidate: TechnicalCompetency, entry: CompetencyLibraryEntry) -> bool:
    if not entry.definition or not candidate.definition:
        return False
    return compute_similarity(candidate.definition, entry.definition) >= _DEFINITION_SIM_THRESHOLD


def _q5_name_works(candidate: TechnicalCompetency, entry: CompetencyLibraryEntry, target_family: str) -> bool:
    name_l = _norm(entry.name)
    family_l = _norm(target_family)
    if family_l and family_l in name_l:
        return False
    cand_tokens = set(_norm(candidate.name).split())
    entry_tokens = set(name_l.split())
    if not cand_tokens or not entry_tokens:
        return False
    return _jaccard(cand_tokens, entry_tokens) >= 0.3


def _decide(score: int) -> Decision:
    if score == 5:
        return "REUSE"
    if score == 4:
        return "ADAPT"
    if score == 3:
        return "VARIANT"
    return "NEW"


def evaluate(
    candidate: TechnicalCompetency,
    library_entry: CompetencyLibraryEntry,
    target_family: str,
    target_scope: AppliedScope,
) -> FiveQMTResult:
    answers = {
        "Q1": _q1_same_domain(candidate, library_entry, target_family),
        "Q2": _q2_same_scope(candidate, library_entry, target_scope),
        "Q3": _q3_levels_transfer(candidate, library_entry),
        "Q4": _q4_descriptor_transfers(candidate, library_entry),
        "Q5": _q5_name_works(candidate, library_entry, target_family),
    }
    score = sum(1 for v in answers.values() if v)
    decision = _decide(score)
    rationale = (
        f"5QMT against library entry {library_entry.competency_id}: "
        f"Q1(domain)={answers['Q1']}, Q2(scope)={answers['Q2']}, "
        f"Q3(levels)={answers['Q3']}, Q4(descriptor)={answers['Q4']}, "
        f"Q5(name)={answers['Q5']} → score {score}/5 → {decision}."
    )
    return FiveQMTResult(score=score, decision=decision, answers=answers, rationale=rationale)
