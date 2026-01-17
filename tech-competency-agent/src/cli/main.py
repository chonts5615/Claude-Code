import click
import yaml
from pathlib import Path
from datetime import datetime
import uuid
import os

from src.schemas.run_state import RunState, RunInputs, RunConfig, ThresholdConfig
from src.orchestrator.graph import WorkflowOrchestrator
from src.utils.logger import setup_logger


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
def run(jobs_file, tech_sources, leadership_file, template_file, config, output_dir, run_id):
    """Execute full workflow: jobs → competencies → template"""

    # Setup
    logger = setup_logger()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not run_id:
        run_id = f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

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


if __name__ == '__main__':
    cli()
