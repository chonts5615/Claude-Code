# Quick Start Guide

Get up and running with the Technical Competency Extraction Agent System in 5 minutes.

## Prerequisites

- Python 3.11+
- Anthropic API key
- Poetry or pip

## Installation

```bash
# Navigate to project directory
cd tech-competency-agent

# Install dependencies (using Poetry)
poetry install

# Or using pip
pip install -e .

# Set up environment
cp .env.example .env
echo "ANTHROPIC_API_KEY=your_actual_key_here" >> .env
```

## Generate Sample Data

```bash
# Create sample input files
cd data/input
python create_sample_data.py
cd ../..
```

This creates:
- `sample_jobs.xlsx` - 3 sample job descriptions
- `sample_tech_competencies.xlsx` - 5 technical competencies
- `sample_leadership.xlsx` - 3 leadership competencies
- `sample_template.xlsx` - Output template

## Initialize Configuration

```bash
# Generate default config files
techcomp init-config

# Optional: Customize thresholds and settings
# Edit config/workflow_config.yaml
# Edit config/thresholds.yaml
```

## Run Your First Workflow

### Option 1: With File Analysis (Recommended)

```bash
techcomp run \
  --jobs-file data/input/sample_jobs.xlsx \
  --tech-sources data/input/sample_tech_competencies.xlsx \
  --leadership-file data/input/sample_leadership.xlsx \
  --template-file data/input/sample_template.xlsx
```

This will:
1. ✅ Analyze files and show structure
2. ✅ Confirm low-confidence detections with you
3. ✅ Run 9-step workflow
4. ✅ Generate output artifacts

### Option 2: Skip File Analysis

```bash
techcomp run --skip-analysis \
  --jobs-file data/input/sample_jobs.xlsx \
  --tech-sources data/input/sample_tech_competencies.xlsx \
  --leadership-file data/input/sample_leadership.xlsx \
  --template-file data/input/sample_template.xlsx
```

## View Results

```bash
# Inspect workflow state
techcomp inspect data/output/run_*/final_state.json

# View generated artifacts
ls -la data/output/run_*/
```

Output artifacts:
- `s1_jobs_extracted.json` - Extracted jobs
- `s2_competency_map_v1.json` - Responsibility → competency mappings
- `s3_normalized_v2.json` - Normalized competencies
- `s4_overlap_audit_v1.json` - Overlap audit results
- `s5_clean_v3.json` - Remediated competencies
- `s6_benchmarked_v4.json` - Benchmarked competencies
- `s7_ranked_top8_v5.json` - Ranked top competencies
- `s8_populated_template.xlsx` - Final output template
- `final_state.json` - Complete workflow state

## Analyze Your Own Files

### Step 1: Analyze File Structure

```bash
# Analyze your files first
techcomp analyze-files \
  path/to/your/jobs.xlsx \
  path/to/your/competencies.xlsx
```

Review the output to verify:
- ✓ File purpose detected correctly
- ✓ Columns mapped appropriately
- ✓ Sample data looks correct
- ✓ Confidence scores are high (>70%)

### Step 2: Run Workflow

```bash
techcomp run \
  --jobs-file path/to/your/jobs.xlsx \
  --tech-sources path/to/your/competencies.xlsx \
  --leadership-file path/to/your/leadership.xlsx \
  --template-file path/to/your/template.xlsx
```

## Add Knowledge Base Documents

Enhance benchmarking with reference documents:

```bash
# Add framework documents
techcomp kb add path/to/sfia_framework.pdf \
  --title "SFIA Framework v8" \
  --category framework \
  --tags "IT,skills,framework"

# Add standards
techcomp kb add path/to/iso_standard.pdf \
  --title "ISO 9001 Quality Standard" \
  --category standard \
  --tags "quality,ISO"

# Verify
techcomp kb stats

# Test search
techcomp kb search "data analysis"
```

The workflow will automatically use KB documents during Step 6 (Benchmarking).

## Common Commands

```bash
# Analyze files
techcomp analyze-files file1.xlsx file2.xlsx

# Run workflow
techcomp run --jobs-file jobs.xlsx --tech-sources comps.xlsx ...

# Inspect results
techcomp inspect data/output/run_XXX/final_state.json

# Knowledge base
techcomp kb add document.pdf
techcomp kb list
techcomp kb search "query"
techcomp kb stats

# Generate configs
techcomp init-config
```

## Troubleshooting

### Issue: Import errors

**Solution**: Ensure all dependencies installed
```bash
poetry install
# or
pip install -e .
```

### Issue: Anthropic API key not found

**Solution**: Set environment variable
```bash
export ANTHROPIC_API_KEY=your_key_here
# or add to .env file
```

### Issue: File analysis shows low confidence

**Causes**:
- Column names don't match expected patterns
- File structure unusual

**Solutions**:
- Check sample data in analysis output
- Verify columns contain expected data types
- Use `--skip-analysis` if confident in file structure

### Issue: No competencies mapped

**Causes**:
- Competency library doesn't match job domain
- Similarity threshold too high

**Solutions**:
- Add more relevant competencies to library
- Lower `min_relevance_threshold` in config
- Check that competency definitions are detailed

### Issue: Many overlap warnings

**Causes**:
- Technical competencies too similar to leadership
- Competency definitions too broad

**Solutions**:
- Review flagged competencies
- Make technical competencies more specific
- Add technical tools/methods to differentiate

## Next Steps

1. **Review Output Quality**
   - Check `final_state.json` for warnings/errors
   - Review ranked competencies in template
   - Validate coverage metrics

2. **Customize Configuration**
   - Adjust thresholds in `config/thresholds.yaml`
   - Modify ranking weights in `config/workflow_config.yaml`
   - Customize competency format in `config/competency_format.yaml`

3. **Build Knowledge Base**
   - Add industry frameworks (SFIA, O*NET, NICE)
   - Include organization-specific standards
   - Upload research papers and guides

4. **Production Use**
   - Process full job catalog
   - Validate with SMEs
   - Integrate into HRIS/TMS

## Getting Help

- Documentation: `docs/` directory
- Knowledge Base Guide: `docs/knowledge_base_guide.md`
- Validation Rules: `docs/validation_rules/quality_gates.md`
- Scoring Rubrics: `docs/scoring_rubrics/criticality_scoring.md`

## Example Workflow Output

```
=== Analyzing Input Files ===

File: sample_jobs.xlsx
  Type: excel
  Rows: 3
  Columns: 5
  Suggested purpose: JOBS_FILE ✓
  Confidence: 90.0%

=== Workflow Summary ===
Run ID: run_20250117_143022_a1b2c3d4
Jobs processed: 3
Competencies identified: 15
Flags: 2 (INFO)

Review package: data/output/run_20250117_143022_a1b2c3d4_final_review.xlsx
```

You're ready to extract competencies! 🚀
