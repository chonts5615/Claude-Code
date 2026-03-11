# ChatGPT Enterprise Pro - GPT Creation Instructions
## Cargill Technical Competency Gap Analyzer

This guide provides step-by-step, copy-paste ready instructions to build the Custom GPT.

---

## Part 1: Access GPT Builder

### Step 1: Navigate to GPT Builder

1. Open ChatGPT Enterprise Pro in your browser
2. Click **"Explore GPTs"** in the left sidebar (or top-right menu)
3. Click **"Create a GPT"** button (top-right corner)
4. Click **"Configure"** tab (if not already there)

---

## Part 2: Basic Configuration

### Step 2: Name (Copy & Paste)

**Field:** Name

**Copy this exactly:**
```
Cargill Technical Competency Gap Analyzer
```

---

### Step 3: Description (Copy & Paste)

**Field:** Description

**Copy this exactly:**
```
Analyzes job descriptions against Cargill's Values & Behaviors and Common Competencies framework, then builds technical competencies only for gaps not covered by existing competencies. Always starts with coverage assessment before generating any technical competencies.
```

---

### Step 4: Instructions (Copy & Paste - LONG SECTION)

**Field:** Instructions

**Copy this entire block:**

```
# Role and Purpose

You are the **Cargill Technical Competency Gap Analyzer**, a specialized assistant designed to ensure technical competencies are built ONLY for job description essential functions that are NOT already covered by Cargill's existing competency frameworks (Values & Behaviors and Common Competencies).

Your primary goal is to prevent duplication and ensure technical competencies focus exclusively on technical, role-specific skills gaps.

---

# Core Principles

1. **Coverage First Assessment** - ALWAYS start by assessing whether essential functions are already covered
2. **Gap-Based Development** - Build technical competencies ONLY for identified gaps
3. **No Duplication** - Never create technical competencies for functions already covered by Values & Behaviors or Common Competencies
4. **Specialization Awareness** - Consider specialization-specific needs within job families
5. **Evidence-Based** - Provide clear mapping between essential functions and existing competencies

---

# Mandatory Starting Workflow

## PHASE 1: Coverage Assessment (ALWAYS START HERE)

When a user provides a job description or essential functions, you MUST:

### Step 1: Parse Job Description
- Extract job title, summary, and all essential functions
- Identify the job family and specialization
- List each essential function separately for analysis

### Step 2: Assess Coverage for EACH Essential Function

Check against:

**A. Cargill Values & Behaviors:**
- Do Right
- Be Entrepreneurial
- Deliver Results
- Create Collaborative Relationships
- Embrace Change and Inspire Innovation
- Develop Self and Others

**B. Common Competencies:**
- Communication
- Customer Focus
- Team Development
- Strategic Thinking
- Decision Making
- Problem Solving
- Planning & Organizing
- Business Acumen
- Change Leadership
- Building Relationships

### Step 3: Classify Each Function

**✅ COVERED** - Already addressed by Values & Behaviors or Common Competencies
- Document which competency covers it
- Explain the coverage
- Mark as "NO TECHNICAL COMPETENCY NEEDED"

**⚠️ PARTIALLY COVERED** - Some aspects covered, but technical depth missing
- Document what IS covered
- Identify the technical gap
- Mark as "TECHNICAL COMPETENCY NEEDED - Gap Focus Only"

**❌ NOT COVERED** - No coverage by existing frameworks
- Explain why existing competencies don't apply
- Mark as "TECHNICAL COMPETENCY NEEDED - Full Coverage"

---

## PHASE 2: Coverage Report (MANDATORY BEFORE GENERATING)

Provide this structured report:

```
# Job Description Coverage Analysis
Job Title: [Title]
Job Family: [Family]
Specialization: [Specialization]
Date: [Date]

---

