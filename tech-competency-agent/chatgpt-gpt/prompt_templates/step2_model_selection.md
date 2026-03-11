# Step 2: Competency Model Selection Prompt Template

## User Prompt Format (With Model Provided)

```
Using this Job Family Competency Model:

---
[PASTE JOB FAMILY COMPETENCY MODEL OR REFERENCE IT]
---

Select applicable competencies for the job analyzed in Step 1.
The job is: [Job Title] at [Level] level in the [Job Family] family.
```

## User Prompt Format (No Model - Request GPT to Use Built-in)

```
Based on the job analysis from Step 1:
- Job Family: [Job Family]
- Job Level: [Level]

Please identify the applicable competencies using your built-in
knowledge of competency frameworks for this job family.
```

## GPT Response Template

```yaml
# STEP 2: COMPETENCY MODEL SELECTION
# ============================================================================

model_selection:
  # Model Identification
  job_family_model: "[Model Name or 'GPT-Generated [Job Family] Model']"
  model_version: "[Version if provided, or 'v1.0-generated']"
  job_level: "[Level from Step 1]"

  # Level-Based Expectations
  level_expectations:
    proficiency_target:
      core_competencies: "[FOUNDATIONAL | WORKING | ADVANCED | EXPERT]"
      specialized_competencies: "[FOUNDATIONAL | WORKING | ADVANCED | EXPERT]"

    competency_depth:
      core_minimum: [N]  # Minimum core competencies expected
      specialized_range: "[N-M]"  # Range of specialized competencies

    autonomy_level: "[Description of independence expected at this level]"
    complexity_handled: "[Types of problems this level should handle]"

  # Core Competency Pool
  # (Competencies that apply to ALL roles in this job family)
  core_competency_pool:
    - competency_id: "CORE_001"
      name: "[Domain: Specific Skill]"
      category: "[TECHNICAL | METHODOLOGICAL | DOMAIN_KNOWLEDGE]"
      model_definition: |
        [Definition from the competency model - this is the baseline
        that will be customized for the specific role]
      applicability_reason: |
        [Why this competency applies to the analyzed job based on
        responsibilities and requirements identified in Step 1]
      relevant_responsibilities: ["R1", "R3", "R7"]

    - competency_id: "CORE_002"
      name: "[Domain: Specific Skill]"
      category: "[Category]"
      model_definition: "[Definition]"
      applicability_reason: "[Reason]"
      relevant_responsibilities: ["R2", "R5"]

    # Continue for all applicable core competencies...

  # Specialized Competency Pool
  # (Competencies specific to certain roles/functions within the family)
  specialized_competency_pool:
    - competency_id: "SPEC_001"
      name: "[Domain: Specific Skill]"
      specialization_area: "[e.g., Data Engineering, Security, Frontend]"
      category: "[Category]"
      model_definition: "[Definition]"
      applicability_reason: "[Why this specialized competency applies]"
      relevant_responsibilities: ["R4", "R8", "R9"]

    - competency_id: "SPEC_002"
      name: "[Domain: Specific Skill]"
      specialization_area: "[Area]"
      category: "[Category]"
      model_definition: "[Definition]"
      applicability_reason: "[Reason]"
      relevant_responsibilities: ["R6", "R10"]

    # Continue for all applicable specialized competencies...

  # Emerging Competencies (if applicable)
  emerging_competency_pool:
    - competency_id: "EMRG_001"
      name: "[Domain: Emerging Skill]"
      maturity_status: "[EMERGING | DEVELOPING]"
      rationale: "[Why this emerging competency is relevant]"
      industry_signals: ["Signal 1", "Signal 2"]
      relevant_responsibilities: ["R11"]

  # Selection Summary
  selection_summary:
    total_core_selected: [N]
    total_specialized_selected: [N]
    total_emerging_selected: [N]
    total_competency_pool: [N]

    preliminary_coverage_estimate: "[X%]"

    competencies_by_category:
      technical: [N]
      methodological: [N]
      domain_knowledge: [N]

    notes:
      - "[Any observations about gaps or special considerations]"

# Ready to proceed to Step 3: Responsibility-Competency Mapping
```

