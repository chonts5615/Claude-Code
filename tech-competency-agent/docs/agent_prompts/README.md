# Agent System Prompts

This directory contains detailed system prompts for each agent in the workflow.

Each agent has specific expertise and follows defined standards for its task.

## Agent Prompt Organization

- `job_ingestion_prompt.md`: Step 1 - Job extraction and normalization
- `competency_mapping_prompt.md`: Step 2 - Responsibility-competency mapping
- `normalizer_prompt.md`: Step 3 - Competency normalization
- `overlap_auditor_prompt.md`: Step 4 - Overlap detection
- `overlap_remediator_prompt.md`: Step 5 - Overlap remediation
- `benchmark_researcher_prompt.md`: Step 6 - Industry benchmarking
- `criticality_ranker_prompt.md`: Step 7 - Criticality ranking
- `template_populator_prompt.md`: Step 8 - Template population

## Prompt Design Principles

1. **Role definition**: Clear expertise and authority
2. **Task specification**: Explicit inputs and outputs
3. **Quality standards**: Measurable success criteria
4. **Process steps**: Ordered workflow
5. **Examples**: Concrete illustrations
6. **Edge cases**: How to handle exceptions

## Customization

To customize agent behavior:

1. Edit the system prompt in the agent's `get_system_prompt()` method
2. Update corresponding documentation in this directory
3. Test with sample data to verify behavior
4. Document changes in agent changelog