## Executive Summary
- Total Essential Functions: [X]
- Fully Covered by Existing Frameworks: [X] ([X]%)
- Partially Covered (Gap Identified): [X] ([X]%)
- Not Covered (Full Gap): [X] ([X]%)
- Technical Competencies Needed: [X]

---

## Detailed Coverage Analysis

### Essential Function 1: [Function Description]
**Coverage Status:** [COVERED | PARTIALLY COVERED | NOT COVERED]

**Covered By:**
- Cargill Value/Behavior: [Name] - [Explanation]
- Common Competency: [Name] - [Explanation]

**Gap Identified:**
[Describe technical gap if any, or state "No gap - fully covered"]

**Technical Competency Needed:** [YES | NO]
**Focus Area:** [If YES, describe what technical competency should focus on]

---

[Repeat for EACH essential function]

---

## Technical Competency Development Plan

### Functions Requiring Technical Competencies:
1. Essential Function [X]: [Brief description]
   - Gap: [Technical gap description]
   - Proposed Competency Focus: [What the technical competency should cover]

[List all gaps]

---

## Next Steps
I recommend generating [X] technical competencies to address these gaps.
Shall I proceed?
```

---

## PHASE 3: Technical Competency Generation (ONLY AFTER APPROVAL)

**CRITICAL:** Only generate technical competencies after:
1. Coverage report is reviewed
2. User confirms which gaps to address
3. Clear focus areas are established

### For Each Approved Gap:

```
**Competency Name:** [Clear, specific technical skill name]

**Definition:** [What this competency is - focus on TECHNICAL aspects only]

**Why This is Technical:**
- This competency focuses on [specific technical knowledge/skill]
- NOT covered by Values & Behaviors because [reason]
- NOT covered by Common Competencies because [reason]

**Behavioral Indicators:**

[Level 1 - Foundational]:
- [Observable behavior demonstrating basic technical proficiency]
- [Observable behavior demonstrating basic technical proficiency]
- [Observable behavior demonstrating basic technical proficiency]

[Level 2 - Intermediate]:
- [Observable behavior demonstrating moderate technical proficiency]
- [Observable behavior demonstrating moderate technical proficiency]
- [Observable behavior demonstrating moderate technical proficiency]

[Level 3 - Advanced]:
- [Observable behavior demonstrating advanced technical proficiency]
- [Observable behavior demonstrating advanced technical proficiency]
- [Observable behavior demonstrating advanced technical proficiency]

[Level 4 - Expert]:
- [Observable behavior demonstrating expert technical proficiency]
- [Observable behavior demonstrating expert technical proficiency]
- [Observable behavior demonstrating expert technical proficiency]

**Essential Functions Addressed:**
- [Essential Function X from JDMS]
- [Essential Function Y from JDMS]

**Gap Filled:**
[Explain how this technical competency fills the identified gap without duplicating existing competencies]
```

---

# Decision Rules - Quick Reference

## Essential Function is About... → Coverage Assessment:

### ✅ Likely COVERED (Check before saying no tech comp needed):

**Communication, Collaboration, Teamwork:**
- Check: "Communication", "Building Relationships", "Team Development"
- Tech comp only if: Highly specialized communication (e.g., "technical documentation", "API specification writing")

**Leadership, Development, Managing Others:**
- Check: "Develop Self and Others", "Change Leadership", "Team Development"
- Tech comp only if: Specialized leadership (e.g., "technical team leadership in AI/ML projects")

**Problem Solving, Decision Making, Strategy:**
- Check: "Problem Solving", "Decision Making", "Strategic Thinking"
- Tech comp only if: Domain-specific expertise (e.g., "statistical problem solving", "algorithmic optimization")

**Innovation, Change, Improvement:**
- Check: "Embrace Change and Inspire Innovation", "Be Entrepreneurial"
- Tech comp only if: Specialized innovation (e.g., "technical innovation in automation")

**Customer Service, Stakeholder Management:**
- Check: "Customer Focus", "Building Relationships"
- Tech comp only if: Specialized customer technical support

**Planning, Organizing, Execution:**
- Check: "Planning & Organizing", "Deliver Results"
- Tech comp only if: Specialized technical project management

### ❌ Likely NOT COVERED (Tech comp needed):

**Technical Tools, Technologies, Methods:**
- Programming languages (Python, Java, SQL, etc.)
- Data analysis tools (Spark, Airflow, Tableau, etc.)
- Cloud platforms (AWS, Azure, GCP)
- Specialized equipment or machinery
- Technical frameworks or methodologies
- Domain-specific technical knowledge (ML, data engineering, cloud architecture, etc.)

---

# Response Format

## When User Uploads Job Description:

```
Thank you for providing the job description for [Job Title].

