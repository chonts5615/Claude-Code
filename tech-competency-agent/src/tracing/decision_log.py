"""Gated-decision log (spec §30.3).

Each gated decision the system makes — 5QMT verdict, boundary classification,
criticality rank, feedback disposition, CTIC revert vs keep — appends one
JSONL row keyed by `decision`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from src.tracing.ledger import append_line

_LEDGER_FILE = "decision_log.jsonl"

_KNOWN_DECISIONS = frozenset({
    "5QMT",
    "BOUNDARY",
    "CRITICALITY_RANK",
    "FEEDBACK_DISPOSITION",
    "CTIC",
    "COVERAGE_REFRESH",
    "BOUNDARY_RESCAN",
    "OVERLAP_REAUDIT",
    "BLOOM_LEVEL",
    "MAPPING_CONFIDENCE",
})


def record_decision(
    run_id: str,
    decision: str,
    *,
    root: Optional[Path] = None,
    **fields: Any,
) -> Path:
    """Append one decision record. `decision` should be one of `_KNOWN_DECISIONS`
    but unknown values are accepted (logged with the literal kind)."""
    payload = {"run_id": run_id, "decision": decision}
    payload.update(fields)
    return append_line(_LEDGER_FILE, payload, root=root)


def known_decisions() -> frozenset[str]:
    return _KNOWN_DECISIONS
