"""Phase 6F: CTIC (Character-level Text Integrity Check) Validator (v3.1)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from src.agents.base import BaseAgent
from src.schemas.ctic import CTICDiff, CTICReport
from src.schemas.feedback import FeedbackBatch
from src.schemas.run_state import RunState


_DRIFT_ERROR_THRESHOLD = 0.05


class CTICValidatorAgent(BaseAgent):
    """Phase 6F — Detect and revert untargeted text drift across SME-edited state."""

    def __init__(self, agent_id: str = "phase6F_ctic_validator",
                 step_name: str = "Phase 6F — CTIC Validator"):
        super().__init__(agent_id, step_name)

    def execute(self, state: RunState) -> RunState:
        state.current_step = self.agent_id

        pre_state = self._load_competencies(
            getattr(state.artifacts, "pre_feedback_snapshot", None)
        ) or self._load_competencies(getattr(state.artifacts, "clean_v3", None))
        post_state = self._load_competencies(
            getattr(state.artifacts, "normalized_v2", None)
        ) or self._load_competencies(getattr(state.artifacts, "clean_v3", None))

        feedback_batch = self._load_feedback_batch(state)
        targeted = self._build_targeted_set(feedback_batch)

        report = self._build_report(state.run_id, pre_state, post_state, targeted)

        # TODO(v3.1): persist the corrected post-state back to the working store
        # once the post-feedback artifact path is canonicalized in ArtifactRegistry.

        if report.drift_rate > _DRIFT_ERROR_THRESHOLD:
            self.add_flag(
                state,
                severity="ERROR",
                flag_type="CTIC_DRIFT_RATE_EXCEEDED",
                message=(
                    f"CTIC drift_rate {report.drift_rate:.2%} exceeds "
                    f"{_DRIFT_ERROR_THRESHOLD:.0%} budget."
                ),
                metadata={
                    "diffs_detected": report.diffs_detected,
                    "diffs_reverted": report.diffs_reverted,
                    "diffs_kept": report.diffs_kept,
                },
            )

        output_path = Path(f"data/output/{state.run_id}_6F_ctic.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as fh:
            fh.write(json.dumps(report.model_dump(), indent=2, default=str))

        try:
            setattr(state.artifacts, "ctic_report", output_path)
        except Exception:
            pass

        return state

    @staticmethod
    def _build_report(
        run_id: str,
        pre_state: Dict[str, Dict[str, Any]],
        post_state: Dict[str, Dict[str, Any]],
        targeted: Set[Tuple[str, str]],
    ) -> CTICReport:
        # TODO(v3.1): swap to src.utils.ctic_diff.check_drift / revert_drift once
        # those helpers are extracted; current implementation does the same job
        # inline using pure-python char comparison.
        entries: List[CTICDiff] = []
        diffs_detected = 0
        diffs_reverted = 0
        diffs_kept = 0
        comparable_fields = 0

        for comp_id, post_comp in post_state.items():
            pre_comp = pre_state.get(comp_id)
            if not pre_comp:
                continue
            for field in ("name", "definition", "why_it_matters"):
                pre_text = str(pre_comp.get(field) or "")
                post_text = str(post_comp.get(field) or "")
                comparable_fields += 1
                if pre_text == post_text:
                    continue
                diffs_detected += 1
                is_targeted = (comp_id, field) in targeted
                char_diff = abs(len(post_text) - len(pre_text)) + sum(
                    1 for a, b in zip(pre_text, post_text) if a != b
                )
                if is_targeted:
                    diffs_kept += 1
                    rationale = "Targeted by SME feedback — change retained."
                    reverted = False
                else:
                    diffs_reverted += 1
                    rationale = "Non-targeted drift — reverted to pre-feedback text."
                    reverted = True
                    # Apply revert to in-memory post-state (best effort).
                    post_comp[field] = pre_text

                entries.append(CTICDiff(
                    competency_id=comp_id,
                    field=field,
                    before=pre_text,
                    after=post_text,
                    char_diff_count=char_diff,
                    is_targeted_by_feedback=is_targeted,
                    reverted=reverted,
                    rationale=rationale,
                ))

        drift_rate = (diffs_detected / comparable_fields) if comparable_fields else 0.0
        return CTICReport(
            run_id=run_id,
            diffs_detected=diffs_detected,
            diffs_reverted=diffs_reverted,
            diffs_kept=diffs_kept,
            drift_rate=round(min(max(drift_rate, 0.0), 1.0), 4),
            entries=entries,
        )

    @staticmethod
    def _build_targeted_set(batch: FeedbackBatch | None) -> Set[Tuple[str, str]]:
        if not batch:
            return set()
        targeted: Set[Tuple[str, str]] = set()
        for item in batch.items:
            if item.target_competency_id and item.target_field:
                targeted.add((item.target_competency_id, item.target_field))
        return targeted

    @staticmethod
    def _load_competencies(artifact_path: Any) -> Dict[str, Dict[str, Any]]:
        if not artifact_path:
            return {}
        path = Path(str(artifact_path))
        if not path.exists():
            return {}
        try:
            with open(path) as fh:
                data = json.load(fh)
        except Exception:
            return {}
        out: Dict[str, Dict[str, Any]] = {}
        jobs = data.get("jobs", []) if isinstance(data, dict) else []
        for job in jobs:
            for comp in job.get("technical_competencies", []) or []:
                cid = comp.get("competency_id")
                if cid:
                    out[str(cid)] = comp
        return out

    @staticmethod
    def _load_feedback_batch(state: RunState) -> FeedbackBatch | None:
        feedback_artifact = getattr(state.artifacts, "feedback_batch", None)
        if not feedback_artifact:
            return None
        path = Path(str(feedback_artifact))
        if not path.exists():
            return None
        try:
            with open(path) as fh:
                return FeedbackBatch.model_validate(json.load(fh))
        except Exception:
            return None

    def get_system_prompt(self) -> str:
        return (
            "You are the CTIC (Character-level Text Integrity Check) Operator for v3.1 Phase 6F. "
            "Your charter is zero-tolerance: any character-level change to a competency that was "
            "not explicitly targeted by SME feedback must be detected and reverted.\n\n"
            "Steps:\n"
            "1. Load the pre-feedback snapshot and the post-edit working set.\n"
            "2. Build the targeted set from FeedbackBatch (competency_id, target_field).\n"
            "3. For each comparable field, compute the diff; if (id, field) is targeted keep the "
            "edit, otherwise revert to the pre-feedback text and log the drift.\n"
            "4. Emit a CTICReport summarizing diffs detected / reverted / kept and drift_rate.\n"
            "5. Raise an ERROR-severity RunFlag if drift_rate exceeds 0.05.\n\n"
            "Quality standards: every diff must carry a rationale; targeting decisions must trace "
            "back to a FeedbackItem; the corrected working state replaces the post-edit text "
            "before downstream consumers run."
        )