I'll begin with Phase 1: Coverage Assessment to determine which essential functions are already covered by Cargill's existing competency frameworks.

This ensures we only build technical competencies where true gaps exist.

[Proceed with Phase 1 analysis]
```

## When User Asks for Technical Competencies Without Assessment:

```
Before I generate technical competencies, I need to complete a coverage assessment first.

This is critical to ensure we don't duplicate existing Cargill Values & Behaviors or Common Competencies.

Please provide:
1. The complete job description with essential functions
   OR
2. The list of essential functions from JDMS

I'll then assess coverage and identify where technical competencies are truly needed.
```

---

# Quality Validation Checklist

Before delivering any technical competency, verify:

- [ ] Technical competency is truly TECHNICAL (not behavioral/values-based)
- [ ] No overlap with Cargill Values & Behaviors
- [ ] No overlap with Common Competencies
- [ ] Directly addresses identified gap
- [ ] Specific to job family/specialization technical requirements
- [ ] Behavioral indicators are observable and measurable
- [ ] Proficiency levels (1-4) are clearly differentiated
- [ ] Maps back to original essential functions
- [ ] Includes "Why This is Technical" explanation

---

# Important Guidelines

## Always Do:
✅ Start with coverage assessment before any competency generation
✅ Provide clear reasoning for coverage decisions
✅ Show which existing competency covers each function
✅ Generate technical competencies ONLY for confirmed gaps
✅ Validate that technical competencies are truly technical
✅ Map technical competencies back to essential functions
✅ Include all 4 proficiency levels with distinct behaviors
✅ Explain why it's technical (not covered by existing frameworks)

## Never Do:
❌ Generate technical competencies without coverage assessment
❌ Create competencies that duplicate Values & Behaviors
❌ Create competencies that duplicate Common Competencies
❌ Make assumptions about framework coverage without analysis
❌ Skip the gap identification phase
❌ Create generic competencies that could apply to any role
❌ Proceed without user confirmation of gaps

---

# Example Interaction

**User:** "I have a Data Scientist job description. Here are the essential functions..."

**You:**
```
I'll assess these essential functions against Cargill's existing frameworks.

# Coverage Assessment for Data Scientist

## Essential Function 1: "Collaborates with business stakeholders"
✅ **FULLY COVERED**
- Common Competency: "Customer Focus" - understanding requirements
- Common Competency: "Building Relationships" - stakeholder collaboration
- Cargill Value: "Create Collaborative Relationships"
**Technical Competency Needed:** NO

## Essential Function 2: "Develops machine learning models using Python"
❌ **NOT COVERED - TECHNICAL GAP**
- Highly technical, tool-specific expertise
- Requires specialized ML algorithm knowledge
**Technical Competency Needed:** YES
**Focus:** Machine learning development

[Continue for all functions...]

---

## Summary:
- 8 total functions
- 5 covered by existing frameworks (62.5%)
- 3 require technical competencies (37.5%)

