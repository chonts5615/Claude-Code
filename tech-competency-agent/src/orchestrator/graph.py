import json
from datetime import UTC, datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from langgraph.graph import END, StateGraph

from src.agents.benchmark_researcher import BenchmarkResearchAgent
from src.agents.competency_mapping import CompetencyMappingAgent
from src.agents.criticality_ranker import CriticalityRankerAgent
from src.agents.job_ingestion import JobIngestionAgent
from src.agents.normalizer import NormalizerAgent
from src.agents.overlap_auditor import OverlapAuditorAgent
from src.agents.overlap_remediator import OverlapRemediatorAgent
from src.agents.template_populator import TemplatePopulatorAgent
from src.orchestrator.gates import QualityGate, ValidationResult
from src.schemas.run_state import RunState


class WorkflowOrchestrator:
    """LangGraph-based workflow orchestrator."""

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.agents = {
            "job_ingestion": JobIngestionAgent("S1", "Job Extraction"),
            "competency_mapping": CompetencyMappingAgent("S2", "Competency Mapping"),
            "normalizer": NormalizerAgent("S3", "Normalization"),
            "overlap_auditor": OverlapAuditorAgent("S4", "Overlap Audit"),
            "overlap_remediator": OverlapRemediatorAgent("S5", "Overlap Remediation"),
            "benchmark_researcher": BenchmarkResearchAgent("S6", "Benchmarking"),
            "criticality_ranker": CriticalityRankerAgent("S7", "Ranking"),
            "template_populator": TemplatePopulatorAgent("S8", "Template Population"),
        }
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build workflow graph with agents and gates."""

        # Initialize graph with state schema
        workflow = StateGraph(RunState)

        # Initialize agents
        # Add nodes
        workflow.add_node("s1_extract_jobs", self.agents["job_ingestion"].execute)
        workflow.add_node("s1_gate", self._gate_s1)

        workflow.add_node("s2_map_competencies", self.agents["competency_mapping"].execute)
        workflow.add_node("s2_gate", self._gate_s2)

        workflow.add_node("s3_normalize", self.agents["normalizer"].execute)

        workflow.add_node("s4_audit_overlap", self.agents["overlap_auditor"].execute)

        workflow.add_node("s5_remediate_overlap", self.agents["overlap_remediator"].execute)
        workflow.add_node("s5_gate", self._gate_s5)

        workflow.add_node("s6_benchmark", self.agents["benchmark_researcher"].execute)

        workflow.add_node("s7_rank", self.agents["criticality_ranker"].execute)
        workflow.add_node("s7_gate", self._gate_s7)

        workflow.add_node("s8_populate", self.agents["template_populator"].execute)

        workflow.add_node("s9_package", self._package_for_review)

        # Define edges
        workflow.set_entry_point("s1_extract_jobs")

        workflow.add_edge("s1_extract_jobs", "s1_gate")
        workflow.add_conditional_edges(
            "s1_gate",
            self._route_after_gate,
            {"continue": "s2_map_competencies", "fail": END}
        )

        workflow.add_edge("s2_map_competencies", "s2_gate")
        workflow.add_conditional_edges(
            "s2_gate",
            self._route_after_gate,
            {"continue": "s3_normalize", "fail": END}
        )

        workflow.add_edge("s3_normalize", "s4_audit_overlap")
        workflow.add_edge("s4_audit_overlap", "s5_remediate_overlap")

        workflow.add_edge("s5_remediate_overlap", "s5_gate")
        workflow.add_conditional_edges(
            "s5_gate",
            self._route_after_gate,
            {"continue": "s6_benchmark", "reaudit": "s4_audit_overlap", "fail": END}
        )

        workflow.add_edge("s6_benchmark", "s7_rank")

        workflow.add_edge("s7_rank", "s7_gate")
        workflow.add_conditional_edges(
            "s7_gate",
            self._route_after_gate,
            {"continue": "s8_populate", "fail": END}
        )

        workflow.add_edge("s8_populate", "s9_package")
        workflow.add_edge("s9_package", END)

        return workflow.compile()

    # Quality Gates
    def _gate_s1(self, state: RunState) -> RunState:
        """Validate job extraction."""
        gate = QualityGate("S1_Gate", state.config.thresholds)

        # Check jobs were extracted
        result = gate.validate_no_jobs_extracted(state)
        if not result.passed:
            self._add_gate_flag(state, result)

        # Check missing summary rate
        result = gate.validate_missing_summary_rate(state, max_rate=0.10)
        if not result.passed:
            self._add_gate_flag(state, result)

        return state

    def _gate_s2(self, state: RunState) -> RunState:
        """Validate competency mapping."""
        gate = QualityGate("S2_Gate", state.config.thresholds)

        result = gate.validate_unmapped_responsibilities(state, max_rate=0.05)
        if not result.passed:
            self._add_gate_flag(state, result)

        return state

    def _gate_s5(self, state: RunState) -> RunState:
        """Validate overlap remediation."""
        gate = QualityGate("S5_Gate", state.config.thresholds)

        result = gate.validate_overlap_resolved(state)
        if not result.passed:
            self._add_gate_flag(state, result)

        return state

    def _gate_s7(self, state: RunState) -> RunState:
        """Validate ranking."""
        gate = QualityGate("S7_Gate", state.config.thresholds)

        result = gate.validate_coverage_threshold(state)
        if not result.passed:
            self._add_gate_flag(state, result)

        result = gate.validate_top_n_count(state)
        if not result.passed:
            self._add_gate_flag(state, result)

        return state

    def _route_after_gate(self, state: RunState) -> str:
        """Route based on gate results."""
        # Check for CRITICAL/ERROR flags from current step
        current_step_flags = [
            f for f in state.flags
            if f.step_id == state.current_step and
            f.severity in ["CRITICAL", "ERROR"]
        ]

        if current_step_flags:
            return "fail"

        # Special routing for S5 (may need reaudit)
        if state.current_step == "S5_Gate":
            # Check if remediation output indicates reaudit needed
            # This would be read from the actual remediation output
            # For now, simplified
            return "continue"

        return "continue"

    def _add_gate_flag(self, state: RunState, result: ValidationResult):
        """Add flag from validation result."""
        from src.schemas.run_state import RunFlag

        flag = RunFlag(
            step_id=state.current_step,
            severity=result.severity,
            flag_type=result.rule_name,
            message=result.message,
            metadata=result.metadata
        )
        state.flags.append(flag)

    def _package_for_review(self, state: RunState) -> RunState:
        """Step 9 - Package all outputs."""
        state.current_step = "S9_Package"
        output_dir = Path("data/output")
        output_dir.mkdir(parents=True, exist_ok=True)

        package_path = output_dir / f"{state.run_id}_review_package.zip"
        artifact_map = state.artifacts.dict()
        package_manifest = {
            "run_id": state.run_id,
            "packaged_at_utc": datetime.now(UTC).isoformat(),
            "artifacts_included": [],
            "artifacts_missing": [],
        }

        with ZipFile(package_path, "w", compression=ZIP_DEFLATED) as zip_file:
            for artifact_name, artifact_path in artifact_map.items():
                if not artifact_path:
                    package_manifest["artifacts_missing"].append(artifact_name)
                    continue

                artifact_file = Path(artifact_path)
                if not artifact_file.exists():
                    package_manifest["artifacts_missing"].append(artifact_name)
                    continue

                archive_name = f"artifacts/{artifact_file.name}"
                zip_file.write(artifact_file, arcname=archive_name)
                package_manifest["artifacts_included"].append(
                    {"name": artifact_name, "path": archive_name}
                )

            zip_file.writestr("manifest.json", json.dumps(package_manifest, indent=2))

        state.artifacts.final_review_package = package_path
        return state

    def run(self, initial_state: RunState) -> RunState:
        """Execute workflow."""
        state = initial_state
        state = self.agents["job_ingestion"].execute(state)
        state = self._gate_s1(state)

        state = self.agents["competency_mapping"].execute(state)
        state = self._gate_s2(state)

        state = self.agents["normalizer"].execute(state)
        state = self.agents["overlap_auditor"].execute(state)
        state = self.agents["overlap_remediator"].execute(state)
        state = self._gate_s5(state)

        state = self.agents["benchmark_researcher"].execute(state)
        state = self.agents["criticality_ranker"].execute(state)
        state = self._gate_s7(state)

        state = self.agents["template_populator"].execute(state)
        state = self._package_for_review(state)
        return state
