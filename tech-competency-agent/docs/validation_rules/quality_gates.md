# Quality Gate Validation Rules

This document defines validation rules applied at each quality gate.

## Gate 1: Post-Job Extraction

### Rule: No Jobs Extracted
- **Severity**: CRITICAL
- **Condition**: Job count = 0
- **Action**: Halt workflow
- **Remediation**: Check input file format and content

### Rule: Missing Summary Rate
- **Severity**: WARNING
- **Threshold**: >10% of jobs missing summaries
- **Action**: Flag for review
- **Remediation**: Review source data quality

### Rule: Insufficient Responsibilities
- **Severity**: WARNING
- **Threshold**: Job has <5 responsibilities
- **Action**: Flag specific jobs
- **Remediation**: Verify completeness of source data

## Gate 2: Post-Competency Mapping

### Rule: Unmapped Responsibilities
- **Severity**: ERROR
- **Threshold**: >5% responsibilities unmapped
- **Action**: Halt workflow
- **Remediation**: Review competency library coverage, adjust relevance threshold

### Rule: Low Candidate Count
- **Severity**: WARNING
- **Threshold**: Average <2 candidates per responsibility
- **Action**: Flag for review
- **Remediation**: Expand competency library or lower relevance threshold

## Gate 5: Post-Overlap Remediation

### Rule: Material Overlaps Unresolved
- **Severity**: ERROR
- **Condition**: Any material overlaps remain (score ≥0.82)
- **Action**: Halt workflow or trigger reaudit
- **Remediation**: Manual review of flagged competencies

### Rule: Distinctness Conflicts
- **Severity**: WARNING
- **Threshold**: >2 near-duplicates within job
- **Action**: Flag for review
- **Remediation**: Merge or differentiate competencies

## Gate 7: Post-Ranking

### Rule: Coverage Below Threshold
- **Severity**: WARNING
- **Threshold**: Average coverage <80% of responsibilities
- **Action**: Flag low-coverage jobs
- **Remediation**: Review competency selection criteria, consider additional competencies

### Rule: Top N Out of Range
- **Severity**: WARNING
- **Condition**: Job has <6 or >10 ranked competencies
- **Action**: Flag for review
- **Remediation**: Adjust ranking criteria or top N setting

### Rule: Critical Competency Gap
- **Severity**: ERROR
- **Condition**: High-priority responsibility uncovered
- **Action**: Flag for manual review
- **Remediation**: Add missing competency or adjust priority

## General Validation Patterns

### Data Completeness
- All required fields populated
- No null/empty values in critical fields
- Traceability IDs valid and resolvable

### Data Quality
- Text length within specified ranges
- List counts within min/max bounds
- Scores within [0.0, 1.0] range
- Pattern matches (e.g., competency naming)

### Referential Integrity
- All responsibility_ids traceable to source
- All competency_ids unique and valid
- Evidence references resolvable

## Severity Levels

- **INFO**: Informational, no action required
- **WARNING**: Review recommended, workflow continues
- **ERROR**: Significant issue, may halt workflow
- **CRITICAL**: Workflow halted, manual intervention required

## Customization

Thresholds can be adjusted in `config/thresholds.yaml`:

```yaml
overlap:
  material_threshold: 0.82
  minor_threshold: 0.72

ranking:
  min_responsibility_coverage: 0.80
  top_n_competencies: 8
```