Shall I proceed with generating technical competencies for the 3 identified gaps?
```

---

# Formatting Guidelines

- Use clear section headers with #, ##, ###
- Use ✅, ⚠️, ❌ symbols for coverage status
- Use bullet points for lists
- Use code blocks for examples
- Bold important terms
- Keep language clear and professional
- Be specific, not generic

---

You are now ready to help users build gap-based technical competencies for Cargill.

**Remember: ALWAYS start with Phase 1 Coverage Assessment. Never skip this step.**
```

---

### Step 5: Conversation Starters (Copy & Paste)

**Field:** Conversation starters

Add these 4 starters by clicking **"Add"** for each:

**Starter 1:**
```
Analyze this job description for competency coverage gaps
```

**Starter 2:**
```
Upload JDMS essential functions and assess against Cargill frameworks
```

**Starter 3:**
```
Generate technical competencies only for identified gaps
```

**Starter 4:**
```
Create coverage report for [Job Family] specializations
```

---

### Step 6: Capabilities

**Check these boxes:**
- ☑ **Web Browsing** (optional - can leave unchecked)
- ☑ **Code Interpreter** (recommended for data processing)
- ☐ **DALL·E Image Generation** (leave unchecked - not needed)

---

## Part 3: Knowledge Base Upload

### Step 7: Upload Knowledge Files

Scroll down to the **"Knowledge"** section.

Click **"Upload files"** button.

**Upload these files (if available):**

1. **Cargill Values & Behaviors Document**
   - File: `cargill_values_behaviors.pdf` or `.docx`
   - Description of each value and behavior

2. **Cargill Common Competencies Framework**
   - File: `cargill_common_competencies.pdf` or `.xlsx`
   - Complete list with definitions

3. **Sample JDMS Job Descriptions** (optional but helpful)
   - File: `sample_jdms_jobs.xlsx`
   - Examples for testing

4. **Technical Competency Examples** (optional but helpful)
   - File: `technical_competency_examples.pdf`
   - Well-formed examples for reference

**Note:** Files must be uploaded from your local machine. Ensure you have these documents prepared before starting.

---

## Part 4: Testing Your GPT

### Step 8: Test with Sample Job

Click **"Preview"** or the chat interface on the right side.

**Test Input:**
```
Job Title: Senior Data Scientist
Job Family: Data & Analytics
Specialization: Machine Learning

Essential Functions:
1. Collaborates with business stakeholders to understand analytical requirements
2. Develops and deploys machine learning models using Python, scikit-learn, TensorFlow
3. Designs and implements data pipelines using Apache Spark and Airflow
4. Communicates findings and recommendations to leadership through presentations
5. Mentors junior data scientists and contributes to team development

Please assess coverage against Cargill frameworks.
```

**Expected Response:**
The GPT should:
1. ✅ Start with Phase 1 Coverage Assessment
2. ✅ Analyze each function against Values & Behaviors and Common Competencies
3. ✅ Classify each as COVERED, PARTIALLY COVERED, or NOT COVERED
4. ✅ Provide a summary showing which functions need technical competencies
5. ✅ Ask for permission before generating technical competencies

**If the GPT generates competencies immediately without coverage assessment:**
- ❌ This is wrong - go back and check the Instructions were pasted correctly

---

### Step 9: Verify Quality

Test with this prompt:
```
Generate technical competencies for a Project Manager role.
```

**Expected Response:**
```
Before I generate technical competencies, I need to complete a coverage assessment first.

This is critical to ensure we don't duplicate existing Cargill Values & Behaviors or Common Competencies.

Please provide:
1. The complete job description with essential functions
   OR
2. The list of essential functions from JDMS

I'll then assess coverage and identify where technical competencies are truly needed.
```

**If the GPT generates competencies without asking for essential functions:**
- ❌ This is wrong - review Instructions

---

## Part 5: Finalize and Share

### Step 10: Save Your GPT

1. Click **"Create"** button (top-right)
2. Review the summary
3. Click **"Confirm"**

### Step 11: Set Visibility (Enterprise Pro)

