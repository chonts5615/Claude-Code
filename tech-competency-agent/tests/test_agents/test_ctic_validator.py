"""Phase 6F CTIC validator — verify drift revert is *persisted*, not just logged.

Critical regression test for the v3.1 spec rule:
  > Non-targeted drift must be reverted, not flagged.

We feed the validator a pre-feedback state and a post-feedback state with one
targeted edit and one untargeted drift. After execution, the artifact written
to disk must contain the pre-feedback text on the untargeted competency and
the post-feedback text on the targeted one.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from src.agents.ctic_validator import CTICValidatorAgent
from src.schemas.feedback import FeedbackBatch, FeedbackItem
from src.schemas.run_state import (
    ArtifactRegistry,
    RunConfig,
    RunInputs,
    RunState,
)


def _state_envelope(comps):
    return {"jobs": [{"job_id": "JOB1", "technical_competencies": comps}]}


def _comp(cid, name, definition, why):
    return {
        "competency_id": cid,
        "name": name,
        "definition": definition,
        "why_it_matters": why,
    }


@pytest.fixture
def ctic_run(tmp_path, monkeypatch):
    """Build pre/post artifacts and a feedback batch in tmp_path; chdir there."""
    monkeypatch.chdir(tmp_path)

    pre_comps = [
        _comp("c1", "Targeted Competency Name",
              "Original definition for c1 with sufficient words to be realistic.",
              "Original why for c1."),
        _comp("c2", "Untouched Competency Name",
              "Original definition for c2 with sufficient words to be realistic.",
              "Original why for c2."),
    ]
    # Post-feedback: c1 has a targeted definition edit, c2 has untargeted drift
    # in `why_it_matters` (must be reverted).
    post_comps = [
        _comp("c1", "Targeted Competency Name",
              "Edited definition for c1 with sufficient words to be realistic.",
              "Original why for c1."),
        _comp("c2", "Untouched Competency Name",
              "Original definition for c2 with sufficient words to be realistic.",
              "DRIFTED why for c2 — should be reverted."),
    ]

    pre_path = tmp_path / "pre.json"
    post_path = tmp_path / "post.json"
    pre_path.write_text(json.dumps(_state_envelope(pre_comps)))
    post_path.write_text(json.dumps(_state_envelope(post_comps)))

    feedback_path = tmp_path / "feedback.json"
    batch = FeedbackBatch(
        run_id="r1",
        stage="R2",
        family="Finance",
        items=[FeedbackItem(
            feedback_id="f1",
            target_competency_id="c1",
            target_field="definition",
            verbatim_comment="Tighten verb.",
            disposition="EDIT",
        )],
        received_timestamp_utc=datetime.utcnow().isoformat(),
    )
    feedback_path.write_text(batch.model_dump_json())

    artifacts = ArtifactRegistry(
        pre_feedback_snapshot=pre_path,
        normalized_v2=post_path,
        feedback_batch=feedback_path,
    )
    state = RunState(
        run_id="r1",
        inputs=RunInputs(),
        config=RunConfig(stage="R2"),
        artifacts=artifacts,
    )
    return state, tmp_path


def test_ctic_persists_reverted_state(ctic_run):
    state, tmp_path = ctic_run
    agent = CTICValidatorAgent()
    new_state = agent.execute(state)

    # 1. New artifact is registered.
    persisted = new_state.artifacts.post_ctic_state
    assert persisted is not None, "post_ctic_state artifact must be registered"
    assert Path(persisted).exists(), "persisted file must exist on disk"

    # 2. File contents reflect REVERT on c2 and KEEP on c1.
    payload = json.loads(Path(persisted).read_text())
    comps_by_id = {
        c["competency_id"]: c
        for job in payload["jobs"]
        for c in job["technical_competencies"]
    }

    # c1 was targeted -> edited definition retained.
    assert "Edited definition" in comps_by_id["c1"]["definition"]

    # c2 was NOT targeted -> drift reverted to pre-feedback text.
    assert comps_by_id["c2"]["why_it_matters"] == "Original why for c2.", (
        "untargeted drift in why_it_matters must be reverted to pre-feedback text"
    )


def test_ctic_report_marks_revert_vs_keep(ctic_run):
    state, tmp_path = ctic_run
    agent = CTICValidatorAgent()
    new_state = agent.execute(state)

    report_path = new_state.artifacts.ctic_report
    assert report_path is not None
    report = json.loads(Path(report_path).read_text())
    by_target = {(e["competency_id"], e["field"]): e for e in report["entries"]}

    assert by_target[("c1", "definition")]["reverted"] is False
    assert by_target[("c1", "definition")]["is_targeted_by_feedback"] is True
    assert by_target[("c2", "why_it_matters")]["reverted"] is True
    assert by_target[("c2", "why_it_matters")]["is_targeted_by_feedback"] is False
