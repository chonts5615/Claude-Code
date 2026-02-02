import click
import yaml
from pathlib import Path
from datetime import datetime
import uuid
import os

from src.schemas.run_state import RunState, RunInputs, RunConfig, ThresholdConfig
from src.orchestrator.graph import WorkflowOrchestrator
from src.utils.logger import setup_logger
from src.utils.file_analyzer import FileAnalyzer, FileAnalysis
from src.utils.knowledge_base import KnowledgeBase


@click.group()
def cli():
    """Technical Competency Extraction Agent System"""
    pass


@cli.command()
@click.option('--jobs-file', type=click.Path(exists=True), required=True,
              help='Path to Excel file containing job descriptions')
@click.option('--tech-sources', type=click.Path(exists=True), multiple=True, required=True,
              help='Path(s) to technical competency source files (can specify multiple)')
@click.option('--leadership-file', type=click.Path(exists=True), required=True,
              help='Path to core/leadership competencies Excel file')
@click.option('--template-file', type=click.Path(exists=True), required=True,
              help='Path to output template Excel file')
@click.option('--config', type=click.Path(exists=True), default='config/workflow_config.yaml',
              help='Path to workflow configuration file')
@click.option('--output-dir', type=click.Path(), default='data/output',
              help='Directory for output artifacts')
@click.option('--run-id', type=str, default=None,
              help='Custom run ID (auto-generated if not provided)')
@click.option('--skip-analysis', is_flag=True,
              help='Skip file analysis and confirmation')
def run(jobs_file, tech_sources, leadership_file, template_file, config, output_dir, run_id, skip_analysis):
    """Execute full workflow: jobs → competencies → template"""

    # Setup
    logger = setup_logger()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not run_id:
        run_id = f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

    # Analyze files first (unless skipped)
    if not skip_analysis:
        click.echo("\n=== Analyzing Input Files ===\n")
        analyzer = FileAnalyzer()

        # Analyze each file
        files_to_analyze = [
            (jobs_file, "jobs"),
            (leadership_file, "leadership"),
            *[(f, "tech_source") for f in tech_sources]
        ]

        confirmed = True
        for file_path, file_role in files_to_analyze:
            analysis = analyzer.analyze_file(Path(file_path))
            _display_file_analysis(analysis, file_role)

            # Ask for confirmation
            if analysis.confidence_score < 0.7:
                confirm = click.confirm(
                    f"\nLow confidence in file purpose. Continue with this file?",
                    default=True
                )
                if not confirm:
                    confirmed = False
                    break

        if not confirmed:
            click.echo("Workflow aborted by user.")
            return

        click.echo("\n" + "="*50 + "\n")

    logger.info(f"Starting workflow run: {run_id}")

    # Load config
    config_path = Path(config)
    if not config_path.exists():
        click.echo(f"Config file not found: {config}. Using default configuration.", err=True)
        config_data = {}
    else:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)

    # Build initial state
    inputs = RunInputs(
        jobs_file=Path(jobs_file),
        tech_comp_source_files=[Path(p) for p in tech_sources],
        core_leadership_file=Path(leadership_file),
        output_template_file=Path(template_file)
    )

    # Load thresholds from config or use defaults
    thresholds_data = config_data.get('thresholds', {})
    thresholds = ThresholdConfig(**thresholds_data) if thresholds_data else ThresholdConfig()

    run_config = RunConfig(
        thresholds=thresholds,
        top_n_competencies=config_data.get('agents', {}).get('criticality_ranker', {}).get('top_n', 8)
    )

    initial_state = RunState(
        run_id=run_id,
        inputs=inputs,
        config=run_config
    )

    # Execute workflow
    try:
        orchestrator = WorkflowOrchestrator(str(config_path))
        final_state = orchestrator.run(initial_state)

        # Save final state
        state_file = output_path / f"{run_id}_final_state.json"
        with open(state_file, 'w') as f:
            f.write(final_state.json(indent=2))

        logger.info(f"Workflow completed: {run_id}")
        logger.info(f"Final state saved to: {state_file}")

        # Print summary
        click.echo("\n=== Workflow Summary ===")
        click.echo(f"Run ID: {run_id}")
        click.echo(f"Jobs processed: {final_state.qa_summary.total_jobs_processed if final_state.qa_summary else 'N/A'}")
        click.echo(f"Flags: {len(final_state.flags)}")

        if final_state.flags:
            click.echo("\nFlags by severity:")
            from collections import Counter
            severity_counts = Counter(f.severity for f in final_state.flags)
            for severity, count in severity_counts.items():
                click.echo(f"  {severity}: {count}")

        if final_state.artifacts.final_review_package:
            click.echo(f"\nReview package: {final_state.artifacts.final_review_package}")

    except Exception as e:
        logger.error(f"Workflow failed: {str(e)}", exc_info=True)
        click.echo(f"ERROR: {str(e)}", err=True)
        raise


