# Technical Competency Extraction Agent System

IO Psychology-grade multi-agent system for extracting validated technical competencies from job descriptions.

## Overview

This system uses a multi-agent architecture orchestrated by LangGraph to convert job descriptions into validated, benchmarked technical competencies with full traceability and governance controls.

### Key Features

- **Schema-first architecture**: Pydantic models ensure data integrity throughout the pipeline
- **Full traceability**: Every competency traces back to source responsibilities with evidence
- **Research-grade rigor**: Follows IO psychology validation standards
- **Governance controls**: Configurable quality gates and thresholds
- **Audit trail**: Complete before/after snapshots of all changes
- **Multi-source benchmarking**: Validates against O*NET, SFIA, NICE frameworks
- **🆕 Intelligent file analysis**: Automatically analyzes input files and confirms structure before processing
- **🆕 Knowledge base management**: Upload and manage reference documents for enhanced benchmarking

## New Features

### Intelligent File Analysis

The system now automatically analyzes your input files before processing:

```bash
# Analyze files to verify structure
techcomp analyze-files data/input/jobs.xlsx data/input/tech_comps.xlsx

# Run with automatic analysis (default)
techcomp run --jobs-file data/input/jobs.xlsx ...

# Skip analysis for trusted files
techcomp run --skip-analysis --jobs-file data/input/jobs.xlsx ...
```

**What it does**:
- Detects file type and structure
- Identifies column purposes
- Suggests column mappings
- Provides confidence scores
- Shows sample data
- Confirms with user before proceeding

See [File Analysis Guide](docs/file_analysis_guide.md) for details.

### Knowledge Base Management

Upload reference documents for enhanced competency benchmarking:

```bash
# Add documents to knowledge base
techcomp kb add frameworks/sfia_v8.pdf \
  --title "SFIA Framework v8" \
  --category framework \
  --tags "IT,skills"

# List documents
techcomp kb list

# Search documents
techcomp kb search "data analysis"

# View statistics
techcomp kb stats
```

**Supported documents**:
- PDF files (frameworks, standards, research papers)
- Word documents (.docx, .doc)
- Excel/CSV files (competency libraries)
- Text files

The benchmark researcher (Step 6) automatically searches your knowledge base to validate competencies against your uploaded documents.

See [Knowledge Base Guide](docs/knowledge_base_guide.md) for details.

## Quick Start

### Automated Installation (Recommended)

```bash
# One-command installation
./install.sh

# This will:
# - Check Python version (3.11+ required)
# - Install all dependencies
# - Set up environment
# - Generate configuration files
# - Create sample data
# - Verify installation
```

### Manual Installation

```bash
# Clone repository
git clone <repo-url>
cd tech-competency-agent

# Install dependencies (using Poetry)
poetry install

# Or using pip
pip install -e .

# Verify installation
python verify_setup.py

# Generate sample data
python data/input/create_sample_data.py
```

### 2. Configuration

```bash
# Generate default config files
techcomp init-config

# Edit thresholds and settings
vim config/thresholds.yaml
vim config/workflow_config.yaml
```

### 3. Set up environment

```bash
cp .env.example .env
# Add your Anthropic API key
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

### 4. Test the system (Optional but Recommended)

```bash
# Run end-to-end tests
python test_e2e.py

# This tests:
# - File parsing
# - File analysis
# - Similarity engine
# - Knowledge base
# - Schema validation
# - Agent execution
```

### 5. Run workflow

```bash
techcomp run \
  --jobs-file data/input/jobs.xlsx \
  --tech-sources data/input/tech_competencies.xlsx \
  --leadership-file data/input/core_leadership.xlsx \
  --template-file data/input/template.xlsx \
  --output-dir data/output
