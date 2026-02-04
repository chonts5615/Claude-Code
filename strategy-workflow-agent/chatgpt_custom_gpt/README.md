# ChatGPT Custom GPT Export

This directory contains the configuration and instructions for deploying the Strategy Workflow Agent as a **ChatGPT Enterprise Pro Custom GPT** with GPT-5.2 Pro extended thinking.

## Overview

The Custom GPT replicates the multi-agent workflow in a conversational format, guiding users through the strategic planning process step-by-step with built-in feedback loops.

## Files Included

1. **`gpt_configuration.json`** - Custom GPT configuration (name, description, instructions)
2. **`system_instructions.md`** - Full system prompt for the Custom GPT
3. **`conversation_starters.md`** - Example conversation starters
4. **`knowledge_files/`** - Reference documents to upload as knowledge
5. **`actions_schema.json`** - Optional API actions specification

## Setup Instructions

### Step 1: Create Custom GPT

1. Go to ChatGPT Enterprise Pro
2. Navigate to "Explore GPTs" → "Create a GPT"
3. Select "Configure" tab

### Step 2: Configure Basic Settings

**Name:** Strategic Planning Workflow Agent

**Description:**
Multi-agent strategic planning system that creates comprehensive strategy documents with pillars, goals, initiatives, risk assessments, and implementation roadmaps. Includes learning feedback loops for continuous improvement.

**Instructions:** Copy the full content from `system_instructions.md`

### Step 3: Configure Capabilities

- [x] Web Browsing (for research validation)
- [x] DALL-E Image Generation (for diagrams - optional)
- [x] Code Interpreter (for data analysis and calculations)

### Step 4: Upload Knowledge Files

Upload the following reference documents:
- Strategy frameworks (if available)
- Organization competency models
- Industry benchmarks
- Previous strategy documents

### Step 5: Set Model Configuration

- **Model:** GPT-5.2 Pro
- **Extended Thinking:** Enabled (default for complex reasoning)
- **Temperature:** 0.3 (for consistency)

### Step 6: Configure Conversation Starters

Add from `conversation_starters.md`:
1. "Create a 3-year strategic plan for our organization"
2. "Analyze our current state and develop strategic pillars"
3. "Generate SMART goals for our strategic priorities"
4. "Assess risks for our strategic initiatives"

### Step 7: Test and Publish

1. Test the GPT with sample inputs
2. Adjust instructions based on output quality
3. Publish to your Enterprise workspace

## Usage Guide

### Input Types Supported

1. **Vision/Strategy Text** - Paste or describe your organization's vision
2. **Document Uploads** - Upload existing strategy documents
3. **Context Information** - Market conditions, constraints, organizational structure

### Workflow Phases

The GPT will guide users through these phases:

1. **Vision Extraction** - Capture and structure strategic vision
2. **Context Analysis** - SWOT, gap analysis, market trends
3. **Pillar Synthesis** - Define 3-5 strategic pillars
4. **Goal Generation** - Create SMART goals for each pillar
5. **Initiative Design** - Design specific initiatives
6. **Risk Assessment** - Identify and mitigate risks
7. **Resource Planning** - Allocate budget and FTE
8. **Timeline Optimization** - Create implementation roadmap
9. **Validation** - Quality checks and certification
10. **Output Generation** - Executive summary and deliverables
11. **Feedback Loop** - Capture learnings for improvement

### Example Interaction

```
User: I want to create a 3-year talent assessment strategy for our global organization.

GPT: I'll help you create a comprehensive talent assessment strategy. Let me guide you through our multi-step planning process.

**Phase 1: Vision Extraction**

Please share the following to get started:

1. **Strategic Vision**: What is your organization's overall vision and how does talent assessment support it?

2. **Current State**: What talent assessment practices exist today?

3. **Key Challenges**: What problems are you trying to solve?

4. **Stakeholders**: Who are the key decision-makers and users?

[User provides information]

GPT: Excellent. I've extracted the following vision elements:

**Vision Statement**: [Extracted]
**Mission**: [Synthesized]
**Core Values**: [Identified]

**Confidence Score**: 0.87

Now moving to **Phase 2: Context Analysis**. I'll perform a SWOT analysis based on your inputs...
```

## Feedback Loop Integration

The Custom GPT maintains a learning context that improves over conversations:

1. **Quality Tracking** - Tracks SMART scores, alignment, completeness
2. **User Feedback** - Asks for ratings and suggestions
3. **Pattern Recognition** - Identifies what works well
4. **Prompt Optimization** - Adjusts guidance based on learnings

Users can trigger feedback collection by saying:
- "Rate this output"
- "What did you learn from this session?"
- "How can this strategy be improved?"

## Customization

### For Specific Organizations

Update the system instructions to include:
- Organization-specific terminology
- Industry-specific frameworks
- Compliance requirements
- Brand guidelines

### For Specific Use Cases

Adjust the workflow phases and agents:
- Talent Assessment Strategy (like Cargill example)
- Digital Transformation Strategy
- Product Development Strategy
- M&A Integration Strategy

## Troubleshooting

### Output Quality Issues

1. Increase extended thinking depth in settings
2. Provide more context in user inputs
3. Break complex requests into phases

### Workflow Interruptions

The GPT maintains state within a conversation. If interrupted:
- Ask "Where were we in the strategic planning workflow?"
- GPT will resume from the last completed phase

### Knowledge Gaps

If the GPT lacks domain knowledge:
- Upload relevant documents to knowledge base
- Provide context in the conversation
- Enable web browsing for research

## Support

For issues with the Custom GPT configuration:
- Review ChatGPT Enterprise documentation
- Check knowledge file formatting
- Test with simplified inputs first
