"""Vision Extractor Agent - Extracts and structures strategic vision from inputs."""

from typing import Optional
import uuid

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState, SeverityLevel, WorkflowPhase
from src.schemas.strategy import StrategicVision, VisionExtractionOutput


class VisionExtractorAgent(BaseAgent[VisionExtractionOutput]):
    """
    Agent that extracts strategic vision from input documents.

    Responsibilities:
    - Parse vision/mission documents
    - Extract core values and success criteria
    - Structure the strategic context
    - Validate completeness of vision elements
    """

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(
            agent_id="S1_VisionExtractor",
            step_name="Vision Extraction",
            phase=WorkflowPhase.INGESTION,
            model_name=model_name,
        )

    def get_system_prompt(self) -> str:
        return """You are an expert strategic planning analyst specializing in extracting and structuring organizational vision and mission statements.

Your task is to analyze input documents and extract a comprehensive strategic vision including:

1. **Vision Statement**: The long-term aspirational future state (what the organization wants to become)
2. **Mission Statement**: The organization's core purpose and reason for existence
3. **Core Values**: The fundamental beliefs and principles that guide behavior
4. **Value Proposition**: The unique value delivered to stakeholders
5. **Strategic Context**: Key assumptions, market conditions, and environmental factors
6. **Success Criteria**: How success will be measured at the strategic level

Guidelines:
- Extract verbatim when possible, or synthesize from multiple sources if needed
- Identify implicit elements that aren't explicitly stated but are clearly implied
- Flag any missing or incomplete elements
- Maintain traceability to source text
- Rate your confidence in each extraction

Output should be structured JSON following the VisionExtractionOutput schema.

Be thorough but concise. Focus on strategic-level elements, not operational details."""

    def get_required_inputs(self) -> list[str]:
        return []  # Can work with raw inputs from RunInputs

    def get_output_keys(self) -> list[str]:
        return ["vision", "vision_extraction_confidence", "vision_warnings"]

    def validate_inputs(self, state: RunState) -> bool:
        """Validate that we have some vision-related input."""
        has_file = state.inputs.vision_document is not None
        has_text = state.inputs.raw_vision_text is not None
        has_goals = state.inputs.raw_goals_text is not None

        return has_file or has_text or has_goals

    def execute(self, state: RunState) -> RunState:
        """Extract vision from inputs."""

        # Gather all available vision-related input
        input_text = self._gather_inputs(state)

        if not input_text:
            self.add_flag(
                state,
                SeverityLevel.CRITICAL,
                "NO_VISION_INPUT",
                "No vision or strategy input provided"
            )
            return state

        # Build the extraction prompt
        user_prompt = f"""Please extract the strategic vision from the following input:

---INPUT START---
{input_text}
---INPUT END---

Extract and structure the following elements:
1. Vision Statement
2. Mission Statement
3. Core Values (as a list)
4. Value Proposition
5. Strategic Context
6. Success Criteria (as a list)
7. Time Horizon (if specified)

For each element, provide:
- The extracted content
- Source text reference (if applicable)
- Confidence score (0-1)

Also provide:
- Overall extraction confidence
- List of warnings for missing or unclear elements

Return your response as valid JSON matching this structure:
{{
    "vision": {{
        "vision_statement": "...",
        "mission_statement": "...",
        "core_values": ["value1", "value2"],
        "value_proposition": "...",
        "strategic_context": "...",
        "success_criteria": ["criterion1", "criterion2"],
        "time_horizon_years": 3,
        "confidence_score": 0.85
    }},
    "extraction_confidence": 0.85,
    "warnings": ["warning1", "warning2"]
}}"""

        # Get enhanced prompt with any learnings
        system_prompt = self.get_prompt_with_learnings(state)

        # Invoke LLM
        response = self.invoke_llm(user_prompt, system_prompt)

        # Parse response
        try:
            result = self.extract_json_from_response(response)

            # Create StrategicVision object
            vision_data = result.get("vision", {})
            vision = StrategicVision(
                vision_statement=vision_data.get("vision_statement", ""),
                mission_statement=vision_data.get("mission_statement", ""),
                core_values=vision_data.get("core_values", []),
                value_proposition=vision_data.get("value_proposition"),
                strategic_context=vision_data.get("strategic_context"),
                success_criteria=vision_data.get("success_criteria", []),
                time_horizon_years=vision_data.get("time_horizon_years", state.config.time_horizon_years),
                confidence_score=vision_data.get("confidence_score", 0.5),
            )

            # Store in working data
            state.working_data["vision"] = vision.model_dump()
            state.working_data["vision_extraction_confidence"] = result.get("extraction_confidence", 0.5)
            state.working_data["vision_warnings"] = result.get("warnings", [])

            # Add flags for warnings
            warnings = result.get("warnings", [])
            for warning in warnings:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "VISION_EXTRACTION_WARNING",
                    warning
                )

            # Check for critical missing elements
            if not vision.vision_statement:
                self.add_flag(
                    state,
                    SeverityLevel.ERROR,
                    "MISSING_VISION_STATEMENT",
                    "Vision statement could not be extracted"
                )

            if not vision.mission_statement:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "MISSING_MISSION_STATEMENT",
                    "Mission statement could not be extracted"
                )

            self.logger.info(
                f"Vision extracted with confidence {result.get('extraction_confidence', 0):.2f}"
            )

        except Exception as e:
            self.add_flag(
                state,
                SeverityLevel.ERROR,
                "VISION_EXTRACTION_FAILED",
                f"Failed to parse vision extraction: {str(e)}"
            )
            self.logger.error(f"Vision extraction failed: {e}")

        return state

    def _gather_inputs(self, state: RunState) -> str:
        """Gather all vision-related inputs into a single text."""
        parts = []

        # Add raw text inputs
        if state.inputs.raw_vision_text:
            parts.append(f"## Vision/Strategy Text\n{state.inputs.raw_vision_text}")

        if state.inputs.raw_goals_text:
            parts.append(f"## Goals Text\n{state.inputs.raw_goals_text}")

        if state.inputs.raw_context_text:
            parts.append(f"## Additional Context\n{state.inputs.raw_context_text}")

        # Read from files if provided
        if state.inputs.vision_document and state.inputs.vision_document.exists():
            try:
                content = state.inputs.vision_document.read_text()
                parts.append(f"## Vision Document\n{content}")
            except Exception as e:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "FILE_READ_ERROR",
                    f"Could not read vision document: {e}"
                )

        if state.inputs.current_state_analysis and state.inputs.current_state_analysis.exists():
            try:
                content = state.inputs.current_state_analysis.read_text()
                parts.append(f"## Current State Analysis\n{content}")
            except Exception as e:
                self.add_flag(
                    state,
                    SeverityLevel.WARNING,
                    "FILE_READ_ERROR",
                    f"Could not read current state analysis: {e}"
                )

        return "\n\n".join(parts)
