# Step 3: Responsibility-Competency Mapping Prompt Template

## User Prompt Format

```
Map the responsibilities from Step 1 to the competencies selected in Step 2.

For each responsibility, identify:
1. Which competencies enable it
2. The relevance score (0.0-1.0)
3. Whether it's a PRIMARY, SECONDARY, or SUPPORTING contribution
4. Clear rationale for the mapping

Ensure at least 80% of responsibilities are mapped.
```

## GPT Response Template

```yaml
# STEP 3: RESPONSIBILITY-COMPETENCY MAPPING
# ============================================================================

responsibility_mapping:
  # Summary Statistics
  mapping_summary:
    total_responsibilities: [N]
    mapped_responsibilities: [N]
    unmapped_responsibilities: [N]
    coverage_rate: [X.XX]  # Must be >= 0.80
    coverage_status: "[PASS | FAIL]"

  # Detailed Mapping Matrix
  mapping_matrix:

    # Responsibility 1
    - responsibility_id: "R1"
      responsibility_text: "[Normalized responsibility from Step 1]"
      importance: "[HIGH | MEDIUM | LOW]"
      category: "[Category from Step 1]"

      mapped_competencies:
        - competency_id: "[CORE_001 or SPEC_001]"
          competency_name: "[Domain: Specific Skill]"
          relevance_score: [0.XX]
          contribution: "[PRIMARY | SECONDARY | SUPPORTING]"
          scoring_breakdown:
            semantic_alignment: [0.XX]  # How well meanings match (40% weight)
            keyword_overlap: [0.XX]     # Common technical terms (30% weight)
            contextual_fit: [0.XX]      # Work context alignment (30% weight)
          rationale: |
            [Explain why this competency maps to this responsibility.
            Reference specific elements from both the responsibility
            and the competency definition that demonstrate alignment.]

        - competency_id: "[CORE_002]"
          competency_name: "[Domain: Specific Skill]"
          relevance_score: [0.XX]
          contribution: "[SECONDARY]"
          scoring_breakdown:
            semantic_alignment: [0.XX]
            keyword_overlap: [0.XX]
            contextual_fit: [0.XX]
          rationale: "[Mapping rationale]"

      mapping_status: "COVERED"

    # Responsibility 2
    - responsibility_id: "R2"
      responsibility_text: "[Normalized responsibility]"
      importance: "[Importance]"
      category: "[Category]"

      mapped_competencies:
        - competency_id: "[ID]"
          competency_name: "[Name]"
          relevance_score: [0.XX]
          contribution: "[Contribution]"
          scoring_breakdown:
            semantic_alignment: [0.XX]
            keyword_overlap: [0.XX]
            contextual_fit: [0.XX]
          rationale: "[Rationale]"

      mapping_status: "COVERED"

    # Continue for all responsibilities...

    # Example of Unmapped Responsibility
    - responsibility_id: "R[N]"
      responsibility_text: "[Responsibility with no good match]"
      importance: "[Importance]"
      category: "[Category]"

      mapped_competencies: []  # Empty - no matches above threshold

      mapping_status: "UNMAPPED"
      gap_analysis: |
        [Explain why this responsibility couldn't be mapped.
        Suggest whether a new competency should be created or
        if this is a cross-functional responsibility that may
        relate to leadership competencies.]

  # Competency Coverage Summary
  # (Shows which responsibilities each competency enables)
  competency_coverage_summary:
    - competency_id: "CORE_001"
      competency_name: "[Domain: Specific Skill]"
      responsibilities_enabled:
        - responsibility_id: "R1"
          contribution: "PRIMARY"
        - responsibility_id: "R3"
          contribution: "SECONDARY"
        - responsibility_id: "R7"
          contribution: "SUPPORTING"
      total_responsibilities_mapped: 3
      coverage_breadth: [0.XX]  # % of total responsibilities
      primary_contribution_count: 1
      weighted_importance: [X.XX]  # Based on responsibility importance levels

    - competency_id: "CORE_002"
      competency_name: "[Name]"
      responsibilities_enabled:
        - responsibility_id: "R2"
          contribution: "PRIMARY"
        - responsibility_id: "R5"
          contribution: "PRIMARY"
      total_responsibilities_mapped: 2
      coverage_breadth: [0.XX]
      primary_contribution_count: 2
      weighted_importance: [X.XX]

    # Continue for all competencies...

  # Gap Analysis (if coverage < 80%)
  gap_analysis:
    unmapped_responsibilities:
      - responsibility_id: "R[N]"
        responsibility_text: "[Text]"
        gap_type: "[NO_MATCH | THRESHOLD_NOT_MET | CROSS_FUNCTIONAL]"
        recommended_action: "[ADD_COMPETENCY | LOWER_THRESHOLD | DEFER_TO_LEADERSHIP]"
        suggested_competency: "[If applicable - suggest what competency might fill gap]"

    coverage_improvement_plan:
      current_coverage: [X.XX]
      target_coverage: 0.80
      actions_needed:
        - action: "[Action description]"
          impact: "[Expected coverage improvement]"

# Quality Check
quality_check:
  coverage_threshold_met: [true | false]
  all_high_importance_mapped: [true | false]
  competency_utilization:
    competencies_with_mappings: [N]
    competencies_without_mappings: [N]
    unused_competencies: ["ID1", "ID2"]

# Ready to proceed to Step 4: Competency Customization
```

