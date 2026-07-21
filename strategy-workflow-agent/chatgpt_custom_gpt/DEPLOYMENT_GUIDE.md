# ChatGPT Custom GPT Deployment Guide

A step-by-step guide to deploying the Strategic Planning Workflow Agent as a ChatGPT Enterprise Pro Custom GPT.

---

## Prerequisites

- ChatGPT Enterprise Pro subscription
- Access to GPT Builder (Explore GPTs → Create)
- GPT-5.2 Pro model access with extended thinking capability

---

## Step 1: Create New Custom GPT

1. Open ChatGPT Enterprise Pro
2. Click **"Explore GPTs"** in the sidebar
3. Click **"Create"** button (top right)
4. Select **"Configure"** tab (not "Create" chat)

---

## Step 2: Basic Configuration

### Name
```
Strategic Planning Workflow Agent
```

### Description
```
Multi-agent strategic planning system that guides you through 11 phases to create comprehensive strategy documents. Includes SMART goal generation, risk assessment, resource planning, and executive deliverables. Features IO Psychology expertise for talent/HR strategies and built-in learning feedback loops.
```

### Profile Picture
Upload a professional icon representing strategy/planning (suggest: abstract network diagram or strategic compass)

---

## Step 3: Instructions

Copy the **entire contents** of `system_instructions.md` into the Instructions field.

> **Important**: The instructions are approximately 500 lines. Ensure you copy everything including:
> - Core Identity section
> - All 11 Workflow Phases
> - Quality Gate specifications
> - Talent Assessment Specialization
> - GPT-5.2 Extended Thinking Guidelines
> - Example Interaction Patterns

---

## Step 4: Conversation Starters

Add these conversation starters:

```
Create a 3-year strategic plan for my organization
```

```
Help me develop a talent assessment strategy with use cases and ROI projections
```

```
Analyze our current strategic position and define strategic pillars
```

```
Assess risks for our strategic initiatives and develop mitigation strategies
```

```
Generate an executive summary and presentation for our strategy
```

---

## Step 5: Knowledge Files (Optional but Recommended)

Upload these reference documents to enhance the GPT's knowledge:

### Recommended Files to Upload

1. **Strategy Frameworks Reference**
   - Balanced Scorecard guide
   - OKR methodology
   - Strategic planning templates

2. **IO Psychology References** (for talent strategies)
   - SIOP Principles for Validation
   - Assessment validity evidence
   - Vendor comparison guides

3. **Industry Benchmarks**
   - Strategic planning best practices
   - Implementation timelines
   - Success metrics

4. **Your Organization's Context** (if creating for internal use)
   - Company strategy documents
   - Competency frameworks
   - Previous strategic plans

### How to Upload
1. Click **"Upload files"** in the Knowledge section
2. Select files (PDF, DOCX, TXT supported)
3. Files are automatically indexed for retrieval

---

## Step 6: Capabilities Configuration

Enable these capabilities:

| Capability | Enable | Purpose |
|------------|--------|---------|
| ✅ Web Browsing | Yes | Research validation, current trends |
| ✅ DALL-E Image Generation | Optional | Generate diagrams if needed |
| ✅ Code Interpreter | Yes | Data analysis, calculations, visualizations |

---

## Step 7: Model Configuration

### Model Selection
Select: **GPT-5.2 Pro**

### Extended Thinking
Enable: **Extended Thinking (default)**

This is critical for:
- Complex SWOT analysis
- Risk scenario modeling
- Resource optimization calculations
- Quality validation logic

### Temperature Setting
If configurable, set to: **0.3** (for consistency in strategic outputs)

---

## Step 8: Actions (API Integration - Optional)

If you want to connect to external systems:

### Example: Connect to Project Management Tool

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Strategy Export API",
    "version": "1.0.0"
  },
  "paths": {
    "/export/initiatives": {
      "post": {
        "summary": "Export initiatives to project tool",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "initiatives": { "type": "array" },
                  "timeline": { "type": "object" }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

> Most deployments won't need Actions - the GPT works standalone.

---

## Step 9: Testing

Before publishing, test these scenarios:

### Test 1: Basic Strategy Flow
```
User: Create a 3-year strategic plan for a mid-size technology company
Expected: GPT initiates Phase 1, asks structured questions
```

### Test 2: Talent Assessment Context
```
User: I need a talent assessment strategy for our global HR function
Expected: GPT activates IO Psychology expertise, mentions assessment types, vendors, compliance
```

### Test 3: Quality Gates
```
User: [Provide minimal vision input]
Expected: GPT flags missing elements, asks for clarification, shows confidence scores
```

### Test 4: Command Usage
```
User: Show progress
Expected: GPT displays workflow progress tracker
```

### Test 5: Output Generation
```
User: Export executive summary
Expected: GPT generates formatted executive summary with all sections
```

---

## Step 10: Publish

### For Enterprise Internal Use
1. Click **"Save"**
2. Select **"Share with my Enterprise"**
3. Add description for internal catalog
4. Publish

### For Team/Group Use
1. Click **"Save"**
2. Select **"Only people with the link"**
3. Share link with your team
4. Publish

### Naming Convention
Consider: `[Dept] Strategic Planning Agent - v1.0`

---

## Post-Deployment

### Monitor Usage
- Track which phases are most used
- Note common user questions
- Identify quality issues

### Collect Feedback
The GPT automatically asks for ratings - review this feedback regularly.

### Update Instructions
Based on feedback:
1. Open GPT in Edit mode
2. Update Instructions
3. Re-save and publish

### Version Control
Keep copies of instructions for each version:
- `v1.0` - Initial deployment
- `v1.1` - Added talent assessment specialization
- `v1.2` - Enhanced quality gates

---

## Troubleshooting

### Issue: GPT Doesn't Follow Workflow Phases
**Solution**: Ensure Instructions include all phase definitions. GPT-5.2 Pro with extended thinking handles long instructions well.

### Issue: Quality Scores Not Showing
**Solution**: Enable Code Interpreter capability for calculations.

### Issue: Talent Assessment Expertise Not Activating
**Solution**: Check that the Talent Assessment Specialization section is in Instructions. User input must contain relevant keywords.

### Issue: Outputs Too Generic
**Solution**: Add more specific knowledge files; enable web browsing for research grounding.

### Issue: Extended Thinking Not Engaging
**Solution**: Verify model is GPT-5.2 Pro; check enterprise settings for extended thinking availability.

---

## Best Practices

1. **Start Simple**: Deploy basic version first, enhance based on feedback
2. **Test Thoroughly**: Run through complete 11-phase workflow before publishing
3. **Document Context**: If uploading knowledge files, include clear descriptions
4. **Train Users**: Share the Conversation Starters to help users get started
5. **Iterate**: Plan to update monthly based on usage patterns

---

## Support Resources

- ChatGPT Enterprise Documentation
- OpenAI GPT Builder Guide
- This repository's README for technical details

---

## Quick Reference Card

| Setting | Value |
|---------|-------|
| Model | GPT-5.2 Pro |
| Extended Thinking | Enabled |
| Temperature | 0.3 |
| Web Browsing | Enabled |
| Code Interpreter | Enabled |
| DALL-E | Optional |
| Instructions | system_instructions.md (full) |
| Starters | 5 provided |

---

*Deployment guide version 1.0 - Updated for GPT-5.2 Pro with Extended Thinking*
