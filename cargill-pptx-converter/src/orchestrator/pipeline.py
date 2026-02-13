"""
Conversion Pipeline Orchestrator

Runs all agents in sequence to transform input documents into
Cargill-branded PowerPoint presentations.
"""

import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from src.agents.base import BaseAgent
from src.agents.brand_compliance import BrandComplianceAgent
from src.agents.chart_builder import ChartBuilderAgent
from src.agents.content_extractor import ContentExtractorAgent
from src.agents.pptx_builder import PptxBuilderAgent
from src.agents.quality_assurance import QualityAssuranceAgent
from src.agents.slide_architect import SlideArchitectAgent
from src.agents.visual_designer import VisualDesignerAgent
from src.schemas.run_state import RunConfig, RunInputs, RunState

logger = logging.getLogger("cargill_pptx")


class ConversionPipeline:
    """Sequential pipeline that runs all conversion agents."""

    def __init__(self, config: RunConfig = None):
        self.config = config or RunConfig()
        self.agents: list[BaseAgent] = [
            ContentExtractorAgent(),    # S1: Extract content
            BrandComplianceAgent(),     # S2: Check brand compliance
            SlideArchitectAgent(),      # S3: Design slide structure
            VisualDesignerAgent(),      # S4: Apply visual design
            ChartBuilderAgent(),        # S5: Build charts
            QualityAssuranceAgent(),    # S6: Quality assurance
            PptxBuilderAgent(),         # S7: Render PPTX
        ]

    def run(self, input_file: str, output_path: str = None) -> RunState:
        """
        Execute the full conversion pipeline.

        Args:
            input_file: Path to the input document.
            output_path: Optional output PPTX path.

        Returns:
            Final RunState with results and artifacts.
        """
        # Initialize state
        state = RunState(
            inputs=RunInputs(
                input_file=input_file,
                output_path=output_path,
            ),
            config=self.config,
        )

        start_time = time.time()
        logger.info(f"Starting Cargill branding pipeline")
        logger.info(f"Input: {input_file}")
        logger.info(f"Run ID: {state.run_id}")

        # Execute each agent
        for agent in self.agents:
            step_start = time.time()
            logger.info(f"Stage {agent.agent_id}: {agent.step_name}")

            try:
                state = agent.execute(state)
            except Exception as e:
                state.add_flag(
                    step_id=agent.agent_id,
                    severity="CRITICAL",
                    message=f"Agent failed with exception: {e}",
                )
                logger.error(f"Agent {agent.agent_id} failed: {e}")

            step_elapsed = time.time() - step_start
            logger.info(f"  Completed in {step_elapsed:.1f}s")

            # Check for critical failures
            critical_flags = [
                f for f in state.flags
                if f.step_id == agent.agent_id and f.severity == "CRITICAL"
            ]
            if critical_flags:
                logger.error(f"Pipeline halted at {agent.step_name}")
                for flag in critical_flags:
                    logger.error(f"  CRITICAL: {flag.message}")
                break

        total_elapsed = time.time() - start_time
        logger.info(f"Pipeline completed in {total_elapsed:.1f}s")

        # Log summary
        self._log_summary(state)

        return state

    def _log_summary(self, state: RunState):
        """Log a summary of the pipeline run."""
        logger.info("=" * 60)
        logger.info("PIPELINE SUMMARY")
        logger.info("=" * 60)

        if state.output_file:
            logger.info(f"Output: {state.output_file}")

        if state.presentation_plan:
            logger.info(f"Slides: {state.presentation_plan.total_slides}")
            logger.info(f"Flow: {state.presentation_plan.presentation_flow}")

        if state.compliance_report:
            logger.info(f"Brand compliance: {state.compliance_report.overall_score}")
            logger.info(f"Compliance status: {state.compliance_report.status}")

        if state.qa_report:
            logger.info(f"QA score: {state.qa_report.overall_score}/100")
            logger.info(f"QA status: {state.qa_report.status}")
            if state.qa_report.issues:
                logger.info(f"QA issues: {len(state.qa_report.issues)}")

        warning_count = sum(1 for f in state.flags if f.severity == "WARNING")
        error_count = sum(1 for f in state.flags if f.severity in ("ERROR", "CRITICAL"))

        if warning_count:
            logger.warning(f"Warnings: {warning_count}")
        if error_count:
            logger.error(f"Errors: {error_count}")

        if state.output_file:
            logger.info("Pipeline completed successfully")
        else:
            logger.error("Pipeline did not produce output")

        logger.info("=" * 60)


def convert_document(
    input_file: str,
    output_path: str = None,
    config: RunConfig = None,
) -> RunState:
    """
    Convenience function to convert a document to Cargill-branded PPTX.

    Args:
        input_file: Path to input document.
        output_path: Optional output path for PPTX.
        config: Optional pipeline configuration.

    Returns:
        RunState with results.
    """
    pipeline = ConversionPipeline(config=config)
    return pipeline.run(input_file, output_path)
