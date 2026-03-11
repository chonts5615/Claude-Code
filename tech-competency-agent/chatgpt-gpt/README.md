# ChatGPT Enterprise Pro GPT: Technical Competency Generator

This directory contains everything needed to create a ChatGPT Enterprise Pro GPT that generates high-quality technical competencies by mapping Job Descriptions against Job Family Competency Models.

## Overview

The **TechComp Pro GPT** follows a 7-step workflow to generate role-specific technical competencies:

```
┌────────────────────────────────────────────────────────────────────────┐
│                         WORKFLOW OVERVIEW                               │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  INPUTS                                                                 │
│  ├── Job Description (from user)                                        │
│  └── Job Family Competency Model (reference library)                    │
│                                                                         │
│  PROCESS                                                                │
│  Step 1: Job Analysis ──────────────────┐                               │
│  Step 2: Model Selection ───────────────┤                               │
│  Step 3: Responsibility Mapping ────────┤── 7-Step Workflow             │
│  Step 4: Customization ─────────────────┤                               │
│  Step 5: Quality Validation ────────────┤                               │
│  Step 6: Criticality Ranking ───────────┤                               │
│  Step 7: Output Generation ─────────────┘                               │
│                                                                         │
│  OUTPUT                                                                 │
│  └── Technical Competency Profile (6-10 ranked competencies)            │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
chatgpt-gpt/
├── README.md                                    # This file
├── CHATGPT_GPT_SYSTEM_INSTRUCTIONS.md          # Complete GPT system prompt
├── GPT_CREATION_GUIDE.md                        # Step-by-step GPT setup guide
├── job_family_competency_model_schema.yaml     # Schema for competency models
│
├── prompt_templates/                            # Step-by-step prompt templates
│   ├── step1_job_analysis.md
│   ├── step2_model_selection.md
│   ├── step3_responsibility_mapping.md
│   ├── step4_customization.md
│   ├── step5_validation.md
│   ├── step6_criticality_ranking.md
│   └── step7_output_generation.md
│
└── example_models/                              # Pre-built competency models
    └── IT_job_family_competency_model.yaml     # Information Technology model
```

## Quick Start

### Option 1: Create ChatGPT Enterprise Pro GPT

1. Open ChatGPT Enterprise
2. Navigate to "Explore GPTs" > "Create a GPT"
3. Copy the contents of `CHATGPT_GPT_SYSTEM_INSTRUCTIONS.md` into the "Instructions" field
4. Upload the example models from `example_models/` as knowledge files
5. Configure the GPT name, description, and capabilities
6. Save and publish

See `GPT_CREATION_GUIDE.md` for detailed instructions.

### Option 2: Use Prompts Manually

You can use the prompt templates directly in any ChatGPT conversation:

1. Start with `step1_job_analysis.md` - paste a Job Description
2. Continue through each step sequentially
3. The final output from `step7_output_generation.md` is your deliverable

## Key Concepts

### Job Family Competency Model

A structured framework defining all potential competencies for a job family (e.g., Information Technology, Engineering, Finance). The model includes:

- **Core Competencies**: Required across ALL roles in the family
- **Specialized Competencies**: Specific to sub-functions (e.g., Data Engineering, Security)
- **Proficiency Levels**: FOUNDATIONAL → WORKING → ADVANCED → EXPERT
- **Behavioral Indicators**: Observable, assessable behaviors

### Competency Generation Process

Rather than creating competencies from scratch, the GPT:

1. **Analyzes** the Job Description to understand role requirements
2. **Selects** applicable competencies from the Job Family Model
3. **Maps** JD responsibilities to model competencies
4. **Customizes** definitions and indicators for the specific role
5. **Validates** against quality standards and leadership overlap
6. **Ranks** by criticality using multi-factor analysis
7. **Generates** the final deliverable

### Quality Standards

All generated competencies must meet:

| Standard | Requirement |
|----------|-------------|
| Coverage | ≥ 80% of JD responsibilities mapped |
| Count | 6-10 competencies per role |
| Definition | 50-150 words, work-context specific |
| Indicators | 3-7 observable behaviors per competency |
| Format | "Domain: Specific Skill" naming convention |
| Overlap | No material overlap with leadership competencies |

## Using the Pre-built IT Model

The included `IT_job_family_competency_model.yaml` provides a comprehensive starting point for Information Technology roles:

### Core Competencies (6)
1. Software Development: Programming & Implementation
2. Systems Design: Architecture & Integration
3. Data Management: Storage & Processing
4. Quality Assurance: Testing & Validation
5. Security: Application Security Fundamentals
6. Problem Solving: Technical Analysis & Debugging

### Specialized Competencies
- **Cloud & DevOps**: Infrastructure Management, CI/CD Pipeline Engineering
- **Data Engineering**: Pipeline Development
- **Machine Learning**: Model Development & Deployment

### Supported Roles
- Software Engineer (Entry → Principal)
- Data Engineer
- DevOps Engineer
- Cloud Architect
- Full Stack Developer
- Machine Learning Engineer
- Site Reliability Engineer
- Security Engineer

## Creating Custom Job Family Models

Use `job_family_competency_model_schema.yaml` as a template to create models for other job families:

1. **Define Metadata**: Model ID, name, version, owner
2. **Describe Job Family**: Purpose, scope, typical roles, career progression
3. **Add Core Competencies**: 4-8 competencies required for all roles
4. **Add Specialized Competencies**: Grouped by specialization area
5. **Define Level Expectations**: From Entry to Principal
6. **Set Generation Rules**: Counts, thresholds, boundaries

### Example Starter for Finance Family

```yaml
job_family_competency_model:
  metadata:
    model_id: "JF_FIN_2024_001"
    model_name: "Finance Competency Framework"
    job_family: "Finance"
    version: "1.0.0"

  competency_architecture:
    core_competencies:
      - competency_id: "FIN_CORE_001"
        name: "Financial Analysis: Performance Assessment"
        category: "TECHNICAL"
        definition:
          text: "The ability to analyze financial data..."
        # ... continue with full structure
```

## Workflow Customization

### Adjusting Quality Thresholds

Modify these in the system instructions:

```yaml
quality_gates:
  coverage_minimum: 0.80      # Increase for stricter coverage
  competency_min: 6           # Adjust range as needed
  competency_max: 10
  definition_words_min: 50    # Adjust word count requirements
  definition_words_max: 150
  overlap_threshold: 0.82     # Lower = stricter overlap detection
```

### Adding Custom Criticality Factors

The default factors and weights:

| Factor | Weight | Description |
|--------|--------|-------------|
| Coverage | 25% | % of responsibilities enabled |
| Impact/Risk | 20% | Consequence if missing |
| Frequency | 15% | How often applied |
| Complexity | 15% | Technical difficulty |
| Differentiation | 15% | Distinguishes high performers |
| Time to Proficiency | 10% | Development investment |

To customize, modify the ranking section in the system instructions.

### Alternative Output Formats

The GPT can generate outputs in multiple formats:

1. **Full YAML Profile** (default) - Complete structured output
2. **Condensed Table** - Quick reference format
3. **Interview Guide** - Assessment-focused format
4. **Development Plan** - Learning-focused format

Request specific formats in your prompts:
- "Generate the output as a condensed table"
- "Create an interview assessment guide"
- "Format as a development plan template"

## Integration Options

### With HR Systems

Export the YAML output and transform for:
- Workday competency libraries
- SuccessFactors skill profiles
- Cornerstone development plans

### With Assessment Platforms

Use behavioral indicators for:
- Interview question generation
- 360 feedback surveys
- Skills assessment rubrics

### With Learning Platforms

Use development resources for:
- Learning path recommendations
- Course mapping
- Certification tracking

## Troubleshooting

### Common Issues

**Low Coverage (<80%)**
- Expand competency selection from specialized pool
- Consider creating custom competency for unmapped responsibilities
- Review if some responsibilities are leadership-focused

**Too Many Competencies (>10)**
- Apply stricter criticality threshold
- Combine closely related competencies
- Focus on core competencies

**Leadership Overlap Detected**
- Review flagged competency definitions
- Emphasize technical aspects over interpersonal
- Replace "influence stakeholders" with "gather technical requirements"

**Definition Too Short/Long**
- Add role-specific context and tools
- Remove redundant phrases
- Focus on observable application

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01 | Initial release with IT model |

## Contributing

To contribute additional job family models or improvements:

1. Follow the schema in `job_family_competency_model_schema.yaml`
2. Include at least 4 core competencies with full structure
3. Test with sample job descriptions
4. Submit for review

## License

Internal use only. Contact Talent Management for external licensing.
