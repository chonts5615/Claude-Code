"""Job-band → target proficiency level helpers (v3.1)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from src.schemas.competency import LevelCode

_DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[2] / "config" / "band_proficiency_targets.yaml"
)


@lru_cache(maxsize=1)
def _load_config(path: str | None = None) -> dict:
    cfg_path = Path(path) if path else _DEFAULT_CONFIG_PATH
    if not cfg_path.exists():
        return {}
    with cfg_path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return data


def _coerce_level(value: str) -> LevelCode:
    v = value.strip().upper()
    return LevelCode(v)


def get_target_levels(band: str) -> list[LevelCode]:
    cfg = _load_config()
    bands = cfg.get("bands", {}) or {}
    entry = bands.get(band) or bands.get(band.upper()) or {}
    raw = entry.get("target_levels", []) if isinstance(entry, dict) else entry
    if not raw:
        return []
    return [_coerce_level(x) for x in raw]


def validate_job_band(band: str, demanded_levels: list[LevelCode]) -> tuple[bool, str]:
    targets = get_target_levels(band)
    if not targets:
        return False, f"No target levels configured for band {band!r}."

    target_set = set(targets)
    demanded_set = set(demanded_levels)
    missing = target_set - demanded_set
    extras = demanded_set - target_set

    if not missing and not extras:
        return True, f"Band {band!r}: demanded levels match target {sorted(t.value for t in targets)}."

    parts: list[str] = []
    if missing:
        parts.append(f"missing target levels {sorted(m.value for m in missing)}")
    if extras:
        parts.append(f"unexpected levels {sorted(e.value for e in extras)}")
    return False, f"Band {band!r}: " + "; ".join(parts) + "."
