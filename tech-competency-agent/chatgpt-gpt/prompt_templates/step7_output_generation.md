# Step 7: Output Generation Prompt Template

## User Prompt Format

```
Generate the final Technical Competency Profile deliverable.

Include:
1. Complete competency profiles ranked by criticality
2. Responsibility traceability matrix
3. Quality summary report

Format as a professional deliverable ready for stakeholder review.
```

## GPT Response Template

```yaml
# ============================================================================
#
#                    TECHNICAL COMPETENCY PROFILE
#
# ============================================================================
#
# Job Title:     [Job Title]
# Job Family:    [Job Family]
# Job Level:     [Level]
# Generated:     [YYYY-MM-DD]
# Model Source:  [Job Family Competency Model Name/Version]
#
# ============================================================================

# ----------------------------------------------------------------------------
# EXECUTIVE SUMMARY
# ----------------------------------------------------------------------------

executive_summary:
  overview: |
    This Technical Competency Profile defines the [N] critical technical
    competencies required for success in the [Job Title] role within the
    [Job Family] job family. The competencies were derived by analyzing
    [N] job responsibilities against the [Model Name] competency framework
    and ranking them by business criticality.

  key_metrics:
    total_competencies: [N]
    responsibility_coverage: "[X.XX%]"
    highest_criticality_score: [X.XX]
    average_criticality_score: [X.XX]

  competency_overview:
    - rank: 1
      name: "[Competency Name]"
      criticality: "[X.XX]"
      summary: "[One-line summary of why this is critical]"
    - rank: 2
      name: "[Competency Name]"
      criticality: "[X.XX]"
      summary: "[Summary]"
    - rank: 3
      name: "[Competency Name]"
      criticality: "[X.XX]"
      summary: "[Summary]"
    # Top 3 for executive summary

  usage_recommendations:
    - "[How to use this profile for hiring]"
    - "[How to use for performance management]"
    - "[How to use for development planning]"

# ----------------------------------------------------------------------------
# TECHNICAL COMPETENCIES (Ranked by Criticality)
# ----------------------------------------------------------------------------

technical_competencies:

  # ==========================================================================
  # COMPETENCY #1 (Highest Criticality)
  # ==========================================================================
  - rank: 1
    competency_id: "[CORE_001 or SPEC_001]"
    name: "[Domain: Specific Skill]"
    category: "[TECHNICAL | METHODOLOGICAL | DOMAIN_KNOWLEDGE]"
    criticality_score: [X.XX]
    proficiency_target: "[FOUNDATIONAL | WORKING | ADVANCED | EXPERT]"

    # Definition (50-150 words)
    definition: |
      [Complete, customized definition that is specific to this role's
      context. Includes relevant tools, methods, and technologies.
      Describes how the competency is applied in day-to-day work.
      Written in clear, professional language without undefined jargon.

      The definition should be substantive enough to clearly communicate
      what this competency entails and how it manifests in this role,
      while remaining concise and actionable for assessment purposes.]

    # Business Impact Statement
    why_it_matters: |
      [2-3 sentences explaining the business impact of this competency.
      Connect to organizational outcomes, quality metrics, delivery
      timelines, or strategic objectives. Help stakeholders understand
      why investment in this competency yields returns.]

    # Behavioral Indicators (3-7)
    behavioral_indicators:
      - "[Verb + Object + Context/Standard] - Observable behavior 1"
      - "[Verb + Object + Context/Standard] - Observable behavior 2"
      - "[Verb + Object + Context/Standard] - Observable behavior 3"
      - "[Verb + Object + Context/Standard] - Observable behavior 4"
      # 3-7 total indicators

    # Applied Scope
    applied_scope:
      tools_methods_technologies:
        - "[Tool/Technology 1]"
        - "[Tool/Technology 2]"
        - "[Tool/Technology 3]"
      standards_frameworks:
        - "[Standard 1]"
        - "[Framework 1]"
      typical_outputs:
        - "[Deliverable 1]"
        - "[Work product 2]"
        - "[Artifact 3]"

    # Proficiency Level Definitions
    proficiency_levels:
      foundational:
        description: "[What foundational looks like for this competency]"
        typical_behaviors:
          - "[Behavior at foundational level]"
          - "[Behavior at foundational level]"
      working:
        description: "[What working level looks like]"
        typical_behaviors:
          - "[Behavior at working level]"
          - "[Behavior at working level]"
      advanced:
        description: "[What advanced looks like]"
        typical_behaviors:
          - "[Behavior at advanced level]"
          - "[Behavior at advanced level]"
      expert:
        description: "[What expert looks like]"
        typical_behaviors:
          - "[Behavior at expert level]"
          - "[Behavior at expert level]"

    # Responsibility Traceability
    responsibility_trace:
      - responsibility_id: "R1"
        responsibility_text: "[Full normalized text]"
        contribution: "PRIMARY"
        justification: "[How this competency enables this responsibility]"
      - responsibility_id: "R3"
        responsibility_text: "[Text]"
        contribution: "SECONDARY"
        justification: "[Justification]"
      # All mapped responsibilities

    # Development Guidance
    development_guidance:
      formal_learning:
        - "[Training course/certification]"
        - "[Educational resource]"
      experiential_learning:
        - "[On-the-job experience to develop this]"
        - "[Project type that builds this competency]"
      assessment_methods:
        - "[How to assess this competency]"
        - "[Evidence to look for]"

  # ==========================================================================
  # COMPETENCY #2
  # ==========================================================================
  - rank: 2
    competency_id: "[ID]"
    name: "[Domain: Specific Skill]"
    category: "[Category]"
    criticality_score: [X.XX]
    proficiency_target: "[Level]"

    definition: |
      [50-150 word customized definition]

    why_it_matters: |
      [Business impact statement]

    behavioral_indicators:
      - "[Indicator 1]"
      - "[Indicator 2]"
      - "[Indicator 3]"

    applied_scope:
      tools_methods_technologies: ["Tool1", "Tool2"]
      standards_frameworks: ["Standard1"]
      typical_outputs: ["Output1", "Output2"]

    proficiency_levels:
      foundational:
        description: "[Description]"
        typical_behaviors: ["Behavior1"]
      working:
        description: "[Description]"
        typical_behaviors: ["Behavior1"]
      advanced:
        description: "[Description]"
        typical_behaviors: ["Behavior1"]
      expert:
        description: "[Description]"
        typical_behaviors: ["Behavior1"]

    responsibility_trace:
      - responsibility_id: "R2"
        responsibility_text: "[Text]"
        contribution: "[Contribution]"
        justification: "[Justification]"

    development_guidance:
      formal_learning: ["Resource"]
      experiential_learning: ["Experience"]
      assessment_methods: ["Method"]

  # Continue for all ranked competencies (typically 6-10)...

# ----------------------------------------------------------------------------
# RESPONSIBILITY TRACEABILITY MATRIX
# ----------------------------------------------------------------------------

traceability_matrix:
  description: |
    This matrix shows how each job responsibility is supported by the
    selected competencies, ensuring comprehensive coverage of role requirements.

  coverage_summary:
    total_responsibilities: [N]
    fully_covered: [N]  # Has PRIMARY mapping
    partially_covered: [N]  # Has SECONDARY/SUPPORTING only
    not_covered: [N]
    coverage_rate: "[X.XX%]"

  detailed_matrix:
    - responsibility_id: "R1"
      responsibility_text: "[Full normalized responsibility text]"
      importance: "[HIGH | MEDIUM | LOW]"
      category: "[TECHNICAL_EXECUTION | ANALYSIS_DESIGN | etc.]"
      coverage_status: "[FULLY_COVERED | PARTIALLY_COVERED | NOT_COVERED]"
      competency_mappings:
        - competency_id: "[ID]"
          competency_name: "[Name]"
          contribution: "PRIMARY"
        - competency_id: "[ID]"
          competency_name: "[Name]"
          contribution: "SECONDARY"

    - responsibility_id: "R2"
      responsibility_text: "[Text]"
      importance: "[Importance]"
      category: "[Category]"
      coverage_status: "[Status]"
      competency_mappings:
        - competency_id: "[ID]"
          competency_name: "[Name]"
          contribution: "[Contribution]"

    # Continue for all responsibilities...

  # Visual Matrix (for easy scanning)
  matrix_visualization: |
    Responsibility    | CORE_001 | CORE_002 | SPEC_001 | SPEC_002 | ...
    ------------------|----------|----------|----------|----------|----
    R1 - [Brief]      |    P     |    S     |          |          |
    R2 - [Brief]      |          |    P     |    S     |          |
    R3 - [Brief]      |    S     |          |    P     |          |
    R4 - [Brief]      |          |          |    P     |    P     |
    ...

    Legend: P = PRIMARY, S = SECONDARY, (blank) = not mapped

# ----------------------------------------------------------------------------
# COMPETENCY DISTRIBUTION ANALYSIS
# ----------------------------------------------------------------------------

competency_analysis:
  by_category:
    technical:
      count: [N]
      percentage: "[X%]"
      competencies: ["ID1", "ID2"]
    methodological:
      count: [N]
      percentage: "[X%]"
      competencies: ["ID3"]
    domain_knowledge:
      count: [N]
      percentage: "[X%]"
      competencies: ["ID4"]

  by_source:
    core_competencies:
      count: [N]
      percentage: "[X%]"
    specialized_competencies:
      count: [N]
      percentage: "[X%]"
    emerging_competencies:
      count: [N]
      percentage: "[X%]"

  criticality_distribution:
    high_criticality: # Score >= 7.5
      count: [N]
      competencies: ["ID1", "ID2"]
    medium_criticality: # Score 5.0-7.5
      count: [N]
      competencies: ["ID3", "ID4"]
    lower_criticality: # Score < 5.0
      count: [N]
      competencies: ["ID5"]

# ----------------------------------------------------------------------------
# QUALITY SUMMARY REPORT
# ----------------------------------------------------------------------------

quality_summary:
  generation_metadata:
    generated_date: "[YYYY-MM-DD]"
    job_family_model_used: "[Model Name/Version]"
    workflow_version: "7-Step Competency Generation v1.0"

  quality_gates_passed:
    - gate: "Job Analysis Completeness"
      status: "PASS"
      details: "[N] responsibilities extracted and normalized"
    - gate: "Model Alignment"
      status: "PASS"
      details: "Competencies selected from [Model Name]"
    - gate: "Responsibility Coverage"
      status: "PASS"
      details: "[X.XX%] coverage achieved (threshold: 80%)"
    - gate: "Competency Count"
      status: "PASS"
      details: "[N] competencies selected (range: 6-10)"
    - gate: "Leadership Overlap"
      status: "PASS"
      details: "No material overlaps detected"
    - gate: "Format Compliance"
      status: "PASS"
      details: "All definitions 50-150 words, 3-7 indicators each"

  validation_metrics:
    responsibility_coverage_rate: "[X.XX%]"
    high_importance_coverage_rate: "[X.XX%]"
    average_relevance_score: "[X.XX]"
    average_criticality_score: "[X.XX]"

  notes_and_observations:
    - "[Any important observation about the competency profile]"
    - "[Recommendations for profile usage]"
    - "[Areas that may need periodic review]"

# ----------------------------------------------------------------------------
# APPENDIX: SOURCE JOB DESCRIPTION
# ----------------------------------------------------------------------------

appendix_job_description:
  original_job_title: "[Title as provided]"
  extracted_responsibilities:
    - id: "R1"
      original_text: "[Original text from JD]"
      normalized_text: "[Normalized version used for analysis]"
    - id: "R2"
      original_text: "[Original]"
      normalized_text: "[Normalized]"
    # All responsibilities

  requirements_noted:
    skills: ["Skill1", "Skill2"]
    tools: ["Tool1", "Tool2"]
    certifications: ["Cert1"]
    experience: "[Experience level noted]"

# ============================================================================
# END OF TECHNICAL COMPETENCY PROFILE
# ============================================================================
```

