"""Cross-run field-level change history (spec §30.4).

Supplements the per-run `Change_Log.xlsx` (§18.2) — the xlsx is a snapshot
deliverable; this JSONL is the rolling system of record.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal, Optional

from src.tracing.ledger import append_line

_LEDGER_FILE = "change_log.jsonl"

ChangeSource = Literal["SME", "CTIC", "AUTO", "MIGRATION", "LIBRARY_MERGER"]


def record_change(
    run_id: str,
    competency_id: str,
    field: str,
    before: str,
    after: str,
    *,
    source: ChangeSource,
    rationale: str = "",
    root: Optional[Path] = None,
) -> Path:
    """Append one field-level change event."""
    return append_line(
        _LEDGER_FILE,
        {
            "run_id": run_id,
            "competency_id": competency_id,
            "field": field,
            "before": before,
            "after": after,
            "source": source,
            "rationale": rationale,
        },
        root=root,
    )
