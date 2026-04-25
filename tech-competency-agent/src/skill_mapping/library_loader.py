"""SM2 — Master Library (v3.1, 23-column xlsx) loader."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.schemas.library import LIBRARY_COLUMNS

PIPE_DELIMITED_FIELDS = {
    "L1_indicators",
    "L2_indicators",
    "L3_indicators",
    "L4_indicators",
    "applied_tools",
    "applied_standards",
    "applied_outputs",
    "source_refs",
    "rosetta_aliases",
}


def _split_pipe(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none"}:
        return []
    return [p.strip() for p in text.split("|") if p.strip()]


def load_library(path: Path | str) -> list[dict]:
    """Load the 23-column Master Library xlsx into list of dicts.

    Pipe-delimited indicator/source fields are split back into lists.
    Missing optional columns are filled with empty defaults.
    """
    p = Path(path)
    df = pd.read_excel(p, dtype=object, engine="openpyxl")
    df.columns = [str(c).strip() for c in df.columns]

    # Reindex against canonical 23-column order so downstream consumers can
    # rely on shape; absent columns become NaN.
    df = df.reindex(columns=LIBRARY_COLUMNS)

    entries: list[dict] = []
    for _, row in df.iterrows():
        entry: dict = {}
        for col in LIBRARY_COLUMNS:
            raw = row.get(col)
            if col in PIPE_DELIMITED_FIELDS:
                entry[col] = _split_pipe(raw)
            else:
                if raw is None or (isinstance(raw, float) and pd.isna(raw)):
                    entry[col] = ""
                else:
                    entry[col] = str(raw).strip()
        if entry["competency_id"]:
            entries.append(entry)
    return entries


def competency_match_text(entry: dict) -> str:
    """Concatenated text used as the similarity target for one competency."""
    name = entry.get("name", "") or ""
    definition = entry.get("definition", "") or ""
    indicators: list[str] = []
    for key in ("L1_indicators", "L2_indicators", "L3_indicators", "L4_indicators"):
        indicators.extend(entry.get(key, []) or [])
    return f"{name}. {definition} {' '.join(indicators)}".strip()