## Relevance Scoring Guide

### Semantic Alignment (40% weight)
Assess how closely the competency's core meaning matches the responsibility:

| Score | Description |
|-------|-------------|
| 0.90-1.00 | Near-perfect semantic match; competency directly describes the activity |
| 0.75-0.89 | Strong alignment; competency clearly enables the responsibility |
| 0.60-0.74 | Moderate alignment; competency is relevant but not direct |
| 0.40-0.59 | Weak alignment; only tangentially related |
| 0.00-0.39 | Poor alignment; minimal semantic connection |

### Keyword Overlap (30% weight)
Check for common technical terms, tools, methods, or domain vocabulary:

| Score | Description |
|-------|-------------|
| 0.90-1.00 | Multiple specific technical terms match exactly |
| 0.75-0.89 | Several keywords or tool names overlap |
| 0.60-0.74 | Some common vocabulary present |
| 0.40-0.59 | Few related terms |
| 0.00-0.39 | No meaningful keyword overlap |

### Contextual Fit (30% weight)
Evaluate whether the competency applies in the work context described:

| Score | Description |
|-------|-------------|
| 0.90-1.00 | Perfect contextual match; same work environment/industry |
| 0.75-0.89 | Strong fit; competency clearly applicable in this context |
| 0.60-0.74 | Good fit; competency transferable to this context |
| 0.40-0.59 | Partial fit; some adaptation needed |
| 0.00-0.39 | Poor fit; different work context |

### Contribution Classification

| Contribution | Relevance Score | Description |
|--------------|-----------------|-------------|
| PRIMARY | ≥ 0.80 | Competency is essential for this responsibility |
| SECONDARY | 0.70-0.79 | Competency provides significant support |
| SUPPORTING | 0.60-0.69 | Competency is tangentially helpful |
| NO MAPPING | < 0.60 | Below threshold; do not map |

## Common Mapping Patterns

### Technical Execution Responsibilities
Often map to:
- Core technical competencies (programming, systems, data)
- Tool-specific specialized competencies
- Quality assurance competencies

### Analysis/Design Responsibilities
Often map to:
- Architecture/design competencies
- Problem-solving competencies
- Requirements engineering competencies

### Collaboration Responsibilities
Watch for overlap with leadership competencies:
- Keep focus on technical collaboration
- "Works with developers to..." → Technical, not leadership
- "Influences stakeholders to..." → May be leadership overlap

### Quality Assurance Responsibilities
Often map to:
- Testing competencies
- Documentation competencies
- Security competencies
