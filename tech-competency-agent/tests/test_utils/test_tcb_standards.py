from src.schemas.tcb_builder import BuilderCompetency, JobFamilyCompetencySet
from src.utils.tcb_standards import TCBStandardsValidator


def _valid_competency(comp_id: str) -> BuilderCompetency:
    return BuilderCompetency(
        competency_id=comp_id,
        title="Industrial Process Optimization",
        definition="Optimize process parameters using statistical control methods to improve throughput, reduce defects, and stabilize operating performance across production assets.",
        technical_efs_covered=["ef1", "ef2"],
        level_indicators={
            "L1": ["Uses SPC charts in assigned area.", "Logs process data daily.", "Escalates out-of-control signals."],
            "L2": ["Adjusts setpoints using trend analysis.", "Correlates deviations to root causes.", "Documents corrective actions."],
            "L3": ["Leads multi-line optimization studies.", "Designs experiments for yield gains.", "Mentors peers on control strategy."],
            "L4": ["Defines enterprise optimization standards.", "Approves plant-wide control architecture.", "Sponsors advanced analytics roadmap."],
        },
    )


def test_validator_accepts_valid_package():
    package = JobFamilyCompetencySet(
        job_family="Manufacturing Engineering",
        technical_efs_total=["ef1", "ef2"],
        competencies=[_valid_competency("c1")],
    )

    report = TCBStandardsValidator().validate([package])

    assert report.report_is_valid is True
    assert report.valid_competencies == 1
    assert report.results[0].package_coverage_rate == 1.0


def test_validator_flags_definition_and_indicator_issues():
    broken = _valid_competency("c2")
    broken.title = "Operations"
    broken.definition = "This is too short. It has two sentences."
    broken.level_indicators["L2"] = ["Only one indicator"]

    package = JobFamilyCompetencySet(
        job_family="Plant Operations",
        technical_efs_total=["ef1", "ef2", "ef3"],
        competencies=[broken],
    )

    report = TCBStandardsValidator().validate([package])
    issues = report.results[0].competency_results[0].issues
    codes = {issue.code for issue in issues}

    assert report.report_is_valid is False
    assert "TITLE_WORD_COUNT" in codes
    assert "DEFINITION_WORD_COUNT" in codes
    assert "DEFINITION_SENTENCE_COUNT" in codes
    assert "LEVEL_INDICATOR_COUNT" in codes