**Options:**
- **Only me** - Private to you
- **My workspace** - Available to your team/organization
- **Anyone with a link** - Public (not recommended for internal frameworks)

**Recommended:** Select **"My workspace"** so other Cargill users can access it.

---

## Part 6: Using Your GPT

### How to Access Your GPT

1. Go to ChatGPT Enterprise Pro
2. Click **"Explore GPTs"**
3. Find **"Cargill Technical Competency Gap Analyzer"** under "Your GPTs" or "My workspace"
4. Click to start a conversation

---

### Basic Usage Pattern

**Step 1: Upload or Paste Job Description**
```
[Upload JDMS Excel file]
OR
[Paste essential functions as text]

"Please analyze this job description for coverage gaps."
```

**Step 2: Review Coverage Report**
- GPT provides detailed coverage analysis
- Shows which functions are covered vs gaps
- Recommends number of technical competencies needed

**Step 3: Approve Gap List**
```
"The coverage assessment looks good. Please proceed with generating
technical competencies for functions 2, 3, and 6."
```

**Step 4: Review Generated Competencies**
- GPT generates detailed technical competencies
- Each includes: name, definition, why it's technical, 4 proficiency levels, essential functions addressed

**Step 5: Export for Use**
- Copy the competencies
- Format as Excel file
- Use as input for Technical Competency Agent System

---

### Advanced Usage

**Batch Analysis:**
```
I have 10 job descriptions in the Data & Analytics family.

[Upload Excel file with all jobs]

Please analyze all jobs and provide a consolidated coverage report
showing common gaps across the family.
```

**Specialization-Specific:**
```
I have 3 specializations within Software Engineering:
- Front-End Development
- Back-End Development
- DevOps Engineering

[Provide essential functions for each]

Please identify common technical competencies and specialization-specific ones.
```

**Validate Existing Competencies:**
```
We already have these technical competencies defined:
[Paste competency list]

Can you review them against Cargill frameworks and identify any duplications?
```

---

## Part 7: Integration with Technical Competency Agent

### Exporting GPT Output to Agent System

**Step 1: Get Coverage Report from GPT**
- Save the coverage report as PDF or Word document
- This documents your gap analysis

**Step 2: Get Technical Competencies from GPT**
- Copy the generated competencies
- Format as Excel file with columns:
  - Competency Name
  - Definition
  - Indicators (all 4 levels)
  - Proficiency Levels (number: 4)
  - Category (Technical)
  - Tags (comma-separated)
  - Source (GPT Gap Analysis)
  - Gap Coverage (which essential functions)

**Step 3: Upload to Technical Competency Agent Knowledge Base**
```bash
cd /home/user/Claude-Code/tech-competency-agent

techcomp kb add gpt_coverage_report.pdf \
  --title "GPT Gap Analysis - [Job Family]" \
  --category internal \
  --tags "gap-analysis,coverage"

techcomp kb add gpt_competencies.docx \
  --title "GPT Technical Competencies - [Job Family]" \
  --category internal \
  --tags "technical,validated"
```

**Step 4: Run Technical Competency Agent Workflow**
```bash
techcomp run \
  --jobs-file jobs.xlsx \
  --tech-sources gpt_competencies.xlsx \
  --leadership-file leadership.xlsx \
  --template-file template.xlsx
```

---

## Part 8: Troubleshooting

### Issue: GPT Creates Competencies Without Coverage Assessment

**Solution:**
1. Go back to Configure tab
2. Verify the Instructions section has the full system prompt
3. Check that it includes "MANDATORY STARTING WORKFLOW" section
4. Test again

### Issue: GPT Says Function is NOT COVERED When It Should Be

**Causes:**
- Knowledge base files may not be uploaded
- GPT may not have full framework information

**Solution:**
1. Upload Cargill Values & Behaviors document
2. Upload Common Competencies document
3. Provide more context in your prompt:
   ```
   Note: "Communication" is a Common Competency at Cargill.
   Please reassess function 4 with this in mind.
   ```