@cli.command()
@click.argument('state_file', type=click.Path(exists=True))
def inspect(state_file):
    """Inspect a completed workflow run state"""

    with open(state_file, 'r') as f:
        state_json = f.read()

    state = RunState.parse_raw(state_json)

    click.echo(f"\n=== Run State: {state.run_id} ===")
    click.echo(f"Timestamp: {state.run_timestamp_utc}")
    click.echo(f"Current step: {state.current_step}")
    click.echo(f"\nInputs:")
    click.echo(f"  Jobs file: {state.inputs.jobs_file}")
    click.echo(f"  Tech sources: {len(state.inputs.tech_comp_source_files)}")

    click.echo(f"\nArtifacts generated:")
    for key, value in state.artifacts.dict().items():
        if value:
            click.echo(f"  {key}: {value}")

    click.echo(f"\nFlags: {len(state.flags)}")
    if state.flags:
        for flag in state.flags[:10]:  # Show first 10
            click.echo(f"  [{flag.severity}] {flag.step_id}: {flag.message}")
        if len(state.flags) > 10:
            click.echo(f"  ... and {len(state.flags) - 10} more")


@cli.command()
@click.option('--output-dir', type=click.Path(), default='config',
              help='Directory for generated config files')
def init_config(output_dir):
    """Generate default configuration files"""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Workflow config template
    workflow_config = {
        'workflow_name': 'JobToTechnicalCompetencyAgent',
        'version': '1.0',
        'orchestration': {
            'max_retries_per_step': 2,
            'enable_parallel_processing': False,
            'checkpoint_enabled': True,
            'checkpoint_directory': './data/checkpoints'
        },
        'agents': {
            'job_ingestion': {
                'parser_type': 'openpyxl',
                'responsibility_detection_mode': 'newline_split'
            },
            'competency_mapping': {
                'similarity_model': 'sentence-transformers/all-MiniLM-L6-v2',
                'lexical_weight': 0.3,
                'semantic_weight': 0.4,
                'llm_weight': 0.3,
                'min_relevance_threshold': 0.6
            },
            'normalizer': {
                'target_definition_word_count': [50, 150],
                'min_indicators': 3,
                'max_indicators': 7
            },
            'criticality_ranker': {
                'top_n': 8,
                'factor_weights': {
                    'coverage': 0.25,
                    'impact_risk': 0.20,
                    'frequency': 0.15,
                    'complexity': 0.15,
                    'differentiation': 0.15,
                    'time_to_proficiency': 0.10
                }
            }
        },
        'llm': {
            'provider': 'anthropic',
            'model': 'claude-sonnet-4-20250514',
            'temperature': 0.3,
            'max_tokens': 4000
        },
        'logging': {
            'level': 'INFO',
            'structured': True,
            'output_file': './data/output/workflow.log'
        }
    }

    # Thresholds config
    thresholds_config = {
        'job_extraction': {
            'min_responsibilities_per_job': 5,
            'max_missing_summary_rate': 0.10
        },
        'competency_mapping': {
            'max_unmapped_responsibility_rate': 0.05,
            'min_candidates_per_responsibility': 1
        },
        'overlap': {
            'material_threshold': 0.82,
            'minor_threshold': 0.72,
            'distinctness_duplicate': 0.88
        },
        'ranking': {
            'top_n_competencies': 8,
            'min_responsibility_coverage': 0.80,
            'min_competencies_per_job': 6,
            'max_competencies_per_job': 10
        }
    }

    # Write config files
    workflow_file = output_path / 'workflow_config.yaml'
    if not workflow_file.exists():
        with open(workflow_file, 'w') as f:
            yaml.dump(workflow_config, f, default_flow_style=False, sort_keys=False)
        click.echo(f"Created: {workflow_file}")
    else:
        click.echo(f"Skipped (exists): {workflow_file}")

    thresholds_file = output_path / 'thresholds.yaml'
    if not thresholds_file.exists():
        with open(thresholds_file, 'w') as f:
            yaml.dump(thresholds_config, f, default_flow_style=False, sort_keys=False)
        click.echo(f"Created: {thresholds_file}")
    else:
        click.echo(f"Skipped (exists): {thresholds_file}")

    click.echo("\nConfiguration files generated successfully!")
    click.echo("Next steps:")
    click.echo("1. Review and customize the configuration files")
    click.echo("2. Set up .env file with ANTHROPIC_API_KEY")
    click.echo("3. Run the workflow with: techcomp run --help")


