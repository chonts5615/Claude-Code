"""SM7 — Gap & surplus reporting from coverage and mappings."""

from __future__ import annotations

from src.schemas.competency import LevelCode
from src.skill_mapping.schemas import (
    CoverageCell,
    GapFinding,
    SkillCompetencyMapping,
    SurplusFinding,
    TrainingItem,
)
from src.skill_mapping.library_loader import competency_match_text
from src.skill_mapping.semantic_matcher import _course_text  # noqa: F401 — reused
from src.utils.similarity import compute_similarity_batch


def _severity_for(level: LevelCode) -> str:
    if level in (LevelCode.L1, LevelCode.L2, LevelCode.L3):
        return "WARNING"
    return "INFO"


def _recommendation(comp_name: str, level: LevelCode, severity: str) -> str:
    if severity == "CRITICAL":
        return (
            f"No catalog coverage at any level for '{comp_name}'. Commission a "
            "foundational eLearning + ILT pair before next planning cycle."
        )
    if level == LevelCode.L4:
        return (
            f"L4 is typically advanced via OJT/coaching, not catalog. Confirm "
            f"'{comp_name}' has a coaching playbook or stretch-assignment guide."
        )
    return (
        f"Add or curate a {level.value} offering for '{comp_name}' "
        "(eLearning for L1/L2, ILT/blended for L3)."
    )


def report_gaps(
    coverage: list[CoverageCell],
    library: list[dict],  # noqa: ARG001 — kept for future per-competency context
) -> list[GapFinding]:
    by_comp: dict[str, list[CoverageCell]] = {}
    for cell in coverage:
        by_comp.setdefault(cell.competency_id, []).append(cell)

    findings: list[GapFinding] = []
    for cid, cells in by_comp.items():
        total_courses = sum(c.count for c in cells)
        comp_name = cells[0].competency_name if cells else cid
        if total_courses == 0:
            for cell in cells:
                findings.append(
                    GapFinding(
                        competency_id=cid,
                        competency_name=comp_name,
                        level=cell.level,
                        severity="CRITICAL",
                        recommendation=_recommendation(comp_name, cell.level, "CRITICAL"),
                    )
                )
            continue
        for cell in cells:
            if cell.has_gap:
                sev = _severity_for(cell.level)
                findings.append(
                    GapFinding(
                        competency_id=cid,
                        competency_name=comp_name,
                        level=cell.level,
                        severity=sev,
                        recommendation=_recommendation(comp_name, cell.level, sev),
                    )
                )
    return findings


def _max_similarity_per_item(
    items: list[TrainingItem], library: list[dict]
) -> dict[str, float]:
    """Compute the best similarity each item achieves against any competency."""
    if not items or not library:
        return {item.course_id: 0.0 for item in items}
    candidate_texts = [competency_match_text(e) for e in library]
    out: dict[str, float] = {}
    for item in items:
        ranked = compute_similarity_batch(_course_text(item), candidate_texts, top_k=1)
        out[item.course_id] = ranked[0][1] if ranked else 0.0
    return out


def report_surplus(
    mappings: list[SkillCompetencyMapping],
    items: list[TrainingItem],
    library: list[dict],
) -> list[SurplusFinding]:
    by_course: dict[str, list[SkillCompetencyMapping]] = {}
    for m in mappings:
        by_course.setdefault(m.course_id, []).append(m)

    unmapped_items = [i for i in items if i.course_id not in by_course]
    max_sim = _max_similarity_per_item(unmapped_items, library)

    findings: list[SurplusFinding] = []
    for item in unmapped_items:
        sim = max_sim.get(item.course_id, 0.0)
        if sim < 0.40:
            reason = "LIKELY_VB_OR_COMMON"
        elif sim < 0.55:
            reason = "NO_TECHNICAL_MATCH"
        else:
            # ≥0.55 but somehow no mapping — still flag as no-tech-match
            reason = "NO_TECHNICAL_MATCH"
        findings.append(
            SurplusFinding(
                course_id=item.course_id,
                title=item.title,
                reason=reason,
                max_similarity=sim,
            )
        )

    item_lookup = {i.course_id: i for i in items}
    for course_id, ms in by_course.items():
        if all("AUDIENCE_BAND_LEVEL_MISMATCH" in m.mismatch_flags for m in ms):
            best = max(m.similarity_score for m in ms)
            title = item_lookup[course_id].title if course_id in item_lookup else ""
            findings.append(
                SurplusFinding(
                    course_id=course_id,
                    title=title,
                    reason="AUDIENCE_LEVEL_MISMATCH",
                    max_similarity=best,
                )
            )

    return findings
