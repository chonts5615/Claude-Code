# Complete Workflow Execution Guide

This guide provides step-by-step instructions for running the Technical Competency Extraction workflow with your own files.

---

## Prerequisites

Ensure you have:
- Python 3.11+
- All dependencies installed (`pip install -r requirements.txt`)
- Anthropic API key configured
- Input files ready (jobs, competencies, template)

---

## Quick Reference: Complete Workflow

```bash
# Navigate to project
cd /home/user/Claude-Code/tech-competency-agent

# Verify installation
python verify_setup.py

# Analyze your files first
techcomp analyze-files \
  /path/to/your/jobs.xlsx \
  /path/to/your/tech_competencies.xlsx \
  /path/to/your/leadership_competencies.xlsx \
  /path/to/your/template.xlsx

# Run the workflow
techcomp run \
  --jobs-file /path/to/your/jobs.xlsx \
  --tech-sources /path/to/your/tech_competencies.xlsx \
  --leadership-file /path/to/your/leadership_competencies.xlsx \
  --template-file /path/to/your/template.xlsx

# View results
techcomp inspect data/output/run_*/final_state.json
```

---

## Step-by-Step Instructions

### Step 1: Navigate to Project Directory

```bash
cd /home/user/Claude-Code/tech-competency-agent
```

### Step 2: Verify Installation

```bash
python verify_setup.py
```

**Expected Output:**
```
✓ Python version 3.11+ installed
✓ All dependencies installed
✓ Project structure valid
✓ Configuration files present
✓ CLI command available
```

If any checks fail, install dependencies:
```bash
pip install -r requirements.txt
```

### Step 3: Set API Key (if not already set)

```bash
# Option A: Export as environment variable
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Option B: Add to .env file
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> .env

# Verify it's set
echo $ANTHROPIC_API_KEY
```

### Step 4: Test with Sample Data (Optional but Recommended)

```bash
# Generate sample data
python data/input/create_sample_data.py

# Run workflow with samples
techcomp run \
  --jobs-file data/input/sample_jobs.xlsx \
  --tech-sources data/input/sample_tech_competencies.xlsx \
  --leadership-file data/input/sample_leadership.xlsx \
  --template-file data/input/sample_template.xlsx

# Check output
ls -lh data/output/run_*/
```

---

## Running with Your Own Files

### Prepare Your Files

You need **4 input files**:

1. **Jobs File** (`.xlsx` or `.csv`)
   - Must contain: Job Title, Summary/Description, Responsibilities

2. **Technical Competencies** (`.xlsx` or `.csv`)
   - Must contain: Competency Name, Definition, Indicators (optional)

3. **Leadership Competencies** (`.xlsx` or `.csv`)
   - Must contain: Competency Name, Definition, Indicators (optional)

4. **Template File** (`.xlsx`)
   - Output format you want

### Analyze Files First (CRITICAL)

Always analyze your files before running the full workflow:

```bash
techcomp analyze-files \
  /path/to/your/jobs.xlsx \
  /path/to/your/tech_competencies.xlsx \
  /path/to/your/leadership_competencies.xlsx \
  /path/to/your/template.xlsx
```

This will:
- Detect column structure automatically
- Identify any issues
- Ask for confirmation

**Example with actual paths:**
```bash
techcomp analyze-files \
  ~/Documents/jobs_catalog.xlsx \
  ~/Documents/tech_competency_library.xlsx \
  ~/Documents/leadership_competency_library.xlsx \
  ~/Documents/output_template.xlsx
```

### Run the Full Workflow

```bash
techcomp run \
  --jobs-file /path/to/your/jobs.xlsx \
  --tech-sources /path/to/your/tech_competencies.xlsx \
  --leadership-file /path/to/your/leadership_competencies.xlsx \
  --template-file /path/to/your/template.xlsx
```