@cli.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True), required=True)
def analyze_files(files):
    """Analyze input files and suggest their purpose and structure"""

    analyzer = FileAnalyzer()

    click.echo("\n=== File Analysis Report ===\n")

    for file_path in files:
        analysis = analyzer.analyze_file(Path(file_path))
        _display_file_analysis(analysis, "unknown")

        # Show suggested mapping
        if analysis.suggested_file_purpose in ["JOBS_FILE", "POSSIBLY_JOBS_FILE"]:
            mapping = analyzer.suggest_column_mapping(analysis, "jobs")
            if mapping:
                click.echo("\n  Suggested column mapping for JOBS:")
                for target, source in mapping.items():
                    click.echo(f"    {target} ← {source}")

        elif analysis.suggested_file_purpose in ["COMPETENCY_LIBRARY", "POSSIBLY_COMPETENCY_LIBRARY"]:
            mapping = analyzer.suggest_column_mapping(analysis, "competencies")
            if mapping:
                click.echo("\n  Suggested column mapping for COMPETENCIES:")
                for target, source in mapping.items():
                    click.echo(f"    {target} ← {source}")

        click.echo("\n" + "-"*60 + "\n")


# Knowledge Base Commands
@cli.group()
def kb():
    """Manage knowledge base documents for benchmarking"""
    pass


@kb.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--title', prompt=True, help='Document title')
@click.option('--category', default='general',
              type=click.Choice(['framework', 'standard', 'reference', 'general']),
              help='Document category')
@click.option('--tags', help='Comma-separated tags')
@click.option('--description', help='Document description')
@click.option('--kb-path', default='data/knowledge_base', help='Knowledge base directory')
def add(file, title, category, tags, description, kb_path):
    """Add a document to the knowledge base"""

    kb_manager = KnowledgeBase(Path(kb_path))

    tag_list = [t.strip() for t in tags.split(',')] if tags else []

    click.echo(f"Adding document: {file}")

    try:
        doc_id = kb_manager.add_document(
            file_path=Path(file),
            title=title,
            category=category,
            tags=tag_list,
            description=description
        )

        click.echo(f"✓ Document added successfully!")
        click.echo(f"  Document ID: {doc_id}")
        click.echo(f"  Category: {category}")
        if tag_list:
            click.echo(f"  Tags: {', '.join(tag_list)}")

    except Exception as e:
        click.echo(f"✗ Error adding document: {str(e)}", err=True)


@kb.command()
@click.option('--category', help='Filter by category')
@click.option('--tags', help='Filter by tags (comma-separated)')
@click.option('--kb-path', default='data/knowledge_base', help='Knowledge base directory')
def list(category, tags, kb_path):
    """List documents in the knowledge base"""

    kb_manager = KnowledgeBase(Path(kb_path))

    tag_list = [t.strip() for t in tags.split(',')] if tags else None

    docs = kb_manager.list_documents(category=category, tags=tag_list)

    if not docs:
        click.echo("No documents found.")
        return

    click.echo(f"\n=== Knowledge Base Documents ({len(docs)}) ===\n")

    for doc in docs:
        click.echo(f"ID: {doc.doc_id}")
        click.echo(f"  Title: {doc.title}")
        click.echo(f"  Category: {doc.category}")
        click.echo(f"  File: {doc.file_path.name}")
        if doc.tags:
            click.echo(f"  Tags: {', '.join(doc.tags)}")
        if doc.word_count:
            click.echo(f"  Words: {doc.word_count:,}")
        click.echo(f"  Uploaded: {doc.upload_timestamp}")
        if doc.description:
            click.echo(f"  Description: {doc.description}")
        click.echo()


