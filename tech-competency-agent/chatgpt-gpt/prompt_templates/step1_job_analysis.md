# Step 1: Job Analysis Prompt Template

## User Prompt Format

```
Analyze this Job Description and extract structured components:

---
[PASTE JOB DESCRIPTION HERE]
---

Please:
1. Identify the job title, job family, and level
2. Extract and summarize the key themes
3. Parse all responsibilities into normalized format
4. Identify mentioned tools, skills, and certifications
```

## GPT Response Template

```yaml
# STEP 1: JOB ANALYSIS RESULTS
# ============================================================================

job_analysis:
  # Core Job Information
  job_title: "[Extracted job title]"
  job_family: "[Inferred job family - e.g., Information Technology, Engineering, Finance]"
  job_level: "[Entry | Mid | Senior | Lead | Principal | Executive]"
  department: "[If mentioned]"
  reports_to: "[If mentioned]"

  # Summary Analysis
  job_purpose: |
    [2-3 sentence summary of what this role exists to accomplish]

  key_themes:
    - "[Theme 1 - Major focus area]"
    - "[Theme 2 - Major focus area]"
    - "[Theme 3 - Major focus area]"

  # Parsed Responsibilities
  responsibilities:
    - id: "R1"
      raw_text: "[Original text from JD]"
      normalized: "[Action Verb] [Object] [Context/Standard]"
      category: "[TECHNICAL_EXECUTION | ANALYSIS_DESIGN | COLLABORATION | MANAGEMENT | QUALITY_ASSURANCE]"
      importance: "[HIGH | MEDIUM | LOW]"

    - id: "R2"
      raw_text: "[Original text]"
      normalized: "[Normalized format]"
      category: "[Category]"
      importance: "[Importance]"

    # Continue for all responsibilities...

  # Requirements Analysis
  requirements_signals:
    required_skills:
      - "[Skill 1]"
      - "[Skill 2]"

    preferred_skills:
      - "[Skill 1]"
      - "[Skill 2]"

    tools_technologies:
      - "[Tool/Technology 1]"
      - "[Tool/Technology 2]"

    certifications:
      - "[Certification 1]"

    experience_level: "[X years typical]"

  # Analysis Summary
  analysis_summary:
    total_responsibilities: [N]
    responsibility_breakdown:
      technical_execution: [N]
      analysis_design: [N]
      collaboration: [N]
      management: [N]
      quality_assurance: [N]

    high_importance_count: [N]
    key_technical_domains:
      - "[Domain 1]"
      - "[Domain 2]"

# Ready to proceed to Step 2: Competency Model Selection
```

## Normalization Guidelines

### Responsibility Normalization Rules:

1. **Start with strong action verb:**
   - Design, Develop, Implement, Analyze, Manage, Lead, Create, Build, Configure, Monitor, Evaluate, Document, Collaborate, Support, Maintain, Optimize

2. **Include clear object:**
   - What is being acted upon (systems, reports, processes, etc.)

3. **Add context/standard when possible:**
   - Quality standard, methodology, framework, tool, or outcome measure

### Examples:

| Raw Text | Normalized |
|----------|------------|
| "Responsible for developing software applications" | "Develops software applications using agile methodology" |
| "Works with stakeholders to gather requirements" | "Collaborates with stakeholders to gather and document business requirements" |
| "Ensures quality of deliverables" | "Validates deliverable quality against defined acceptance criteria" |
| "Manages team of 5 developers" | "Manages team of 5 developers providing technical direction and mentorship" |

### Category Assignment Guide:

| Category | Characteristics |
|----------|-----------------|
| TECHNICAL_EXECUTION | Hands-on building, coding, configuring, implementing |
| ANALYSIS_DESIGN | Research, analysis, architecture, planning, design |
| COLLABORATION | Working with others, communication, coordination |
| MANAGEMENT | Supervision, project management, resource allocation |
| QUALITY_ASSURANCE | Testing, validation, review, compliance checking |

### Importance Assignment Guide:

| Importance | Indicators |
|------------|------------|
| HIGH | Core to role purpose, mentioned multiple times, tied to key deliverables |
| MEDIUM | Important but not central, supports other responsibilities |
| LOW | Administrative, occasional, or supporting activities |
