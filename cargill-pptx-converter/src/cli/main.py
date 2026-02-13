"""
CLI entry point for the Cargill PPTX Converter.

Usage:
    cargill-pptx convert <input_file> [-o output.pptx]
    cargill-pptx verify <pptx_file>
    cargill-pptx formats
"""

import logging
import sys
from pathlib import Path

import click

from src.extractors.registry import SUPPORTED_FORMATS, is_supported_format
from src.orchestrator.pipeline import ConversionPipeline, convert_document
from src.schemas.run_state import RunConfig


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )


@click.group()
@click.version_option(version="0.1.0", prog_name="cargill-pptx")
def cli():
    """Cargill PPTX Converter - Transform documents into branded presentations."""
    pass


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None,
    help="Output PPTX file path. Default: <input_name>_Cargill_Branded.pptx",
)
@click.option(
    "--max-words", "-w",
    type=int,
    default=150,
    help="Maximum words per slide (default: 150)",
)
@click.option(
    "--max-bullets", "-b",
    type=int,
    default=7,
    help="Maximum bullet points per slide (default: 7)",
)
@click.option(
    "--no-footer",
    is_flag=True,
    help="Omit footer from slides",
)
@click.option(
    "--no-logo",
    is_flag=True,
    help="Omit logo placeholder from slides",
)
@click.option(
    "--fallback-fonts",
    is_flag=True,
    help="Use fallback fonts (Georgia/Arial) instead of brand fonts",
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose logging",
)
def convert(input_file, output, max_words, max_bullets, no_footer, no_logo, fallback_fonts, verbose):
    """Convert a document to a Cargill-branded PPTX presentation.

    Supports: DOCX, PDF, PPTX, TXT, MD, CSV, XLSX
    """
    setup_logging(verbose)

    input_path = Path(input_file)

    if not is_supported_format(input_path):
        click.echo(f"Error: Unsupported file format '{input_path.suffix}'", err=True)
        click.echo("Run 'cargill-pptx formats' to see supported formats.", err=True)
        sys.exit(1)

    config = RunConfig(
        max_words_per_slide=max_words,
        max_bullets_per_slide=max_bullets,
        include_footer=not no_footer,
        include_logo=not no_logo,
        use_brand_fonts=not fallback_fonts,
    )

    click.echo(f"Converting: {input_path.name}")
    click.echo(f"Format: {input_path.suffix}")

    state = convert_document(
        input_file=str(input_path),
        output_path=output,
        config=config,
    )

    if state.output_file:
        click.echo(f"\nOutput: {state.output_file}")

        if state.presentation_plan:
            click.echo(f"Slides: {state.presentation_plan.total_slides}")

        if state.qa_report:
            click.echo(f"Quality: {state.qa_report.overall_score}/100 ({state.qa_report.status})")
            if state.qa_report.issues:
                click.echo(f"Issues: {len(state.qa_report.issues)}")
                for issue in state.qa_report.issues[:5]:
                    click.echo(f"  [{issue.severity.value}] {issue.description}")
                if len(state.qa_report.issues) > 5:
                    click.echo(f"  ... and {len(state.qa_report.issues) - 5} more")

        if state.compliance_report and state.compliance_report.terminology_corrections:
            click.echo(
                f"Terminology corrections: {len(state.compliance_report.terminology_corrections)}"
            )

        click.echo("\nDone.")
    else:
        click.echo("\nConversion failed.", err=True)
        for flag in state.flags:
            if flag.severity in ("CRITICAL", "ERROR"):
                click.echo(f"  [{flag.severity}] {flag.message}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("pptx_file", type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def verify(pptx_file, verbose):
    """Run brand compliance checks on an existing PPTX file.

    This re-extracts content from a PPTX and runs brand compliance and QA checks.
    """
    setup_logging(verbose)

    pptx_path = Path(pptx_file)
    if pptx_path.suffix.lower() not in (".pptx", ".ppt"):
        click.echo("Error: Input must be a PowerPoint file (.pptx)", err=True)
        sys.exit(1)

    click.echo(f"Verifying: {pptx_path.name}")

    # Run extraction + compliance only
    from src.agents.content_extractor import ContentExtractorAgent
    from src.agents.brand_compliance import BrandComplianceAgent
    from src.schemas.run_state import RunInputs, RunState

    state = RunState(inputs=RunInputs(input_file=str(pptx_path)))

    extractor = ContentExtractorAgent()
    state = extractor.execute(state)

    if state.extracted_content:
        compliance = BrandComplianceAgent()
        state = compliance.execute(state)

        if state.compliance_report:
            report = state.compliance_report
            click.echo(f"\nCompliance Score: {report.overall_score}")
            click.echo(f"Status: {report.status}")

            if report.tone_analysis:
                click.echo("\nPersonality Alignment:")
                for trait in ["optimistic", "curious", "courageous", "compassionate", "humble"]:
                    data = getattr(report.tone_analysis, trait, {})
                    if data:
                        click.echo(f"  {trait}: {data.get('score', 'N/A')} ({data.get('assessment', 'N/A')})")

            if report.terminology_corrections:
                click.echo(f"\nTerminology Issues: {len(report.terminology_corrections)}")
                for tc in report.terminology_corrections[:10]:
                    click.echo(f"  '{tc['original']}' -> '{tc['replacement']}'")

            if report.recommendations:
                click.echo("\nRecommendations:")
                for rec in report.recommendations:
                    click.echo(f"  - {rec}")
    else:
        click.echo("Error: Could not extract content from file.", err=True)
        sys.exit(1)


@cli.command()
def formats():
    """List all supported input formats."""
    click.echo("Supported input formats:\n")
    for ext, desc in sorted(SUPPORTED_FORMATS.items()):
        click.echo(f"  {ext:12s} {desc}")
    click.echo(f"\nOutput format: .pptx (Microsoft PowerPoint)")


if __name__ == "__main__":
    cli()
