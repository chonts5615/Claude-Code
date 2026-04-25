"""TCB v3.1 CLI: run, map-skills, inspect, init-config."""

from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path

import click
import yaml

from src.orchestrator.graph import WorkflowOrchestrator
from src.schemas.run_state import RunConfig, RunInputs, RunState, ThresholdConfig
from src.utils.logger import setup_logger


@click.group()
def cli():
    """Technical Competency Builder v3.1 + Skill Mapping."""


@cli.command()
@click.option("--stage", type=click.Choice(["R1", "R2", "FINAL", "RESUME"]), default="R1",
              help="Stage to run (R1=full pipeline, R2/FINAL=feedback, RESUME=continue last run).")
@click.option("--family", type=str, default=None, help="Cargill job family (Finance, HR, ...).")
@click.option("--jobs-file", type=click.Path(exists=True), required=False,
              help="Path to Excel file containing job descriptions (R1 only).")
@click.option("--tech-sources", type=click.Path(exists=True), multiple=True,
              help="Path(s) to technical competency source files.")
@click.option("--leadership-file", type=click.Path(exists=True), required=False,
              help="Path to core/leadership competencies Excel file.")
@click.option("--template-file", type=click.Path(exists=True), required=False,
              help="Path to output template Excel file.")
@click.option("--feedback-file", type=click.Path(exists=True), required=False,
              help="SME feedback file (required for R2/FINAL).")
@click.option("--config", type=click.Path(exists=True), default="config/workflow_config.yaml",
              help="Path to workflow configuration file.")
@click.option("--thresholds", type=click.Path(exists=True), default="config/thresholds.yaml",
              help="Path to thresholds configuration file.")
@click.option("--output-dir", type=click.Path(), default="data/output",
              help="Directory for output artifacts.")
@click.option("--run-id", type=str, default=None,
              help="Custom run ID (auto-generated if not provided).")
def run(stage, family, jobs_file, tech_sources, leadership_file, template_file, feedback_file,
        config, thresholds, output_dir, run_id):
    """Execute a TCB v3.1 workflow run."""
    logger = setup_logger()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not run_id:
        run_id = f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    logger.info(f"Starting v3.1 workflow run {run_id} (stage={stage}, family={family})")

    if stage == "R1" and not jobs_file:
        raise click.UsageError("--jobs-file is required for stage R1")
    if stage in ("R2", "FINAL") and not feedback_file:
        raise click.UsageError("--feedback-file is required for stage R2/FINAL")

    if Path(config).exists():
        with open(config, "r") as f:
            yaml.safe_load(f)  # presence check; per-agent config consumed downstream

    threshold_data = {}
    if Path(thresholds).exists():
        with open(thresholds, "r") as f:
            raw = yaml.safe_load(f) or {}
            # Flatten v3.1 thresholds.yaml structure into ThresholdConfig fields
            threshold_data = {
                "min_responsibilities_per_job": raw.get("job_extraction", {}).get(
                    "min_responsibilities_per_job", 3),
                "overlap_material": raw.get("overlap", {}).get("material_threshold", 0.82),
                "overlap_minor": raw.get("overlap", {}).get("minor_threshold", 0.72),
                "distinctness_duplicate": raw.get("overlap", {}).get("distinctness_duplicate", 0.88),
                "top_n_competencies": raw.get("ranking", {}).get("top_n_competencies", 6),
                "min_responsibility_coverage": raw.get("ranking", {}).get(
                    "min_responsibility_coverage", 0.90),
                "max_drift_rate": raw.get("ctic", {}).get("max_drift_rate", 0.05),
                "max_qa_cycles": raw.get("qa", {}).get("max_cycles", 3),
            }

    inputs = RunInputs(
        jobs_file=Path(jobs_file) if jobs_file else Path("data/input/_placeholder.xlsx"),
        tech_comp_source_files=[Path(p) for p in tech_sources],
        core_leadership_file=Path(leadership_file) if leadership_file else None,
        output_template_file=Path(template_file) if template_file else None,
        feedback_file=Path(feedback_file) if feedback_file else None,
    )
    run_config = RunConfig(
        stage=stage,
        family=family,
        thresholds=ThresholdConfig(**threshold_data) if threshold_data else ThresholdConfig(),
    )
    initial_state = RunState(run_id=run_id, inputs=inputs, config=run_config)

    orchestrator = WorkflowOrchestrator(str(config))
    final_state = orchestrator.run(initial_state)

    state_file = output_path / f"{run_id}_final_state.json"
    with open(state_file, "w") as f:
        f.write(final_state.json(indent=2))

    click.echo("\n=== v3.1 Workflow Summary ===")
    click.echo(f"Run ID:  {run_id}")
    click.echo(f"Stage:   {stage}")
    click.echo(f"Family:  {family}")
    click.echo(f"Flags:   {len(final_state.flags)}")
    if final_state.flags:
        from collections import Counter
        for sev, n in Counter(f.severity for f in final_state.flags).items():
            click.echo(f"  {sev}: {n}")
    click.echo(f"State:   {state_file}")


