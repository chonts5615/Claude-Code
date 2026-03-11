# Knowledge Base Management Guide

The knowledge base allows you to upload and manage reference documents that the system uses for competency benchmarking.

## Overview

The knowledge base stores reference documents such as:
- Industry competency frameworks (SFIA, O*NET, NICE)
- Professional standards (ISO, IEEE, NIST)
- Organization-specific competency libraries
- Academic research papers
- Best practice guides

These documents are automatically chunked, indexed, and searchable for competency validation.

## Getting Started

### Initialize Knowledge Base

The knowledge base is created automatically in `data/knowledge_base/` when you add your first document.

### Add Documents

```bash
techcomp kb add path/to/document.pdf \
  --title "SFIA Framework v8" \
  --category framework \
  --tags "IT,skills,framework" \
  --description "Skills Framework for the Information Age version 8"
```

Interactive mode (prompts for title):
```bash
techcomp kb add path/to/document.pdf
```

#### Supported File Types

- **PDF** (.pdf) - Extracted page by page
- **Word** (.docx, .doc) - Full text extraction
- **Excel** (.xlsx, .xls, .csv) - Tabular data as text
- **Text** (.txt) - Plain text

### List Documents

```bash
# List all documents
techcomp kb list

# Filter by category
techcomp kb list --category framework

# Filter by tags
techcomp kb list --tags "IT,skills"
```

Output example:
```
=== Knowledge Base Documents (3) ===

ID: DOC_20250117_143022_a1b2c3d4
  Title: SFIA Framework v8
  Category: framework
  File: DOC_20250117_143022_a1b2c3d4.pdf
  Tags: IT, skills, framework
  Words: 45,231
  Uploaded: 2025-01-17T14:30:22
  Description: Skills Framework for the Information Age version 8

...
```

### Search Documents

```bash
# Basic search
techcomp kb search "data analysis"

# Filter by category
techcomp kb search "security" --category standard

# Filter by tags
techcomp kb search "python" --tags programming

# Return more results
techcomp kb search "machine learning" --top-k 10
```

Output example:
```
=== Search Results for: 'data analysis' ===

1. SFIA Framework v8
   Document: DOC_20250117_143022_a1b2c3d4
   Category: framework
   Relevance: 15
   Page: 42
   Content preview:
   Data analysis involves examining, cleaning, transforming, and modeling data
   to discover useful information, inform conclusions, and support decision-making...

2. O*NET Database - Data Scientists
   Document: DOC_20250117_145533_e5f6g7h8
   Category: reference
   Relevance: 12
   Content preview:
   Analyze data using statistical techniques to identify trends, patterns, and
   relationships that inform business strategy...
```

### Remove Documents

```bash
techcomp kb remove DOC_20250117_143022_a1b2c3d4
```

You'll be prompted for confirmation:
```
Are you sure you want to remove this document? [y/N]:
```

### View Statistics

```bash
techcomp kb stats
```

Output:
```
=== Knowledge Base Statistics ===

Total documents: 5
Total chunks: 247
Total words: 123,456

Documents by category:
  framework: 2
  standard: 1
  reference: 2

Available categories: framework, standard, reference
```

## Document Categories

### framework
Competency frameworks and skill taxonomies
- Examples: SFIA, O*NET, NICE, CompTIA
- Use for: Defining competency standards

### standard
Professional standards and certifications
- Examples: ISO standards, IEEE standards, NIST guidelines
- Use for: Compliance and best practices

### reference
General reference materials
- Examples: Research papers, case studies, guides
- Use for: Additional context and evidence

### general
Uncategorized documents
- Default category
- Use for: Miscellaneous documents

## How It Works

### Document Processing

1. **Upload**: File is copied to knowledge base
2. **Extraction**: Text is extracted from document
3. **Chunking**: Text is split into overlapping chunks (~1000 chars)
4. **Indexing**: Chunks are indexed for search
5. **Storage**: Metadata and chunks saved to JSON

### Search Process

