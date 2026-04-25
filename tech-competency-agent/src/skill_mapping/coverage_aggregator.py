"""SM6 — Aggregate mappings into a (competency × level) coverage matrix."""

from __future__ import annotations

from src.schemas.competency import LevelCode
from src.skill_mapping.schemas import CoverageCell, SkillCompetencyMapping

_LEVELS: list[LevelCode] = [LevelCode.L1, LevelCode.L2, LevelCode.L3, LevelCode.L4]


def aggregate(
    mappings: list[SkillCompetencyMapping],
    library: list[dict],
) -> list[CoverageCell]:
    by_key: dict[tuple[str, LevelCode], list[str]] = {}
    for m in mappings:
        by_key.setdefault((m.competency_id, m.level), []).append(m.course_id)

    cells: list[CoverageCell] = []
    for entry in library:
        cid = entry.get("competency_id", "")
        cname = entry.get("name", "")
        if not cid:
            continue
        for lvl in _LEVELS:
            course_ids = by_key.get((cid, lvl), [])
            cells.append(
                CoverageCell(
                    competency_id=cid,
                    competency_name=cname,
                    level=lvl,
                    course_ids=list(dict.fromkeys(course_ids)),
                    count=len(course_ids),
                    has_gap=len(course_ids) == 0,
                )
            )
    return cells
