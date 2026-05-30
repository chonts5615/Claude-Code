"""Entry point for the research agent using AgentDefinition for subagents.

A "Lead Agent" coordinates the workflow and delegates to three specialized
subagents via the Task tool:

    researcher    -> web search, writes notes to files/research_notes/
    data-analyst  -> reads notes, extracts metrics, renders charts
    report-writer -> synthesizes everything into a PDF report

All tool calls are tracked through SDK hooks so we can attribute each call to
the subagent that made it, and a per-session transcript + JSONL log is written
to logs/.
"""

import asyncio
import os
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


def load_prompt(filename: str) -> str:
    """Load a prompt from the prompts directory."""
    prompt_path = PROMPTS_DIR / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


async def chat() -> None:
    """Start an interactive chat session with the research agent."""

    # Check API key first, before creating any files.
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\nError: ANTHROPIC_API_KEY not found.")
        print("Set it in a .env file or export it in your shell.")
        print("Get your key at: https://console.anthropic.com/settings/keys\n")
        return

    # Set up session directory and transcript.
    transcript_file, session_dir = setup_session()
    transcript = TranscriptWriter(transcript_file)

    # Load prompts.
    lead_agent_prompt = load_prompt("lead_agent.txt")
    researcher_prompt = load_prompt("researcher.txt")
    data_analyst_prompt = load_prompt("data_analyst.txt")
    report_writer_prompt = load_prompt("report_writer.txt")

    # Initialize the subagent tracker with the transcript writer and session dir.
    tracker = SubagentTracker(transcript_writer=transcript, session_dir=session_dir)

    # Define the specialized subagents.
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
            model="haiku",
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
            model="haiku",
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
            model="haiku",
        ),
    }

    # Set up hooks for tracking every tool call.
    hooks = {
        "PreToolUse": [
            HookMatcher(matcher=None, hooks=[tracker.pre_tool_use_hook]),
        ],
        "PostToolUse": [
            HookMatcher(matcher=None, hooks=[tracker.post_tool_use_hook]),
        ],
    }

    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"],  # Load skills/commands from project .claude directory
        system_prompt=lead_agent_prompt,
        allowed_tools=["Task"],
        agents=agents,
        hooks=hooks,
        model="haiku",
    )

    print("\n" + "=" * 50)
    print("  Research Agent")
    print("=" * 50)
    print("\nResearch any topic and get a comprehensive PDF")
    print("report with data visualizations.")
    print("\nType 'exit' to quit.\n")

    try:
        async with ClaudeSDKClient(options=options) as client:
            while True:
                try:
                    user_input = input("\nYou: ").strip()
                except (EOFError, KeyboardInterrupt):
                    break

                if not user_input or user_input.lower() in ["exit", "quit", "q"]:
                    break

                # Write user input to transcript file only (not console - it's echoed).
                transcript.write_to_file(f"\nYou: {user_input}\n")

                # Send to the agent.
                await client.query(prompt=user_input)

                transcript.write("\nAgent: ", end="")

                # Stream and process the response.
                async for msg in client.receive_response():
                    if type(msg).__name__ == "AssistantMessage":
                        process_assistant_message(msg, tracker, transcript)

                transcript.write("\n")
    finally:
        transcript.write("\n\nGoodbye!\n")
        transcript.close()
        tracker.close()
        print(f"\nSession logs saved to: {session_dir}")
        print(f"  - Transcript: {transcript_file}")
        print(f"  - Tool calls: {session_dir / 'tool_calls.jsonl'}")


if __name__ == "__main__":
    asyncio.run(chat())