**Example with actual paths:**
```bash
techcomp run \
  --jobs-file ~/Documents/jobs_catalog.xlsx \
  --tech-sources ~/Documents/tech_competency_library.xlsx \
  --leadership-file ~/Documents/leadership_competency_library.xlsx \
  --template-file ~/Documents/output_template.xlsx
```

### Advanced Options

**Custom output directory:**
```bash
techcomp run \
  --jobs-file jobs.xlsx \
  --tech-sources tech.xlsx \
  --leadership-file leadership.xlsx \
  --template-file template.xlsx \
  --output-dir /path/to/custom/output
```

**Custom run ID:**
```bash
techcomp run \
  --jobs-file jobs.xlsx \
  --tech-sources tech.xlsx \
  --leadership-file leadership.xlsx \
  --template-file template.xlsx \
  --run-id "production-run-2026-01-20"
```

**Custom configuration:**
```bash
techcomp run \
  --jobs-file jobs.xlsx \
  --tech-sources tech.xlsx \
  --leadership-file leadership.xlsx \
  --template-file template.xlsx \
  --config /path/to/custom_config.yaml
```

---

## Using Knowledge Base (Optional)

Enhance results by uploading reference documents:

### Upload Reference Documents

```bash
# Upload SFIA framework
techcomp kb add /path/to/sfia_framework.pdf \
  --title "SFIA Framework v8" \
  --category framework \
  --tags "IT,skills,framework"

# Upload internal competency guide
techcomp kb add /path/to/competency_guide.docx \
  --title "Company Competency Guide" \
  --category internal \
  --tags "competencies,internal"

# Upload industry benchmark
techcomp kb add /path/to/industry_benchmark.pdf \
  --title "Industry Skills Report 2026" \
  --category benchmark \
  --tags "industry,benchmark"
```

### Verify Uploads

```bash
# List all documents
techcomp kb list

# View statistics
techcomp kb stats

# Search knowledge base
techcomp kb search "machine learning"
```

### Complete Example with Knowledge Base

```bash
# 1. Upload reference documents
techcomp kb add sfia_v8.pdf --title "SFIA v8" --category framework
techcomp kb add internal_guide.docx --title "Internal Guide" --category internal

# 2. Verify uploads
techcomp kb stats

# 3. Run workflow (automatically uses knowledge base)
techcomp run \
  --jobs-file jobs.xlsx \
  --tech-sources tech.xlsx \
  --leadership-file leadership.xlsx \
  --template-file template.xlsx
```

---

## Viewing Results

### Output Location

Results are saved to: `data/output/run_YYYYMMDD_HHMMSS/`

### Key Output Files

```bash
# Main output - populated template
data/output/run_*/s8_populated_template.xlsx

# Complete audit trail
data/output/run_*/final_state.json

# Intermediate artifacts
data/output/run_*/s1_jobs_extracted.json          # Extracted jobs
data/output/run_*/s2_competency_map_v1.json       # Initial mappings
data/output/run_*/s3_normalized_v2.json           # Normalized competencies
data/output/run_*/s4_overlap_audit_v1.json        # Overlap analysis
data/output/run_*/s5_clean_v3.json                # After remediation
data/output/run_*/s6_benchmarked_v4.json          # After benchmarking
data/output/run_*/s7_ranked_top8_v5.json          # Final rankings
```

### View Results Commands

```bash
# Inspect complete state
techcomp inspect data/output/run_*/final_state.json

# View in spreadsheet application
libreoffice data/output/run_*/s8_populated_template.xlsx
# OR
open data/output/run_*/s8_populated_template.xlsx  # macOS
# OR
start data/output/run_*/s8_populated_template.xlsx  # Windows

# View JSON with formatting
cat data/output/run_*/s7_ranked_top8_v5.json | jq '.'

# List all outputs
ls -lh data/output/run_*/
```

### Find Latest Run

```bash
# List all runs sorted by date
ls -lt data/output/

# View latest run
LATEST_RUN=$(ls -t data/output/ | head -1)
echo "Latest run: $LATEST_RUN"
ls -lh data/output/$LATEST_RUN/

# Open latest output
libreoffice data/output/$LATEST_RUN/s8_populated_template.xlsx
```

