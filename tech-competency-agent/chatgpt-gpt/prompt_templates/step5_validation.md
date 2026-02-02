# Step 5: Quality Validation Prompt Template

## User Prompt Format

```
Validate the customized competencies against quality standards:

1. Check for leadership competency overlap
2. Verify responsibility coverage (must be >= 80%)
3. Confirm competency count is 6-10
4. Validate definition and indicator formats

Flag any issues and provide remediation recommendations.
```

## GPT Response Template

```yaml
# STEP 5: QUALITY VALIDATION
# ============================================================================

validation_timestamp: "[YYYY-MM-DD HH:MM:SS]"
job_context:
  job_title: "[Title]"
  job_level: "[Level]"
  total_competencies: [N]

# ---------------------------------------------------------------------------
# 5.1 LEADERSHIP OVERLAP CHECK
# ---------------------------------------------------------------------------
leadership_overlap_check:
  description: |
    Comparing technical competencies against common leadership competency
    domains to ensure they remain distinctly technical in nature.

  leadership_competencies_checked:
    - "Communication: Stakeholder Engagement"
    - "Influence: Persuasion & Negotiation"
    - "Team Leadership: People Management"
    - "Strategic Thinking: Vision & Planning"
    - "Change Management: Organizational Change"
    - "Decision Making: Judgment & Accountability"
    - "Collaboration: Cross-functional Partnership"

  results:
    - competency_id: "CORE_001"
      competency_name: "[Name]"
      overlap_status: "NONE"
      similarity_score: 0.35
      assessment: |
        No material overlap detected. Competency focuses on technical
        execution without encroaching on leadership domains.

    - competency_id: "CORE_002"
      competency_name: "[Name]"
      overlap_status: "NONE"
      similarity_score: 0.42
      assessment: "[Assessment]"

    - competency_id: "SPEC_001"
      competency_name: "[Name]"
      overlap_status: "MINOR"
      similarity_score: 0.76
      overlap_domain: "Collaboration: Cross-functional Partnership"
      assessment: |
        Minor overlap detected with collaboration competency. The
        technical competency mentions "working with stakeholders"
        which could be perceived as leadership-adjacent.
      remediation_recommendation: |
        Revise definition to emphasize the TECHNICAL aspects of
        stakeholder interaction (e.g., "gathering technical requirements"
        rather than "building stakeholder relationships").
      suggested_revision: |
        Change: "Works with stakeholders to understand needs"
        To: "Gathers and analyzes technical requirements from stakeholders"

    - competency_id: "SPEC_002"
      competency_name: "[Name]"
      overlap_status: "MATERIAL"
      similarity_score: 0.85
      overlap_domain: "Team Leadership: People Management"
      assessment: |
        MATERIAL OVERLAP DETECTED. The competency "Technical Mentoring"
        significantly overlaps with leadership's mentoring domain.
      remediation_recommendation: |
        MUST remediate before proceeding. Options:
        1. REMOVE: Remove this competency entirely
        2. REVISE: Narrow focus to technical knowledge transfer only
        3. REPLACE: Substitute with different technical competency
      recommended_action: "REVISE"
      suggested_revision: |
        Original: "Mentors junior team members on technical and professional skills"
        Revised: "Provides technical guidance on coding standards, architecture
        patterns, and tool usage through code reviews and pair programming sessions"

  summary:
    total_checked: [N]
    no_overlap: [N]
    minor_overlap: [N]
    material_overlap: [N]
    overall_status: "[PASS | REVIEW_NEEDED | FAIL]"

# ---------------------------------------------------------------------------
# 5.2 COVERAGE VALIDATION
# ---------------------------------------------------------------------------
coverage_validation:
  description: |
    Verifying that the selected competencies adequately cover the
    job responsibilities identified in the job description.

  metrics:
    total_responsibilities: [N]
    responsibilities_with_primary_mapping: [N]
    responsibilities_with_any_mapping: [N]
    unmapped_responsibilities: [N]

    coverage_calculations:
      strict_coverage: "[X.XX]"  # Only PRIMARY contributions
      inclusive_coverage: "[X.XX]"  # PRIMARY + SECONDARY + SUPPORTING
      threshold: 0.80

  coverage_by_importance:
    high_importance:
      total: [N]
      covered: [N]
      coverage_rate: "[X.XX]"
    medium_importance:
      total: [N]
      covered: [N]
      coverage_rate: "[X.XX]"
    low_importance:
      total: [N]
      covered: [N]
      coverage_rate: "[X.XX]"

  unmapped_details:
    - responsibility_id: "R[N]"
      responsibility_text: "[Text]"
      importance: "[HIGH | MEDIUM | LOW]"
      category: "[Category]"
      gap_reason: "[Why no competency mapped]"
      remediation_options:
        - option: "Add competency from model"
          suggested_competency: "[ID and name if available]"
        - option: "Create custom competency"
          suggested_name: "[Domain: Skill]"
          suggested_definition_elements: ["Element 1", "Element 2"]
        - option: "Accept as leadership-related"
          justification: "[Why this is OK to leave unmapped]"

  status: "[PASS | FAIL]"
  notes: |
    [Additional observations about coverage patterns]

# ---------------------------------------------------------------------------
# 5.3 COUNT VALIDATION
# ---------------------------------------------------------------------------
count_validation:
  description: |
    Ensuring the number of competencies falls within the acceptable
    range of 6-10 for effective competency profiles.

  metrics:
    current_count: [N]
    minimum_required: 6
    maximum_allowed: 10

  composition:
    core_competencies: [N]
    specialized_competencies: [N]
    emerging_competencies: [N]

  status: "[PASS | FAIL - TOO FEW | FAIL - TOO MANY]"

  remediation_if_needed:
    if_too_few:
      - "Review unmapped responsibilities for additional competency needs"
      - "Consider splitting complex competencies into distinct skills"
      - "Add relevant specialized competencies from model"
    if_too_many:
      - "Apply stricter criticality threshold in Step 6"
      - "Combine closely related competencies"
      - "Remove lowest-coverage competencies"

# ---------------------------------------------------------------------------
# 5.4 FORMAT VALIDATION
# ---------------------------------------------------------------------------
format_validation:
  description: |
    Checking that all competencies meet the format standards for
    names, definitions, and behavioral indicators.

  name_validation:
    pattern: "Domain: Specific Skill"
    max_length: 80

    results:
      - competency_id: "CORE_001"
        name: "[Name]"
        matches_pattern: true
        character_count: [N]
        status: "PASS"

      - competency_id: "SPEC_001"
        name: "[Name]"
        matches_pattern: false
        issue: "Missing domain prefix"
        suggested_fix: "[Suggested name with proper format]"
        status: "FAIL"

  definition_validation:
    min_words: 50
    max_words: 150

    results:
      - competency_id: "CORE_001"
        word_count: [N]
        is_work_context_specific: true
        includes_tools_tech: true
        describes_observable_application: true
        status: "PASS"

      - competency_id: "SPEC_002"
        word_count: 42
        is_work_context_specific: true
        includes_tools_tech: false
        describes_observable_application: true
        status: "FAIL"
        issues:
          - "Word count below minimum (42 < 50)"
          - "Missing tools/technologies reference"
        suggested_additions: |
          Add: "utilizing [Tool1] and [Tool2] to..." to increase
          word count and include technology references.

  indicator_validation:
    min_count: 3
    max_count: 7
    required_format: "Verb + Object + Context"

    results:
      - competency_id: "CORE_001"
        indicator_count: [N]
        count_status: "PASS"
        format_check:
          - indicator: "[Indicator text]"
            has_verb: true
            has_object: true
            has_context: true
            status: "PASS"
          - indicator: "[Indicator text]"
            has_verb: true
            has_object: true
            has_context: false
            status: "NEEDS_CONTEXT"
            suggestion: "Add standard or outcome measure"

  applied_scope_validation:
    results:
      - competency_id: "CORE_001"
        tools_tech_count: [N]
        minimum_required: 2
        has_standards: true
        has_outputs: true
        status: "PASS"

      - competency_id: "SPEC_001"
        tools_tech_count: 1
        minimum_required: 2
        has_standards: false
        has_outputs: true
        status: "FAIL"
        issues:
          - "Only 1 tool/technology (minimum 2)"
          - "Missing standards/frameworks"

  summary:
    all_names_valid: [true | false]
    all_definitions_valid: [true | false]
    all_indicators_valid: [true | false]
    all_scopes_valid: [true | false]
    overall_format_status: "[PASS | FAIL]"

# ---------------------------------------------------------------------------
# OVERALL VALIDATION SUMMARY
# ---------------------------------------------------------------------------
overall_validation:
  status: "[PASS | NEEDS_REVISION | FAIL]"

  gate_results:
    - gate: "Leadership Overlap"
      status: "[PASS | REVIEW | FAIL]"
      blocking: [true | false]
    - gate: "Coverage"
      status: "[PASS | FAIL]"
      blocking: true
    - gate: "Count"
      status: "[PASS | FAIL]"
      blocking: true
    - gate: "Format"
      status: "[PASS | FAIL]"
      blocking: false

  required_remediations:
    - competency_id: "[ID]"
      issue: "[Issue description]"
      action_required: "[REVISE | REMOVE | ADD]"
      priority: "[HIGH | MEDIUM]"

  recommended_improvements:
    - competency_id: "[ID]"
      suggestion: "[Non-blocking improvement suggestion]"

# Action Required
next_steps:
  if_pass: "Proceed to Step 6: Criticality Ranking"
  if_needs_revision: |
    Address the following before proceeding:
    1. [Remediation item 1]
    2. [Remediation item 2]
    Then re-run validation.
  if_fail: |
    Critical failures must be resolved:
    1. [Critical issue 1]
    2. [Critical issue 2]
    Return to Step 4 for significant revisions.
```

