"""Continuous tracing infrastructure (spec §30).

Append-only JSONL ledgers that record every run, step transition, gated
decision, and field-level change across the lifetime of the system.

Public API:
    record_run_start(run_id, type_, stage, family) -> Path
    record_run_complete(run_id, agents_run, gates, artifacts_produced, flag_summary)
    record_step_enter(run_id, step, fingerprint=None)
    record_step_exit(run_id, step, fingerprint=None)
    record_decision(run_id, decision, **fields)
    record_change(run_id, competency_id, field, before, after, source, rationale)
    record_review(review_id, findings, severity_counts, prs_opened)
"""

from src.tracing.change_log import record_change
from src.tracing.decision_log import record_decision
from src.tracing.review_log import record_review
from src.tracing.run_ledger import record_run_complete, record_run_start
from src.tracing.step_log import record_step_enter, record_step_exit

__all__ = [
    "record_change",
    "record_decision",
    "record_review",
    "record_run_complete",
    "record_run_start",
    "record_step_enter",
    "record_step_exit",
]
