"""Phase 6E-quater: Overlap Re-audit Agent (v3.1)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from src.agents.base import BaseAgent
from src.schemas.bco_ledger import BCOLedger, OverlapEntry
from src.schemas.run_state import RunState
from src.utils.similarity import compute_pairwise_similarity


_MATERIAL_THRESHOLD = 0.82
_MINOR_THRESHOLD = 0.72
_REGRESSION_DELTA = 0.05


class OverlapReauditAgent(BaseAgent):
    """Phase 6E-quater — Recompute pairwise overlap and compare to pre-feedback snapshot."""

    def __init__(self, agent_id: str = "phase6E_quater_overlap_reaudit",
                 step_name: str = "Phase 6E-quater — Overlap Re-audit"):
        super().__init__(agent_id, step_name)

    def execute(self, state: RunState) -> RunState:
        state.current_step = self.agent_id

        competencies = self._load_competencies(state)
        prior_overlap = self._load_prior_overlap(state)

        ids: List[str] = []
        names: List[str] = []
        definitions: List[str] = []
        for comp in competencies:
            ids.append(str(comp.get("competency_id") or ""))
            names.append(str(comp.get("name") or ""))
            definitions.append(str(comp.get("definition") or ""))

        entries: List[OverlapEntry] = []
        if len(definitions) >= 2:
            # TODO(v3.1): integrate LLM judgment to short-circuit obvious non-overlap pairs
            matrix = compute_pairwise_similarity(definitions)
            n = len(definitions)
            for i in range(n):
                for j in range(i + 1, n):
                    score = float(matrix[i, j])
                    severity = self._severity(score)
                    if severity == "NONE":
                        continue
                    entry = OverlapEntry(
                        competency_id_a=ids[i],
                        competency_id_b=ids[j],
                        similarity_score=round(score, 4),
                        severity=severity,
                        resolution=None,
                    )
                    entries.append(entry)

                    pair_key = self._pair_key(ids[i], ids[j])
                    prior_score = prior_overlap.get(pair_key)
                    if prior_score is None and severity == "MATERIAL":
                        self.add_flag(
                            state,
                            severity="WARNING",
                            flag_type="NEW_MATERIAL_OVERLAP",
                            message=(
                                f"New MATERIAL overlap between {ids[i]} and {ids[j]} "
                                f"(score {score:.3f})."
                            ),
                            metadata={"pair": [ids[i], ids[j]], "score": score},
                        )
                    elif prior_score is not None and (score - prior_score) >= _REGRESSION_DELTA:
                        self.add_flag(
                            state,
                            severity="WARNING",
                            flag_type="OVERLAP_REGRESSION",
                            message=(
                                f"Overlap worsened for {ids[i]} / {ids[j]}: "
                                f"{prior_score:.3f} -> {score:.3f}."
                            ),
                            metadata={
                                "pair": [ids[i], ids[j]],
                                "prior": prior_score,
                                "current": score,
                                "delta": round(score - prior_score, 4),
                            },
                        )

        ledger = self._load_or_init_ledger(state, stage="6E_quater")
        ledger.overlap = entries
        ledger.timestamp_utc = datetime.utcnow().isoformat()

        output_path = Path(f"data/output/{state.run_id}_6E_quater_overlap.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as fh:
            fh.write(json.dumps(ledger.model_dump(), indent=2, default=str))

        try:
            setattr(state.artifacts, "bco_ledger", output_path)
        except Exception:
            pass

        return state

    @staticmethod
    def _severity(score: float) -> str:
        if score >= _MATERIAL_THRESHOLD:
            return "MATERIAL"
        if score >= _MINOR_THRESHOLD:
            return "MINOR"
        return "NONE"

    @staticmethod
    def _pair_key(a: str, b: str) -> Tuple[str, str]:
        return tuple(sorted((a, b)))  # type: ignore[return-value]

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

    def _load_prior_overlap(self, state: RunState) -> Dict[Tuple[str, str], float]:
        prior: Dict[Tuple[str, str], float] = {}
        existing = getattr(state.artifacts, "bco_ledger", None)
        if not existing:
            return prior
        path = Path(str(existing))
        if not path.exists():
            return prior
        try:
            with open(path) as fh:
                data = json.load(fh)
        except Exception:
            return prior
        for entry in data.get("overlap", []) or []:
            key = self._pair_key(
                str(entry.get("competency_id_a", "")),
                str(entry.get("competency_id_b", "")),
            )
            prior[key] = float(entry.get("similarity_score", 0.0))
        return prior

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
            "You are the Overlap Re-audit Operator for v3.1 Phase 6E-quater. After SME edits "
            "land, you recompute pairwise similarity across the surviving technical "
            "competencies and check whether the edit improved or worsened overlap.\n\n"
            "Steps:\n"
            "1. Load the post-feedback competency working set.\n"
            "2. Compute pairwise similarity over each competency's definition (and supporting text).\n"
            "3. Compare to the pre-feedback overlap snapshot stored on the BCOLedger.\n"
            "4. Emit a WARNING when a pair worsens by >= 0.05 or when a brand-new MATERIAL "
            "(>= 0.82) pair appears.\n"
            "5. Persist the updated BCOLedger overlap entries to the run artifact.\n\n"
            "Quality standards: scores stored to 4 decimals; thresholds applied consistently "
            "(MATERIAL >= 0.82, MINOR >= 0.72); deterministic ordering of pairs in output."
        )