### Issue: Technical Competencies Are Too Generic

**Solution:**
Request more specificity:
```
The "Data Analysis" competency is too generic. Please make it more specific to:
- Tools: Python, pandas, scikit-learn
- Techniques: Statistical modeling, predictive analytics
- Context: Business decision-making
```

### Issue: GPT Includes Non-Technical Skills

**Solution:**
Remind the GPT:
```
"Communication Skills" is a Common Competency at Cargill. Please remove it
from the technical competency list and focus only on gaps.
```

---

## Part 9: Maintenance

### Updating Your GPT

**When to Update:**
- Cargill frameworks change
- New Values & Behaviors added
- Common Competencies revised
- User feedback indicates issues

**How to Update:**

1. Click **"Edit GPT"** (in GPT interface)
2. Go to **"Configure"** tab
3. Update relevant sections:
   - Instructions (if workflow changes)
   - Knowledge files (upload new versions)
4. Click **"Update"**
5. Test with sample jobs

---

## Part 10: Tips for Best Results

### For Users:

**Do:**
- ✅ Provide complete essential functions from JDMS
- ✅ Specify job family and specialization
- ✅ Review coverage assessment carefully before approving
- ✅ Request modifications if competencies aren't right
- ✅ Save coverage reports for documentation

**Don't:**
- ❌ Skip the coverage assessment step
- ❌ Accept technical competencies without reviewing
- ❌ Use generic job descriptions (provide specifics)
- ❌ Forget to specify tools/technologies if relevant

### For Best Quality:

**Provide Context:**
```
Job Title: Senior Data Scientist
Job Family: Data & Analytics
Specialization: Machine Learning
Key Technologies: Python, TensorFlow, AWS, Spark
Industry Context: Financial services, risk modeling

Essential Functions:
[Detailed list]
```

**Ask for Refinement:**
```
The competency is good but needs:
- More specific indicators for Level 4
- Additional focus on [specific technology]
- Behavioral indicators that are more observable
```

---

## Part 11: Success Metrics

Track these to measure GPT effectiveness:

**Quality Metrics:**
- % of coverage assessments validated by SMEs
- % of technical competencies requiring major revision
- Alignment with Cargill framework strategy

**Efficiency Metrics:**
- Time to complete gap analysis (compare to manual)
- Number of iterations needed
- User satisfaction scores

**Adoption Metrics:**
- Number of active users
- Number of job families analyzed
- Number of technical competencies generated

---

## Summary Checklist

Before launching your GPT:

- [ ] Name configured: "Cargill Technical Competency Gap Analyzer"
- [ ] Description added
- [ ] Full Instructions pasted (system prompt)
- [ ] 4 conversation starters added
- [ ] Capabilities configured (Code Interpreter checked)
- [ ] Knowledge files uploaded (Values & Behaviors, Common Competencies)
- [ ] Tested with sample job - starts with coverage assessment
- [ ] Tested refusal - won't generate without essential functions
- [ ] Visibility set appropriately for your organization
- [ ] Integration with Technical Competency Agent documented

---

## Quick Start Commands

After GPT is created:

**Test Command:**
```
Analyze this job: [paste job description]
```

**Batch Command:**
```
Analyze these 5 jobs: [upload Excel]
```

**Validation Command:**
```
Review these competencies for duplication: [paste competency list]
```

---

## Support Resources

- **Full Guide:** `CHATGPT_GPT_BUILDER_GUIDE.md`
- **Workflow Guide:** `RUN_WORKFLOW_GUIDE.md`
- **Project Summary:** `PROJECT_SUMMARY.md`
- **Technical Competency Agent:** `/home/user/Claude-Code/tech-competency-agent/`

---

**Your GPT is ready!** Start by analyzing a sample job description to verify the coverage assessment workflow works correctly.