1. **Query**: User searches with keywords
2. **Filtering**: Apply category/tag filters
3. **Matching**: Simple keyword matching (future: semantic search)
4. **Ranking**: Results ranked by relevance score
5. **Return**: Top K results with context

### Integration with Workflow

During benchmarking (Step 6), the system:
1. Searches knowledge base for each competency
2. Retrieves relevant chunks
3. Uses chunks as evidence for validation
4. Documents sources in benchmark records

## Best Practices

### Document Selection

✓ **Upload**:
- Official framework documentation
- Industry standards
- Validated competency models
- Authoritative sources

✗ **Avoid**:
- Outdated documents
- Unverified sources
- Duplicate content
- Internal-only documents (unless appropriate)

### Tagging Strategy

Use consistent, hierarchical tags:

```bash
# Good tagging
--tags "IT,software,python,programming"
--tags "healthcare,nursing,clinical"
--tags "finance,accounting,GAAP"

# Poor tagging
--tags "stuff,misc,document"
```

### Organization

Group related documents:

```bash
# Framework documents
techcomp kb add sfia_v8.pdf --category framework --tags "IT,skills"
techcomp kb add onet_database.xlsx --category framework --tags "occupational,skills"

# Standards
techcomp kb add iso_9001.pdf --category standard --tags "quality,ISO"
techcomp kb add nist_cybersecurity.pdf --category standard --tags "security,NIST"
```

## Advanced Usage

### Batch Upload

```bash
# Upload multiple documents
for file in frameworks/*.pdf; do
  techcomp kb add "$file" \
    --category framework \
    --tags "competency,framework"
done
```

### Custom Knowledge Base Location

```bash
# Use different KB directory
techcomp kb add document.pdf --kb-path /custom/path/kb
techcomp kb list --kb-path /custom/path/kb
```

## Troubleshooting

### Issue: Document not found in searches

**Possible causes**:
- Search terms don't match document content
- Document in wrong category
- Text extraction failed

**Solutions**:
- Try broader search terms
- Check document category with `kb list`
- Verify document content readable

### Issue: Duplicate documents

**Prevention**:
- System checks file hash before upload
- Duplicate files automatically detected
- Returns existing document ID

### Issue: Low relevance scores

**Causes**:
- Keywords not in document
- Document poorly matched to query

**Solutions**:
- Refine search query
- Add more specific documents
- Check document tags

## Example Workflows

### Setup Framework Library

```bash
# 1. Download frameworks
# (download SFIA, O*NET, NICE frameworks)

# 2. Add to KB
techcomp kb add sfia_v8.pdf \
  --title "SFIA Framework v8" \
  --category framework \
  --tags "IT,skills,framework"

techcomp kb add onet_data_scientists.xlsx \
  --title "O*NET Data Scientists" \
  --category reference \
  --tags "data,science,occupational"

techcomp kb add nice_framework.pdf \
  --title "NICE Cybersecurity Framework" \
  --category framework \
  --tags "cybersecurity,NICE"

# 3. Verify
techcomp kb stats

# 4. Test search
techcomp kb search "data analysis"
```

### Maintain Knowledge Base

```bash
# Regular maintenance
techcomp kb stats  # Check size
techcomp kb list  # Review documents
techcomp kb search "outdated_term"  # Find old docs
techcomp kb remove DOC_xxx  # Remove outdated

# Update document (remove + re-add)
techcomp kb remove DOC_old_version
techcomp kb add new_version.pdf --title "Updated Framework"
```

## Integration Example

During workflow execution:

```bash
# 1. Add benchmarking documents
techcomp kb add frameworks/*.pdf --category framework

# 2. Run workflow (automatically uses KB)
techcomp run \
  --jobs-file jobs.xlsx \
  --tech-sources tech_comps.xlsx \
  --leadership-file leadership.xlsx \
  --template-file template.xlsx

# 3. Check logs for KB usage
grep "KB_AVAILABLE" data/output/run_*/final_state.json
```

The workflow will automatically search the knowledge base during Step 6 (Benchmarking) and include evidence from your uploaded documents.
