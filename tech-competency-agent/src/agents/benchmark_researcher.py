"""Step 6: Benchmark Researcher Agent - Validates against industry standards."""

from pathlib import Path
from typing import List, Dict
import anthropic

from src.agents.base import BaseAgent
from src.schemas.run_state import RunState
from src.schemas.competency import NormalizedCompetenciesOutput, TechnicalCompetency
from src.utils.knowledge_base import KnowledgeBase


class BenchmarkResearchAgent(BaseAgent):
    """Validates and refines competencies against industry benchmarks."""

    def __init__(self, agent_id: str, step_name: str, kb_path: str = "data/knowledge_base"):
        super().__init__(agent_id, step_name)
        self.client = anthropic.Anthropic()
        self.kb = KnowledgeBase(Path(kb_path))

    def execute(self, state: RunState) -> RunState:
        """
        Benchmark competencies against industry standards.

        Args:
            state: Current workflow state

        Returns:
            Updated state with benchmarked competencies
        """
        state.current_step = self.agent_id

        # Check if knowledge base has documents
        kb_stats = self.kb.get_statistics()
        if kb_stats['total_documents'] > 0:
            self.add_flag(
                state,
                severity="INFO",
                flag_type="KB_AVAILABLE",
                message=f"Using knowledge base with {kb_stats['total_documents']} documents",
                metadata=kb_stats
            )
        else:
            self.add_flag(
                state,
                severity="WARNING",
                flag_type="KB_EMPTY",
                message="Knowledge base is empty. Using default benchmarking sources only.",
                metadata={}
            )

        # Load clean competencies from Step 5
        clean_comps = self._load_clean_competencies(state)

        # Benchmark each job's competencies
        benchmarked_jobs = []
        for job_comps in clean_comps.jobs:
            benchmarked_job = self._benchmark_job(job_comps, state)
            benchmarked_jobs.append(benchmarked_job)

        # Create benchmarked output (v4)
        output = NormalizedCompetenciesOutput(
            jobs=benchmarked_jobs,
            processing_version="v4",
            total_competencies=sum(jc.competency_count() for jc in benchmarked_jobs)
        )

        # Save artifact
        output_path = Path(f"data/output/{state.run_id}_s6_benchmarked_v4.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(output.json(indent=2))

        state.artifacts.benchmarked_v4 = output_path

        # Add quality flags for benchmarking results
        self._add_benchmarking_flags(state, benchmarked_jobs)

        return state

    def _load_clean_competencies(self, state: RunState) -> NormalizedCompetenciesOutput:
        """Load clean competencies from Step 5."""
        if not state.artifacts.clean_v3:
            raise ValueError("Clean competencies not available - Step 5 must run first")

        with open(state.artifacts.clean_v3, 'r') as f:
            return NormalizedCompetenciesOutput.parse_raw(f.read())

    def _benchmark_job(
        self,
        job_comps,
        state: RunState
    ):
        """Benchmark all competencies for a single job."""
        from src.schemas.competency import JobCompetencies, TechnicalCompetency, BenchmarkingRecord
        import copy

        benchmarked_comps = []

        for comp in job_comps.technical_competencies:
            # Create a copy to update
            benchmarked_comp = copy.deepcopy(comp)

            # Search knowledge base for relevant benchmarks
            benchmark_results = self.benchmark_competency(comp)

            # Update benchmarking record
            benchmarked_against = []
            evidence_refs = []

            for evidence in benchmark_results["evidence"]:
                benchmarked_against.append(evidence["source"])
                evidence_refs.append(evidence["doc_id"])

            # Calculate alignment score based on sources found
            sources_found = benchmark_results["sources_found"]
            if sources_found >= 3:
                alignment_score = 0.9
            elif sources_found == 2:
                alignment_score = 0.8
            elif sources_found == 1:
                alignment_score = 0.7
            else:
                alignment_score = 0.5  # No benchmarks found

            # Update benchmarking record
            benchmarked_comp.benchmarking = BenchmarkingRecord(
                benchmarked_against=benchmarked_against[:3],  # Top 3 sources
                changes_made=None if not benchmarked_against else "Validated against industry standards",
                evidence_refs=evidence_refs[:3],  # Top 3 evidence
                benchmark_alignment_score=alignment_score
            )

            benchmarked_comps.append(benchmarked_comp)

        return JobCompetencies(
            job_id=job_comps.job_id,
            technical_competencies=benchmarked_comps
        )

    def _add_benchmarking_flags(self, state: RunState, benchmarked_jobs: List):
        """Add quality flags for benchmarking results."""
        for job_comps in benchmarked_jobs:
            unbenchmarked_count = 0

            for comp in job_comps.technical_competencies:
                # Check if competency was benchmarked
                if not comp.benchmarking.benchmarked_against:
                    unbenchmarked_count += 1

                # Check alignment score
                if comp.benchmarking.benchmark_alignment_score and comp.benchmarking.benchmark_alignment_score < 0.7:
                    self.add_flag(
                        state,
                        severity="WARNING",
                        flag_type="LOW_ALIGNMENT",
                        message=f"Competency {comp.name} has low alignment score ({comp.benchmarking.benchmark_alignment_score:.2f})",
                        job_id=job_comps.job_id,
                        metadata={"competency_id": comp.competency_id, "alignment_score": comp.benchmarking.benchmark_alignment_score}
                    )

            # Flag if job has many unbenchmarked competencies
            if unbenchmarked_count > 0:
                self.add_flag(
                    state,
                    severity="INFO",
                    flag_type="UNBENCHMARKED_COMPETENCIES",
                    message=f"Job {job_comps.job_id} has {unbenchmarked_count} competencies without benchmarks",
                    job_id=job_comps.job_id,
                    metadata={"unbenchmarked_count": unbenchmarked_count}
                )

    def benchmark_competency(self, competency: TechnicalCompetency) -> Dict:
        """
        Benchmark a single competency against knowledge base.

        Args:
            competency: Competency to benchmark

        Returns:
            Dictionary with benchmark results
        """
        # Search knowledge base for relevant content
        search_query = f"{competency.name} {competency.definition}"

        results = self.kb.search_documents(
            query=search_query,
            category="framework",  # Focus on framework documents
            top_k=3
        )

        benchmark_results = {
            "sources_found": len(results),
            "evidence": [],
            "alignment_suggestions": []
        }

        for result in results:
            benchmark_results["evidence"].append({
                "source": result['doc_title'],
                "doc_id": result['doc_id'],
                "content": result['content'][:500],  # First 500 chars
                "relevance": result['relevance_score']
            })

        return benchmark_results

    def get_system_prompt(self) -> str:
        """Return system prompt for benchmarking."""
        return """You are a Competency Benchmarking Specialist with access to industry frameworks.

Your task is to validate and refine competencies against established standards.

Benchmark sources (priority order):
1. O*NET (Occupational Information Network)
2. SFIA (Skills Framework for the Information Age)
3. NICE (National Initiative for Cybersecurity Education)
4. Industry-specific frameworks

Benchmarking process:
1. Search relevant frameworks for each competency
2. Compare definitions, indicators, and proficiency levels
3. Identify gaps or misalignments
4. Refine competency content to align with standards
5. Document evidence and changes made
6. Assign alignment score

Quality standards:
- All competencies benchmarked against ≥1 source
- Clear documentation of changes
- Evidence references included
- Alignment scores >= 0.7

Output structured JSON conforming to NormalizedCompetenciesOutput schema (v4)."""
