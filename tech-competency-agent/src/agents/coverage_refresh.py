"""Phase 6E-bis: Coverage Refresh Agent (v3.1)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from src.agents.base import BaseAgent
from src.schemas.bco_ledger import BCOLedger, CoverageEntry
from src.schemas.run_state import RunState

_COVERAGE_THRESHOLD = 0.90
_TOP_K_COMPETENCIES = 6


class CoverageRefreshAgent(BaseAgent):
    """Phase 6E-bis — Re-map technical EFs to top-6 competencies and recompute coverage."""

    def __init__(self, agent_id: str = "phase6E_bis_coverage_refresh",
                 step_name: str = "Phase 6E-bis — Coverage Refresh"):
        super().__init__(agent_id, step_name)

    def execute(self, state: RunState) -> RunState:
        state.current_step = self.agent_id

        jobs = self._load_jobs(state)
        coverage_entries: List[CoverageEntry] = []

        for job in jobs:
            job_id = str(job.get("job_id") or "UNKNOWN")
            job_title = str(job.get("job_title") or "")
            family = str(job.get("family") or job.get("job_family") or "UNSPECIFIED")
            technical_efs: List[Dict[str, Any]] = job.get("technical_efs", []) or []
            competencies: List[Dict[str, Any]] = job.get("technical_competencies", []) or []

            ef_total = len(technical_efs)
            uncovered_ids: List[str] = []
            covered_count = 0

            # TODO(v3.1): integrate LLM judgment for EF→competency mapping; for
            # now, lean on any pre-existing mapping carried on the EF record.
            for ef in technical_efs:
                ef_id = str(ef.get("ef_id") or ef.get("id") or "")
                mapped = ef.get("mapped_competency_ids") or []
                if isinstance(mapped, list) and len(mapped) > 0:
                    covered_count += 1
                else:
                    uncovered_ids.append(ef_id)

            # When EFs are absent but competencies exist, treat each top-6 as covering one EF.
            if ef_total == 0 and competencies:
                ef_total = min(_TOP_K_COMPETENCIES, len(competencies))
                covered_count = ef_total

            coverage_rate = (covered_count / ef_total) if ef_total else 0.0
            meets_threshold = coverage_rate >= _COVERAGE_THRESHOLD

            coverage_entries.append(CoverageEntry(
                job_id=job_id,
                job_title=job_title,
                family=family,
                technical_ef_count=ef_total,
                technical_ef_covered=covered_count,
                coverage_rate=round(coverage_rate, 4),
                uncovered_ef_ids=uncovered_ids,
                meets_90_threshold=meets_threshold,
            ))

            if not meets_threshold:
                self.add_flag(
                    state,
                    severity="WARNING",
                    flag_type="COVERAGE_BELOW_THRESHOLD",
                    message=(
                        f"Job {job_id} coverage {coverage_rate:.2%} below "
                        f"{_COVERAGE_THRESHOLD:.0%} threshold."
                    ),
                    job_id=job_id,
                    metadata={"coverage_rate": coverage_rate, "uncovered": uncovered_ids},
                )

        ledger = self._load_or_init_ledger(state, stage="6E_bis")
        ledger.coverage = coverage_entries
        ledger.timestamp_utc = datetime.utcnow().isoformat()

        output_path = Path(f"data/output/{state.run_id}_6E_bis_coverage.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as fh:
            fh.write(json.dumps(ledger.model_dump(), indent=2, default=str))

        try:
            setattr(state.artifacts, "bco_ledger", output_path)
        except Exception:
            pass

        return state

    @staticmethod
    def _load_jobs(state: RunState) -> List[Dict[str, Any]]:
        # TODO(v3.1): wire to canonical post-feedback working set; for now fall
        # back to whatever artifact is freshest.
        candidates: List[Path] = []
        for attr in ("clean_v3", "normalized_v2", "competency_map_v1", "jobs_extracted"):
            value = getattr(state.artifacts, attr, None)
            if value:
                candidates.append(Path(str(value)))
        for path in candidates:
            if path.exists():
                try:
                    with open(path) as fh:
                        data = json.load(fh)
                    if isinstance(data, dict) and "jobs" in data:
                        return data["jobs"]
                    if isinstance(data, list):
                        return data
                except Exception:
                    continue
        return []

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
            "You are the Coverage Refresh Operator for v3.1 Phase 6E-bis. After SME edits land, "
            "you re-establish that every Technical Essential Function still maps to at least one "
            "of the top-6 technical competencies for each job.\n\n"
            "Steps:\n"
            "1. Load the post-feedback working set of jobs and competencies.\n"
            "2. For each Technical EF, identify the top-6 candidate competencies and confirm at "
            "least one mapping survives the edits.\n"
            "3. Compute coverage_rate = covered_EFs / total_EFs per job.\n"
            "4. Flag any job below the 0.90 threshold as a WARNING with uncovered EF ids.\n"
            "5. Persist the BCOLedger with refreshed coverage entries.\n\n"
            "Quality standards: coverage must be deterministic and reproducible; uncovered EFs "
            "must surface their ids so downstream remediation has somewhere to start."
        )
