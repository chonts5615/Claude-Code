# Multi-Agent Research System

A small multi-agent research system built on the [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python).
A **Lead Agent** breaks a request into subtopics and orchestrates a team of
specialized subagents to research the web, analyze the findings, and produce a
polished PDF report — all from a single interactive prompt.

This is an independent re-implementation of the structure demonstrated in
Anthropic's [`research-agent`](https://github.com/anthropics/claude-agent-sdk-demos/tree/main/research-agent)
demo, written from scratch.

## Architecture

The Lead Agent's only tool is `Task`. It delegates every step to three
specialized subagents defined via `AgentDefinition`:

| Step | Mechanism | Purpose |
|------|-----------|---------|
| **Lead Agent** | `Task` | Spawns the research/analysis subagents for the phases the orchestrator drives |
| **researcher** (subagent) | `WebSearch`, `Write` | Web research → Markdown notes in `files/research_notes/` |
| **data-analyst** (subagent) | `Glob`, `Read`, `Bash`, `Write` | Extracts metrics, renders charts to `files/charts/`, summary to `files/data/` |
| **report generation** | controlled `query()` | Synthesizes the report as Markdown → `files/reports/report.md` (text captured in code) |
| **PDF render** | code (`render.py`) | Deterministically renders the branded PDF from `report.md` + charts |
| **QA review** | controlled `query()` | Critically reviews the report → `files/reports/qa_review.md` (PASS/REVISE) |

Report generation and QA run as **controlled, tool-less `query()` calls whose
text is captured and written to disk in code** — subagents reliably compose text
but inconsistently call the `Write` tool, so the file-creation is owned by the
orchestrator. Web research and chart analysis remain parallel subagents.

### Deterministic orchestration

A code-driven state machine (`run_pipeline`) — not the lead agent's judgement —
sequences the work and gates each phase on a filesystem check, retrying only the
missing piece:

1. **Plan** — the lead emits a JSON subtopic list, which the code parses.
2. **Research** — one researcher per subtopic, in parallel; gate: all notes exist.
3. **Analyze** — the data-analyst builds charts + a data summary.
4. **Report** — the report-writer writes `report.md`; the **branded PDF is then
   rendered deterministically in code** (`research_agent/render.py`) from the
   markdown + charts + brand config (no agent-driven PDF building).
5. **QA** — a critique emits PASS/REVISE; a REVISE regenerates the report and
   re-renders, then re-reviews, looping until it passes or `MAX_QA_ROUNDS` (3).

The report-writer and qa-reviewer run on at least **sonnet** (`heavy_model`); the
researchers and analyst use the lighter default model.

### Quality skills

Three skill specs under `.claude/skills/` are embedded in the pipeline:

- **report-branding** — the brand spec applied by the PDF renderer (configurable
  via `config/brand.json` / `--brand-config`; neutral default).
- **report-format-qc** — formatting/consistency checks, embedded in QA.
- **io-psych-exec-review** — QA review through an I-O psychology
  research-practitioner and a principal executive consultant lens.

### Subagent tracking & logging

SDK `PreToolUse` / `PostToolUse` hooks track every tool call and attribute it to
the subagent that made it (e.g. `RESEARCHER-1`). Each session writes two logs to
`logs/session_<timestamp>/`:

- `transcript.txt` — a human-readable transcript of the conversation.
- `tool_calls.jsonl` — one structured JSON record per tool call (agent id, tool,
  input, output, timestamp).

## Project layout

```
research-agent/
├── research_agent/
│   ├── agent.py                 # Entry point: defines agents, hooks, chat loop
│   ├── prompts/                 # System prompt per agent (.txt)
│   │   ├── lead_agent.txt
│   │   ├── researcher.txt
│   │   ├── data_analyst.txt
│   │   └── report_writer.txt
│   └── utils/
│       ├── subagent_tracker.py  # Hook-based tool-call tracking + JSONL log
│       ├── transcript.py        # Session setup + transcript writer
│       └── message_handler.py   # Streams assistant messages to the transcript
├── .claude/commands/            # Slash commands (/research, /fact-check, …)
├── files/                       # Runtime outputs (notes, data, charts, reports)
├── logs/                        # Per-session transcripts + tool-call logs
├── .env.example
└── pyproject.toml
```

## Setup

Requires Python 3.10+. Using [`uv`](https://github.com/astral-sh/uv):

```bash
cd research-agent
uv sync                       # or: pip install -e .
cp .env.example .env          # then add your ANTHROPIC_API_KEY
```

Get an API key at https://console.anthropic.com/settings/keys.

### Running in a container as root

The agent uses `permission_mode="bypassPermissions"` so subagents can run their
tools non-interactively. Under the hood the SDK launches the `claude` CLI with
`--dangerously-skip-permissions`, which the CLI **refuses to run as root** (e.g.
in a Docker image or CI runner that defaults to UID 0). If you see:

```
--dangerously-skip-permissions cannot be used with root/sudo privileges for security reasons
```

either run as a non-root user, or — only inside a disposable sandbox/container —
set `IS_SANDBOX=1` to allow it:

```bash
IS_SANDBOX=1 uv run python -m research_agent.agent
```

In a [managed Claude Code environment](https://code.claude.com/docs/en/claude-code-on-the-web)
the authenticated `claude` CLI also supplies credentials, so a separate
`ANTHROPIC_API_KEY` isn't required (the startup check accepts either).

## Usage

### Interactive

```bash
uv run python -m research_agent.agent   # or: research-agent
```

Then research any topic in natural language, or use a slash command:

```
You: /research electric vehicle adoption in Europe 2024
You: /competitive-analysis Notion vs Obsidian vs Roam
You: /market-trends global solar energy market
You: /fact-check "the human body has 206 bones"
You: /summarize
```

Type `exit` to quit. When you do, the paths to the session transcript and
tool-call log are printed.

### One-shot (non-interactive)

Useful for automation and long unattended runs:

```bash
research-agent --query "EV adoption in Norway: market share, growth, drivers"
research-agent --query-file brief.txt          # read the request from a file
research-agent --query "..." --model sonnet     # override the model (default: haiku)
```

Outputs always land under `./files/` (created automatically) relative to the
directory you launch from — `research_notes/`, `data/`, `charts/`, `reports/`.

## Tests

Offline unit tests (no API key or network needed) cover the tracker attribution
logic, the message handler, and output-path handling:

```bash
pip install -e ".[dev]"
pytest
```

## How it maps to the Agent SDK

- `AgentDefinition` defines each subagent's tools, model, and system prompt.
- `ClaudeAgentOptions(allowed_tools=["Task"], agents=...)` restricts the lead
  agent to delegation only.
- `setting_sources=["project"]` loads the `.claude/` commands and any skills.
- `HookMatcher` wires the tracker into `PreToolUse` / `PostToolUse`.
- `permission_mode="bypassPermissions"` lets subagents run their tools without
  interactive prompts (this is a non-interactive batch workflow).
