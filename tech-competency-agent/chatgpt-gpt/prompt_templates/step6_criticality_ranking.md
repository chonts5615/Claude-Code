# Step 6: Criticality Ranking Prompt Template

## User Prompt Format

```
Rank the validated competencies by criticality using multi-factor analysis:

Factors to consider:
- Coverage: % of responsibilities enabled
- Impact/Risk: Consequence if competency is missing
- Frequency: How often the competency is applied
- Complexity: Technical/cognitive difficulty
- Differentiation: Distinguishes high performers
- Time to Proficiency: Development investment required

Select the top 6-10 most critical competencies while maintaining >= 80% coverage.
```

## GPT Response Template

```yaml
# STEP 6: CRITICALITY RANKING
# ============================================================================

ranking_context:
  job_title: "[Title]"
  job_level: "[Level]"
  total_competencies_to_rank: [N]
  target_selection: "6-10 competencies"
  minimum_coverage_required: 0.80

# ---------------------------------------------------------------------------
# SCORING METHODOLOGY
# ---------------------------------------------------------------------------
scoring_methodology:
  description: |
    Each competency is scored on six factors with defined weights.
    The weighted sum produces a criticality score (0-10 scale).

  factors:
    - name: "Coverage"
      weight: 0.25
      description: "Percentage of job responsibilities this competency enables"
      scoring_guide: |
        10: Enables >50% of responsibilities
        8: Enables 40-50% of responsibilities
        6: Enables 30-40% of responsibilities
        4: Enables 20-30% of responsibilities
        2: Enables <20% of responsibilities

    - name: "Impact/Risk"
      weight: 0.20
      description: "Business consequence if this competency is missing or weak"
      scoring_guide: |
        10: Business-critical; failure causes major impact
        8: High impact; significant quality/delivery issues
        6: Moderate impact; noticeable performance degradation
        4: Low impact; minor issues, workarounds exist
        2: Minimal impact; rarely affects outcomes

    - name: "Frequency"
      weight: 0.15
      description: "How often this competency is applied in daily work"
      scoring_guide: |
        10: Daily, multiple times per day
        8: Daily or almost daily
        6: Several times per week
        4: Weekly or bi-weekly
        2: Monthly or less frequently

    - name: "Complexity"
      weight: 0.15
      description: "Cognitive and technical difficulty level"
      scoring_guide: |
        10: Highly complex; requires deep expertise
        8: Complex; requires significant skill
        6: Moderate; requires solid foundation
        4: Straightforward; following established patterns
        2: Simple; routine application

    - name: "Differentiation"
      weight: 0.15
      description: "Degree to which this distinguishes high performers"
      scoring_guide: |
        10: Key differentiator; defines top performers
        8: Strong differentiator; clearly separates performers
        6: Moderate differentiator; noticeable difference
        4: Minor differentiator; subtle distinction
        2: Baseline; expected of all performers

    - name: "Time to Proficiency"
      weight: 0.10
      description: "Investment required to develop this competency"
      scoring_guide: |
        10: >2 years to develop proficiency
        8: 1-2 years to develop
        6: 6-12 months to develop
        4: 3-6 months to develop
        2: <3 months to develop

  formula: |
    Criticality Score = (0.25 × Coverage) + (0.20 × Impact) + (0.15 × Frequency) +
                        (0.15 × Complexity) + (0.15 × Differentiation) + (0.10 × Time)

# ---------------------------------------------------------------------------
# DETAILED SCORING
# ---------------------------------------------------------------------------
competency_scoring:

  # Competency 1
  - competency_id: "CORE_001"
    competency_name: "[Domain: Specific Skill]"

    factor_scores:
      coverage:
        score: [1-10]
        responsibilities_enabled: ["R1", "R3", "R5", "R7"]
        percentage: "[X%]"
        rationale: "[Why this coverage score]"

      impact_risk:
        score: [1-10]
        risk_scenarios:
          - "[What happens if this competency is weak]"
          - "[Business impact example]"
        rationale: "[Why this impact score]"

      frequency:
        score: [1-10]
        application_pattern: "[Daily/Weekly/Monthly]"
        rationale: "[Why this frequency score]"

      complexity:
        score: [1-10]
        complexity_factors:
          - "[Factor 1 adding to complexity]"
          - "[Factor 2]"
        rationale: "[Why this complexity score]"

      differentiation:
        score: [1-10]
        differentiation_evidence: "[How this separates performers]"
        rationale: "[Why this differentiation score]"

      time_to_proficiency:
        score: [1-10]
        estimated_time: "[X months/years]"
        development_path: "[Typical development approach]"
        rationale: "[Why this time score]"

    weighted_calculation:
      coverage_weighted: "[0.25 × score = X.XX]"
      impact_weighted: "[0.20 × score = X.XX]"
      frequency_weighted: "[0.15 × score = X.XX]"
      complexity_weighted: "[0.15 × score = X.XX]"
      differentiation_weighted: "[0.15 × score = X.XX]"
      time_weighted: "[0.10 × score = X.XX]"

    criticality_score: [X.XX]  # Sum of weighted scores

  # Competency 2
  - competency_id: "CORE_002"
    competency_name: "[Name]"
    factor_scores:
      coverage:
        score: [N]
        responsibilities_enabled: ["R2", "R4"]
        percentage: "[X%]"
        rationale: "[Rationale]"
      impact_risk:
        score: [N]
        risk_scenarios: ["Scenario"]
        rationale: "[Rationale]"
      frequency:
        score: [N]
        application_pattern: "[Pattern]"
        rationale: "[Rationale]"
      complexity:
        score: [N]
        complexity_factors: ["Factors"]
        rationale: "[Rationale]"
      differentiation:
        score: [N]
        differentiation_evidence: "[Evidence]"
        rationale: "[Rationale]"
      time_to_proficiency:
        score: [N]
        estimated_time: "[Time]"
        development_path: "[Path]"
        rationale: "[Rationale]"

    weighted_calculation:
      coverage_weighted: "[X.XX]"
      impact_weighted: "[X.XX]"
      frequency_weighted: "[X.XX]"
      complexity_weighted: "[X.XX]"
      differentiation_weighted: "[X.XX]"
      time_weighted: "[X.XX]"

    criticality_score: [X.XX]

  # Continue for all competencies...

# ---------------------------------------------------------------------------
# RANKED RESULTS
# ---------------------------------------------------------------------------
ranked_competencies:

  - rank: 1
    competency_id: "[ID]"
    competency_name: "[Name]"
    criticality_score: [X.XX]
    factor_highlights:
      highest_factor: "[Factor name]: [score]"
      second_highest: "[Factor name]: [score]"
    key_insight: "[Why this ranks highest]"

  - rank: 2
    competency_id: "[ID]"
    competency_name: "[Name]"
    criticality_score: [X.XX]
    factor_highlights:
      highest_factor: "[Factor]: [score]"
      second_highest: "[Factor]: [score]"
    key_insight: "[Insight]"

  - rank: 3
    competency_id: "[ID]"
    competency_name: "[Name]"
    criticality_score: [X.XX]
    factor_highlights:
      highest_factor: "[Factor]: [score]"
      second_highest: "[Factor]: [score]"
    key_insight: "[Insight]"

  # Continue for all ranked competencies...

# ---------------------------------------------------------------------------
# SELECTION DECISION
# ---------------------------------------------------------------------------
selection_decision:
  selection_threshold:
    method: "[TOP_N | SCORE_CUTOFF | COVERAGE_OPTIMIZED]"
    value: "[N competencies | score >= X.XX | optimize for 80%+ coverage]"

  # Iterative selection to maintain coverage
  selection_iterations:
    - iteration: 1
      action: "Select top 6 by criticality score"
      competencies_selected: ["ID1", "ID2", "ID3", "ID4", "ID5", "ID6"]
      coverage_achieved: "[X.XX%]"
      coverage_status: "[PASS | FAIL]"

    - iteration: 2  # Only if needed
      action: "Add next highest to improve coverage"
      competencies_selected: ["ID1", "ID2", "ID3", "ID4", "ID5", "ID6", "ID7"]
      coverage_achieved: "[X.XX%]"
      coverage_status: "[PASS | FAIL]"

  final_selection:
    count: [N]
    competency_ids: ["ID1", "ID2", "ID3", ...]
    total_criticality_score: [XX.XX]
    average_criticality_score: [X.XX]

# ---------------------------------------------------------------------------
# COVERAGE VERIFICATION
# ---------------------------------------------------------------------------
coverage_verification:
  responsibilities_covered_by_selection:
    - responsibility_id: "R1"
      covered_by: ["ID1", "ID3"]
      best_contribution: "PRIMARY"
    - responsibility_id: "R2"
      covered_by: ["ID2"]
      best_contribution: "PRIMARY"
    # Continue for all responsibilities...

  coverage_metrics:
    total_responsibilities: [N]
    responsibilities_covered: [N]
    responsibilities_uncovered: [N]
    final_coverage_rate: "[X.XX%]"
    coverage_status: "[PASS | FAIL]"

  uncovered_responsibilities:
    - responsibility_id: "R[N]"
      responsibility_text: "[Text]"
      importance: "[Importance]"
      impact_assessment: |
        [Assessment of leaving this uncovered - is it acceptable?]

# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------
ranking_summary:

  final_selection:
    - rank: 1
      competency_id: "[ID]"
      competency_name: "[Name]"
      criticality_score: [X.XX]
      included: true

    - rank: 2
      competency_id: "[ID]"
      competency_name: "[Name]"
      criticality_score: [X.XX]
      included: true

    # ... continue for all, marking included: true/false

  statistics:
    competencies_included: [N]
    competencies_excluded: [N]
    score_range: "[X.XX - Y.YY]"
    score_cutoff: "[X.XX]"

  insights:
    - "[Key insight about the ranking results]"
    - "[Pattern observed across high-ranking competencies]"
    - "[Note about excluded competencies]"

# Ready to proceed to Step 7: Output Generation
```