@kb.command()
@click.argument('query')
@click.option('--category', help='Filter by category')
@click.option('--tags', help='Filter by tags (comma-separated)')
@click.option('--top-k', default=5, help='Number of results to return')
@click.option('--kb-path', default='data/knowledge_base', help='Knowledge base directory')
def search(query, category, tags, top_k, kb_path):
    """Search knowledge base documents"""

    kb_manager = KnowledgeBase(Path(kb_path))

    tag_list = [t.strip() for t in tags.split(',')] if tags else None

    results = kb_manager.search_documents(
        query=query,
        category=category,
        tags=tag_list,
        top_k=top_k
    )

    if not results:
        click.echo("No results found.")
        return

    click.echo(f"\n=== Search Results for: '{query}' ===\n")

    for i, result in enumerate(results, 1):
        click.echo(f"{i}. {result['doc_title']}")
        click.echo(f"   Document: {result['doc_id']}")
        click.echo(f"   Category: {result['category']}")
        click.echo(f"   Relevance: {result['relevance_score']}")
        if result['page_number']:
            click.echo(f"   Page: {result['page_number']}")
        click.echo(f"   Content preview:")
        preview = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
        click.echo(f"   {preview}\n")


@kb.command()
@click.argument('doc_id')
@click.option('--kb-path', default='data/knowledge_base', help='Knowledge base directory')
@click.confirmation_option(prompt='Are you sure you want to remove this document?')
def remove(doc_id, kb_path):
    """Remove a document from the knowledge base"""

    kb_manager = KnowledgeBase(Path(kb_path))

    if kb_manager.remove_document(doc_id):
        click.echo(f"✓ Document {doc_id} removed successfully.")
    else:
        click.echo(f"✗ Document {doc_id} not found.", err=True)


@kb.command()
@click.option('--kb-path', default='data/knowledge_base', help='Knowledge base directory')
def stats(kb_path):
    """Show knowledge base statistics"""

    kb_manager = KnowledgeBase(Path(kb_path))
    stats = kb_manager.get_statistics()

    click.echo("\n=== Knowledge Base Statistics ===\n")
    click.echo(f"Total documents: {stats['total_documents']}")
    click.echo(f"Total chunks: {stats['total_chunks']}")
    click.echo(f"Total words: {stats['total_words']:,}")

    if stats['documents_by_category']:
        click.echo("\nDocuments by category:")
        for cat, count in stats['documents_by_category'].items():
            click.echo(f"  {cat}: {count}")

    if stats['categories']:
        click.echo(f"\nAvailable categories: {', '.join(stats['categories'])}")


def _display_file_analysis(analysis: FileAnalysis, expected_role: str):
    """Display file analysis results."""
    click.echo(f"File: {analysis.file_path.name}")
    click.echo(f"  Type: {analysis.file_type}")

    if analysis.sheet_names:
        click.echo(f"  Sheets: {', '.join(analysis.sheet_names)}")
        click.echo(f"  Active sheet: {analysis.active_sheet}")

    click.echo(f"  Rows: {analysis.row_count}")
    click.echo(f"  Columns: {analysis.column_count}")

    if analysis.suggested_file_purpose:
        confidence_indicator = "✓" if analysis.confidence_score >= 0.7 else "?"
        click.echo(f"  Suggested purpose: {analysis.suggested_file_purpose} {confidence_indicator}")
        click.echo(f"  Confidence: {analysis.confidence_score:.1%}")

    if analysis.columns:
        click.echo(f"\n  Column details:")
        for col in analysis.columns[:10]:  # Show first 10 columns
            click.echo(f"    • {col.name}")
            click.echo(f"      - Type: {col.data_type}")
            click.echo(f"      - Purpose: {col.suggested_purpose}")
            click.echo(f"      - Non-null: {col.non_null_count}/{col.total_rows}")
            if col.sample_values:
                sample = col.sample_values[0]
                if len(sample) > 50:
                    sample = sample[:50] + "..."
                click.echo(f"      - Sample: {sample}")

        if len(analysis.columns) > 10:
            click.echo(f"    ... and {len(analysis.columns) - 10} more columns")

    click.echo()


if __name__ == '__main__':
    cli()
