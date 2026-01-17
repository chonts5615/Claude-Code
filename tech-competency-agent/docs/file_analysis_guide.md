# File Analysis Guide

The system includes intelligent file analysis capabilities that inspect your input files and suggest their purpose and structure before running the workflow.

## Features

### Automatic File Analysis

When you run the workflow, the system automatically analyzes each input file and:
- Detects file type (Excel, CSV, etc.)
- Identifies column structure and purposes
- Suggests file role (jobs file, competency library, etc.)
- Provides confidence score
- Shows sample data from each column

### Confidence Scoring

The analyzer assigns a confidence score (0.0-1.0) based on:
- Number of matching columns for expected purpose
- Column name patterns
- Data type consistency
- Sample content analysis

**Confidence Levels**:
- ≥ 0.7: High confidence (✓)
- 0.4-0.7: Medium confidence (?)
- < 0.4: Low confidence (?)

## Using File Analysis

### Interactive Analysis During Workflow

By default, the `run` command analyzes files before execution:

```bash
techcomp run \
  --jobs-file data/input/jobs.xlsx \
  --tech-sources data/input/tech_comps.xlsx \
  --leadership-file data/input/leadership.xlsx \
  --template-file data/input/template.xlsx
```

Output example:
```
=== Analyzing Input Files ===

File: jobs.xlsx
  Type: excel
  Sheets: Jobs
  Active sheet: Jobs
  Rows: 45
  Columns: 5
  Suggested purpose: JOBS_FILE ✓
  Confidence: 85.0%

  Column details:
    • Job Title
      - Type: short_text
      - Purpose: job_title
      - Sample: Senior Data Scientist

    • Job Family
      - Type: short_text
      - Purpose: job_family
      - Sample: Analytics

    • Responsibilities
      - Type: long_text
      - Purpose: responsibilities
      - Sample: Develop machine learning models...

  ... more columns ...
```

If confidence is low, you'll be prompted:
```
Low confidence in file purpose. Continue with this file? [Y/n]:
```

### Skip Analysis

To skip interactive analysis:

```bash
techcomp run --skip-analysis \
  --jobs-file data/input/jobs.xlsx \
  ...
```

### Standalone File Analysis

Analyze files without running the workflow:

```bash
techcomp analyze-files data/input/jobs.xlsx data/input/tech_comps.xlsx
```

This displays detailed analysis including:
- File structure
- Column purposes
- Sample data
- Suggested column mappings

## Column Purpose Detection

The analyzer recognizes these column purposes:

### For Jobs Files
- `job_title` - Job title or position name
- `job_family` - Job family, department, or category
- `job_level` - Job level, grade, or tier
- `job_summary` - Job description or overview
- `responsibilities` - Duties, tasks, or responsibilities
- `identifier` - Job ID or code

### For Competency Files
- `competency_name` - Competency or skill name
- `competency_definition` - Definition or description
- `behavioral_indicators` - Observable behaviors
- `tags` - Categories or tags

### Generic
- `text_content` - Long text content
- `general_data` - General data field

## Column Mapping Suggestions

After analyzing a file, the system suggests column mappings:

```
Suggested column mapping for JOBS:
  Job Title ← Position Name
  Job Family ← Department
  Job Level ← Grade
  Summary ← Description
  Responsibilities ← Key Duties
```

These mappings show how source columns map to expected fields.

## File Type Detection

Supported file types:
- **Excel** (.xlsx, .xls) - Analyzes all sheets, focuses on active sheet
- **CSV** (.csv) - Analyzes structure and content
- **Future**: Word (.docx), PDF (.pdf)

## Best Practices

1. **Use descriptive column names**: Names like "Job Title", "Responsibilities" are easier to detect than "Col1", "Col2"

2. **Keep headers in first row**: The analyzer assumes row 1 contains column headers

3. **Use consistent data types**: Keep data types consistent within columns (don't mix text and numbers)

4. **Review low-confidence results**: If confidence < 0.7, manually verify the file structure

5. **Check sample data**: Sample values help verify the analyzer detected the right purpose

## Troubleshooting

### Issue: Wrong file purpose detected

**Solution**: Check that:
- Column names match expected patterns
- Data is in the correct format
- First row contains headers, not data

### Issue: Columns not detected

**Solution**:
- Ensure columns have headers in row 1
- Remove merged cells in header row
- Use text headers (not formulas)

### Issue: Low confidence score

**Causes**:
- Generic column names ("Column1", "Field A")
- Mixed data types in columns
- Sparse data (many empty cells)
- Non-standard structure

**Solution**: Use the suggested mappings and proceed with caution, or restructure the file with clearer column names.

## Example Workflows

### Analyze Before Running

```bash
# 1. Analyze files first
techcomp analyze-files data/input/*.xlsx

# 2. Review analysis output

# 3. Run workflow
techcomp run --jobs-file data/input/jobs.xlsx ...
```

### Quick Run (Skip Analysis)

```bash
# For trusted/validated files
techcomp run --skip-analysis \
  --jobs-file data/input/jobs.xlsx \
  --tech-sources data/input/tech_comps.xlsx \
  --leadership-file data/input/leadership.xlsx \
  --template-file data/input/template.xlsx
```
