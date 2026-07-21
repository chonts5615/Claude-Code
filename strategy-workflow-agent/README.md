# Strategy Workflow Agent

**Multi-Agent Strategic Planning System with Learning Feedback Loops**

A sophisticated multi-step, multi-agent workflow system for creating comprehensive strategic plans. Built with LangGraph for orchestration and featuring continuous improvement through integrated feedback loops.

## Overview

This system implements a 12-agent workflow that transforms strategic inputs into validated, actionable strategic plans with full traceability and quality assurance.

### Key Features

- **Multi-Agent Architecture**: 12 specialized agents handling different aspects of strategic planning
- **Learning Feedback Loop**: Continuous improvement through feedback collection and optimization
- **Quality Gates**: Validation checkpoints ensuring output quality at each phase
- **Schema-First Design**: Pydantic models ensuring data integrity throughout the pipeline
- **Dual Platform Support**: Runs on Claude (Anthropic) and exports to ChatGPT Enterprise Pro (GPT-5.2)
- **Full Traceability**: Every output traces back to source inputs with confidence scores

## Quick Start

### Installation

```bash
# Clone repository
git clone <repo-url>
cd strategy-workflow-agent

# Install with pip
pip install -e .

# Or with poetry
poetry install
```

### Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Add your API key
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

### Run Workflow

```bash
# Basic run with vision text
strategy-workflow run --vision "Our vision is to become the global leader..."

# Run with file input
strategy-workflow run --vision-file strategy_input.txt --horizon 3

# Run with all options
strategy-workflow run \
  --vision "Our strategic vision..." \
  --goals "Key goals include..." \
  --context "Market conditions are..." \
  --horizon 3 \
  --format comprehensive \
  --output ./output \
  --feedback \
  --auto-optimize
```

### Inspect Results

```bash
# View full state
strategy-workflow inspect data/output/run_xyz_final_state.json

# View specific section
strategy-workflow inspect data/output/run_xyz_final_state.json --section strategic_pillars

# Validate quality
strategy-workflow validate data/output/run_xyz_final_state.json
```

## Architecture

### Workflow Phases

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         STRATEGY WORKFLOW                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│  │   INGESTION  │ -> │   ANALYSIS   │ -> │  SYNTHESIS   │               │
│  │              │    │              │    │              │               │
│  │ S1: Vision   │    │ S2: Context  │    │ S3: Pillars  │               │
│  │   Extractor  │    │   Analyzer   │    │ S4: Goals    │               │
│  └──────────────┘    └──────────────┘    └──────────────┘               │
│         │                   │                   │                        │
│         └─────────[G1]──────┴───────[G2,G3]─────┘                        │
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│  │   PLANNING   │ -> │ OPTIMIZATION │ -> │  VALIDATION  │               │
│  │              │    │              │    │              │               │
│  │ S5: Initiat. │    │ S8: Timeline │    │ S9: Validate │               │
│  │ S6: Risks    │    │   Optimizer  │    │              │               │
│  │ S7: Resource │    │              │    │              │               │
│  └──────────────┘    └──────────────┘    └──────────────┘               │
│         │                   │                   │                        │
│         └─────[G4,G5]───────┴───────────[G6]────┘                        │
│                                                                          │
│  ┌──────────────┐    ┌──────────────────────────────────┐               │
│  │    OUTPUT    │ -> │         FEEDBACK LOOP            │               │
│  │              │    │                                   │               │
│  │ S10: Output  │    │ F1: Feedback    F2: Learning     │               │
│  │   Generator  │    │   Processor  ->   Optimizer      │               │
│  └──────────────┘    └──────────────────────────────────┘               │
│                                                                          │
│  [G1-G6] = Quality Gates                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

### Agent Responsibilities

| Agent | ID | Phase | Purpose |
|-------|-----|-------|---------|
| Vision Extractor | S1 | Ingestion | Extract vision, mission, values from inputs |
| Context Analyzer | S2 | Analysis | SWOT, gap analysis, trend identification |
| Pillar Synthesizer | S3 | Synthesis | Create 3-5 strategic pillars |
| Goal Generator | S4 | Synthesis | Generate SMART goals for each pillar |
| Initiative Designer | S5 | Planning | Design initiatives with resources |
| Risk Assessor | S6 | Planning | Identify and mitigate strategic risks |
| Resource Planner | S7 | Planning | Allocate budget and FTE |
| Timeline Optimizer | S8 | Optimization | Sequence and optimize schedule |
| Validator | S9 | Validation | Quality scores and certification |
| Output Generator | S10 | Output | Executive deliverables |
| Feedback Processor | F1 | Feedback | Collect and analyze feedback |
| Learning Optimizer | F2 | Feedback | Apply learnings and optimize |

### Quality Gates

Quality gates validate outputs before proceeding:

- **G1 (Vision)**: Vision statement exists, confidence adequate
- **G2 (Pillars)**: 3-5 distinct pillars with rationale
- **G3 (Goals)**: SMART score ≥ 0.70, goals per pillar met
- **G4 (Initiatives)**: Feasibility ≥ 0.60, resources defined
- **G5 (Risks)**: Mitigation coverage ≥ 80%, critical risks ≤ 3
- **G6 (Validation)**: Alignment ≥ 0.75, Coherence ≥ 0.80, Completeness ≥ 0.85

