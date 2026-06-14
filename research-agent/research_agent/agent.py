"""Entry point for the research agent using AgentDefinition for subagents.

A "Lead Agent" coordinates the workflow and delegates to three specialized
subagents via the Task tool:

    researcher    -> web search, writes notes to files/research_notes/
    data-analyst  -> reads notes, extracts metrics, renders charts
    report-writer -> synthesizes everything into a PDF report

All tool calls are tracked through SDK hooks so we can attribute each call to
the subagent that made it, and a per-session transcript + JSONL log is written
to logs/.

Run interactively (REPL) or as a one-shot:

    python -m research_agent.agent                       # interactive
    python -m research_agent.agent --query "..."         # one-shot
    python -m research_agent.agent --query-file brief.txt # one-shot from file
"""

import argparse
import asyncio
import os
import shutil
from pathlib import Path

from dotenv import load_dotenv

from claude_agent_sdk import (
    AgentDefinition,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    HookMatcher,
)

from research_agent.utils.message_handler import process_assistant_message
from research_agent.utils.subagent_tracker import SubagentTracker
from research_agent.utils.transcript import TranscriptWriter, setup_session

# Load environment variables
load_dotenv()

# Paths to prompt files
PROMPTS_DIR = Path(__file__).parent / "prompts"

# Subdirectories created under the output directory.
OUTPUT_SUBDIRS = ("research_notes", "data", "charts", "reports")


def load_prompt(filename: str) -> str:
    """Load a prompt from the prompts directory."""
    prompt_path = PROMPTS_DIR / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def ensure_output_dirs(files_dir: Path) -> None:
    """Create the output directory tree so subagents never have to."""
    for sub in OUTPUT_SUBDIRS:
        (files_dir / sub).mkdir(parents=True, exist_ok=True)


def with_output_locations(prompt: str, files_dir: Path) -> str:
    """Append an authoritative, absolute output-location block to a prompt.

    Subagents sometimes invent an absolute project-root path instead of using
    the relative ``files/...`` path, scattering outputs. Pinning the SDK ``cwd``
    fixes relative writes; spelling out the absolute directories here fixes the
    rest, so outputs are deterministic regardless of how the model phrases the
    path.
    """
    locations = "\n".join(
        f"- {sub.replace('_', ' ').title()}: {files_dir / sub}/" for sub in OUTPUT_SUBDIRS
    )
    return (
        f"{prompt}\n\n"
        "OUTPUT LOCATIONS (authoritative — overrides any other path mentioned above):\n"
        "Write every output file inside these exact absolute directories:\n"
        f"{locations}\n"
        "Do not write to any other location and do not invent a different path."
    )


def build_options(files_dir: Path, tracker: SubagentTracker, model: str) -> ClaudeAgentOptions:
    """Construct the SDK options: subagents, hooks, working dir, and model."""
    researcher_prompt = with_output_locations(load_prompt("researcher.txt"), files_dir)
    data_analyst_prompt = with_output_locations(load_prompt("data_analyst.txt"), files_dir)
    report_writer_prompt = with_output_locations(load_prompt("report_writer.txt"), files_dir)

    agents = {
        "researcher": AgentDefinition(
            description=(
                "Use this agent when you need to gather research information on any topic. "
                "The researcher uses web search to find relevant information, articles, and "
                "sources from across the internet. Writes research findings to "
                "files/research_notes/ for later use by report writers. Ideal for complex "
                "research tasks that require deep searching and cross-referencing."
            ),
            tools=["WebSearch", "Write"],
            prompt=researcher_prompt,
            model=model,
        ),
        "data-analyst": AgentDefinition(
            description=(
                "Use this agent AFTER researchers have completed their work to generate "
                "quantitative analysis and visualizations. The data-analyst reads research "
                "notes from files/research_notes/, extracts numerical data (percentages, "
                "rankings, trends, comparisons), and generates charts using Python/matplotlib "
                "via Bash. Saves charts to files/charts/ and writes a data summary to "
                "files/data/. Use this before the report-writer to add visual insights."
            ),
            tools=["Glob", "Read", "Bash", "Write"],
            prompt=data_analyst_prompt,
            model=model,
        ),
        "report-writer": AgentDefinition(
            description=(
                "Use this agent when you need to create a formal research report document. "
                "The report-writer reads research findings from files/research_notes/, data "
                "analysis from files/data/, and charts from files/charts/, then synthesizes "
                "them into clear, concise, professionally formatted PDF reports in "
                "files/reports/ using reportlab. Ideal for creating structured documents with "
                "proper citations, data, and embedded visuals. Does NOT conduct web searches - "
                "only reads existing research notes and creates PDF reports."
            ),
            tools=["Skill", "Write", "Glob", "Read", "Bash"],
            prompt=report_writer_prompt,
            model=model,
        ),
    }

    hooks = {
        "PreToolUse": [HookMatcher(matcher=None, hooks=[tracker.pre_tool_use_hook])],
        "PostToolUse": [HookMatcher(matcher=None, hooks=[tracker.post_tool_use_hook])],
    }

    return ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        cwd=str(files_dir.parent),  # Pin the working dir so relative file paths
        # (files/...) resolve to the same place for every agent and subagent.
        setting_sources=["project"],  # Load skills/commands from project .claude directory
        system_prompt=load_prompt("lead_agent.txt"),
        allowed_tools=["Task"],
        agents=agents,
        hooks=hooks,
        model=model,
    )


