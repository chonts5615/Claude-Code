"""Phase 6 entry: SME Feedback Ingestion Agent (v3.1)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from src.agents.base import BaseAgent
from src.schemas.feedback import FeedbackBatch, FeedbackItem
from src.schemas.run_state import RunState

_REQUIRED_REVIEW_METADATA_FIELDS = ("reviewer", "review_date", "stage")
_VALID_DISPOSITIONS = {"KEEP", "EDIT", "GAP", "DISCUSS", "REJECT"}


class FeedbackIngestionAgent(BaseAgent):
    """Phase 6 — Ingest SME feedback file into a typed FeedbackBatch."""

    def __init__(self, agent_id: str = "phase6_feedback_ingestion",
                 step_name: str = "Phase 6 — Feedback Ingestion"):
        super().__init__(agent_id, step_name)

    def execute(self, state: RunState) -> RunState:
        state.current_step = self.agent_id

        feedback_file = getattr(state.inputs, "feedback_file", None)
        if feedback_file is None:
            self.add_flag(
                state,
                severity="ERROR",
                flag_type="MISSING_INPUT",
                message="state.inputs.feedback_file is not set; cannot ingest feedback.",
            )
            return state

        feedback_path = Path(str(feedback_file))
        if not feedback_path.exists():
            self.add_flag(
                state,
                severity="ERROR",
                flag_type="FEEDBACK_FILE_NOT_FOUND",
                message=f"Feedback file not found at {feedback_path}",
            )
            return state

        raw_payload = self._load_feedback(feedback_path)
        review_metadata: Dict[str, Any] = raw_payload.get("review_metadata", {}) or {}
        raw_items: List[Dict[str, Any]] = raw_payload.get("items", []) or []

        # REVIEW_METADATA gate
        missing_meta = [f for f in _REQUIRED_REVIEW_METADATA_FIELDS if not review_metadata.get(f)]
        if missing_meta:
            self.add_flag(
                state,
                severity="ERROR",
                flag_type="REVIEW_METADATA_GATE_FAILED",
                message=f"REVIEW_METADATA missing required fields: {missing_meta}",
                metadata={"missing_fields": missing_meta},
            )

        items: List[FeedbackItem] = []
        for idx, raw in enumerate(raw_items):
            disposition = str(raw.get("disposition") or "EDIT").upper()
            if disposition not in _VALID_DISPOSITIONS:
                # TODO(v3.1): integrate LLM judgment for disposition classification
                disposition = "EDIT"

            verbatim = (raw.get("verbatim_comment") or "").strip()
            if not verbatim:
                self.add_flag(
                    state,
                    severity="WARNING",
                    flag_type="MISSING_VERBATIM_COMMENT",
                    message=f"Feedback item {raw.get('feedback_id', idx)} lacks verbatim_comment.",
                    metadata={"feedback_id": raw.get("feedback_id", str(idx))},
                )

            items.append(FeedbackItem(
                feedback_id=str(raw.get("feedback_id") or f"FB_{idx:04d}"),
                sme_name=raw.get("sme_name"),
                sme_role=raw.get("sme_role"),
                target_competency_id=raw.get("target_competency_id"),
                target_field=raw.get("target_field"),
                target_level=raw.get("target_level"),
                verbatim_comment=verbatim or "(empty)",
                disposition=disposition,  # type: ignore[arg-type]
                proposed_text=raw.get("proposed_text"),
                rationale=raw.get("rationale"),
                is_anchor_sme=bool(raw.get("is_anchor_sme", False)),
            ))

        stage_value = str(raw_payload.get("stage") or review_metadata.get("stage") or "R2").upper()
        if stage_value not in ("R2", "FINAL"):
            stage_value = "R2"

        batch = FeedbackBatch(
            run_id=state.run_id,
            stage=stage_value,  # type: ignore[arg-type]
            family=str(raw_payload.get("family") or review_metadata.get("family") or "UNSPECIFIED"),
            items=items,
            review_metadata=review_metadata,
            received_timestamp_utc=raw_payload.get(
                "received_timestamp_utc", datetime.utcnow().isoformat()
            ),
        )

        output_path = Path(f"data/output/{state.run_id}_phase6_feedback.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as fh:
            fh.write(json.dumps(batch.model_dump(), indent=2, default=str))

        # Best-effort artifact pointer (ArtifactRegistry may not have this field yet).
        try:
            setattr(state.artifacts, "feedback_batch", output_path)
        except Exception:
            pass

        return state

    @staticmethod
    def _load_feedback(path: Path) -> Dict[str, Any]:
        suffix = path.suffix.lower()
        if suffix in (".json",):
            with open(path) as fh:
                return json.load(fh)

        if suffix in (".xlsx", ".xlsm"):
            try:
                import openpyxl  # local import to avoid hard dep at module load
            except ImportError as exc:  # pragma: no cover
                raise RuntimeError("openpyxl is required to ingest .xlsx feedback") from exc

            wb = openpyxl.load_workbook(path, data_only=True)
            sheet = wb.active
            headers = [str(c.value).strip() if c.value else "" for c in sheet[1]]
            items: List[Dict[str, Any]] = []
            review_metadata: Dict[str, Any] = {}
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not row or not any(row):
                    continue
                record = {h: v for h, v in zip(headers, row) if h}
                # Allow a single-row metadata sheet pattern: rows whose feedback_id
                # is 'METADATA' carry review_metadata fields.
                if str(record.get("feedback_id", "")).upper() == "METADATA":
                    review_metadata.update({k: v for k, v in record.items() if k != "feedback_id"})
                else:
                    items.append(record)
            wb.close()
            return {"items": items, "review_metadata": review_metadata}

        raise ValueError(f"Unsupported feedback file format: {suffix}")

    def get_system_prompt(self) -> str:
        return (
            "You are the SME Feedback Ingestion Operator for v3.1 Phase 6. Your job is to "
            "translate raw SME comments into a structured FeedbackBatch without paraphrasing "
            "any verbatim text and without losing review provenance.\n\n"
            "Steps:\n"
            "1. Load the feedback artifact (JSON or Excel) referenced by state.inputs.feedback_file.\n"
            "2. Verify REVIEW_METADATA gate fields ('reviewer', 'review_date', 'stage').\n"
            "3. Parse each comment into a FeedbackItem and classify disposition as one of "
            "KEEP / EDIT / GAP / DISCUSS / REJECT (default EDIT only when ambiguous).\n"
            "4. Preserve verbatim_comment text exactly; never edit or summarize it.\n"
            "5. Persist the FeedbackBatch JSON and update state.artifacts.feedback_batch.\n\n"
            "Quality standards: every item must carry a verbatim_comment; missing values raise "
            "WARNING flags. Anchor-SME edits are tagged so downstream agents can propagate them "
            "to shared competencies. Disposition labels must come from the controlled vocabulary."
        )