## Feedback Loop

The learning feedback loop continuously improves the workflow:

```
┌─────────────────────────────────────────────────────────────────┐
│                     FEEDBACK LOOP CYCLE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐   │
│  │ Execute │ --> │ Collect │ --> │ Analyze │ --> │  Apply  │   │
│  │Workflow │     │Feedback │     │Patterns │     │Learning │   │
│  └─────────┘     └─────────┘     └─────────┘     └─────────┘   │
│       ^                                               │         │
│       └───────────────────────────────────────────────┘         │
│                                                                  │
│  Feedback Sources:                                               │
│  • Quality metrics from validation                               │
│  • User ratings and comments                                     │
│  • Execution performance data                                    │
│  • Outcome tracking (long-term)                                  │
│                                                                  │
│  Optimization Types:                                             │
│  • Threshold adjustments                                         │
│  • Prompt refinements                                            │
│  • Weight tuning                                                 │
│  • Process improvements                                          │
└─────────────────────────────────────────────────────────────────┘
```

## Configuration

### Workflow Configuration

Edit `config/workflow_config.yaml`:

```yaml
thresholds:
  goal_smart_score_min: 0.70
  initiative_feasibility_min: 0.60
  risk_mitigation_coverage: 0.80
  alignment_score_min: 0.75

feedback:
  enabled: true
  auto_optimize: true
  learning_rate: 0.1
```

### Agent Configuration

Each agent can be configured individually:

```yaml
agents:
  goal_generator:
    min_goals_per_pillar: 2
    max_goals_per_pillar: 5
    require_smart_compliance: true
```

## Output Artifacts

Each run generates:

| Artifact | Description |
|----------|-------------|
| `*_final_state.json` | Complete workflow state with all data |
| `*_executive_summary.json` | Executive summary content |
| Strategic elements | Pillars, goals, initiatives, risks, milestones |
| Quality scores | Alignment, coherence, completeness, feasibility |
| Feedback data | Insights, recommendations, optimizations |

## ChatGPT Custom GPT Export

Deploy as a ChatGPT Enterprise Pro Custom GPT:

1. Navigate to `chatgpt_custom_gpt/`
2. Follow `README.md` setup instructions
3. Use `system_instructions.md` as the GPT instructions
4. Configure for GPT-5.2 Pro with extended thinking

See [ChatGPT Export Documentation](chatgpt_custom_gpt/README.md) for details.

## Use Cases

### Talent Assessment Strategy
Perfect for IO psychology-driven talent assessment strategies (like Cargill example):
- Assessment use cases (hiring, development, succession)
- Vendor evaluation and governance
- ROI projections and metrics

### Digital Transformation
- Technology roadmaps
- Capability building
- Change management

### Market Expansion
- Geographic/product expansion
- Competitive analysis
- Resource allocation

## API Reference

### Python API

```python
from src.orchestrator import StrategyWorkflowOrchestrator, create_initial_state

# Create initial state
state = create_initial_state(
    vision_text="Our vision is...",
    time_horizon_years=3,
    enable_feedback=True
)

# Run workflow
orchestrator = StrategyWorkflowOrchestrator()
final_state = orchestrator.run(state)

# Access results
pillars = final_state.working_data["strategic_pillars"]
goals = final_state.working_data["strategic_goals"]
quality_scores = final_state.working_data["quality_scores"]
```

### CLI Reference

```bash
# Run workflow
strategy-workflow run [OPTIONS]

# Inspect state
strategy-workflow inspect STATE_FILE [OPTIONS]

# Validate quality
strategy-workflow validate STATE_FILE

# Submit feedback
strategy-workflow feedback STATE_FILE [OPTIONS]
```

## Development

### Run Tests

```bash
pytest tests/
```

### Type Checking

```bash
mypy src/
```

### Code Formatting

```bash
black src/ tests/
ruff check src/ tests/
```

## Project Structure

```
strategy-workflow-agent/
├── src/
│   ├── agents/              # 12 specialized agents
│   │   ├── base.py          # Base agent class
│   │   ├── vision_extractor.py
│   │   ├── context_analyzer.py
│   │   ├── pillar_synthesizer.py
│   │   ├── goal_generator.py
│   │   ├── initiative_designer.py
│   │   ├── risk_assessor.py
│   │   ├── resource_planner.py
│   │   ├── timeline_optimizer.py
│   │   ├── validator.py
│   │   ├── output_generator.py
│   │   ├── feedback_processor.py
│   │   └── learning_optimizer.py
│   ├── orchestrator/        # LangGraph workflow
│   │   ├── graph.py         # Workflow definition
│   │   ├── gates.py         # Quality gates
│   │   └── state.py         # State management
│   ├── schemas/             # Pydantic data models
│   │   ├── run_state.py     # Workflow state
│   │   ├── strategy.py      # Strategy elements
│   │   └── feedback.py      # Feedback loop
│   └── cli/                 # Command-line interface
├── config/                  # Configuration files
├── chatgpt_custom_gpt/      # ChatGPT export
├── data/                    # Input/output directories
├── tests/                   # Test suite
└── docs/                    # Documentation
```

## License

MIT License - see LICENSE file.

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## Support

- GitHub Issues: [repo-url]/issues
- Documentation: `docs/` directory
