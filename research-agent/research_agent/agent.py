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
import json
import os
import re
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

# Max attempts per orchestrated phase before moving on (degrade gracefully
# rather than block forever if a phase can't fully complete).
PHASE_ATTEMPTS = {"research": 3, "analyze": 2, "report": 3, "qa": 2}

# The SDK's default stdout buffer is 1 MB; a single large tool result (e.g. an
# agent accidentally reading a multi-MB PDF/PNG, or a big web result) overflows
# it and fatally crashes the message reader. Raise it for resilience.
MAX_BUFFER_SIZE = 20 * 1024 * 1024  # 20 MB


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
    qa_reviewer_prompt = with_output_locations(load_prompt("qa_reviewer.txt"), files_dir)

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
            maxTurns=40,  # chart generation is multi-step (script + run + verify)
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
            maxTurns=40,  # read inputs + build PDF + build script + markdown copy
        ),
        "qa-reviewer": AgentDefinition(
            description=(
                "Use this agent AFTER the report-writer to critically review the drafted "
                "report against the research notes. The qa-reviewer reads the notes, the data "
                "summary, and files/reports/report.md, then writes a critical review to "
                "files/reports/qa_review.md flagging coverage gaps, outdated statistics, vague "
                "citations, and inconsistencies, ending with a PASS/REVISE verdict. Does not "
                "do web research or rewrite the report."
            ),
            tools=["Glob", "Read", "Write"],
            prompt=qa_reviewer_prompt,
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
        max_buffer_size=MAX_BUFFER_SIZE,
    )


def has_credentials() -> bool:
    """True if the SDK can authenticate (API key or an installed claude CLI)."""
    return bool(os.environ.get("ANTHROPIC_API_KEY")) or shutil.which("claude") is not None


async def _run_turn(
    client: ClaudeSDKClient, prompt: str, tracker: SubagentTracker, transcript: TranscriptWriter
) -> str:
    """Send one prompt, stream the response into the transcript, return its text."""
    transcript.write_to_file(f"\nYou: {prompt}\n")
    await client.query(prompt=prompt)
    transcript.write("\nAgent: ", end="")
    text_parts: list[str] = []
    async for msg in client.receive_response():
        if type(msg).__name__ == "AssistantMessage":
            process_assistant_message(msg, tracker, transcript)
            for block in msg.content:
                if type(block).__name__ == "TextBlock":
                    text_parts.append(block.text)
    transcript.write("\n")
    return "".join(text_parts)


# ---------------------------------------------------------------------------- #
# Deterministic phase orchestration
# ---------------------------------------------------------------------------- #
def _present_notes(files_dir: Path) -> set[str]:
    return {p.name for p in (files_dir / "research_notes").glob("*.md")}


def _missing_notes(files_dir: Path, plan: list[dict]) -> list[dict]:
    present = _present_notes(files_dir)
    return [s for s in plan if s["filename"] not in present]


def _analysis_done(files_dir: Path) -> bool:
    return bool(list((files_dir / "charts").glob("*.png"))) or bool(
        list((files_dir / "data").glob("*.md"))
    )


def _final_report_exists(files_dir: Path) -> bool:
    """True once the report-writer has produced a PDF."""
    return any((files_dir / "reports").glob("*.pdf"))


def _report_md_path(files_dir: Path) -> Path:
    return files_dir / "reports" / "report.md"


def _report_done(files_dir: Path) -> bool:
    """The report phase needs BOTH the markdown (for QA) and the PDF deliverable."""
    return _report_md_path(files_dir).exists() and _final_report_exists(files_dir)


def _report_missing(files_dir: Path) -> list[str]:
    missing = []
    if not _report_md_path(files_dir).exists():
        missing.append("files/reports/report.md")
    if not _final_report_exists(files_dir):
        missing.append("the PDF in files/reports/")
    return missing


def _qa_review_path(files_dir: Path) -> Path:
    return files_dir / "reports" / "qa_review.md"


