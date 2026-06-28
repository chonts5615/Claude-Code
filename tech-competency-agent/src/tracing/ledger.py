"""Append-only JSONL ledger writer with file-locking semantics (spec §30).

All tracing files in `data/trace/*.jsonl` go through `append_line`.

Design constraints:
- Never rewrite an existing file.
- Always append a complete JSON line (newline-terminated).
- Always include `at_utc` ISO8601 timestamp unless caller supplies one.
- Tolerate process-level concurrency via `os.open(..., O_APPEND)` writes (atomic
  on POSIX for writes <= PIPE_BUF).
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


def _default_root() -> Path:
    return Path("data/trace")


def _utc_now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def append_line(
    filename: str,
    payload: Dict[str, Any],
    *,
    root: Optional[Path] = None,
    add_timestamp: bool = True,
) -> Path:
    """Append one JSON record to `data/trace/<filename>`.

    Returns the resolved path. Creates the parent directory if needed.
    """
    root = root or _default_root()
    root.mkdir(parents=True, exist_ok=True)
    path = root / filename

    record: Dict[str, Any] = dict(payload)
    if add_timestamp and "at_utc" not in record:
        record["at_utc"] = _utc_now_iso()

    line = json.dumps(record, default=str, sort_keys=False) + "\n"
    # O_APPEND guarantees atomicity for short writes on POSIX.
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, line.encode("utf-8"))
    finally:
        os.close(fd)
    return path


def read_all(filename: str, *, root: Optional[Path] = None) -> list[Dict[str, Any]]:
    """Read every record from a ledger. Returns [] if file is missing."""
    root = root or _default_root()
    path = root / filename
    if not path.exists():
        return []
    out: list[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            try:
                out.append(json.loads(raw))
            except json.JSONDecodeError:
                # Skip corrupt lines rather than crashing readers.
                continue
    return out