---

## File Format Requirements

### Jobs File Format

**Required columns** (names auto-detected):
- Job Title: "Position Title", "Job Name", "Role", "Title"
- Summary: "Job Summary", "Description", "Overview", "Job Description"
- Responsibilities: "Key Responsibilities", "Duties", "Tasks", "Responsibilities"

**Example:**
```
Position Title          | Job Summary                    | Key Responsibilities
------------------------|--------------------------------|--------------------------------
Senior Data Scientist   | Leads ML projects and builds   | - Build ML pipelines
                        | predictive models              | - Analyze large datasets
                        |                                | - Deploy models to production
------------------------|--------------------------------|--------------------------------
Software Engineer       | Develops and maintains         | - Write clean, testable code
                        | software applications          | - Review code
                        |                                | - Fix bugs
```

### Competency Library Format

**Required columns**:
- Competency Name: "Name", "Competency", "Competency Name"
- Definition: "Definition", "Description", "Details"
- Indicators: "Indicators", "Behavioral Indicators", "Examples" (optional)

**Example:**
```
Competency Name         | Definition                     | Indicators
------------------------|--------------------------------|--------------------------------
Machine Learning        | Develops and deploys ML        | - Implements ML algorithms
                        | models and algorithms          | - Trains and validates models
                        |                                | - Optimizes model performance
------------------------|--------------------------------|--------------------------------
Cloud Architecture      | Designs and implements         | - Works with AWS/Azure/GCP
                        | cloud-based solutions          | - Implements IaC
                        |                                | - Ensures security
```

### Template File Format

Your desired output structure with columns like:
- Job information columns (Title, Summary, etc.)
- Competency ranking columns (Competency 1, Competency 2, ... Competency 8)
- Metadata columns (any additional fields you want)

---

## Troubleshooting

### Issue: "Command not found: techcomp"

**Solution:**
```bash
# Install in development mode
cd /home/user/Claude-Code/tech-competency-agent
pip install -e .

# Verify installation
which techcomp
techcomp --help
```

### Issue: "API key not found"

**Solution:**
```bash
# Set API key
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Or add to .env file
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> .env

# Verify
echo $ANTHROPIC_API_KEY
```

### Issue: "Column not found" during analysis

**Solution:**
The system couldn't detect required columns. Run analysis to manually map:
```bash
techcomp analyze-files your_file.xlsx
# Follow prompts to map columns
```

### Issue: "Quality gate failed"

**Solution:**
Check and adjust thresholds:
```bash
# View current thresholds
cat config/thresholds.yaml

# Edit if needed
nano config/thresholds.yaml

# Common adjustments:
# - min_confidence_score: 0.6 → 0.5
# - min_similarity_score: 0.7 → 0.6
# - min_responsibilities_per_job: 3 → 2
```

### Issue: "Low confidence mappings"

**Solution:**
Add reference documents to improve benchmarking:
```bash
techcomp kb add framework.pdf --category framework
techcomp kb add guide.docx --category internal
techcomp kb stats
```

### Issue: "Out of memory" with large files

**Solution:**
Process in batches or increase timeout:
```bash
# Increase timeout per step (in seconds)
techcomp run \
  --jobs-file large_file.xlsx \
  --tech-sources tech.xlsx \
  --leadership-file leadership.xlsx \
  --template-file template.xlsx \
  --timeout 600  # 10 minutes per step
```

### Issue: "File encoding error"

**Solution:**
Ensure files are UTF-8 encoded:
```bash
# Convert CSV to UTF-8 (if needed)
iconv -f ISO-8859-1 -t UTF-8 input.csv > input_utf8.csv

# For Excel files, re-save from Excel as .xlsx with UTF-8
```

---

## Performance Optimization

### For Large Job Catalogs (100+ jobs)

