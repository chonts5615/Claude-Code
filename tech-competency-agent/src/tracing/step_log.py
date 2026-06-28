"""Orchestrator step transition log (spec §30.2).

Append a record on every phase entry / exit so we can reconstruct the exact
sequence of nodes the LangGraph DAG executed for any run.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.tracing.ledger import append_line

_LEDGER_FILE = "step_log.jsonl"


def record_step_enter(
    run_id: str,
    step: str,
    *,
    fingerprint: Optional[str] = None,
    root: Optional[Path] = None,
) -> Path:
    return append_line(
        _LEDGER_FILE,
        {"run_id": run_id, "step": step, "event": "enter", "fingerprint": fingerprint},
        root=root,
    )


def record_step_exit(
    run_id: str,
    step: str,
    *,
    fingerprint: Optional[str] = None,
    root: Optional[Path] = None,
) -> Path:
    return append_line(
        _LEDGER_FILE,
        {"run_id": run_id, "step": step, "event": "exit", "fingerprint": fingerprint},
        root=root,
    )