## Alternative Output Formats

### Condensed Table Format (for quick reference)

```markdown
# Technical Competency Profile: [Job Title]

| Rank | Competency | Category | Criticality | Proficiency Target |
|------|------------|----------|-------------|-------------------|
| 1 | [Domain: Skill] | TECHNICAL | 8.75 | ADVANCED |
| 2 | [Domain: Skill] | METHODOLOGICAL | 8.20 | WORKING |
| 3 | [Domain: Skill] | TECHNICAL | 7.85 | ADVANCED |
| 4 | [Domain: Skill] | DOMAIN_KNOWLEDGE | 7.50 | WORKING |
| 5 | [Domain: Skill] | TECHNICAL | 7.25 | ADVANCED |
| 6 | [Domain: Skill] | METHODOLOGICAL | 6.90 | WORKING |

**Coverage:** 87.5% of responsibilities | **Quality:** All gates passed
```

### Interview Assessment Format

```markdown
# Interview Assessment Guide: [Job Title]

## Competency 1: [Name] (Criticality: X.XX)

**Definition:** [Abbreviated definition]

**Interview Questions:**
1. "Tell me about a time when you [applied this competency]..."
2. "How would you approach [scenario requiring this competency]?"
3. "What tools/methods do you use for [competency area]?"

**Look For:**
- [ ] [Behavioral indicator 1]
- [ ] [Behavioral indicator 2]
- [ ] [Behavioral indicator 3]

**Rating Scale:**
- EXPERT (5): [Description]
- ADVANCED (4): [Description]
- WORKING (3): [Description]
- FOUNDATIONAL (2): [Description]
- NOT DEMONSTRATED (1): [Description]
```

### Development Plan Format

```markdown
# Development Plan Template: [Job Title]

## Current State Assessment

| Competency | Target Level | Current Level | Gap |
|------------|--------------|---------------|-----|
| [Name] | ADVANCED | [To assess] | [To calculate] |
| [Name] | WORKING | [To assess] | [To calculate] |

## Development Priorities (by gap size)

### Priority 1: [Competency Name]

**Target:** [Level]
**Timeline:** [Suggested timeframe]

**Development Activities:**
- [ ] [Formal learning activity]
- [ ] [Experiential learning activity]
- [ ] [Practice/project opportunity]

**Success Indicators:**
- [How we'll know the gap is closed]
```
