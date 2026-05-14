"""Packaging smoke tests for orchestrator outputs."""

import json
import zipfile
from pathlib import Path

from openpyxl import Workbook

from src.orchestrator.graph import WorkflowOrchestrator


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_review_package_contains_all_available_artifacts(sample_run_state, tmp_path):
    """Package all available artifacts and verify zip + manifest contents."""
    sample_run_state.run_id = "package_smoke_001"

    s1 = tmp_path / "s1_jobs.json"
    s8 = tmp_path / "s8_template.xlsx"
    _write_json(s1, {"ok": True})
    wb = Workbook()
    wb.save(s8)

    sample_run_state.artifacts.jobs_extracted = s1
    sample_run_state.artifacts.populated_template = s8

    orchestrator = WorkflowOrchestrator(config_path="config/workflow_config.yaml")
    final_state = orchestrator._package_for_review(sample_run_state)

    assert final_state.artifacts.final_review_package is not None
    assert final_state.artifacts.final_review_package.exists()

    with zipfile.ZipFile(final_state.artifacts.final_review_package, "r") as zf:
        names = set(zf.namelist())
        assert "manifest.json" in names
        assert "artifacts/s1_jobs.json" in names
        assert "artifacts/s8_template.xlsx" in names

        manifest = json.loads(zf.read("manifest.json").decode("utf-8"))
        included = {item["name"] for item in manifest["artifacts_included"]}
        assert "jobs_extracted" in included
        assert "populated_template" in included
