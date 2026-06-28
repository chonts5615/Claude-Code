"""Run-level ledger (spec §30.1).

One JSONL line per workflow run: TCB R1/R2/FINAL/RESUME or SKILL_MAPPING.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.tracing.ledger import append_line

_LEDGER_FILE = "run_ledger.jsonl"


def record_run_start(
    run_id: str,
    type_: str,
    *,
    stage: Optional[str] = None,
    family: Optional[str] = None,
    root: Optional[Path] = None,
) -> Path:
    """Emit a `RUN_START` record. Called once at the entry of every workflow run.

    `type_` is "TCB" or "SKILL_MAPPING".
    """
    payload: Dict[str, Any] = {
        "event": "RUN_START",
        "run_id": run_id,
        "type": type_,
        "stage": stage,
        "family": family,
        "started_at_utc": datetime.utcnow().isoformat() + "Z",
    }
    return append_line(_LEDGER_FILE, payload, root=root)


def record_run_complete(
    run_id: str,
    *,
    agents_run: Optional[List[str]] = None,
    gates: Optional[Dict[str, str]] = None,
    artifacts_produced: Optional[List[str]] = None,
    flag_summary: Optional[Dict[str, int]] = None,
    root: Optional[Path] = None,
) -> Path:
    """Emit a `RUN_COMPLETE` record. Called once at the exit of every workflow run."""
    payload: Dict[str, Any] = {
        "event": "RUN_COMPLETE",
        "run_id": run_id,
        "completed_at_utc": datetime.utcnow().isoformat() + "Z",
        "agents_run": list(agents_run or []),
        "gates": dict(gates or {}),
        "artifacts_produced": [str(p) for p in (artifacts_produced or [])],
        "flag_summary": dict(flag_summary or {}),
    }
    return append_line(_LEDGER_FILE, payload, root=root)