```bash
# Use increased timeout
techcomp run \
  --jobs-file large_catalog.xlsx \
  --tech-sources tech.xlsx \
  --leadership-file leadership.xlsx \
  --template-file template.xlsx \
  --timeout 900  # 15 minutes per step
```

### For Better Quality Results

1. **Upload comprehensive reference documents:**
   ```bash
   techcomp kb add framework1.pdf --category framework
   techcomp kb add framework2.pdf --category framework
   techcomp kb add benchmark.docx --category benchmark
   ```

2. **Use detailed competency definitions:**
   - Include full definitions (not just names)
   - Add behavioral indicators
   - Provide examples where possible

3. **Review configuration:**
   ```bash
   cat config/workflow_config.yaml
   cat config/thresholds.yaml
   ```

---

## Complete Example Workflows

### Example 1: Simple Workflow (No Knowledge Base)

```bash
cd /home/user/Claude-Code/tech-competency-agent
python verify_setup.py
export ANTHROPIC_API_KEY="your-key-here"

techcomp analyze-files \
  jobs.xlsx \
  tech_competencies.xlsx \
  leadership_competencies.xlsx \
  template.xlsx

techcomp run \
  --jobs-file jobs.xlsx \
  --tech-sources tech_competencies.xlsx \
  --leadership-file leadership_competencies.xlsx \
  --template-file template.xlsx

techcomp inspect data/output/run_*/final_state.json
```

### Example 2: Enhanced Workflow (With Knowledge Base)

```bash
cd /home/user/Claude-Code/tech-competency-agent
python verify_setup.py
export ANTHROPIC_API_KEY="your-key-here"

# Upload reference documents
techcomp kb add sfia_v8.pdf --title "SFIA v8" --category framework
techcomp kb add company_guide.docx --title "Company Guide" --category internal
techcomp kb stats

# Analyze files
techcomp analyze-files \
  jobs.xlsx \
  tech_competencies.xlsx \
  leadership_competencies.xlsx \
  template.xlsx

# Run workflow
techcomp run \
  --jobs-file jobs.xlsx \
  --tech-sources tech_competencies.xlsx \
  --leadership-file leadership_competencies.xlsx \
  --template-file template.xlsx

# View results
LATEST_RUN=$(ls -t data/output/ | head -1)
techcomp inspect data/output/$LATEST_RUN/final_state.json
libreoffice data/output/$LATEST_RUN/s8_populated_template.xlsx
```

### Example 3: Production Workflow (Custom Config)

```bash
cd /home/user/Claude-Code/tech-competency-agent
python verify_setup.py

# Use production API key
export ANTHROPIC_API_KEY="sk-ant-production-key"

# Upload all reference documents
techcomp kb add references/sfia_v8.pdf --title "SFIA v8" --category framework
techcomp kb add references/onet_data.xlsx --title "O*NET Data" --category benchmark
techcomp kb add references/company_framework.pptx --title "Company Framework" --category internal

# Verify knowledge base
techcomp kb stats

# Analyze files
techcomp analyze-files \
  input/production_jobs_2026.xlsx \
  input/tech_library_v3.xlsx \
  input/leadership_library_v3.xlsx \
  input/output_template_v2.xlsx

# Run with custom config
techcomp run \
  --jobs-file input/production_jobs_2026.xlsx \
  --tech-sources input/tech_library_v3.xlsx \
  --leadership-file input/leadership_library_v3.xlsx \
  --template-file input/output_template_v2.xlsx \
  --config config/production_config.yaml \
  --run-id "prod-run-$(date +%Y%m%d)" \
  --output-dir output/production

# Archive results
LATEST_RUN=$(ls -t output/production/ | head -1)
tar -czf "production_results_$(date +%Y%m%d).tar.gz" output/production/$LATEST_RUN/
```

---

## Workflow Output Explanation

### Step-by-Step Artifacts

Each workflow step produces specific outputs:

**S1: Job Extraction** → `s1_jobs_extracted.json`
- Extracted job descriptions from input file
- Parsed responsibilities and summaries