def has_credentials() -> bool:
    """True if the SDK can authenticate (API key or an installed claude CLI)."""
    return bool(os.environ.get("ANTHROPIC_API_KEY")) or shutil.which("claude") is not None


async def _run_turn(
    client: ClaudeSDKClient, prompt: str, tracker: SubagentTracker, transcript: TranscriptWriter
) -> None:
    """Send one prompt and stream the response into the transcript."""
    transcript.write_to_file(f"\nYou: {prompt}\n")
    await client.query(prompt=prompt)
    transcript.write("\nAgent: ", end="")
    async for msg in client.receive_response():
        if type(msg).__name__ == "AssistantMessage":
            process_assistant_message(msg, tracker, transcript)
    transcript.write("\n")


async def run_research(query: str | None = None, model: str = "haiku") -> None:
    """Run the research agent, either one-shot (query given) or interactive."""

    # Verify we can authenticate before creating any files.
    if not has_credentials():
        print("\nError: no Anthropic credentials found.")
        print("Set ANTHROPIC_API_KEY in a .env file or your shell, or install and")
        print("authenticate the Claude Code CLI.")
        print("Get an API key at: https://console.anthropic.com/settings/keys\n")
        return

    files_dir = (Path.cwd() / "files").resolve()
    ensure_output_dirs(files_dir)

    transcript_file, session_dir = setup_session()
    transcript = TranscriptWriter(transcript_file)
    tracker = SubagentTracker(transcript_writer=transcript, session_dir=session_dir)
    options = build_options(files_dir, tracker, model)

    print("\n" + "=" * 50)
    print("  Research Agent")
    print("=" * 50)
    print(f"\nOutputs: {files_dir}")
    if query is None:
        print("\nResearch any topic and get a comprehensive PDF report.")
        print("Type 'exit' to quit.\n")

    try:
        async with ClaudeSDKClient(options=options) as client:
            if query is not None:
                await _run_turn(client, query, tracker, transcript)
            else:
                while True:
                    try:
                        user_input = input("\nYou: ").strip()
                    except (EOFError, KeyboardInterrupt):
                        break
                    if not user_input or user_input.lower() in ["exit", "quit", "q"]:
                        break
                    await _run_turn(client, user_input, tracker, transcript)
    finally:
        transcript.write("\n\nGoodbye!\n")
        transcript.close()
        tracker.close()
        print(f"\nSession logs saved to: {session_dir}")
        print(f"  - Transcript: {transcript_file}")
        print(f"  - Tool calls: {session_dir / 'tool_calls.jsonl'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-agent research system.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--query", help="Run one research request non-interactively, then exit.")
    group.add_argument(
        "--query-file",
        type=Path,
        help="Run one research request read from a file non-interactively, then exit.",
    )
    parser.add_argument("--model", default="haiku", help="Model for all agents (default: haiku).")
    args = parser.parse_args()

    query = args.query
    if args.query_file is not None:
        query = args.query_file.read_text(encoding="utf-8").strip()

    asyncio.run(run_research(query=query, model=args.model))


if __name__ == "__main__":
    main()