## Leadership Overlap Reference

### Technical vs Leadership Distinction

| Technical Domain | Leadership Domain | Key Differentiator |
|-----------------|-------------------|-------------------|
| Technical Collaboration | Interpersonal Communication | Focus on technical information exchange |
| Technical Mentoring | People Development | Focus on technical skills, not career growth |
| Technical Decision Making | Strategic Decision Making | Focus on technical trade-offs, not business strategy |
| Requirements Gathering | Stakeholder Management | Focus on technical requirements, not relationships |
| Technical Presentations | Executive Communication | Focus on technical content, not persuasion |
| Code Reviews | Performance Management | Focus on code quality, not people evaluation |

### Overlap Similarity Thresholds

| Score Range | Classification | Action Required |
|-------------|---------------|-----------------|
| < 0.72 | NONE | Pass - no action needed |
| 0.72 - 0.82 | MINOR | Review - consider revision |
| > 0.82 | MATERIAL | Fail - must remediate |

### Common Overlap Triggers (words to watch)

| Watch Word | Technical Framing | Leadership Framing |
|------------|------------------|-------------------|
| "Influence" | "Influences technical decisions through data-driven analysis" | "Influences stakeholders to adopt changes" |
| "Lead" | "Leads technical design sessions" | "Leads team members" |
| "Mentor" | "Provides technical guidance on coding practices" | "Mentors career development" |
| "Collaborate" | "Collaborates on technical specifications" | "Builds collaborative relationships" |
| "Communicate" | "Communicates technical designs through documentation" | "Communicates vision and strategy" |