def _qa_verdict(files_dir: Path) -> str:
    """Return PASS / REVISE / UNKNOWN parsed from the QA review file."""
    path = _qa_review_path(files_dir)
    if not path.exists():
        return "UNKNOWN"
    text = path.read_text(encoding="utf-8", errors="ignore").upper()
    if "VERDICT: REVISE" in text:
        return "REVISE"
    if "VERDICT: PASS" in text:
        return "PASS"
    return "UNKNOWN"


def _parse_plan(text: str) -> list[dict]:
    """Extract a subtopic plan (list of {title, filename, brief}) from JSON text."""
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        return []
    try:
        raw = json.loads(match.group(0))
    except json.JSONDecodeError:
        return []
    plan: list[dict] = []
    for i, item in enumerate(raw, 1):
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or f"Subtopic {i}").strip()
        filename = str(item.get("filename") or f"subtopic_{i}.md").strip()
        filename = filename.replace("/", "_").lstrip("_")
        if not filename.endswith(".md"):
            filename += ".md"
        brief = str(item.get("brief") or title).strip()
        plan.append({"title": title, "filename": filename, "brief": brief})
    return plan[:4]  # cap at 4 subtopics


def _plan_prompt(query: str) -> str:
    return (
        "PLANNING PHASE. Do NOT spawn any subagents or call any tools. Decompose the research "
        "request below into 2-4 focused, non-overlapping subtopics. Reply with ONLY a JSON array "
        "(no prose, no code fence) of objects with keys \"title\", \"filename\" (snake_case, "
        "ending in .md) and \"brief\" (one sentence describing what that subtopic must cover).\n\n"
        f"Request:\n{query}"
    )


def _research_prompt(query: str, targets: list[dict], first: bool) -> str:
    header = (
        "RESEARCH PHASE." if first else "RESEARCH PHASE (continuing — these notes are missing)."
    )
    lines = "\n".join(f'- {s["filename"]}: {s["title"]} — {s["brief"]}' for s in targets)
    return (
        f"{header} Spawn one \"researcher\" subagent per item below, all in parallel in this "
        "turn. Each researcher MUST write its notes file to files/research_notes/ using exactly "
        "the given filename. Do not run the data-analyst or report-writer yet.\n\n"
        f"Subtopics to research now:\n{lines}\n\n"
        f"Overall research goal for context:\n{query}"
    )


def _analyze_prompt() -> str:
    return (
        "ANALYSIS PHASE. The research notes are in files/research_notes/. Spawn the "
        '"data-analyst" subagent now to read every note (any extension), extract the key '
        "quantitative findings, render charts as PNGs into files/charts/, and write a data "
        "summary into files/data/. Do not run the report-writer yet."
    )


def _report_prompt(revise: bool = False, first: bool = True, missing: list[str] | None = None) -> str:
    if revise:
        return (
            "REVISION PHASE. The QA review at files/reports/qa_review.md requested changes. Spawn "
            'the "report-writer" subagent now to read files/reports/qa_review.md and the research '
            "notes, address every issue raised (especially updating outdated statistics and "
            "replacing vague 'multiple sources' attributions with specific citations), and "
            "regenerate BOTH the PDF and files/reports/report.md."
        )
    if first:
        retry_note = ""
    else:
        what = ", ".join(missing) if missing else "the required outputs"
        retry_note = (
            f" A previous attempt did not produce {what}; spawn a NEW report-writer now — do not "
            "assume any earlier subagent is still running. It MUST write files/reports/report.md "
            "(the full report text) AND the PDF."
        )
    return (
        'REPORT PHASE. Spawn the "report-writer" subagent now to synthesize the research notes, '
        "the data summary in files/data/, and the charts in files/charts/ into a single cited PDF "
        "in files/reports/ with an appropriate title. Also have it write a plain-markdown copy of "
        "the same report (text only, no images) to files/reports/report.md so it can be reviewed."
        + retry_note
    )


