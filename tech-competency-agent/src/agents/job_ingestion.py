"""Step 1: Job Ingestion Agent - Extracts jobs from Excel/Word/PDF files."""

from pathlib import Path
from datetime import datetime
from typing import List
import anthropic

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.job import (
    Job,
    Responsibility,
    JobSummary,
    SourceMetadata,
    JobExtractionOutput,
    ExtractionWarning
)
from src.utils.file_parsers import parse_excel_jobs


class JobIngestionAgent(BaseAgent):
    """Extracts and normalizes job descriptions from source files."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()

    def execute(self, state: RunState) -> RunState:
        """
        Extract jobs from input file.

        Args:
            state: Current workflow state

        Returns:
            Updated state with job extraction output
        """
        state.current_step = self.agent_id

        # Parse jobs from file
        jobs_file = state.inputs.jobs_file
        jobs, warnings = self._parse_jobs_file(jobs_file)

        # Create output
        output = JobExtractionOutput(
            jobs=jobs,
            extraction_warnings=warnings,
            total_jobs_extracted=len(jobs),
            total_responsibilities_extracted=sum(j.responsibility_count() for j in jobs)
        )

        # Save artifact
        output_path = Path(f"data/output/{state.run_id}_s1_jobs_extracted.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(output.json(indent=2))

        state.artifacts.jobs_extracted = output_path

        # Add warnings as flags
        for warning in warnings:
            self.add_flag(
                state,
                severity=warning.severity,
                flag_type=warning.warning_type,
                message=warning.message,
                job_id=warning.job_id,
                metadata={}
            )

        return state

    def _parse_jobs_file(self, file_path: Path) -> tuple[List[Job], List[ExtractionWarning]]:
        """Parse jobs from file based on file type."""
        if file_path.suffix.lower() in ['.xlsx', '.xls']:
            return parse_excel_jobs(file_path)
        elif file_path.suffix.lower() in ['.docx', '.doc']:
            # TODO: Implement Word parsing
            return [], [ExtractionWarning(
                warning_type="OTHER",
                message=f"Word file parsing not yet implemented: {file_path}",
                severity="ERROR"
            )]
        elif file_path.suffix.lower() == '.pdf':
            # TODO: Implement PDF parsing
            return [], [ExtractionWarning(
                warning_type="OTHER",
                message=f"PDF parsing not yet implemented: {file_path}",
                severity="ERROR"
            )]
        else:
            return [], [ExtractionWarning(
                warning_type="OTHER",
                message=f"Unsupported file format: {file_path.suffix}",
                severity="ERROR"
            )]

    def get_system_prompt(self) -> str:
        """Return system prompt for job extraction."""
        return """You are a Job Description Extraction Specialist with expertise in IO Psychology.

Your task is to extract and normalize job descriptions from provided documents.

For each job, extract:
1. Job title
2. Job family/category (if available)
3. Job level/grade (if available)
4. Job summary (2-3 sentence overview)
5. List of responsibilities (each as a separate item)

Normalization rules:
- Clean up formatting artifacts (bullets, numbering, extra whitespace)
- Preserve technical terms and acronyms
- Split combined responsibilities into separate items
- Flag ambiguous or unclear entries
- Maintain traceability to source location

Quality standards:
- Minimum 5 responsibilities per job (flag if fewer)
- Job summary should be present (flag if missing)
- Each responsibility should be a complete, actionable statement
- Avoid duplicates within same job

Output structured JSON conforming to the Job schema."""
