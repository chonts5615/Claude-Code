"""v3.1 LangGraph orchestrator with R1/R2/FINAL/Resume stage routing."""

from __future__ import annotations

from langgraph.graph import END, StateGraph

from src.agents.benchmark_researcher import BenchmarkResearchAgent
from src.agents.boundary_rescan import BoundaryRescanAgent
from src.agents.competency_mapping import CompetencyMappingAgent
from src.agents.coverage_refresh import CoverageRefreshAgent
from src.agents.criticality_ranker import CriticalityRankerAgent
from src.agents.ctic_validator import CTICValidatorAgent
from src.agents.feedback_ingestion import FeedbackIngestionAgent
from src.agents.focus_group_prep import FocusGroupPrepAgent
from src.agents.job_ingestion import JobIngestionAgent
from src.agents.learning_synthesis import LearningSynthesisAgent
from src.agents.normalizer import NormalizerAgent
from src.agents.overlap_auditor import OverlapAuditorAgent
from src.agents.overlap_reaudit import OverlapReauditAgent
from src.agents.overlap_remediator import OverlapRemediatorAgent
from src.agents.template_populator import TemplatePopulatorAgent
from src.orchestrator.gates import QualityGate, ValidationResult
from src.schemas.run_state import RunState


class WorkflowOrchestrator:
    """LangGraph orchestrator that builds one of four DAGs by stage."""

    def __init__(self, config_path: str):
        self.config_path = config_path
        self._compiled: dict = {}

    def graph_for(self, stage: str):
        if stage in self._compiled:
            return self._compiled[stage]
        if stage == "R1":
            g = self._build_r1()
        elif stage in ("R2", "FINAL"):
            g = self._build_r2_or_final(include_phase7=(stage == "FINAL"))
        else:
            raise ValueError(f"Unsupported stage {stage!r} (use R1, R2, FINAL, or RESUME via run_resume)")
        self._compiled[stage] = g
        return g

    # --- R1 (full pipeline) -------------------------------------------------

    def _build_r1(self):
        wf = StateGraph(RunState)

        wf.add_node("s1_extract_jobs", JobIngestionAgent("S1", "Job Extraction").execute)
        wf.add_node("s1_gate", self._gate_s1)
        wf.add_node("s2_map_competencies", CompetencyMappingAgent("S2", "Competency Mapping").execute)
        wf.add_node("s2_gate", self._gate_s2)
        wf.add_node("s3_normalize", NormalizerAgent("S3", "Normalization").execute)
        wf.add_node("s3_gate", self._gate_s3_v31_format)
        wf.add_node("s4_audit_overlap", OverlapAuditorAgent("S4", "Overlap Audit").execute)
        wf.add_node("s5_remediate_overlap", OverlapRemediatorAgent("S5", "Overlap Remediation").execute)
        wf.add_node("s5_gate", self._gate_s5)
        wf.add_node("s6_benchmark", BenchmarkResearchAgent("S6", "Benchmarking").execute)
        wf.add_node("s7_rank", CriticalityRankerAgent("S7", "Ranking").execute)
        wf.add_node("s7_gate", self._gate_s7)
        wf.add_node("s8_populate", TemplatePopulatorAgent("S8", "Template Population").execute)
        wf.add_node("s9_package", self._package_for_review)

        wf.set_entry_point("s1_extract_jobs")
        wf.add_edge("s1_extract_jobs", "s1_gate")
        wf.add_conditional_edges("s1_gate", self._route, {"continue": "s2_map_competencies", "fail": END})
        wf.add_edge("s2_map_competencies", "s2_gate")
        wf.add_conditional_edges("s2_gate", self._route, {"continue": "s3_normalize", "fail": END})
        wf.add_edge("s3_normalize", "s3_gate")
        wf.add_conditional_edges("s3_gate", self._route, {"continue": "s4_audit_overlap", "fail": END})
        wf.add_edge("s4_audit_overlap", "s5_remediate_overlap")
        wf.add_edge("s5_remediate_overlap", "s5_gate")
        wf.add_conditional_edges("s5_gate", self._route, {"continue": "s6_benchmark", "reaudit": "s4_audit_overlap", "fail": END})
        wf.add_edge("s6_benchmark", "s7_rank")
        wf.add_edge("s7_rank", "s7_gate")
        wf.add_conditional_edges("s7_gate", self._route, {"continue": "s8_populate", "fail": END})
        wf.add_edge("s8_populate", "s9_package")
        wf.add_edge("s9_package", END)
        return wf.compile()

    # --- R2 / FINAL (feedback + 6E-bis/ter/quater + CTIC + 6G + Phase 7) ---

    def _build_r2_or_final(self, include_phase7: bool):
        wf = StateGraph(RunState)

        wf.add_node("p6_feedback", FeedbackIngestionAgent("P6", "Feedback Ingestion").execute)
        wf.add_node("p6_review_metadata_gate", self._gate_review_metadata)
        wf.add_node("p6e_bis_coverage", CoverageRefreshAgent("P6E_bis", "Coverage Refresh").execute)
        wf.add_node("p6e_ter_boundary", BoundaryRescanAgent("P6E_ter", "Boundary Re-Scan").execute)
        wf.add_node("p6e_quater_overlap", OverlapReauditAgent("P6E_quater", "Overlap Re-Audit").execute)
        wf.add_node("p6f_ctic", CTICValidatorAgent("P6F", "CTIC Validator").execute)
        wf.add_node("p6f_gate", self._gate_ctic)
        wf.add_node("p6g_focus_group", FocusGroupPrepAgent("P6G", "Focus Group Prep").execute)
        wf.add_node("p5_output", TemplatePopulatorAgent("S8", "Template Population").execute)
        wf.add_node("p5_package", self._package_for_review)
        if include_phase7:
            wf.add_node("p7_synth", LearningSynthesisAgent("P7", "Learning Synthesis").execute)

        wf.set_entry_point("p6_feedback")
        wf.add_edge("p6_feedback", "p6_review_metadata_gate")
        wf.add_conditional_edges("p6_review_metadata_gate", self._route, {"continue": "p6e_bis_coverage", "fail": END})
        wf.add_edge("p6e_bis_coverage", "p6e_ter_boundary")
        wf.add_edge("p6e_ter_boundary", "p6e_quater_overlap")
        wf.add_edge("p6e_quater_overlap", "p6f_ctic")
        wf.add_edge("p6f_ctic", "p6f_gate")
        wf.add_conditional_edges("p6f_gate", self._route, {"continue": "p6g_focus_group", "fail": END})
        wf.add_edge("p6g_focus_group", "p5_output")
        wf.add_edge("p5_output", "p5_package")
        if include_phase7:
            wf.add_edge("p5_package", "p7_synth")
            wf.add_edge("p7_synth", END)
        else:
            wf.add_edge("p5_package", END)
        return wf.compile()

    # --- gates -------------------------------------------------------------

    def _gate_s1(self, state: RunState) -> RunState:
        gate = QualityGate("S1_Gate", state.config.thresholds)
        for r in (gate.validate_no_jobs_extracted(state),
                  gate.validate_missing_summary_rate(state, max_rate=0.10)):
            if not r.passed:
                self._add_flag(state, r)
        return state

    def _gate_s2(self, state: RunState) -> RunState:
        gate = QualityGate("S2_Gate", state.config.thresholds)
        r = gate.validate_unmapped_responsibilities(state, max_rate=0.05)
        if not r.passed:
            self._add_flag(state, r)
        return state

    def _gate_s3_v31_format(self, state: RunState) -> RunState:
        gate = QualityGate("S3_Gate_v31", state.config.thresholds)
        r = gate.validate_v31_competency_format(state)
        if not r.passed:
            self._add_flag(state, r)
        return state

    def _gate_s5(self, state: RunState) -> RunState:
        gate = QualityGate("S5_Gate", state.config.thresholds)
        r = gate.validate_overlap_resolved(state)
        if not r.passed:
            self._add_flag(state, r)
        return state

    def _gate_s7(self, state: RunState) -> RunState:
        gate = QualityGate("S7_Gate", state.config.thresholds)
        for r in (gate.validate_coverage_threshold(state),
                  gate.validate_top_n_count(state)):
            if not r.passed:
                self._add_flag(state, r)
        return state

    def _gate_review_metadata(self, state: RunState) -> RunState:
        if not state.artifacts.feedback_batch:
            self._add_flag(state, ValidationResult(
                rule_name="review_metadata",
                passed=False,
                severity="ERROR",
                message="REVIEW_METADATA gate: no feedback_batch artifact",
                metadata={},
            ))
            return state
        import json
        with open(state.artifacts.feedback_batch, "r") as f:
            batch = json.load(f)
        meta = batch.get("review_metadata", {}) or {}
        missing = [k for k in ("reviewer", "review_date", "stage") if k not in meta]
        if missing:
            self._add_flag(state, ValidationResult(
                rule_name="review_metadata",
                passed=False,
                severity="ERROR",
                message=f"REVIEW_METADATA missing keys: {missing}",
                metadata={"missing": missing},
            ))
        return state

    def _gate_ctic(self, state: RunState) -> RunState:
        gate = QualityGate("P6F_Gate", state.config.thresholds)
        r = gate.validate_ctic_drift(state)
        if not r.passed:
            self._add_flag(state, r)
        return state

    def _route(self, state: RunState) -> str:
        current_step_flags = [
            f for f in state.flags
            if f.step_id == state.current_step
            and f.severity in ("CRITICAL", "ERROR")
        ]
        if current_step_flags:
            return "fail"
        if state.current_step == "S5_Gate":
            return "continue"  # reaudit hook reserved for remediator output read
        return "continue"

    def _add_flag(self, state: RunState, result: ValidationResult):
        from src.schemas.run_state import RunFlag
        state.flags.append(RunFlag(
            step_id=state.current_step or "unknown",
            severity=result.severity,
            flag_type=result.rule_name,
            message=result.message,
            metadata=result.metadata,
        ))

    def _package_for_review(self, state: RunState) -> RunState:
        state.current_step = "S9_Package"
        return state

    # --- entry points ------------------------------------------------------

    def run(self, initial_state: RunState):
        """Run a workflow stage.

        LangGraph remains available through ``graph_for`` for future durable
        orchestration, but the CLI uses this deterministic linear runner today.
        It avoids nested Pydantic mutation loss in end-to-end runs and mirrors
        the same node/gate order as the compiled graph.
        """
        stage = initial_state.config.stage
        if stage == "R1":
            return self._run_r1_linear(initial_state)
        if stage in ("R2", "FINAL"):
            return self._run_r2_or_final_linear(initial_state, include_phase7=(stage == "FINAL"))
        raise ValueError(f"Unsupported stage {stage!r} (use R1, R2, FINAL, or RESUME via run_resume)")

    def _run_r1_linear(self, state: RunState) -> RunState:
        steps = [
            (JobIngestionAgent("S1", "Job Extraction").execute, self._gate_s1),
            (CompetencyMappingAgent("S2", "Competency Mapping").execute, self._gate_s2),
            (NormalizerAgent("S3", "Normalization").execute, self._gate_s3_v31_format),
            (OverlapAuditorAgent("S4", "Overlap Audit").execute, None),
            (OverlapRemediatorAgent("S5", "Overlap Remediation").execute, self._gate_s5),
            (BenchmarkResearchAgent("S6", "Benchmarking").execute, None),
            (CriticalityRankerAgent("S7", "Ranking").execute, self._gate_s7),
            (TemplatePopulatorAgent("S8", "Template Population").execute, None),
            (self._package_for_review, None),
        ]
        for node, gate in steps:
            state = node(state)
            if gate:
                state = gate(state)
                if self._route(state) == "fail":
                    return state
        return state

    def _run_r2_or_final_linear(self, state: RunState, include_phase7: bool) -> RunState:
        steps = [
            (FeedbackIngestionAgent("P6", "Feedback Ingestion").execute, self._gate_review_metadata),
            (CoverageRefreshAgent("P6E_bis", "Coverage Refresh").execute, None),
            (BoundaryRescanAgent("P6E_ter", "Boundary Re-Scan").execute, None),
            (OverlapReauditAgent("P6E_quater", "Overlap Re-Audit").execute, None),
            (CTICValidatorAgent("P6F", "CTIC Validator").execute, self._gate_ctic),
            (FocusGroupPrepAgent("P6G", "Focus Group Prep").execute, None),
            (TemplatePopulatorAgent("S8", "Template Population").execute, None),
            (self._package_for_review, None),
        ]
        if include_phase7:
            steps.append((LearningSynthesisAgent("P7", "Learning Synthesis").execute, None))
        for node, gate in steps:
            state = node(state)
            if gate:
                state = gate(state)
                if self._route(state) == "fail":
                    return state
        return state

    def run_resume(self, initial_state: RunState):
        # RESUME reads ArtifactRegistry to skip completed nodes; for now invoke
        # the requested stage from start and rely on agents to short-circuit
        # when their artifact already exists (TODO).
        return self.run(initial_state)