```

### 6. Inspect results

```bash
techcomp inspect data/output/run_<timestamp>_final_state.json
```

## Testing & Verification

The system includes comprehensive testing tools:

- **`verify_setup.py`** - Automated installation verification
  ```bash
  python verify_setup.py
  ```

- **`test_e2e.py`** - End-to-end system tests
  ```bash
  python test_e2e.py
  ```

- **`install.sh`** - Automated installation script
  ```bash
  ./install.sh
  ```

## Project Structure

```
tech-competency-agent/
├── config/                      # Configuration files
│   ├── workflow_config.yaml    # Orchestrator settings
│   ├── thresholds.yaml         # Quality gate thresholds
│   ├── competency_format.yaml  # Writing standards
│   └── template_specs/         # Output template specs
├── src/
│   ├── schemas/                # Pydantic data models
│   ├── agents/                 # Individual agent modules
│   ├── orchestrator/           # LangGraph workflow
│   ├── utils/                  # Shared utilities
│   └── cli/                    # Command-line interface
├── tests/                      # Test suite
├── data/
│   ├── input/                  # User-provided files
│   ├── output/                 # Generated artifacts
│   └── reference/              # Benchmark sources
└── docs/                       # Documentation
```

## Workflow Steps

The system executes a 9-step workflow:

1. **Job Ingestion**: Extract and normalize job descriptions
2. **Competency Mapping**: Map responsibilities to candidate competencies
3. **Normalization**: Standardize competency format and content
4. **Overlap Audit**: Detect overlap with core/leadership competencies
5. **Overlap Remediation**: Fix overlap issues
6. **Benchmarking**: Validate against industry frameworks
7. **Criticality Ranking**: Rank by multi-factor criticality score
8. **Template Population**: Populate output template
9. **Packaging**: Bundle final deliverables

Each step includes quality gates that validate outputs before proceeding.

## Configuration

### Quality Thresholds

Edit `config/thresholds.yaml` to customize:

- Minimum responsibilities per job
- Overlap detection thresholds
- Coverage requirements
- Top N competency count

### Agent Settings

Edit `config/workflow_config.yaml` to customize:

- LLM model and parameters
- Similarity models
- Ranking weights
- Benchmarking sources

## Input File Formats

### Jobs File (Excel)

| Job Title | Job Family | Job Level | Summary | Responsibilities |
|-----------|-----------|-----------|---------|------------------|
| Data Scientist | Analytics | Senior | ... | • Responsibility 1<br>• Responsibility 2 |

### Technical Competencies Source (Excel)

| Competency Name | Definition | Indicators | Tags |
|-----------------|-----------|-----------|------|
| Data Analysis: Statistical Modeling | ... | • Indicator 1<br>• Indicator 2 | analysis, statistics |

## Output Artifacts

Each run generates:

- `s1_jobs_extracted.json`: Normalized job structures
- `s2_competency_map_v1.json`: Responsibility-competency mappings
- `s3_normalized_v2.json`: Normalized competencies
- `s4_overlap_audit_v1.json`: Overlap audit results
- `s5_clean_v3.json`: Remediated competencies
- `s6_benchmarked_v4.json`: Benchmarked competencies
- `s7_ranked_top8_v5.json`: Ranked top competencies
- `s8_populated_template.xlsx`: Final output template
- `final_state.json`: Complete workflow state

## Development

### Run tests

```bash
pytest
```

### Type checking

```bash
mypy src/
```

### Format code

```bash
black src/ tests/
```

### Lint code

```bash
ruff check src/ tests/
```

## Architecture

### Schema-First Design

All data flows through strongly-typed Pydantic models:

- `RunState`: Workflow execution state
- `Job`, `Responsibility`: Job structure
- `TechnicalCompetency`: Competency structure
- `CompetencyMapping`: Mapping relationships
- `OverlapAudit`, `Ranking`: Validation outputs

### Agent Pattern

Each agent:
- Inherits from `BaseAgent`
- Implements `execute(state: RunState) -> RunState`
- Has a dedicated system prompt
- Adds flags to state for quality tracking

### Quality Gates

Quality gates validate outputs at critical points:
- Post-extraction: Job count, missing summaries
- Post-mapping: Unmapped responsibilities
- Post-remediation: Overlap resolution
- Post-ranking: Coverage threshold

## Customization

### Add New Agent

1. Create agent class in `src/agents/`
2. Inherit from `BaseAgent`
3. Implement `execute()` and `get_system_prompt()`
4. Add to orchestrator graph in `src/orchestrator/graph.py`

### Add Quality Gate

1. Add validation method to `QualityGate` class
2. Call from gate node in orchestrator
3. Configure thresholds in `config/thresholds.yaml`

### Add Benchmark Source

1. Update `config/workflow_config.yaml` sources list
2. Implement fetcher in `BenchmarkResearchAgent`
3. Map source format to `SourceEvidence` schema

## Troubleshooting

### Issue: Jobs not extracted

- Check Excel file format matches expected columns
- Review `extraction_warnings` in output
- Verify file path is correct

### Issue: High unmapped responsibility rate

- Lower `min_relevance_threshold` in config
- Add more competency sources
- Review responsibility text quality

### Issue: Material overlap detected

- Review overlap audit output
- Adjust `material_threshold` in config
- Manually review flagged competencies

## License

[Add license information]

## Contributing

[Add contribution guidelines]

## Support

For issues or questions:
- GitHub Issues: [repo-url]/issues
- Documentation: `docs/` directory
- Email: [support email]
