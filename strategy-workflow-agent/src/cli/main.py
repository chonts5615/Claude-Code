"""Command-line interface for the strategy workflow agent."""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from src.orchestrator import StrategyWorkflowOrchestrator, create_initial_state
from src.orchestrator.state import save_final_state

app = typer.Typer(
    name="strategy-workflow",
    help="Multi-Agent Strategic Planning Workflow with Learning Feedback Loops"
)
console = Console()


@app.command()
def run(
    vision_text: Optional[str] = typer.Option(
        None, "--vision", "-v",
        help="Vision/strategy text input"
    ),
    goals_text: Optional[str] = typer.Option(
        None, "--goals", "-g",
        help="Goals text input"
    ),
    context_text: Optional[str] = typer.Option(
        None, "--context", "-c",
        help="Additional context text"
    ),
    vision_file: Optional[Path] = typer.Option(
        None, "--vision-file", "-f",
        help="Path to vision document file"
    ),
    time_horizon: int = typer.Option(
        3, "--horizon", "-h",
        help="Planning time horizon in years (1-10)"
    ),
    output_format: str = typer.Option(
        "comprehensive", "--format",
        help="Output format: comprehensive, executive, or minimal"
    ),
    output_dir: Path = typer.Option(
        Path("./data/output"), "--output", "-o",
        help="Output directory for results"
    ),
    enable_feedback: bool = typer.Option(
        True, "--feedback/--no-feedback",
        help="Enable learning feedback loop"
    ),
    auto_optimize: bool = typer.Option(
        True, "--auto-optimize/--no-auto-optimize",
        help="Automatically apply optimizations"
    ),
    strict_mode: bool = typer.Option(
        False, "--strict/--no-strict",
        help="Fail on any quality gate violation"
    ),
    model: str = typer.Option(
        "claude-sonnet-4-20250514", "--model", "-m",
        help="LLM model to use"
    ),
    verbose: bool = typer.Option(
        False, "--verbose",
        help="Verbose output"
    ),
):
    """
    Run the multi-agent strategic planning workflow.

    Example:
        strategy-workflow run --vision "Our vision is to become..." --horizon 3
    """
    console.print(Panel.fit(
        "[bold green]Strategy Workflow Agent[/bold green]\n"
        "Multi-Agent Strategic Planning with Learning Feedback Loops",
        border_style="green"
    ))

    # Validate inputs
    if not vision_text and not vision_file:
        console.print("[yellow]Warning: No vision input provided. Using interactive mode.[/yellow]")
        vision_text = typer.prompt("Enter your strategic vision/strategy")

    # Read vision file if provided
    if vision_file and vision_file.exists():
        vision_text = vision_file.read_text()
        console.print(f"[green]Loaded vision from {vision_file}[/green]")

    # Create initial state
    state = create_initial_state(
        vision_text=vision_text,
        goals_text=goals_text,
        context_text=context_text,
        time_horizon_years=time_horizon,
        output_format=output_format,
        enable_feedback=enable_feedback,
        auto_optimize=auto_optimize,
        strict_mode=strict_mode,
    )

    console.print(f"\n[cyan]Run ID:[/cyan] {state.run_id}")
    console.print(f"[cyan]Time Horizon:[/cyan] {time_horizon} years")
    console.print(f"[cyan]Output Format:[/cyan] {output_format}")
    console.print(f"[cyan]Feedback Loop:[/cyan] {'Enabled' if enable_feedback else 'Disabled'}")

    # Initialize orchestrator
    orchestrator = StrategyWorkflowOrchestrator(
        model_name=model,
        enable_feedback_loop=enable_feedback
    )

    # Run workflow with progress
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Running strategic planning workflow...", total=None)

        try:
            final_state = orchestrator.run(state)
            progress.update(task, description="[green]Workflow completed!")
        except Exception as e:
            progress.update(task, description=f"[red]Workflow failed: {e}")
            raise typer.Exit(1)

    # Display results summary
    _display_results_summary(final_state)

    # Save outputs
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = save_final_state(final_state, output_dir)
    console.print(f"\n[green]Results saved to:[/green] {output_path}")

    # Save executive summary if available
    exec_summary = final_state.working_data.get("executive_summary")
    if exec_summary:
        summary_path = output_dir / f"{final_state.run_id}_executive_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(exec_summary, f, indent=2)
        console.print(f"[green]Executive summary saved to:[/green] {summary_path}")


