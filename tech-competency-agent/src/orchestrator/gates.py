"""Quality gates and validation logic."""

from pydantic import BaseModel

from src.schemas.audit import OverlapAuditOutput
from src.schemas.job import JobExtractionOutput
from src.schemas.mapping import CompetencyMappingOutput
from src.schemas.ranking import RankingOutput
from src.schemas.run_state import RunState, ThresholdConfig


class ValidationResult(BaseModel):
    """Result of a validation check."""
    rule_name: str
    passed: bool
    severity: str  # INFO, WARNING, ERROR, CRITICAL
    message: str
    metadata: dict = {}


class QualityGate:
    """Quality gate validator."""

    def __init__(self, gate_id: str, thresholds: ThresholdConfig):
        self.gate_id = gate_id
        self.thresholds = thresholds

    def validate_no_jobs_extracted(self, state: RunState) -> ValidationResult:
        """Check if any jobs were extracted."""
        if not state.artifacts.jobs_extracted:
            return ValidationResult(
                rule_name="no_jobs_extracted",
                passed=False,
                severity="CRITICAL",
                message="No jobs were extracted from input file",
                metadata={}
            )

        # Load and check job count
        with open(state.artifacts.jobs_extracted, 'r') as f:
            extraction = JobExtractionOutput.parse_raw(f.read())

        if extraction.total_jobs_extracted == 0:
            return ValidationResult(
                rule_name="no_jobs_extracted",
                passed=False,
                severity="CRITICAL",
                message="Job extraction completed but found 0 jobs",
                metadata={}
            )

        return ValidationResult(
            rule_name="no_jobs_extracted",
            passed=True,
            severity="INFO",
            message=f"Successfully extracted {extraction.total_jobs_extracted} jobs",
            metadata={"job_count": extraction.total_jobs_extracted}
        )

    def validate_missing_summary_rate(self, state: RunState, max_rate: float = 0.10) -> ValidationResult:
        """Check rate of jobs missing summaries."""
        if not state.artifacts.jobs_extracted:
            return ValidationResult(
                rule_name="missing_summary_rate",
                passed=False,
                severity="ERROR",
                message="Cannot validate: jobs not extracted",
                metadata={}
            )

        with open(state.artifacts.jobs_extracted, 'r') as f:
            extraction = JobExtractionOutput.parse_raw(f.read())

        missing_summary_count = sum(
            1 for w in extraction.extraction_warnings
            if w.warning_type == "MISSING_SUMMARY"
        )

        rate = missing_summary_count / extraction.total_jobs_extracted if extraction.total_jobs_extracted > 0 else 0

        if rate > max_rate:
            return ValidationResult(
                rule_name="missing_summary_rate",
                passed=False,
                severity="WARNING",
                message=f"Missing summary rate ({rate:.1%}) exceeds threshold ({max_rate:.1%})",
                metadata={"rate": rate, "threshold": max_rate, "count": missing_summary_count}
            )

        return ValidationResult(
            rule_name="missing_summary_rate",
            passed=True,
            severity="INFO",
            message=f"Missing summary rate ({rate:.1%}) within threshold",
            metadata={"rate": rate, "count": missing_summary_count}
        )

    def validate_unmapped_responsibilities(self, state: RunState, max_rate: float = 0.05) -> ValidationResult:
        """Check rate of unmapped responsibilities."""
        if not state.artifacts.competency_map_v1:
            return ValidationResult(
                rule_name="unmapped_responsibilities",
                passed=False,
                severity="ERROR",
                message="Cannot validate: competency mapping not completed",
                metadata={}
            )

        with open(state.artifacts.competency_map_v1, 'r') as f:
            mapping = CompetencyMappingOutput.parse_raw(f.read())

        if mapping.unmapped_responsibility_rate > max_rate:
            return ValidationResult(
                rule_name="unmapped_responsibilities",
                passed=False,
                severity="ERROR",
                message=f"Unmapped responsibility rate ({mapping.unmapped_responsibility_rate:.1%}) exceeds threshold ({max_rate:.1%})",
                metadata={"rate": mapping.unmapped_responsibility_rate, "threshold": max_rate}
            )

        return ValidationResult(
            rule_name="unmapped_responsibilities",
            passed=True,
            severity="INFO",
            message=f"Unmapped responsibility rate ({mapping.unmapped_responsibility_rate:.1%}) within threshold",
            metadata={"rate": mapping.unmapped_responsibility_rate}
        )

    def validate_overlap_resolved(self, state: RunState) -> ValidationResult:
        """Check if overlap issues are resolved."""
        if not state.artifacts.overlap_audit_v1:
            return ValidationResult(
                rule_name="overlap_resolved",
                passed=False,
                severity="ERROR",
                message="Cannot validate: overlap audit not completed",
                metadata={}
            )

        with open(state.artifacts.overlap_audit_v1, 'r') as f:
            audit = OverlapAuditOutput.parse_raw(f.read())

        if audit.total_material_overlaps > 0:
            return ValidationResult(
                rule_name="overlap_resolved",
                passed=False,
                severity="ERROR",
                message=f"Material overlaps still exist: {audit.total_material_overlaps}",
                metadata={"material_overlaps": audit.total_material_overlaps}
            )

        return ValidationResult(
            rule_name="overlap_resolved",
            passed=True,
            severity="INFO",
            message="All overlap issues resolved",
            metadata={}
        )

    def validate_coverage_threshold(self, state: RunState) -> ValidationResult:
        """Check if responsibility coverage meets threshold."""
        if not state.artifacts.ranked_top8_v5:
            return ValidationResult(
                rule_name="coverage_threshold",
                passed=False,
                severity="ERROR",
                message="Cannot validate: ranking not completed",
                metadata={}
            )

        with open(state.artifacts.ranked_top8_v5, 'r') as f:
            ranking = RankingOutput.parse_raw(f.read())

        if ranking.average_coverage_rate < self.thresholds.min_responsibility_coverage:
            return ValidationResult(
                rule_name="coverage_threshold",
                passed=False,
                severity="WARNING",
                message=f"Average coverage ({ranking.average_coverage_rate:.1%}) below threshold ({self.thresholds.min_responsibility_coverage:.1%})",
                metadata={
                    "average_coverage": ranking.average_coverage_rate,
                    "threshold": self.thresholds.min_responsibility_coverage,
                    "low_coverage_jobs": ranking.low_coverage_jobs
                }
            )

        return ValidationResult(
            rule_name="coverage_threshold",
            passed=True,
            severity="INFO",
            message=f"Average coverage ({ranking.average_coverage_rate:.1%}) meets threshold",
            metadata={"average_coverage": ranking.average_coverage_rate}
        )

    def validate_top_n_count(self, state: RunState) -> ValidationResult:
        """Check if top N competency count is within range."""
        if not state.artifacts.ranked_top8_v5:
            return ValidationResult(
                rule_name="top_n_count",
                passed=False,
                severity="ERROR",
                message="Cannot validate: ranking not completed",
                metadata={}
            )

        with open(state.artifacts.ranked_top8_v5, 'r') as f:
            ranking = RankingOutput.parse_raw(f.read())

        # v3.1: max 6 per job description
        jobs_out_of_range = []
        for job_ranking in ranking.jobs:
            comp_count = len(job_ranking.ranked_competencies)
            if comp_count > 6 or comp_count < 1:
                jobs_out_of_range.append({
                    "job_id": job_ranking.job_id,
                    "count": comp_count
                })

        if jobs_out_of_range:
            return ValidationResult(
                rule_name="top_n_count",
                passed=False,
                severity="ERROR",
                message=f"{len(jobs_out_of_range)} jobs violate v3.1 max-6 cap",
                metadata={"jobs_out_of_range": jobs_out_of_range}
            )

        return ValidationResult(
            rule_name="top_n_count",
            passed=True,
            severity="INFO",
            message="All jobs satisfy v3.1 top-6 cap",
            metadata={}
        )

    def validate_v31_competency_format(self, state: RunState) -> ValidationResult:
        """v3.1 structural format gate: title 3-6 words, definition 15-25
        single-sentence words, exactly 4 levels with 3 indicators each.

        Validators on TechnicalCompetency raise on construction; this gate
        re-asserts the contract from a serialized artifact and surfaces a
        clean RunFlag rather than a stack trace.
        """
        from src.schemas.competency import TechnicalCompetency

        ref = state.artifacts.normalized_competencies_v3 or state.artifacts.normalized_competencies_v2
        if not ref:
            return ValidationResult(
                rule_name="v31_competency_format",
                passed=False,
                severity="ERROR",
                message="Cannot validate v3.1 format: normalized competencies missing",
                metadata={},
            )
        import json
        try:
            with open(ref, "r") as f:
                payload = json.load(f)
            count = 0
            for job in payload.get("jobs", []):
                for c in job.get("technical_competencies", []):
                    TechnicalCompetency(**c)
                    count += 1
        except Exception as exc:
            return ValidationResult(
                rule_name="v31_competency_format",
                passed=False,
                severity="ERROR",
                message=f"v3.1 format violation: {exc}",
                metadata={},
            )
        return ValidationResult(
            rule_name="v31_competency_format",
            passed=True,
            severity="INFO",
            message=f"All {count} competencies satisfy v3.1 structural rules",
            metadata={"competency_count": count},
        )

    def validate_ctic_drift(self, state: RunState) -> ValidationResult:
        """Phase 6F: drift rate must be <= configured tolerance (default 0.05)."""
        if not state.artifacts.ctic_report:
            return ValidationResult(
                rule_name="ctic_drift",
                passed=False,
                severity="ERROR",
                message="Cannot validate CTIC: report missing",
                metadata={},
            )
        import json
        with open(state.artifacts.ctic_report, "r") as f:
            report = json.load(f)
        rate = float(report.get("drift_rate", 0.0))
        max_rate = 0.05
        if rate > max_rate:
            return ValidationResult(
                rule_name="ctic_drift",
                passed=False,
                severity="ERROR",
                message=f"CTIC drift rate {rate:.1%} exceeds tolerance {max_rate:.1%}",
                metadata={"drift_rate": rate, "max_rate": max_rate},
            )
        return ValidationResult(
            rule_name="ctic_drift",
            passed=True,
            severity="INFO",
            message=f"CTIC drift rate {rate:.1%} within tolerance",
            metadata={"drift_rate": rate},
        )
