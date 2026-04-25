"""Phase 7 (FINAL only): Learning Synthesis Agent (v3.1)."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from src.agents.base import BaseAgent
from src.schemas.feedback import FeedbackBatch
from src.schemas.run_state import RunState


class LearningSynthesisAgent(BaseAgent):
    """Phase 7 — Synthesize cross-family learnings at FINAL stage only."""

    def __init__(self, agent_id: str = "phase7_learning_synthesis",
                 step_name: str = "Phase 7 — Learning Synthesis"):
        super().__init__(agent_id, step_name)

    def execute(self, state: RunState) -> RunState:
        state.current_step = self.agent_id

        competencies = self._load_competencies(state)
        feedback_batch = self._load_feedback_batch(state)
        bco = self._load_bco(state)

        shared_competencies = self._find_shared_competencies(competencies)
        boundary_patterns = self._summarize_boundary_patterns(bco)
        common_gaps = self._summarize_common_gaps(bco, feedback_batch)
        disposition_stats = self._disposition_stats(feedback_batch)
        recommendations = self._draft_recommendations(
            shared_competencies, boundary_patterns, common_gaps, disposition_stats
        )

        synthesis: Dict[str, Any] = {
            "run_id": state.run_id,
            "stage": "FINAL",
            "generated_utc": datetime.utcnow().isoformat(),
            "shared_competencies": shared_competencies,
            "boundary_patterns": boundary_patterns,
            "common_gaps": common_gaps,
            "feedback_disposition_stats": disposition_stats,
            "recommendations": recommendations,
        }

        output_path = Path(f"data/output/{state.run_id}_phase7_learnings.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as fh:
            fh.write(json.dumps(synthesis, indent=2, default=str))

        try:
            setattr(state.artifacts, "learning_synthesis", output_path)
        except Exception:
            pass

        return state

    @staticmethod
    def _load_competencies(state: RunState) -> List[Dict[str, Any]]:
        for attr in ("ranked_top8_v5", "benchmarked_v4", "clean_v3"):
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
                family = job.get("family") or job.get("job_family") or "UNSPECIFIED"
                for comp in job.get("technical_competencies", []) or []:
                    enriched = dict(comp)
                    enriched["_job_id"] = job.get("job_id")
                    enriched["_family"] = family
                    collected.append(enriched)
            if collected:
                return collected
        return []

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

    @staticmethod
    def _load_bco(state: RunState) -> Dict[str, Any]:
        existing = getattr(state.artifacts, "bco_ledger", None)
        if not existing:
            return {}
        path = Path(str(existing))
        if not path.exists():
            return {}
        try:
            with open(path) as fh:
                return json.load(fh)
        except Exception:
            return {}

    @staticmethod
    def _find_shared_competencies(competencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # TODO(v3.1): integrate LLM judgment for fuzzier "Rosetta Stone" matching.
        by_name: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for comp in competencies:
            name = str(comp.get("name") or "").strip().lower()
            if name:
                by_name[name].append(comp)
        shared: List[Dict[str, Any]] = []
        for name, group in by_name.items():
            families = sorted({str(c.get("_family")) for c in group if c.get("_family")})
            if len(families) >= 2:
                shared.append({
                    "name": group[0].get("name"),
                    "families": families,
                    "occurrences": len(group),
                    "competency_ids": [c.get("competency_id") for c in group],
                })
        return sorted(shared, key=lambda x: x["occurrences"], reverse=True)

    @staticmethod
    def _summarize_boundary_patterns(bco: Dict[str, Any]) -> List[Dict[str, Any]]:
        counter: Counter = Counter()
        for entry in bco.get("boundary", []) or []:
            counter[entry.get("classification", "UNKNOWN")] += 1
        return [
            {"classification": cls, "count": cnt}
            for cls, cnt in counter.most_common()
        ]

    @staticmethod
    def _summarize_common_gaps(
        bco: Dict[str, Any],
        feedback_batch: FeedbackBatch | None,
    ) -> List[Dict[str, Any]]:
        gaps: List[Dict[str, Any]] = []
        for entry in bco.get("coverage", []) or []:
            if not entry.get("meets_90_threshold", True):
                gaps.append({
                    "source": "COVERAGE",
                    "job_id": entry.get("job_id"),
                    "family": entry.get("family"),
                    "uncovered_ef_ids": entry.get("uncovered_ef_ids", []),
                    "coverage_rate": entry.get("coverage_rate"),
                })
        if feedback_batch:
            for item in feedback_batch.items:
                if item.disposition == "GAP":
                    gaps.append({
                        "source": "FEEDBACK",
                        "feedback_id": item.feedback_id,
                        "family": feedback_batch.family,
                        "target_competency_id": item.target_competency_id,
                        "verbatim": item.verbatim_comment,
                    })
        return gaps

    @staticmethod
    def _disposition_stats(feedback_batch: FeedbackBatch | None) -> Dict[str, int]:
        base = {"KEEP": 0, "EDIT": 0, "GAP": 0, "DISCUSS": 0, "REJECT": 0}
        if not feedback_batch:
            return base
        for item in feedback_batch.items:
            base[item.disposition] = base.get(item.disposition, 0) + 1
        return base

    @staticmethod
    def _draft_recommendations(
        shared: List[Dict[str, Any]],
        boundary_patterns: List[Dict[str, Any]],
        gaps: List[Dict[str, Any]],
        disposition_stats: Dict[str, int],
    ) -> List[str]:
        # TODO(v3.1): integrate LLM judgment to author narrative recommendations.
        recs: List[str] = []
        if shared:
            recs.append(
                f"Promote {len(shared)} shared competency name(s) into the cross-family Rosetta Stone."
            )
        misclass = next((p for p in boundary_patterns if p["classification"] == "MIXED"), None)
        if misclass and misclass["count"] > 0:
            recs.append(
                f"Review {misclass['count']} MIXED-boundary competencies for cleaner V&B vs Technical splits."
            )
        if gaps:
            recs.append(
                f"Address {len(gaps)} open coverage / SME gap(s) before publishing the FINAL package."
            )
        if disposition_stats.get("DISCUSS", 0) > 0:
            recs.append(
                "Schedule a focus group to resolve outstanding DISCUSS items from SME feedback."
            )
        if not recs:
            recs.append("No cross-family interventions required at FINAL stage.")
        return recs

    def get_system_prompt(self) -> str:
        return (
            "You are the Learning Synthesis Operator for v3.1 Phase 7. You run only at the "
            "FINAL stage and produce a single, durable cross-family learnings record from "
            "everything the run has produced.\n\n"
            "Steps:\n"
            "1. Load the final competency working set, BCOLedger, and FeedbackBatch.\n"
            "2. Identify Rosetta Stone (shared) competencies by name across families.\n"
            "3. Summarize recurring boundary classifications and misclassification patterns.\n"
            "4. Aggregate common gaps from coverage shortfalls and SME GAP dispositions.\n"
            "5. Compute SME disposition stats (KEEP/EDIT/GAP/DISCUSS/REJECT).\n"
            "6. Draft actionable recommendations and persist phase7_learnings.json.\n\n"
            "Quality standards: synthesis is descriptive, not normative — never invent gaps that "
            "do not appear in the artifacts; tie every recommendation back to evidence in the run; "
            "the JSON must conform to the documented schema."
        )