@app.command()
def inspect(
    state_file: Path = typer.Argument(..., help="Path to state JSON file"),
    section: Optional[str] = typer.Option(
        None, "--section", "-s",
        help="Specific section to inspect (e.g., 'vision', 'pillars', 'goals')"
    ),
):
    """
    Inspect a workflow state file.

    Example:
        strategy-workflow inspect data/output/run_xyz_final_state.json
    """
    if not state_file.exists():
        console.print(f"[red]File not found: {state_file}[/red]")
        raise typer.Exit(1)

    with open(state_file, 'r') as f:
        state_data = json.load(f)

    if section:
        # Show specific section
        working_data = state_data.get("working_data", {})
        if section in working_data:
            console.print(Panel.fit(f"[bold]Section: {section}[/bold]", border_style="blue"))
            console.print_json(json.dumps(working_data[section], indent=2, default=str))
        else:
            console.print(f"[yellow]Section '{section}' not found[/yellow]")
            console.print(f"Available sections: {list(working_data.keys())}")
    else:
        # Show overview
        _display_state_overview(state_data)


@app.command()
def validate(
    state_file: Path = typer.Argument(..., help="Path to state JSON file"),
):
    """
    Validate a workflow state and show quality scores.

    Example:
        strategy-workflow validate data/output/run_xyz_final_state.json
    """
    if not state_file.exists():
        console.print(f"[red]File not found: {state_file}[/red]")
        raise typer.Exit(1)

    with open(state_file, 'r') as f:
        state_data = json.load(f)

    working_data = state_data.get("working_data", {})
    quality_scores = working_data.get("quality_scores", {})
    validation_result = working_data.get("validation_result", {})

    # Display quality scores
    table = Table(title="Quality Scores")
    table.add_column("Metric", style="cyan")
    table.add_column("Score", style="green")
    table.add_column("Status", style="yellow")

    thresholds = {
        "alignment_score": 0.75,
        "coherence_score": 0.80,
        "completeness_score": 0.85,
        "feasibility_score": 0.60,
    }

    for metric, score in quality_scores.items():
        threshold = thresholds.get(metric, 0.7)
        status = "PASS" if score >= threshold else "FAIL"
        status_color = "green" if score >= threshold else "red"
        table.add_row(metric, f"{score:.2f}", f"[{status_color}]{status}[/{status_color}]")

    console.print(table)

    # Show certification status
    certification = validation_result.get("certification", {})
    ready = certification.get("ready_for_approval", False)
    status = "[green]READY[/green]" if ready else "[yellow]NOT READY[/yellow]"
    console.print(f"\n[bold]Approval Status:[/bold] {status}")

    if not ready:
        blocking = certification.get("blocking_issues", [])
        if blocking:
            console.print("[red]Blocking Issues:[/red]")
            for issue in blocking:
                console.print(f"  - {issue}")


@app.command()
def feedback(
    state_file: Path = typer.Argument(..., help="Path to state JSON file"),
    rating: Optional[float] = typer.Option(
        None, "--rating", "-r",
        help="Overall rating (1-5)"
    ),
    comment: Optional[str] = typer.Option(
        None, "--comment", "-c",
        help="Feedback comment"
    ),
):
    """
    Submit feedback for a workflow run.

    Example:
        strategy-workflow feedback data/output/run_xyz_final_state.json --rating 4.5 --comment "Good pillars"
    """
    if not state_file.exists():
        console.print(f"[red]File not found: {state_file}[/red]")
        raise typer.Exit(1)

    with open(state_file, 'r') as f:
        state_data = json.load(f)

    run_id = state_data.get("run_id", "unknown")

    if not rating and not comment:
        rating = typer.prompt("Rating (1-5)", type=float)
        comment = typer.prompt("Comment (optional)", default="")

    feedback_entry = {
        "run_id": run_id,
        "timestamp": datetime.utcnow().isoformat(),
        "rating": rating,
        "comment": comment,
        "type": "user_feedback",
    }

    # Append to feedback log
    feedback_dir = Path("./data/feedback_logs")
    feedback_dir.mkdir(parents=True, exist_ok=True)
    feedback_file = feedback_dir / f"{run_id}_feedback.json"

    existing_feedback = []
    if feedback_file.exists():
        with open(feedback_file, 'r') as f:
            existing_feedback = json.load(f)

    existing_feedback.append(feedback_entry)

    with open(feedback_file, 'w') as f:
        json.dump(existing_feedback, f, indent=2)

    console.print(f"[green]Feedback recorded for run {run_id}[/green]")


