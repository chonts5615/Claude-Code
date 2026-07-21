"""Base agent class for strategy workflow."""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Dict, Any
from datetime import datetime
import json
import logging

from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from src.schemas.run_state import RunState, RunFlag, SeverityLevel, WorkflowPhase


OutputT = TypeVar('OutputT', bound=BaseModel)


class AgentExecutionResult(BaseModel):
    """Result from agent execution."""
    success: bool
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    tokens_used: int = 0
    metadata: Dict[str, Any] = {}


class BaseAgent(ABC, Generic[OutputT]):
    """Base class for all agents in the strategy workflow."""

    def __init__(
        self,
        agent_id: str,
        step_name: str,
        phase: WorkflowPhase,
        model_name: str = "claude-sonnet-4-20250514",
        temperature: float = 0.3,
    ):
        self.agent_id = agent_id
        self.step_name = step_name
        self.phase = phase
        self.model_name = model_name
        self.temperature = temperature
        self.logger = logging.getLogger(f"agent.{agent_id}")

        # Initialize LLM based on model name
        self._llm = self._initialize_llm()

    def _initialize_llm(self):
        """Initialize the LLM client."""
        if "claude" in self.model_name.lower():
            return ChatAnthropic(
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=8192,
            )
        elif "gpt" in self.model_name.lower():
            return ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=8192,
            )
        else:
            # Default to Claude
            return ChatAnthropic(
                model="claude-sonnet-4-20250514",
                temperature=self.temperature,
                max_tokens=8192,
            )

    @abstractmethod
    def execute(self, state: RunState) -> RunState:
        """
        Execute agent logic.

        Args:
            state: Current workflow state

        Returns:
            Updated workflow state
        """
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return agent-specific system prompt."""
        pass

    def validate_inputs(self, state: RunState) -> bool:
        """
        Validate required inputs exist in state.

        Override in subclasses to add specific validation.
        Returns True if inputs are valid.
        """
        return True

    def get_required_inputs(self) -> list[str]:
        """Return list of required input keys in state.working_data."""
        return []

    def get_output_keys(self) -> list[str]:
        """Return list of keys this agent adds to state.working_data."""
        return []

    def add_flag(
        self,
        state: RunState,
        severity: SeverityLevel,
        flag_type: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a quality flag to the run state."""
        flag = RunFlag(
            step_id=self.agent_id,
            phase=self.phase,
            severity=severity,
            flag_type=flag_type,
            message=message,
            metadata=metadata or {}
        )
        state.flags.append(flag)
        self.logger.info(f"Flag added: [{severity.value}] {flag_type}: {message}")

    def invoke_llm(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        output_schema: Optional[type[BaseModel]] = None
    ) -> str:
        """
        Invoke the LLM with the given messages.

        Args:
            user_message: The user message to send
            system_prompt: Optional override for system prompt
            output_schema: Optional Pydantic model for structured output

        Returns:
            LLM response text
        """
        prompt = system_prompt or self.get_system_prompt()

        messages = [
            ("system", prompt),
            ("human", user_message)
        ]

        if output_schema:
            # Use structured output
            structured_llm = self._llm.with_structured_output(output_schema)
            response = structured_llm.invoke(messages)
            return response
        else:
            response = self._llm.invoke(messages)
            return response.content

    def invoke_llm_with_history(
        self,
        messages: list[tuple[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Invoke the LLM with conversation history.

        Args:
            messages: List of (role, content) tuples
            system_prompt: Optional override for system prompt

        Returns:
            LLM response text
        """
        prompt = system_prompt or self.get_system_prompt()
        full_messages = [("system", prompt)] + messages

        response = self._llm.invoke(full_messages)
        return response.content

    def extract_json_from_response(self, response: str) -> Dict[str, Any]:
        """
        Extract JSON from an LLM response.

        Handles responses with markdown code blocks.
        """
        # Try to find JSON in code blocks
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            json_str = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            json_str = response[start:end].strip()
        else:
            json_str = response.strip()

        return json.loads(json_str)

    def pre_execute(self, state: RunState) -> RunState:
        """
        Pre-execution hook. Called before execute().

        Updates state tracking and validates inputs.
        """
        state.current_step = self.agent_id
        state.current_phase = self.phase

        self.logger.info(f"Starting {self.step_name} (Phase: {self.phase.value})")

        # Validate inputs
        if not self.validate_inputs(state):
            self.add_flag(
                state,
                SeverityLevel.ERROR,
                "INPUT_VALIDATION_FAILED",
                f"Required inputs not available for {self.agent_id}"
            )

        return state

    def post_execute(self, state: RunState) -> RunState:
        """
        Post-execution hook. Called after execute().

        Updates completion tracking.
        """
        state.mark_step_complete(self.agent_id)
        self.logger.info(f"Completed {self.step_name}")

        return state

    def apply_learning_context(self, state: RunState) -> Dict[str, Any]:
        """
        Get any learning context relevant to this agent.

        Returns adjustments/optimizations from feedback loop.
        """
        agent_learnings = state.learning_context.get(self.agent_id, {})
        return agent_learnings

    def get_prompt_with_learnings(self, state: RunState) -> str:
        """
        Get system prompt enhanced with learning context.

        Incorporates feedback-driven optimizations.
        """
        base_prompt = self.get_system_prompt()
        learnings = self.apply_learning_context(state)

        if not learnings:
            return base_prompt

        # Add learning-based additions to prompt
        additions = learnings.get("prompt_additions", [])
        if additions:
            additions_text = "\n\nAdditional guidance from system learning:\n"
            for addition in additions:
                additions_text += f"- {addition}\n"
            return base_prompt + additions_text

        return base_prompt


class AgentChain:
    """Chain multiple agents together for sequential execution."""

    def __init__(self, agents: list[BaseAgent]):
        self.agents = agents

    def execute(self, state: RunState) -> RunState:
        """Execute all agents in sequence."""
        for agent in self.agents:
            state = agent.pre_execute(state)
            state = agent.execute(state)
            state = agent.post_execute(state)

            # Check for critical flags that should halt execution
            critical_flags = [
                f for f in state.flags
                if f.step_id == agent.agent_id
                and f.severity == SeverityLevel.CRITICAL
                and not f.resolved
            ]
            if critical_flags:
                break

        return state