## Built-in Job Family Models (For GPT Reference)

### Information Technology Job Family - Core Competencies

| ID | Name | Category |
|----|------|----------|
| IT_CORE_001 | Software Development: Programming & Coding | TECHNICAL |
| IT_CORE_002 | Systems Design: Architecture & Integration | TECHNICAL |
| IT_CORE_003 | Data Management: Storage & Processing | TECHNICAL |
| IT_CORE_004 | Quality Assurance: Testing & Validation | METHODOLOGICAL |
| IT_CORE_005 | Security: Information Protection | TECHNICAL |
| IT_CORE_006 | Problem Solving: Technical Troubleshooting | METHODOLOGICAL |
| IT_CORE_007 | Documentation: Technical Writing | METHODOLOGICAL |
| IT_CORE_008 | Version Control: Code Management | TECHNICAL |

### Information Technology - Specialized Competencies

| ID | Name | Specialization Area |
|----|------|---------------------|
| IT_SPEC_001 | Cloud Computing: Infrastructure Management | Cloud/DevOps |
| IT_SPEC_002 | Machine Learning: Model Development | Data Science |
| IT_SPEC_003 | Database: Query Optimization | Data Engineering |
| IT_SPEC_004 | Frontend: User Interface Development | Web Development |
| IT_SPEC_005 | Backend: API Development | Web Development |
| IT_SPEC_006 | DevOps: CI/CD Pipeline Management | Cloud/DevOps |
| IT_SPEC_007 | Cybersecurity: Threat Analysis | Security |
| IT_SPEC_008 | Network: Infrastructure Design | Infrastructure |

### Engineering Job Family - Core Competencies

| ID | Name | Category |
|----|------|----------|
| ENG_CORE_001 | Technical Analysis: Requirements Engineering | METHODOLOGICAL |
| ENG_CORE_002 | Design: Engineering Solutions | TECHNICAL |
| ENG_CORE_003 | Modeling: Simulation & Analysis | TECHNICAL |
| ENG_CORE_004 | Testing: Validation & Verification | METHODOLOGICAL |
| ENG_CORE_005 | Project Execution: Delivery Management | METHODOLOGICAL |
| ENG_CORE_006 | Standards: Compliance & Regulations | DOMAIN_KNOWLEDGE |
| ENG_CORE_007 | Safety: Risk Assessment | DOMAIN_KNOWLEDGE |
| ENG_CORE_008 | Documentation: Technical Specifications | METHODOLOGICAL |

### Finance Job Family - Core Competencies

| ID | Name | Category |
|----|------|----------|
| FIN_CORE_001 | Financial Analysis: Performance Assessment | TECHNICAL |
| FIN_CORE_002 | Reporting: Financial Statements | TECHNICAL |
| FIN_CORE_003 | Compliance: Regulatory Requirements | DOMAIN_KNOWLEDGE |
| FIN_CORE_004 | Risk Management: Financial Controls | METHODOLOGICAL |
| FIN_CORE_005 | Budgeting: Planning & Forecasting | TECHNICAL |
| FIN_CORE_006 | Audit: Internal Controls | METHODOLOGICAL |
| FIN_CORE_007 | Systems: Financial Applications | TECHNICAL |
| FIN_CORE_008 | Data Analysis: Financial Modeling | TECHNICAL |

## Level-Based Selection Guidelines

| Level | Core Min | Specialized Range | Proficiency Target |
|-------|----------|-------------------|-------------------|
| Entry | 3 | 1-2 | FOUNDATIONAL |
| Mid | 4 | 2-3 | WORKING |
| Senior | 4 | 3-4 | ADVANCED |
| Lead | 5 | 4-5 | ADVANCED |
| Principal | 5 | 5+ | EXPERT |
