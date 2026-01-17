from langgraph.graph import StateGraph, END
from src.schemas.run_state import RunState
from src.agents.job_ingestion import JobIngestionAgent
from src.agents.competency_mapping import CompetencyMappingAgent
from src.agents.normalizer import NormalizerAgent
from src.agents.overlap_auditor import OverlapAuditorAgent
from src.agents.overlap_remediator import OverlapRemediatorAgent
from src.agents.benchmark_researcher import BenchmarkResearchAgent
from src.agents.criticality_ranker import CriticalityRankerAgent
from src.agents.template_populator import TemplatePopulatorAgent
from src.orchestrator.gates import QualityGate, ValidationResult


class WorkflowOrchestrator:
    """LangGraph-based workflow orchestrator."""

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build workflow graph with agents and gates."""

        # Initialize graph with state schema
        workflow = StateGraph(RunState)

        # Initialize agents
        agents = {
            "job_ingestion": JobIngestionAgent("S1", "Job Extraction"),
            "competency_mapping": CompetencyMappingAgent("S2", "Competency Mapping"),
            "normalizer": NormalizerAgent("S3", "Normalization"),
            "overlap_auditor": OverlapAuditorAgent("S4", "Overlap Audit"),
            "overlap_remediator": OverlapRemediatorAgent("S5", "Overlap Remediation"),
            "benchmark_researcher": BenchmarkResearchAgent("S6", "Benchmarking"),
            "criticality_ranker": CriticalityRankerAgent("S7", "Ranking"),
            "template_populator": TemplatePopulatorAgent("S8", "Template Population")
        }

        # Add nodes
        workflow.add_node("s1_extract_jobs", agents["job_ingestion"].execute)
        workflow.add_node("s1_gate", self._gate_s1)

        workflow.add_node("s2_map_competencies", agents["competency_mapping"].execute)
        workflow.add_node("s2_gate", self._gate_s2)

        workflow.add_node("s3_normalize", agents["normalizer"].execute)

        workflow.add_node("s4_audit_overlap", agents["overlap_auditor"].execute)

        workflow.add_node("s5_remediate_overlap", agents["overlap_remediator"].execute)
        workflow.add_node("s5_gate", self._gate_s5)

        workflow.add_node("s6_benchmark", agents["benchmark_researcher"].execute)

        workflow.add_node("s7_rank", agents["criticality_ranker"].execute)
        workflow.add_node("s7_gate", self._gate_s7)

        workflow.add_node("s8_populate", agents["template_populator"].execute)

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
        # This would call a packaging agent
        # For now, just update state
        state.current_step = "S9_Package"
        return state

    def run(self, initial_state: RunState) -> RunState:
        """Execute workflow."""
        return self.graph.invoke(initial_state)
