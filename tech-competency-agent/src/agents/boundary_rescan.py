"""Phase 6E-ter: Boundary Rescan Agent (v3.1)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from src.agents.base import BaseAgent
from src.schemas.bco_ledger import BCOLedger, BoundaryEntry
from src.schemas.run_state import RunState
from src.utils.boundary_classifier import classify_boundary


class BoundaryRescanAgent(BaseAgent):
    """Phase 6E-ter — Rerun the V&B / Common / Technical / Mixed classifier."""

    def __init__(self, agent_id: str = "phase6E_ter_boundary_rescan",
                 step_name: str = "Phase 6E-ter — Boundary Rescan"):
        super().__init__(agent_id, step_name)

    def execute(self, state: RunState) -> RunState:
        state.current_step = self.agent_id

        competencies = self._load_competencies(state)
        boundary_terms = self._load_boundary_terms()

        entries: List[BoundaryEntry] = []
        for comp in competencies:
            comp_id = str(comp.get("competency_id") or "")
            name = str(comp.get("name") or "")
            definition = str(comp.get("definition") or "")
            indicator_texts = self._collect_indicator_texts(comp)
            current_class = comp.get("boundary_class")

            classification = classify_boundary(
                name=name,
                definition=definition,
                indicators=indicator_texts,
                boundary_terms=boundary_terms,
            )
            new_class = classification.classification

            entries.append(BoundaryEntry(
                competency_id=comp_id,
                competency_name=name,
                classification=new_class,
                confidence=classification.confidence,
                rationale=classification.rationale,
            ))

            if current_class and current_class != new_class:
                self.add_flag(
                    state,
                    severity="WARNING",
                    flag_type="BOUNDARY_RECLASSIFIED",
                    message=(
                        f"Competency {comp_id} reclassified {current_class} -> {new_class}."
                    ),
                    metadata={
                        "competency_id": comp_id,
                        "previous": current_class,
                        "current": new_class,
                        "confidence": classification.confidence,
                    },
                )

        ledger = self._load_or_init_ledger(state, stage="6E_ter")
        ledger.boundary = entries
        ledger.timestamp_utc = datetime.utcnow().isoformat()

        output_path = Path(f"data/output/{state.run_id}_6E_ter_boundary.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as fh:
            fh.write(json.dumps(ledger.model_dump(), indent=2, default=str))

        try:
            setattr(state.artifacts, "bco_ledger", output_path)
        except Exception:
            pass

        return state

    @staticmethod
    def _collect_indicator_texts(comp: Dict[str, Any]) -> List[str]:
        texts: List[str] = []
        for level in comp.get("proficiency_levels", []) or []:
            for ind in level.get("indicators", []) or []:
                if isinstance(ind, dict):
                    text = ind.get("text")
                    if text:
                        texts.append(str(text))
                elif isinstance(ind, str):
                    texts.append(ind)
        return texts

    @staticmethod
    def _load_competencies(state: RunState) -> List[Dict[str, Any]]:
        for attr in ("clean_v3", "normalized_v2", "competency_map_v1"):
            value = getattr(state.artifacts, attr, None)
            if not value:
                continue
            path = Path(str(value))
            if not path.exists():
                continue
            try:
                with open(path) as fh:
                    data = json.load(fh)
            except Exception:
                continue
            collected: List[Dict[str, Any]] = []
            jobs = data.get("jobs", []) if isinstance(data, dict) else []
            for job in jobs:
                collected.extend(job.get("technical_competencies", []) or [])
            if collected:
                return collected
        return []

    @staticmethod
    def _load_boundary_terms() -> Dict[str, Any]:
        # TODO(v3.1): load curated boundary_terms.yaml from data/reference; fall
        # back to a small default lexicon so the classifier still runs.
        ref_path = Path("data/reference/boundary_terms.json")
        if ref_path.exists():
            try:
                with open(ref_path) as fh:
                    return json.load(fh)
            except Exception:
                pass
        return {
            "v_and_b": {
                "leadership": ["leads", "coaches", "mentors", "influences"],
                "values": ["integrity", "ethics", "respect", "inclusion"],
            },
            "common": {
                "communication": ["communicates", "presents", "writes"],
                "collaboration": ["collaborates", "partners", "teamwork"],
            },
        }

    @staticmethod
    def _load_or_init_ledger(state: RunState, stage: str) -> BCOLedger:
        existing = getattr(state.artifacts, "bco_ledger", None)
        if existing:
            try:
                with open(Path(str(existing))) as fh:
                    return BCOLedger.model_validate(json.load(fh))
            except Exception:
                pass
        return BCOLedger(
            run_id=state.run_id,
            stage=stage,
            timestamp_utc=datetime.utcnow().isoformat(),
        )

    def get_system_prompt(self) -> str:
        return (
            "You are the Boundary Rescan Operator for v3.1 Phase 6E-ter. After SME edits, you "
            "rerun the boundary classifier (V&B / Common / Technical / Mixed) on every "
            "competency and surface anything that has crossed boundaries.\n\n"
            "Steps:\n"
            "1. Load the post-feedback competency working set.\n"
            "2. Run src.utils.boundary_classifier.classify_boundary on name + definition + indicators.\n"
            "3. Compare the new classification against the stored boundary_class.\n"
            "4. Emit a RunFlag whenever a competency was reclassified, recording the old and new label.\n"
            "5. Update the BCOLedger boundary entries and persist the JSON artifact.\n\n"
            "Quality standards: classification rationale must be human-readable; confidence "
            "scores must accompany every entry; do not silently overwrite the working state — "
            "the ledger is the system of record."
        )
