"""LangGraph-based workflow orchestrator."""

from typing import Literal, Optional
from langgraph.graph import StateGraph, END

from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase
from src.agents.vision_extractor import VisionExtractorAgent
from src.agents.context_analyzer import ContextAnalyzerAgent
from src.agents.pillar_synthesizer import PillarSynthesizerAgent
from src.agents.goal_generator import GoalGeneratorAgent
from src.agents.initiative_designer import InitiativeDesignerAgent
from src.agents.risk_assessor import RiskAssessorAgent
from src.agents.resource_planner import ResourcePlannerAgent
from src.agents.timeline_optimizer import TimelineOptimizerAgent
from src.agents.validator import ValidatorAgent
from src.agents.output_generator import OutputGeneratorAgent
from src.agents.feedback_processor import FeedbackProcessorAgent
from src.agents.learning_optimizer import LearningOptimizerAgent
from src.orchestrator.gates import QualityGate, GateResult


class StrategyWorkflowOrchestrator:
    """
    LangGraph-based orchestrator for the multi-agent strategy workflow.

    The workflow consists of 12 agents organized into phases:
    1. Ingestion: Vision extraction
    2. Analysis: Context analysis
    3. Synthesis: Pillar synthesis, Goal generation
    4. Planning: Initiative design, Risk assessment, Resource planning
    5. Optimization: Timeline optimization
    6. Validation: Strategy validation
    7. Output: Document generation
    8. Feedback: Learning and optimization (loop)

    Quality gates are placed after critical steps to validate outputs
    before proceeding.
    """

    def __init__(
        self,
        model_name: str = "claude-sonnet-4-20250514",
        enable_feedback_loop: bool = True,
    ):
        self.model_name = model_name
        self.enable_feedback_loop = enable_feedback_loop
        self._initialize_agents()
        self.graph = self._build_graph()

    def _initialize_agents(self):
        """Initialize all agents."""
        self.agents = {
            "vision_extractor": VisionExtractorAgent(self.model_name),
            "context_analyzer": ContextAnalyzerAgent(self.model_name),
            "pillar_synthesizer": PillarSynthesizerAgent(self.model_name),
            "goal_generator": GoalGeneratorAgent(self.model_name),
            "initiative_designer": InitiativeDesignerAgent(self.model_name),
            "risk_assessor": RiskAssessorAgent(self.model_name),
            "resource_planner": ResourcePlannerAgent(self.model_name),
            "timeline_optimizer": TimelineOptimizerAgent(self.model_name),
            "validator": ValidatorAgent(self.model_name),
            "output_generator": OutputGeneratorAgent(self.model_name),
            "feedback_processor": FeedbackProcessorAgent(self.model_name),
            "learning_optimizer": LearningOptimizerAgent(self.model_name),
        }

    def _build_graph(self) -> StateGraph:
        """Build the workflow graph with agents and gates."""

        # Initialize graph with state schema
        workflow = StateGraph(RunState)

        # Add agent nodes
        workflow.add_node("s1_extract_vision", self._run_vision_extractor)
        workflow.add_node("g1_vision_gate", self._gate_vision)

        workflow.add_node("s2_analyze_context", self._run_context_analyzer)

        workflow.add_node("s3_synthesize_pillars", self._run_pillar_synthesizer)
        workflow.add_node("g2_pillar_gate", self._gate_pillars)

        workflow.add_node("s4_generate_goals", self._run_goal_generator)
        workflow.add_node("g3_goal_gate", self._gate_goals)

        workflow.add_node("s5_design_initiatives", self._run_initiative_designer)
        workflow.add_node("g4_initiative_gate", self._gate_initiatives)

        workflow.add_node("s6_assess_risks", self._run_risk_assessor)
        workflow.add_node("g5_risk_gate", self._gate_risks)

        workflow.add_node("s7_plan_resources", self._run_resource_planner)

        workflow.add_node("s8_optimize_timeline", self._run_timeline_optimizer)

        workflow.add_node("s9_validate", self._run_validator)
        workflow.add_node("g6_validation_gate", self._gate_validation)

        workflow.add_node("s10_generate_outputs", self._run_output_generator)

        # Feedback loop nodes
        workflow.add_node("f1_process_feedback", self._run_feedback_processor)
        workflow.add_node("f2_apply_learnings", self._run_learning_optimizer)

        # Define edges - Main flow
        workflow.set_entry_point("s1_extract_vision")

        workflow.add_edge("s1_extract_vision", "g1_vision_gate")
        workflow.add_conditional_edges(
            "g1_vision_gate",
            self._route_after_gate,
            {"continue": "s2_analyze_context", "fail": END}
        )

        workflow.add_edge("s2_analyze_context", "s3_synthesize_pillars")

        workflow.add_edge("s3_synthesize_pillars", "g2_pillar_gate")
        workflow.add_conditional_edges(
            "g2_pillar_gate",
            self._route_after_gate,
            {"continue": "s4_generate_goals", "fail": END}
        )

        workflow.add_edge("s4_generate_goals", "g3_goal_gate")
        workflow.add_conditional_edges(
            "g3_goal_gate",
            self._route_after_gate,
            {"continue": "s5_design_initiatives", "fail": END}
        )

        workflow.add_edge("s5_design_initiatives", "g4_initiative_gate")
        workflow.add_conditional_edges(
            "g4_initiative_gate",
            self._route_after_gate,
            {"continue": "s6_assess_risks", "fail": END}
        )

        workflow.add_edge("s6_assess_risks", "g5_risk_gate")
        workflow.add_conditional_edges(
            "g5_risk_gate",
            self._route_after_gate,
            {"continue": "s7_plan_resources", "fail": END}
        )

        workflow.add_edge("s7_plan_resources", "s8_optimize_timeline")
        workflow.add_edge("s8_optimize_timeline", "s9_validate")

        workflow.add_edge("s9_validate", "g6_validation_gate")
        workflow.add_conditional_edges(
            "g6_validation_gate",
            self._route_after_validation,
            {"continue": "s10_generate_outputs", "remediate": "s5_design_initiatives", "fail": END}
        )

        workflow.add_edge("s10_generate_outputs", "f1_process_feedback")
        workflow.add_edge("f1_process_feedback", "f2_apply_learnings")
        workflow.add_edge("f2_apply_learnings", END)

        return workflow.compile()

    # Agent execution methods
    def _run_vision_extractor(self, state: RunState) -> RunState:
        agent = self.agents["vision_extractor"]
        state = agent.pre_execute(state)
        state = agent.execute(state)
        return agent.post_execute(state)

    def _run_context_analyzer(self, state: RunState) -> RunState:
        agent = self.agents["context_analyzer"]
        state = agent.pre_execute(state)
        state = agent.execute(state)
        return agent.post_execute(state)

    def _run_pillar_synthesizer(self, state: RunState) -> RunState:
        agent = self.agents["pillar_synthesizer"]
        state = agent.pre_execute(state)
        state = agent.execute(state)
        return agent.post_execute(state)

    def _run_goal_generator(self, state: RunState) -> RunState:
        agent = self.agents["goal_generator"]
        state = agent.pre_execute(state)
        state = agent.execute(state)
        return agent.post_execute(state)

    def _run_initiative_designer(self, state: RunState) -> RunState:
        agent = self.agents["initiative_designer"]
        state = agent.pre_execute(state)
        state = agent.execute(state)
        return agent.post_execute(state)

    def _run_risk_assessor(self, state: RunState) -> RunState:
        agent = self.agents["risk_assessor"]
        state = agent.pre_execute(state)
        state = agent.execute(state)
        return agent.post_execute(state)

    def _run_resource_planner(self, state: RunState) -> RunState:
        agent = self.agents["resource_planner"]
        state = agent.pre_execute(state)
        state = agent.execute(state)
        return agent.post_execute(state)

    def _run_timeline_optimizer(self, state: RunState) -> RunState:
        agent = self.agents["timeline_optimizer"]
        state = agent.pre_execute(state)
        state = agent.execute(state)
        return agent.post_execute(state)

    def _run_validator(self, state: RunState) -> RunState:
        agent = self.agents["validator"]
        state = agent.pre_execute(state)
        state = agent.execute(state)
        return agent.post_execute(state)

    def _run_output_generator(self, state: RunState) -> RunState:
        agent = self.agents["output_generator"]
        state = agent.pre_execute(state)
        state = agent.execute(state)
        return agent.post_execute(state)

    def _run_feedback_processor(self, state: RunState) -> RunState:
        if not self.enable_feedback_loop or not state.config.feedback.enabled:
            return state
        agent = self.agents["feedback_processor"]
        state = agent.pre_execute(state)
        state = agent.execute(state)
        return agent.post_execute(state)

    def _run_learning_optimizer(self, state: RunState) -> RunState:
        if not self.enable_feedback_loop or not state.config.feedback.enabled:
            return state
        agent = self.agents["learning_optimizer"]
        state = agent.pre_execute(state)
        state = agent.execute(state)
        return agent.post_execute(state)

    # Quality gate methods
    def _gate_vision(self, state: RunState) -> RunState:
        gate = QualityGate("G1_Vision", state.config.thresholds)
        results = gate.validate_vision_extraction(state)
        self._process_gate_results(state, "G1_Vision", results)
        return state

    def _gate_pillars(self, state: RunState) -> RunState:
        gate = QualityGate("G2_Pillars", state.config.thresholds)
        results = gate.validate_pillar_synthesis(state)
        self._process_gate_results(state, "G2_Pillars", results)
        return state

    def _gate_goals(self, state: RunState) -> RunState:
        gate = QualityGate("G3_Goals", state.config.thresholds)
        results = gate.validate_goal_generation(state)
        self._process_gate_results(state, "G3_Goals", results)
        return state

    def _gate_initiatives(self, state: RunState) -> RunState:
        gate = QualityGate("G4_Initiatives", state.config.thresholds)
        results = gate.validate_initiative_design(state)
        self._process_gate_results(state, "G4_Initiatives", results)
        return state

    def _gate_risks(self, state: RunState) -> RunState:
        gate = QualityGate("G5_Risks", state.config.thresholds)
        results = gate.validate_risk_assessment(state)
        self._process_gate_results(state, "G5_Risks", results)
        return state

    def _gate_validation(self, state: RunState) -> RunState:
        gate = QualityGate("G6_Validation", state.config.thresholds)
        results = gate.validate_strategy_quality(state)
        self._process_gate_results(state, "G6_Validation", results)
        return state

    def _process_gate_results(self, state: RunState, gate_id: str, results: list):
        """Process gate validation results and add flags."""
        for result in results:
            if not result.passed:
                severity = SeverityLevel(result.severity)
                state.add_flag(
                    step_id=gate_id,
                    severity=severity,
                    flag_type=result.rule_name,
                    message=result.message,
                    metadata=result.metadata
                )

        # Store gate result for routing
        blocking_count = sum(1 for r in results if r.blocking and not r.passed)
        state.working_data[f"{gate_id}_blocking_failures"] = blocking_count

    def _route_after_gate(self, state: RunState) -> Literal["continue", "fail"]:
        """Route based on gate results."""
        # Get the most recent gate result
        current_step = state.current_step or ""

        # Check for blocking failures in current step
        blocking_key = f"{current_step}_blocking_failures"
        blocking_failures = state.working_data.get(blocking_key, 0)

        if blocking_failures > 0:
            return "fail"

        # In strict mode, any error is blocking
        if state.config.strict_mode:
            error_flags = [
                f for f in state.flags
                if f.step_id == current_step and
                f.severity in [SeverityLevel.ERROR, SeverityLevel.CRITICAL] and
                not f.resolved
            ]
            if error_flags:
                return "fail"

        return "continue"

    def _route_after_validation(self, state: RunState) -> Literal["continue", "remediate", "fail"]:
        """Route after validation gate - may trigger remediation."""
        validation_result = state.working_data.get("validation_result", {})
        certification = validation_result.get("certification", {})

        # Critical failure
        if state.working_data.get("G6_Validation_blocking_failures", 0) > 0:
            return "fail"

        # Check if remediation needed (not yet implemented - would loop back)
        # For now, just continue or fail
        if certification.get("ready_for_approval", True):
            return "continue"

        # Has blocking issues
        if certification.get("blocking_issues", []):
            return "fail"

        return "continue"

    def run(self, initial_state: RunState) -> RunState:
        """Execute the workflow."""
        return self.graph.invoke(initial_state)

    def run_with_checkpoints(
        self,
        initial_state: RunState,
        checkpoint_dir: Optional[str] = None
    ) -> RunState:
        """Execute the workflow with checkpointing enabled."""
        from pathlib import Path
        from src.orchestrator.state import save_state_checkpoint

        if checkpoint_dir:
            checkpoint_path = Path(checkpoint_dir)
        else:
            checkpoint_path = Path("./data/checkpoints")

        # Add checkpoint callback
        def checkpoint_callback(state: RunState) -> RunState:
            if state.config.checkpoint_enabled:
                save_state_checkpoint(state, checkpoint_path)
            return state

        # Run with checkpointing (simplified - full implementation would use LangGraph checkpointing)
        return self.graph.invoke(initial_state)
