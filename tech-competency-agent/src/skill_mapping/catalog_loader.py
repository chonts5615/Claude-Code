"""SM1 — L&D training catalog loader.

Accepts .xlsx (openpyxl) or .csv (pandas). Column names are matched
case-insensitively with rapidfuzz fuzzy matching to tolerate small spelling
variation in human-curated catalogs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
from rapidfuzz import fuzz, process

from src.skill_mapping.schemas import Modality, TrainingItem

CANONICAL_COLUMNS = {
    "course_id": ["course_id", "course id", "id", "courseid"],
    "title": ["title", "course_title", "name", "course name"],
    "description": ["description", "summary", "course_description", "abstract"],
    "learning_objectives": [
        "learning_objectives",
        "objectives",
        "learning objectives",
        "outcomes",
    ],
    "duration_hours": ["duration_hours", "duration", "hours", "length_hours"],
    "modality": ["modality", "delivery", "format", "delivery_method"],
    "audience_band": ["audience_band", "audience", "band", "target_band"],
    "prerequisites": ["prerequisites", "prereqs", "pre_requisites", "prerequisite"],
    "vendor": ["vendor", "provider", "supplier", "source"],
}

VALID_MODALITIES: set[str] = {"ELEARNING", "ILT", "COACHING", "OJT", "BLENDED"}


def _resolve_columns(actual: Iterable[str]) -> dict[str, str | None]:
    """Map canonical field → actual column name (or None if not present)."""
    actual_list = [a for a in actual]
    lower_map = {a.lower().strip(): a for a in actual_list}
    resolved: dict[str, str | None] = {}
    for canonical, aliases in CANONICAL_COLUMNS.items():
        hit: str | None = None
        for alias in aliases:
            if alias in lower_map:
                hit = lower_map[alias]
                break
        if hit is None:
            match = process.extractOne(
                canonical, list(lower_map.keys()), scorer=fuzz.ratio, score_cutoff=85
            )
            if match:
                hit = lower_map[match[0]]
        resolved[canonical] = hit
    return resolved


def _split_pipe_or_newline(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none"}:
        return []
    if "|" in text:
        parts = text.split("|")
    else:
        parts = text.splitlines()
    return [p.strip() for p in parts if p.strip()]


def _normalize_modality(value: object) -> Modality:
    if value is None:
        return "ELEARNING"
    raw = str(value).strip().upper().replace("-", "").replace(" ", "")
    aliases = {
        "ELEARNING": "ELEARNING",
        "ELRN": "ELEARNING",
        "ONLINE": "ELEARNING",
        "WBT": "ELEARNING",
        "ILT": "ILT",
        "INSTRUCTORLED": "ILT",
        "CLASSROOM": "ILT",
        "VILT": "ILT",
        "COACHING": "COACHING",
        "COACH": "COACHING",
        "OJT": "OJT",
        "ONTHEJOB": "OJT",
        "BLENDED": "BLENDED",
        "HYBRID": "BLENDED",
    }
    return aliases.get(raw, "ELEARNING")  # type: ignore[return-value]


def _coerce_float(value: object) -> float:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _read_dataframe(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, dtype=object, keep_default_na=False)
    if suffix in {".xlsx", ".xlsm"}:
        return pd.read_excel(path, dtype=object, engine="openpyxl")
    raise ValueError(f"Unsupported catalog file type: {suffix}")


def load_catalog(path: Path | str) -> tuple[list[TrainingItem], list[str]]:
    """Load training catalog from disk.

    Returns (items, warnings). Rows missing course_id are skipped with a warning.
    """
    p = Path(path)
    df = _read_dataframe(p)
    df.columns = [str(c) for c in df.columns]

    resolved = _resolve_columns(df.columns)
    warnings: list[str] = []
    if resolved["course_id"] is None:
        raise ValueError(
            f"Catalog {p.name} missing required column 'course_id' (no fuzzy match found)."
        )
    if resolved["title"] is None:
        warnings.append("No 'title' column resolved; titles will be empty strings.")

    items: list[TrainingItem] = []
    for idx, row in df.iterrows():
        course_id_raw = row.get(resolved["course_id"]) if resolved["course_id"] else None
        course_id = str(course_id_raw).strip() if course_id_raw is not None else ""
        if not course_id or course_id.lower() in {"nan", "none"}:
            warnings.append(f"Row {idx}: missing course_id — skipped.")
            continue

        title = (
            str(row.get(resolved["title"], "") or "").strip()
            if resolved["title"]
            else ""
        )
        description = (
            str(row.get(resolved["description"], "") or "").strip()
            if resolved["description"]
            else ""
        )
        objectives = (
            _split_pipe_or_newline(row.get(resolved["learning_objectives"]))
            if resolved["learning_objectives"]
            else []
        )
        duration = (
            _coerce_float(row.get(resolved["duration_hours"]))
            if resolved["duration_hours"]
            else 0.0
        )
        modality = (
            _normalize_modality(row.get(resolved["modality"]))
            if resolved["modality"]
            else "ELEARNING"
        )
        band_raw = (
            row.get(resolved["audience_band"]) if resolved["audience_band"] else None
        )
        audience_band = (
            str(band_raw).strip() if band_raw not in (None, "", "nan") else None
        )
        prereqs = (
            _split_pipe_or_newline(row.get(resolved["prerequisites"]))
            if resolved["prerequisites"]
            else []
        )
        vendor_raw = row.get(resolved["vendor"]) if resolved["vendor"] else None
        vendor = (
            str(vendor_raw).strip() if vendor_raw not in (None, "", "nan") else None
        )

        items.append(
            TrainingItem(
                course_id=course_id,
                title=title,
                description=description,
                learning_objectives=objectives,
                duration_hours=duration,
                modality=modality,
                audience_band=audience_band,
                prerequisites=prereqs,
                vendor=vendor,
            )
        )

    return items, warnings