## Factor Scoring Quick Reference

### Coverage Scoring Matrix
| % Responsibilities | Score |
|-------------------|-------|
| >50% | 10 |
| 40-50% | 8 |
| 30-40% | 6 |
| 20-30% | 4 |
| <20% | 2 |

### Impact/Risk Scoring Matrix
| Impact Level | Score | Examples |
|-------------|-------|----------|
| Business-Critical | 10 | System security, data integrity, customer-facing reliability |
| High | 8 | Delivery timelines, quality standards, regulatory compliance |
| Moderate | 6 | Team efficiency, code maintainability |
| Low | 4 | Documentation quality, minor optimizations |
| Minimal | 2 | Style preferences, optional enhancements |

### Frequency Scoring Matrix
| Application Frequency | Score |
|----------------------|-------|
| Multiple times daily | 10 |
| Daily | 8 |
| Several times/week | 6 |
| Weekly | 4 |
| Monthly or less | 2 |

### Complexity Scoring Matrix
| Complexity Level | Score | Indicators |
|-----------------|-------|------------|
| Highly Complex | 10 | Novel problems, cross-domain integration, strategic decisions |
| Complex | 8 | Significant technical depth, multiple considerations |
| Moderate | 6 | Standard professional work, some judgment required |
| Straightforward | 4 | Established patterns, clear procedures |
| Simple | 2 | Routine tasks, well-documented processes |

### Differentiation Scoring Matrix
| Differentiation Level | Score | Observable Difference |
|----------------------|-------|----------------------|
| Key Differentiator | 10 | Top 10% vs others clearly visible |
| Strong | 8 | Top 25% distinguishable |
| Moderate | 6 | Noticeable quality difference |
| Minor | 4 | Subtle distinctions |
| Baseline | 2 | Expected minimum competence |

### Time to Proficiency Scoring Matrix
| Time Period | Score | Typical Development |
|------------|-------|---------------------|
| >2 years | 10 | Deep expertise, advanced specialization |
| 1-2 years | 8 | Significant skill development |
| 6-12 months | 6 | Solid foundation building |
| 3-6 months | 4 | Targeted skill acquisition |
| <3 months | 2 | Quick learning, existing foundation |