def _display_results_summary(state):
    """Display a summary of workflow results."""
    console.print("\n" + "=" * 60)
    console.print("[bold green]WORKFLOW RESULTS SUMMARY[/bold green]")
    console.print("=" * 60)

    # Counts
    working_data = state.working_data
    pillars = working_data.get("strategic_pillars", [])
    goals = working_data.get("strategic_goals", [])
    initiatives = working_data.get("initiatives", [])
    risks = working_data.get("risks", [])
    milestones = working_data.get("milestones", [])

    table = Table(title="Strategic Elements")
    table.add_column("Element", style="cyan")
    table.add_column("Count", style="green")

    table.add_row("Strategic Pillars", str(len(pillars)))
    table.add_row("Strategic Goals", str(len(goals)))
    table.add_row("Initiatives", str(len(initiatives)))
    table.add_row("Risks Identified", str(len(risks)))
    table.add_row("Milestones", str(len(milestones)))

    console.print(table)

    # Quality scores
    quality_scores = working_data.get("quality_scores", {})
    if quality_scores:
        console.print("\n[bold]Quality Scores:[/bold]")
        for metric, score in quality_scores.items():
            bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
            console.print(f"  {metric}: [{bar}] {score:.2f}")

    # Flags summary
    flag_counts = {}
    for flag in state.flags:
        severity = flag.severity.value
        flag_counts[severity] = flag_counts.get(severity, 0) + 1

    if flag_counts:
        console.print("\n[bold]Flags:[/bold]")
        for severity, count in flag_counts.items():
            color = {"CRITICAL": "red", "ERROR": "red", "WARNING": "yellow", "INFO": "blue"}.get(severity, "white")
            console.print(f"  [{color}]{severity}[/{color}]: {count}")

    # Feedback loop status
    if state.config.feedback.enabled:
        insights = working_data.get("learning_insights", [])
        optimizations = working_data.get("applied_optimizations", [])
        console.print(f"\n[bold]Feedback Loop:[/bold]")
        console.print(f"  Learning Insights: {len(insights)}")
        console.print(f"  Optimizations Applied: {len(optimizations)}")


def _display_state_overview(state_data):
    """Display an overview of the state file."""
    console.print(Panel.fit("[bold]State File Overview[/bold]", border_style="blue"))

    console.print(f"[cyan]Run ID:[/cyan] {state_data.get('run_id', 'N/A')}")
    console.print(f"[cyan]Timestamp:[/cyan] {state_data.get('run_timestamp_utc', 'N/A')}")
    console.print(f"[cyan]Current Phase:[/cyan] {state_data.get('current_phase', 'N/A')}")
    console.print(f"[cyan]Current Step:[/cyan] {state_data.get('current_step', 'N/A')}")

    completed = state_data.get("completed_steps", [])
    console.print(f"[cyan]Completed Steps:[/cyan] {len(completed)}")

    working_data = state_data.get("working_data", {})
    console.print(f"\n[cyan]Available Data Sections:[/cyan]")
    for key in sorted(working_data.keys()):
        value = working_data[key]
        if isinstance(value, list):
            console.print(f"  - {key}: {len(value)} items")
        elif isinstance(value, dict):
            console.print(f"  - {key}: {len(value)} keys")
        else:
            console.print(f"  - {key}: {type(value).__name__}")


if __name__ == "__main__":
    app()
