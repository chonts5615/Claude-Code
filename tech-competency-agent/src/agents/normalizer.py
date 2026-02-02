"""Step 3: Normalizer Agent - Normalizes competencies to standard format."""

from pathlib import Path
from typing import List, Dict, Set
from collections import defaultdict
import anthropic
import json

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.competency import (
    NormalizedCompetenciesOutput,
    JobCompetencies,
    TechnicalCompetency,
    AppliedScope,
    ResponsibilityTrace,
    OverlapCheck,
    BenchmarkingRecord,
    CompetencyLibrary,
    CompetencyLibraryEntry
)
from src.schemas.job import Job, JobExtractionOutput
from src.schemas.mapping import CompetencyMappingOutput, JobMapping, ResponsibilityMapping


class NormalizerAgent(BaseAgent):
    """Normalizes competencies to standard format with proper structure."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()

    def execute(self, state: RunState) -> RunState:
        """
        Normalize competencies to standard format.

        Args:
            state: Current workflow state

        Returns:
            Updated state with normalized competencies
        """
        state.current_step = self.agent_id

        # Load previous step outputs
        jobs = self._load_jobs(state)
        mappings = self._load_mappings(state)
        competency_library = self._load_competency_library(state)

        # Create normalized competencies for each job
        jobs_competencies = []
        for job, job_mapping in zip(jobs, mappings.job_mappings):
            job_comps = self._normalize_job_competencies(
                job, job_mapping, competency_library, state
            )
            jobs_competencies.append(job_comps)

        # Create output
        output = NormalizedCompetenciesOutput(
            jobs=jobs_competencies,
            processing_version="v2",
            total_competencies=sum(jc.competency_count() for jc in jobs_competencies)
        )

        # Save artifact
        output_path = Path(f"data/output/{state.run_id}_s3_normalized_v2.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(output.json(indent=2))

        state.artifacts.normalized_v2 = output_path

        # Add quality flags
        self._add_quality_flags(state, jobs_competencies)

        return state

    def _load_jobs(self, state: RunState) -> List[Job]:
        """Load jobs from Step 1 output."""
        if not state.artifacts.jobs_extracted:
            raise ValueError("Jobs not extracted yet - Step 1 must run first")

        with open(state.artifacts.jobs_extracted, 'r') as f:
            output = JobExtractionOutput.parse_raw(f.read())
        return output.jobs

    def _load_mappings(self, state: RunState) -> CompetencyMappingOutput:
        """Load competency mappings from Step 2 output."""
        if not state.artifacts.competency_map_v1:
            raise ValueError("Competency mappings not created yet - Step 2 must run first")

        with open(state.artifacts.competency_map_v1, 'r') as f:
            return CompetencyMappingOutput.parse_raw(f.read())

    def _load_competency_library(self, state: RunState) -> Dict[str, CompetencyLibraryEntry]:
        """Load competency library and create lookup dictionary."""
        from src.utils.file_parsers import parse_competency_library

        all_comps = []
        for source_file in state.inputs.tech_comp_source_files:
            comps = parse_competency_library(source_file)
            all_comps.extend(comps)

        # Create lookup dictionary
        return {comp.competency_id: comp for comp in all_comps}

    def _normalize_job_competencies(
        self,
        job: Job,
        job_mapping: JobMapping,
        library: Dict[str, CompetencyLibraryEntry],
        state: RunState
    ) -> JobCompetencies:
        """Create normalized competencies for a single job."""

        # Group responsibilities by competency (select top candidate for each responsibility)
        competency_responsibilities = defaultdict(list)
        for resp_mapping in job_mapping.responsibility_mappings:
            top_candidate = resp_mapping.top_candidate()
            if top_candidate and top_candidate.relevance_score >= 0.6:
                competency_responsibilities[top_candidate.competency_id].append(
                    (resp_mapping.responsibility_id, top_candidate)
                )

        # Create normalized competencies
        normalized_comps = []
        for comp_id, resp_list in competency_responsibilities.items():
            if comp_id in library:
                lib_entry = library[comp_id]
                normalized_comp = self._create_normalized_competency(
                    lib_entry, resp_list, job
                )
                normalized_comps.append(normalized_comp)

        return JobCompetencies(
            job_id=job.job_id,
            technical_competencies=normalized_comps
        )

    def _create_normalized_competency(
        self,
        lib_entry: CompetencyLibraryEntry,
        resp_list: List[tuple],
        job: Job
    ) -> TechnicalCompetency:
        """Create a normalized technical competency from library entry."""

        # Extract behavioral indicators from library entry
        behavioral_indicators = lib_entry.indicators[:7] if lib_entry.indicators else []

        # Ensure we have at least 3 indicators (quality standard)
        if len(behavioral_indicators) < 3:
            behavioral_indicators.extend([
                f"Applies {lib_entry.name} in work context",
                f"Demonstrates proficiency in {lib_entry.name}",
                f"Delivers outcomes using {lib_entry.name}"
            ][:3 - len(behavioral_indicators)])

        # Create applied scope from tags and evidence
        tools_methods = []
        standards_frameworks = []

        for evidence in lib_entry.source_evidence:
            if evidence.source_type in ["SFIA", "NICE", "ONET"]:
                standards_frameworks.append(evidence.source_title)

        # Extract tools from tags
        tech_keywords = ["Python", "SQL", "AWS", "Java", "Kubernetes", "Docker", "React", "API"]
        for tag in lib_entry.tags:
            for keyword in tech_keywords:
                if keyword.lower() in tag.lower():
                    tools_methods.append(keyword)

        applied_scope = AppliedScope(
            tools_methods_tech=list(set(tools_methods))[:5],
            standards_frameworks=list(set(standards_frameworks))[:3],
            typical_outputs=["Technical deliverables", "Work products"]
        )

        # Create responsibility traces
        responsibility_traces = []
        for resp_id, candidate in resp_list:
            trace = ResponsibilityTrace(
                responsibility_id=resp_id,
                contribution="PRIMARY" if candidate.relevance_score >= 0.8 else "SECONDARY",
                justification=candidate.mapping_rationale
            )
            responsibility_traces.append(trace)

        # Create placeholder overlap check (will be populated in Step 4)
        overlap_check = OverlapCheck(
            core_leadership_overlap="NONE",
            overlap_domains=[],
            similarity_score=None,
            remediation_notes=None
        )

        # Create placeholder benchmarking record (will be populated in Step 6)
        benchmarking = BenchmarkingRecord(
            benchmarked_against=[],
            changes_made=None,
            evidence_refs=[],
            benchmark_alignment_score=None
        )

        # Create normalized competency
        definition = lib_entry.definition if len(lib_entry.definition.split()) >= 50 else \
                    f"{lib_entry.definition} This competency is essential for effective job performance."

        word_count = len(definition.split())

        return TechnicalCompetency(
            competency_id=lib_entry.competency_id,
            name=lib_entry.name[:80],  # Enforce 80 char limit
            definition=definition,
            why_it_matters=f"This competency is critical for {job.job_title} because it directly supports key job responsibilities and enables successful performance.",
            behavioral_indicators=behavioral_indicators,
            applied_scope=applied_scope,
            responsibility_trace=responsibility_traces,
            overlap_check=overlap_check,
            benchmarking=benchmarking,
            word_count_definition=word_count,
            indicator_count=len(behavioral_indicators)
        )

    def _add_quality_flags(self, state: RunState, jobs_competencies: List[JobCompetencies]):
        """Add quality flags for normalization issues."""
        for job_comps in jobs_competencies:
            # Check if job has too few competencies
            if job_comps.competency_count() < 3:
                self.add_flag(
                    state,
                    severity="WARNING",
                    flag_type="LOW_COMPETENCY_COUNT",
                    message=f"Job {job_comps.job_id} has only {job_comps.competency_count()} competencies",
                    job_id=job_comps.job_id,
                    metadata={"count": job_comps.competency_count()}
                )

            # Check individual competency quality
            for comp in job_comps.technical_competencies:
                # Check definition length
                if comp.word_count_definition and comp.word_count_definition < 50:
                    self.add_flag(
                        state,
                        severity="WARNING",
                        flag_type="SHORT_DEFINITION",
                        message=f"Competency {comp.name} has short definition ({comp.word_count_definition} words)",
                        job_id=job_comps.job_id,
                        metadata={"competency_id": comp.competency_id, "word_count": comp.word_count_definition}
                    )

                # Check indicator count
                if comp.indicator_count and comp.indicator_count < 3:
                    self.add_flag(
                        state,
                        severity="WARNING",
                        flag_type="FEW_INDICATORS",
                        message=f"Competency {comp.name} has only {comp.indicator_count} behavioral indicators",
                        job_id=job_comps.job_id,
                        metadata={"competency_id": comp.competency_id, "indicator_count": comp.indicator_count}
                    )

    def get_system_prompt(self) -> str:
        """Return system prompt for normalization."""
        return """You are a Competency Normalization Specialist with expertise in IO Psychology.

Your task is to normalize competencies to a consistent, high-quality format.

Normalization standards:
1. Name: "Domain: Specific Skill" format (max 80 chars)
2. Definition: 50-150 words, work-context specific, includes tools/methods
3. Why it matters: 2-3 sentences explaining business/role impact
4. Behavioral indicators: 3-7 observable, assessable behaviors
5. Applied scope: Tools, standards, typical outputs

Quality criteria:
- Definitions are concrete and applied (not generic)
- Indicators are measurable and observable
- Technical terms are explained where needed
- All fields complete and coherent

Output structured JSON conforming to TechnicalCompetency schema."""