def _qa_prompt() -> str:
    return (
        'QA PHASE. Spawn the "qa-reviewer" subagent now. It must read every research note in '
        "files/research_notes/, the data summary in files/data/, and the report at "
        "files/reports/report.md, then write a critical review to files/reports/qa_review.md "
        "ending with a line 'QA VERDICT: PASS' or 'QA VERDICT: REVISE'."
    )


async def _drive_phase(
    client: ClaudeSDKClient,
    tracker: SubagentTracker,
    transcript: TranscriptWriter,
    *,
    name: str,
    instruction_for_attempt,
    is_done,
    max_attempts: int,
) -> bool:
    """Run a phase until its filesystem gate passes or attempts are exhausted."""
    for attempt in range(1, max_attempts + 1):
        if is_done():
            return True
        print(f"\n[phase: {name}] attempt {attempt}/{max_attempts}\n")
        await _run_turn(client, instruction_for_attempt(attempt), tracker, transcript)
    done = is_done()
    print(f"[phase: {name}] {'complete' if done else 'INCOMPLETE — continuing anyway'}.\n")
    return done


async def run_pipeline(
    client: ClaudeSDKClient,
    query: str,
    files_dir: Path,
    tracker: SubagentTracker,
    transcript: TranscriptWriter,
) -> None:
    """Drive the research pipeline deterministically, gating each phase on disk state."""
    # Phase 0: PLAN — the code (not the lead's judgement) owns the sequence.
    plan_text = await _run_turn(client, _plan_prompt(query), tracker, transcript)
    plan = _parse_plan(plan_text) or [
        {"title": "Research findings", "filename": "findings.md", "brief": query[:200]}
    ]
    print(f"\n[plan] {len(plan)} subtopics: {[s['filename'] for s in plan]}\n")

    # Phase 1: RESEARCH — gate on all planned notes existing.
    await _drive_phase(
        client, tracker, transcript, name="research",
        instruction_for_attempt=lambda a: _research_prompt(
            query, _missing_notes(files_dir, plan), first=(a == 1)
        ),
        is_done=lambda: not _missing_notes(files_dir, plan),
        max_attempts=PHASE_ATTEMPTS["research"],
    )

    # Phase 2: ANALYZE — gate on charts or a data summary existing.
    await _drive_phase(
        client, tracker, transcript, name="analyze",
        instruction_for_attempt=lambda a: _analyze_prompt(),
        is_done=lambda: _analysis_done(files_dir),
        max_attempts=PHASE_ATTEMPTS["analyze"],
    )

    # Phase 3: REPORT — gate on BOTH the markdown (QA reviews it) and the PDF.
    await _drive_phase(
        client, tracker, transcript, name="report",
        instruction_for_attempt=lambda a: _report_prompt(
            first=(a == 1), missing=_report_missing(files_dir)
        ),
        is_done=lambda: _report_done(files_dir),
        max_attempts=PHASE_ATTEMPTS["report"],
    )

    # Phase 4: QA — runs whenever there's a report (markdown preferred) to review.
    if _report_md_path(files_dir).exists() or _final_report_exists(files_dir):
        await _drive_phase(
            client, tracker, transcript, name="qa",
            instruction_for_attempt=lambda a: _qa_prompt(),
            is_done=lambda: _qa_review_path(files_dir).exists(),
            max_attempts=PHASE_ATTEMPTS["qa"],
        )
        # Phase 5: one revision pass if QA flagged material issues.
        if _qa_verdict(files_dir) == "REVISE":
            print("\n[qa] verdict REVISE — running one revision pass.\n")
            await _run_turn(client, _report_prompt(revise=True), tracker, transcript)
        else:
            print(f"\n[qa] verdict: {_qa_verdict(files_dir)}.\n")


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
                await run_pipeline(client, query, files_dir, tracker, transcript)
                if _final_report_exists(files_dir):
                    print("\n[pipeline] final report present.\n")
                else:
                    print("\n[pipeline] finished without a report PDF.\n")
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
