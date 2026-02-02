# ChatGPT Enterprise Pro GPT Creation Guide

This guide provides step-by-step instructions for creating the TechComp Pro GPT in ChatGPT Enterprise Pro.

## Prerequisites

- ChatGPT Enterprise Pro subscription
- Access to create custom GPTs
- The files from this directory:
  - `CHATGPT_GPT_SYSTEM_INSTRUCTIONS.md`
  - Job Family Competency Model files (from `example_models/`)

## Step 1: Access GPT Builder

1. Log into ChatGPT Enterprise
2. Click the **Explore GPTs** option in the sidebar
3. Click **Create a GPT** or the **+** button

## Step 2: Configure GPT Identity

### Name
```
TechComp Pro - Technical Competency Generator
```

### Description
```
Generate high-quality technical competencies for any role by mapping Job Descriptions
against structured Job Family Competency Models. Follows a 7-step IO Psychology-based
workflow with quality gates and criticality ranking.
```

### Profile Picture
Use an appropriate icon representing competency/skills development (optional).

## Step 3: Enter System Instructions

Copy the ENTIRE contents of `CHATGPT_GPT_SYSTEM_INSTRUCTIONS.md` into the **Instructions** field.

This is a large document (~4000+ words) that includes:
- GPT identity and purpose
- Complete 7-step workflow
- Quality standards
- Output formats
- Interaction guidelines

**Important**: Do not truncate or summarize. The full instructions are required for proper operation.

## Step 4: Configure Conversation Starters

Add these suggested conversation starters:

```
1. "I have a Job Description to analyze. Help me generate technical competencies."

2. "I want to use a specific Job Family Competency Model for competency generation."

3. "Walk me through the 7-step competency generation workflow."

4. "Generate competencies for a Senior Software Engineer role."

5. "Help me create a Job Family Competency Model for [job family]."
```

## Step 5: Upload Knowledge Files

Upload the following files as knowledge:

### Required
1. **IT Job Family Competency Model**
   - File: `example_models/IT_job_family_competency_model.yaml`
   - Purpose: Pre-built model for IT roles

### Optional (if available)
2. Additional Job Family Models (Engineering, Finance, etc.)
3. Company-specific competency frameworks
4. Industry standards documentation (SFIA, O*NET excerpts)

### Upload Process
1. Click **Knowledge** section
2. Click **Upload files**
3. Select the YAML files
4. Wait for processing confirmation

## Step 6: Configure Capabilities

Enable these capabilities:

| Capability | Enabled | Notes |
|------------|---------|-------|
| Web Browsing | Optional | For industry research if needed |
| DALL-E Image Generation | No | Not needed |
| Code Interpreter | Optional | For data analysis if user uploads Excel |

Recommended: Enable **Code Interpreter** for handling uploaded Job Description files.

## Step 7: Test the GPT

Before publishing, test with these scenarios:

### Test 1: Basic Job Description Analysis
```
Prompt: "Analyze this job description and generate competencies:

Job Title: Senior Software Engineer
Summary: Lead development of cloud-native applications...
Responsibilities:
- Design and implement scalable microservices
- Lead code reviews and mentor junior developers
- Collaborate with product teams on technical requirements
- Troubleshoot production issues and optimize performance
- Write technical documentation and architecture decisions"

Expected: GPT should walk through Step 1 (Job Analysis) and continue through workflow
```

### Test 2: Model-Based Generation
```
Prompt: "Using the IT Job Family Competency Model, generate competencies for a
Mid-level DevOps Engineer with these responsibilities:
- Manage CI/CD pipelines using GitHub Actions
- Deploy and maintain Kubernetes clusters
- Implement infrastructure as code with Terraform
- Monitor system performance and respond to incidents
- Automate operational tasks"

Expected: GPT should reference the IT model and select appropriate competencies
```

### Test 3: Quality Validation
```
Prompt: "Check these competencies for leadership overlap and format compliance"

Expected: GPT should run Step 5 validation and identify any issues
```

## Step 8: Publish the GPT

### Visibility Options

| Option | Use Case |
|--------|----------|
| Only me | Testing and personal use |
| People with the link | Share with specific teams |
| Everyone in [Organization] | Organization-wide deployment |
| Public | Not recommended for enterprise tools |

### Recommended
1. Start with **People with the link** for pilot testing
2. Gather feedback from HR/Talent Management
3. Move to **Organization-wide** after validation

## Step 9: Share and Onboard Users

### User Guide Email Template

```
Subject: New Tool Available - TechComp Pro GPT for Competency Generation

Team,

We've launched TechComp Pro, a ChatGPT-based tool for generating technical
competencies. Here's how to use it:

**Access**: [Insert GPT Link]

**What it does**:
- Analyzes Job Descriptions to extract requirements
- Maps responsibilities to our Job Family Competency Models
- Generates 6-10 ranked technical competencies per role
- Ensures quality through automated validation

**How to use**:
1. Open the GPT link
2. Paste a Job Description or describe the role
3. Follow the 7-step workflow prompts
4. Review and refine the generated competencies

**Best for**:
- Creating competency profiles for new roles
- Updating existing role competencies
- Ensuring consistency across job family

**Not for**:
- Leadership/behavioral competencies (separate model)
- Final publication without HR review

Questions? Contact [HR/Talent Management contact]
```

## Configuration Reference

### System Instruction Sections

| Section | Purpose | Location in Instructions |
|---------|---------|-------------------------|
| Identity | GPT persona and expertise | Top |
| Workflow Overview | 7-step process diagram | Early |
| Step 1-7 Details | Detailed process for each step | Middle |
| Output Formats | How to structure deliverables | Middle-Late |
| Interaction Guidelines | How to respond to users | Late |
| Quality Standards | Format requirements | Late |
| Error Handling | Common issues and resolutions | End |
| Memory Instructions | Context handling | End |

### Key Thresholds (Modifiable)

These values appear in the system instructions and can be adjusted:

```yaml
# Coverage
minimum_coverage: 0.80  # 80% of responsibilities must be mapped

# Competency Count
min_competencies: 6
max_competencies: 10

# Definition Word Count
min_words: 50
max_words: 150

# Indicators
min_indicators: 3
max_indicators: 7

# Overlap Detection
material_overlap: 0.82  # Above this is flagged
minor_overlap: 0.72     # Review zone

# Relevance Scoring
minimum_relevance: 0.60  # Below this, no mapping
```

## Maintenance

### Monthly Review
- Check usage analytics
- Review user feedback
- Update competency models if needed

### Quarterly Updates
- Refresh industry alignment
- Add new job family models
- Incorporate organizational changes

### Annual Overhaul
- Full model review
- Workflow optimization
- User experience improvements

## Troubleshooting

### GPT Doesn't Follow Workflow
- Verify full system instructions are entered
- Check for truncation in instructions field
- Test with explicit step prompts

### Knowledge Files Not Recognized
- Re-upload files
- Ensure YAML syntax is valid
- Check file size limits

### Inconsistent Output Quality
- Add explicit quality reminders to instructions
- Include more examples in knowledge
- Guide users to provide complete JDs

### Timeout on Long JDs
- Break JD into sections
- Process steps individually
- Use condensed analysis mode

## Support

For issues with the GPT:
1. Check this guide's troubleshooting section
2. Contact [IT Support/Admin]
3. Submit feedback through ChatGPT interface

For competency model questions:
1. Contact Talent Management
2. Reference industry frameworks (SFIA, O*NET)
3. Review example model structure