@cli.command("map-skills")
@click.option("--library", type=click.Path(exists=True), required=True,
              help="Path to TechComp_Library_Master.xlsx (23-column).")
@click.option("--catalog", type=click.Path(exists=True), required=True,
              help="Path to L&D training catalog xlsx/csv.")
@click.option("--family", type=str, required=True, help="Job family name.")
@click.option("--out", type=click.Path(), default="data/output/skill_mapping/",
              help="Output directory for crosswalk Excel.")
@click.option("--config", type=click.Path(exists=True), default="config/skill_mapping.yaml",
              help="Skill mapping config.")
@click.option("--min-confidence", type=float, default=0.55,
              help="Minimum mapping confidence (default 0.55).")
@click.option("--llm-tiebreak/--no-llm-tiebreak", default=True,
              help="Enable LLM tie-break in Bloom classifier (default on).")
def map_skills(library, catalog, family, out, config, min_confidence, llm_tiebreak):
    """Map L&D training catalog to v3.1 technical competencies."""
    from src.skill_mapping.graph import SkillMappingPipeline

    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    pipeline = SkillMappingPipeline(config_path=config)
    crosswalk = pipeline.run(
        library_path=Path(library),
        catalog_path=Path(catalog),
        family=family,
        out_dir=out_dir,
        llm_tiebreak=llm_tiebreak,
        min_confidence=min_confidence,
    )

    click.echo("\n=== Skill Mapping Complete ===")
    click.echo(f"Family:    {family}")
    click.echo(f"Crosswalk: {crosswalk}")
    for attr in ("last_unmapped_rate", "last_zero_training_rate", "last_mapping_count"):
        if hasattr(pipeline, attr):
            click.echo(f"{attr}: {getattr(pipeline, attr)}")


@cli.command()
@click.argument("state_file", type=click.Path(exists=True))
def inspect(state_file):
    """Inspect a completed workflow run state."""
    state = RunState.parse_file(state_file)
    click.echo(f"\n=== Run State: {state.run_id} ===")
    click.echo(f"Timestamp: {state.run_timestamp_utc}")
    click.echo(f"Stage:     {state.config.stage}")
    click.echo(f"Family:    {state.config.family}")
    click.echo(f"Step:      {state.current_step}")
    click.echo("\nArtifacts generated:")
    for key, value in state.artifacts.dict().items():
        if value:
            click.echo(f"  {key}: {value}")
    click.echo(f"\nFlags: {len(state.flags)}")
    for flag in state.flags[:10]:
        click.echo(f"  [{flag.severity}] {flag.step_id}: {flag.message}")
    if len(state.flags) > 10:
        click.echo(f"  ... and {len(state.flags) - 10} more")


@cli.command("init-config")
@click.option("--output-dir", type=click.Path(), default="config",
              help="Directory for generated config files.")
def init_config(output_dir):
    """Generate v3.1 default configuration files (no-op if they exist)."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    expected = [
        "workflow_config.yaml", "thresholds.yaml", "band_proficiency_targets.yaml",
        "boundary_terms.yaml", "domain_registry.yaml", "stage_routes.yaml",
        "skill_mapping.yaml", "bloom_verbs.yaml",
    ]
    for name in expected:
        path = output_path / name
        if path.exists():
            click.echo(f"Skipped (exists): {path}")
        else:
            click.echo(f"Missing: {path}  (re-clone repo or run from project root)")
    click.echo("\nNext steps:")
    click.echo("1. Set up .env with ANTHROPIC_API_KEY")
    click.echo("2. R1 run: techcomp run --stage R1 --family Finance --jobs-file ...")
    click.echo("3. Skill mapping: techcomp map-skills --library ... --catalog ... --family Finance")


if __name__ == "__main__":
    cli()
