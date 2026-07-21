"""Review-cycle log (spec §31.4).

Every review-and-update cycle (triggered by PR, FINAL completion, quarterly, or
operator request) appends one record.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.tracing.ledger import append_line

_LEDGER_FILE = "review_log.jsonl"


def record_review(
    review_id: str,
    *,
    findings: Optional[List[Dict[str, Any]]] = None,
    severity_counts: Optional[Dict[str, int]] = None,
    prs_opened: Optional[List[str]] = None,
    triggered_by: str = "OPERATOR",
    root: Optional[Path] = None,
) -> Path:
    payload = {
        "review_id": review_id,
        "triggered_by": triggered_by,
        "completed_at_utc": datetime.utcnow().isoformat() + "Z",
        "severity_counts": dict(severity_counts or {}),
        "prs_opened": list(prs_opened or []),
        "finding_count": len(findings or []),
        "findings": list(findings or []),
    }
    return append_line(_LEDGER_FILE, payload, root=root)