**S2: Competency Mapping** → `s2_competency_map_v1.json`
- Initial mappings between jobs and competencies
- Hybrid scoring (semantic + keyword)

**S3: Normalization** → `s3_normalized_v2.json`
- Unified competency representations
- Deduplicated similar competencies

**S4: Overlap Detection** → `s4_overlap_audit_v1.json`
- Identified overlapping competencies
- Similarity analysis

**S5: Remediation** → `s5_clean_v3.json`
- Resolved overlaps
- Final clean competency set

**S6: Benchmarking** → `s6_benchmarked_v4.json`
- Compared against knowledge base
- Confidence scoring

**S7: Ranking** → `s7_ranked_top8_v5.json`
- Top 8 competencies per job
- Priority rankings

**S8: Template Population** → `s8_populated_template.xlsx`
- **FINAL OUTPUT FILE**
- Ready for use/review

**Final State** → `final_state.json`
- Complete audit trail
- All metadata and provenance

---

## Next Steps After Workflow Completion

1. **Review Output:**
   ```bash
   libreoffice data/output/run_*/s8_populated_template.xlsx
   ```

2. **Validate Results:**
   - Check top competencies make sense for each job
   - Review confidence scores
   - Verify rankings align with expectations

3. **SME Review:**
   - Share populated template with subject matter experts
   - Gather feedback on accuracy
   - Note any needed adjustments

4. **Iterate if Needed:**
   - Adjust thresholds in `config/thresholds.yaml`
   - Add more reference documents to knowledge base
   - Refine competency library definitions
   - Re-run workflow

5. **Production Deployment:**
   - Integrate with HRIS/TMS
   - Set up automated runs
   - Establish review cadence

---

## Additional Commands

### Configuration Management

```bash
# View current configuration
cat config/workflow_config.yaml
cat config/thresholds.yaml

# Create custom config
cp config/workflow_config.yaml config/custom_config.yaml
nano config/custom_config.yaml

# Use custom config
techcomp run --config config/custom_config.yaml ...
```

### Knowledge Base Management

```bash
# List all documents
techcomp kb list

# Search for specific content
techcomp kb search "machine learning"
techcomp kb search "cloud architecture"

# View statistics
techcomp kb stats

# Add multiple documents
techcomp kb add doc1.pdf --title "Doc 1" --category framework
techcomp kb add doc2.docx --title "Doc 2" --category internal
techcomp kb add doc3.pptx --title "Doc 3" --category benchmark
```

### Utility Commands

```bash
# Initialize new configuration
techcomp init-config

# Inspect workflow state
techcomp inspect data/output/run_*/final_state.json

# View all available commands
techcomp --help

# Get help for specific command
techcomp run --help
techcomp kb --help
techcomp analyze-files --help
```

---

## Support Resources

- **Project Documentation**: `cat PROJECT_SUMMARY.md`
- **Quick Start Guide**: `cat QUICKSTART.md`
- **Knowledge Base Guide**: `cat docs/knowledge_base_guide.md`
- **Quality Gates**: `cat docs/validation_rules/quality_gates.md`
- **CLI Reference**: `techcomp --help`

---

## Summary Checklist

Before running the workflow, ensure:

- [ ] Project installed and verified (`python verify_setup.py`)
- [ ] API key configured (`export ANTHROPIC_API_KEY=...`)
- [ ] Input files prepared (jobs, tech, leadership, template)
- [ ] Files analyzed (`techcomp analyze-files ...`)
- [ ] Reference documents uploaded (optional but recommended)
- [ ] Configuration reviewed (`cat config/*.yaml`)

Run workflow:
```bash
techcomp run \
  --jobs-file jobs.xlsx \
  --tech-sources tech.xlsx \
  --leadership-file leadership.xlsx \
  --template-file template.xlsx
```

View results:
```bash
techcomp inspect data/output/run_*/final_state.json
libreoffice data/output/run_*/s8_populated_template.xlsx
```

---

**Ready to run!** Start with the sample data to test, then process your own files.
