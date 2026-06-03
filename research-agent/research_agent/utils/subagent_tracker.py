"""Tracking of subagent tool calls via Claude Agent SDK hooks.

Every tool call flows through the ``PreToolUse`` / ``PostToolUse`` hooks. The SDK
includes ``agent_id`` and ``agent_type`` in the hook payload for calls made by a
subagent (the lead agent's own calls omit them), so each call can be attributed
to the exact subagent that made it — independent of message ordering and safe
under parallel subagents.

The tracker mints a stable, human-readable id per subagent (e.g. ``RESEARCHER-1``)
the first time it sees that subagent's ``agent_id``, prints a readable line to
the transcript, and appends a structured record to ``tool_calls.jsonl``. The
message handler additionally calls :meth:`register_subagent_spawn` so spawns are
announced to the user and logged as they happen.
"""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# Map an agent/subagent type to a short id prefix.
_TYPE_PREFIXES = {
    "researcher": "RESEARCHER",
    "data-analyst": "DATA-ANALYST",
    "report-writer": "REPORT-WRITER",
}

# Identifier used for tool calls made directly by the lead/main agent.
_LEAD_ID = "LEAD"

# Tool names under which the SDK surfaces a subagent spawn. These are announced
# by the message handler, so the hooks skip them to avoid double-counting.
# "Task" is the legacy name; current SDK builds emit "Agent".
_SPAWN_TOOLS = {"Task", "Agent"}


@dataclass
class ToolCallRecord:
    """A single tool invocation made by an agent."""

    subagent_id: str
    tool_name: str
    tool_input: dict
    timestamp: str
    output: Optional[str] = None
    error: Optional[str] = None


@dataclass
class SubagentSession:
    """Execution context for one spawned subagent."""

    subagent_id: str
    subagent_type: str
    spawned_at: str
    tool_calls: list = field(default_factory=list)


class SubagentTracker:
    """Track and log all tool calls, attributing them to the right agent."""

    def __init__(self, transcript_writer: Any = None, session_dir: Optional[Path] = None):
        self.transcript = transcript_writer
        self.session_dir = session_dir

        # Per-prefix counters for minting ids like RESEARCHER-1, RESEARCHER-2.
        self._counters: dict[str, int] = {}

        # SDK agent_id -> our stable subagent_id.
        self._id_by_agent: dict[str, str] = {}

        # subagent_id -> SubagentSession.
        self.sessions: dict[str, SubagentSession] = {}

        # tool_use_id -> ToolCallRecord for in-flight calls (pre -> post).
        self._pending: dict[str, ToolCallRecord] = {}

        # Structured JSONL log.
        self._jsonl = None
        if session_dir is not None:
            self._jsonl = open(session_dir / "tool_calls.jsonl", "w", encoding="utf-8")

    # ------------------------------------------------------------------ #
    # Subagent registration / attribution
    # ------------------------------------------------------------------ #
    def register_subagent_spawn(self, subagent_type: str, description: str) -> None:
        """Log a subagent spawn announced by the message handler."""
        self._write_jsonl(
            {
                "event": "subagent_spawn",
                "subagent_type": subagent_type,
                "description": description,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def _resolve_subagent_id(self, input_data: dict) -> str:
        """Return the stable id of the agent that made this tool call.

        Uses ``agent_id`` / ``agent_type`` from the hook payload; calls without
        an ``agent_id`` were made by the lead agent.
        """
        agent_id = input_data.get("agent_id")
        if not agent_id:
            return _LEAD_ID
        if agent_id in self._id_by_agent:
            return self._id_by_agent[agent_id]

        agent_type = input_data.get("agent_type", "subagent")
        prefix = _TYPE_PREFIXES.get(agent_type, agent_type.upper())
        self._counters[prefix] = self._counters.get(prefix, 0) + 1
        subagent_id = f"{prefix}-{self._counters[prefix]}"

        self._id_by_agent[agent_id] = subagent_id
        self.sessions[subagent_id] = SubagentSession(
            subagent_id=subagent_id,
            subagent_type=agent_type,
            spawned_at=datetime.now().isoformat(),
        )
        return subagent_id

    # ------------------------------------------------------------------ #
    # Hooks
    # ------------------------------------------------------------------ #
    async def pre_tool_use_hook(
        self, input_data: dict, tool_use_id: Optional[str], context: Any
    ) -> dict:
        """Record the start of a tool call and print a readable line."""
        tool_name = input_data.get("tool_name", "unknown")
        tool_input = input_data.get("tool_input", {}) or {}

        # Subagent spawns are surfaced by the message handler, not here.
        if tool_name in _SPAWN_TOOLS:
            return {}

        subagent_id = self._resolve_subagent_id(input_data)
        record = ToolCallRecord(
            subagent_id=subagent_id,
            tool_name=tool_name,
            tool_input=tool_input,
            timestamp=datetime.now().isoformat(),
        )
        if tool_use_id:
            self._pending[tool_use_id] = record

        summary = self._format_tool_input(tool_name, tool_input)
        if self.transcript is not None:
            self.transcript.write(f"\n  [{subagent_id}] {tool_name}: {summary}", end="")

        return {}

    async def post_tool_use_hook(
        self, input_data: dict, tool_use_id: Optional[str], context: Any
    ) -> dict:
        """Attach the result to the pending record and log it."""
        tool_name = input_data.get("tool_name", "unknown")
        if tool_name in _SPAWN_TOOLS:
            return {}

        record = self._pending.pop(tool_use_id, None) if tool_use_id else None
        if record is None:
            record = ToolCallRecord(
                subagent_id=self._resolve_subagent_id(input_data),
                tool_name=tool_name,
                tool_input=input_data.get("tool_input", {}) or {},
                timestamp=datetime.now().isoformat(),
            )

        response = input_data.get("tool_response")
        record.output = self._stringify_response(response)

        session = self.sessions.get(record.subagent_id)
        if session is not None:
            session.tool_calls.append(record)

        self._write_jsonl({"event": "tool_call", **asdict(record)})
        return {}

    # ------------------------------------------------------------------ #
    # Formatting / output helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _format_tool_input(tool_name: str, tool_input: dict) -> str:
        """Produce a short, human-readable summary of a tool's input."""
        if tool_name == "WebSearch":
            return tool_input.get("query", "")
        if tool_name in ("Write", "Read", "Edit"):
            return tool_input.get("file_path", "")
        if tool_name == "Glob":
            return tool_input.get("pattern", "")
        if tool_name == "Bash":
            command = tool_input.get("command", "")
            return command if len(command) <= 80 else command[:77] + "..."
        if tool_name == "Skill":
            return tool_input.get("command", tool_input.get("skill", ""))
        # Fallback: compact JSON of the first couple of keys.
        try:
            return json.dumps(tool_input)[:80]
        except (TypeError, ValueError):
            return str(tool_input)[:80]

    @staticmethod
    def _stringify_response(response: Any) -> Optional[str]:
        """Best-effort conversion of a tool response to a short string."""
        if response is None:
            return None
        if isinstance(response, str):
            text = response
        else:
            try:
                text = json.dumps(response)
            except (TypeError, ValueError):
                text = str(response)
        return text if len(text) <= 2000 else text[:2000] + "...[truncated]"

    def _write_jsonl(self, obj: dict) -> None:
        if self._jsonl is not None:
            self._jsonl.write(json.dumps(obj) + "\n")
            self._jsonl.flush()

    def close(self) -> None:
        """Flush and close the JSONL log."""
        if self._jsonl is not None:
            self._jsonl.close()
            self._jsonl = None
