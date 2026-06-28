"""Master Skills Library + cross-run mergers (spec §28-30).

Public API:
    SKILLS_LIBRARY_COLUMNS — canonical 22-column schema
    SkillsLibraryEntry     — pydantic row model
    merge_skills_into_master(per_run_items, master_path, run_id) -> Path
    CROSSWALK_COLUMNS      — canonical rolling crosswalk columns
    CrosswalkEntry         — pydantic row model
    merge_crosswalk(per_run_mappings, master_path, run_id) -> Path
    merge_library_into_master(per_run_competencies, master_path, run_id) -> Path
"""

from src.skill_library.crosswalk_merger import (
    CROSSWALK_COLUMNS,
    CrosswalkEntry,
    merge_crosswalk,
)
from src.skill_library.library_merger import merge_library_into_master
from src.skill_library.skill_library import (
    SKILLS_LIBRARY_COLUMNS,
    SkillsLibraryEntry,
    merge_skills_into_master,
)

__all__ = [
    "CROSSWALK_COLUMNS",
    "CrosswalkEntry",
    "SKILLS_LIBRARY_COLUMNS",
    "SkillsLibraryEntry",
    "merge_crosswalk",
    "merge_library_into_master",
    "merge_skills_into_master",
]
