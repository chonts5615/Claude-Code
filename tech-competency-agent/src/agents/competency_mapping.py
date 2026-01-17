"""Step 2: Competency Mapping Agent - Maps responsibilities to competencies."""

from pathlib import Path
from typing import List
import anthropic

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.job import Job, JobExtractionOutput
from src.schemas.competency import CompetencyLibrary, CompetencyLibraryEntry
from src.schemas.mapping import (
    CompetencyMappingOutput,
    JobMapping,
    ResponsibilityMapping,
    CompetencyCandidate
)
from src.utils.file_parsers import parse_competency_library
from src.utils.similarity import compute_similarity


class CompetencyMappingAgent(BaseAgent):
    """Maps job responsibilities to technical competencies."""

    def __init__(self, agent_id: str, step_name: str):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()

    def execute(self, state: RunState) -> RunState:
        """
        Map responsibilities to competencies.

        Args:
            state: Current workflow state

        Returns:
            Updated state with mapping output
        """
        state.current_step = self.agent_id

        # Load jobs
        jobs = self._load_jobs(state)

        # Load competency library
        competency_library = self._load_competency_library(state)

        # Map each job's responsibilities
        job_mappings = []
        for job in jobs:
            job_mapping = self._map_job_responsibilities(job, competency_library)
            job_mappings.append(job_mapping)

        # Calculate statistics
        total_mappings = sum(
            len(jm.responsibility_mappings) for jm in job_mappings
        )
        total_candidates = sum(
            len(rm.candidates)
            for jm in job_mappings
            for rm in jm.responsibility_mappings
        )
        avg_candidates = total_candidates / total_mappings if total_mappings > 0 else 0

        total_responsibilities = sum(len(jm.responsibility_mappings) for jm in job_mappings)
        unmapped_count = sum(len(jm.unmapped_responsibilities()) for jm in job_mappings)
        unmapped_rate = unmapped_count / total_responsibilities if total_responsibilities > 0 else 0

        # Create output
        output = CompetencyMappingOutput(
            job_mappings=job_mappings,
            total_mappings_created=total_mappings,
            average_candidates_per_responsibility=avg_candidates,
            unmapped_responsibility_rate=unmapped_rate
        )

        # Save artifact
        output_path = Path(f"data/output/{state.run_id}_s2_competency_map_v1.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(output.json(indent=2))

        state.artifacts.competency_map_v1 = output_path

        return state

    def _load_jobs(self, state: RunState) -> List[Job]:
        """Load jobs from previous step."""
        if not state.artifacts.jobs_extracted:
            raise ValueError("Jobs not extracted yet")

        with open(state.artifacts.jobs_extracted, 'r') as f:
            extraction_output = JobExtractionOutput.parse_raw(f.read())

        return extraction_output.jobs

    def _load_competency_library(self, state: RunState) -> CompetencyLibrary:
        """Load and parse competency library from source files."""
        competencies = []
        for source_file in state.inputs.tech_comp_source_files:
            comps = parse_competency_library(source_file)
            competencies.extend(comps)

        return CompetencyLibrary(
            competencies=competencies,
            total_sources_processed=len(state.inputs.tech_comp_source_files),
            ingestion_timestamp=str(state.run_timestamp_utc)
        )

    def _map_job_responsibilities(
        self,
        job: Job,
        library: CompetencyLibrary
    ) -> JobMapping:
        """Map all responsibilities for a single job."""
        mappings = []
        for resp in job.responsibilities:
            candidates = self._find_candidate_competencies(resp.normalized_text, library)
            mappings.append(ResponsibilityMapping(
                responsibility_id=resp.responsibility_id,
                candidates=candidates
            ))

        return JobMapping(
            job_id=job.job_id,
            responsibility_mappings=mappings
        )

    def _find_candidate_competencies(
        self,
        responsibility_text: str,
        library: CompetencyLibrary,
        top_k: int = 5
    ) -> List[CompetencyCandidate]:
        """Find top candidate competencies for a responsibility."""
        candidates = []

        for comp in library.competencies:
            # Compute similarity scores
            semantic_score = compute_similarity(responsibility_text, comp.definition)
            lexical_score = self._compute_lexical_overlap(responsibility_text, comp.name)

            # Weighted relevance score
            relevance_score = 0.4 * semantic_score + 0.3 * lexical_score + 0.3 * 0.5  # Placeholder LLM score

            if relevance_score >= 0.6:  # Threshold from config
                candidates.append(CompetencyCandidate(
                    competency_id=comp.competency_id,
                    competency_name=comp.name,
                    relevance_score=relevance_score,
                    mapping_rationale=f"Semantic similarity: {semantic_score:.2f}, Lexical overlap: {lexical_score:.2f}",
                    evidence_refs=[comp.competency_id],
                    lexical_match_score=lexical_score,
                    semantic_similarity_score=semantic_score,
                    llm_relevance_score=0.5  # Placeholder
                ))

        # Sort by relevance and take top k
        candidates.sort(key=lambda c: c.relevance_score, reverse=True)
        return candidates[:top_k]

    def _compute_lexical_overlap(self, text1: str, text2: str) -> float:
        """Compute simple lexical overlap score."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        overlap = len(words1.intersection(words2))
        return overlap / max(len(words1), len(words2))

    def get_system_prompt(self) -> str:
        """Return system prompt for competency mapping."""
        return """You are a Competency Mapping Specialist with expertise in IO Psychology and job analysis.

Your task is to map job responsibilities to relevant technical competencies.

Mapping process:
1. Analyze the responsibility statement
2. Identify key skills, knowledge, and abilities required
3. Search competency library for relevant matches
4. Score each candidate based on:
   - Semantic similarity (meaning alignment)
   - Lexical overlap (keyword matching)
   - Contextual relevance (LLM assessment)
5. Provide rationale for each mapping

Quality standards:
- Each responsibility should have 1-5 candidate competencies
- Relevance scores must be >= 0.6
- Provide clear mapping rationale
- Flag unmapped responsibilities

Output structured JSON conforming to the CompetencyMappingOutput schema."""
