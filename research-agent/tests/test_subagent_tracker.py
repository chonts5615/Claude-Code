"""Offline tests for SubagentTracker attribution and logging (no SDK/network)."""

import asyncio
import json

from research_agent.utils.subagent_tracker import SubagentTracker


def _run(coro):
    return asyncio.run(coro)


def _records(session_dir):
    path = session_dir / "tool_calls.jsonl"
    text = path.read_text().strip()
    return [json.loads(line) for line in text.splitlines()] if text else []


def test_lead_calls_attributed_to_lead(tmp_path):
    t = SubagentTracker(transcript_writer=None, session_dir=tmp_path)
    payload = {"tool_name": "WebSearch", "tool_input": {"query": "q"}}
    _run(t.pre_tool_use_hook(payload, "tu1", None))
    _run(t.post_tool_use_hook({**payload, "tool_response": "r"}, "tu1", None))
    t.close()

    calls = [r for r in _records(tmp_path) if r["event"] == "tool_call"]
    assert len(calls) == 1
    assert calls[0]["subagent_id"] == "LEAD"


def test_subagent_calls_attributed_by_agent_id(tmp_path):
    t = SubagentTracker(transcript_writer=None, session_dir=tmp_path)
    r1 = {"tool_name": "WebSearch", "tool_input": {}, "agent_id": "abc", "agent_type": "researcher"}
    r2 = {**r1, "agent_id": "def"}

    for payload, tu in [(r1, "1"), (r2, "2"), (r1, "3")]:  # r1 reappears -> stable id
        _run(t.pre_tool_use_hook(payload, tu, None))
        _run(t.post_tool_use_hook({**payload, "tool_response": "r"}, tu, None))
    t.close()

    ids = [r["subagent_id"] for r in _records(tmp_path) if r["event"] == "tool_call"]
    assert ids == ["RESEARCHER-1", "RESEARCHER-2", "RESEARCHER-1"]


def test_spawn_tools_are_skipped(tmp_path):
    t = SubagentTracker(transcript_writer=None, session_dir=tmp_path)
    _run(t.pre_tool_use_hook({"tool_name": "Agent", "tool_input": {}}, "tu1", None))
    _run(t.post_tool_use_hook({"tool_name": "Task", "tool_input": {}}, "tu1", None))
    t.close()

    assert [r for r in _records(tmp_path) if r["event"] == "tool_call"] == []


def test_register_spawn_is_logged(tmp_path):
    t = SubagentTracker(transcript_writer=None, session_dir=tmp_path)
    t.register_subagent_spawn("researcher", "find X")
    t.close()

    recs = _records(tmp_path)
    assert recs[0]["event"] == "subagent_spawn"
    assert recs[0]["subagent_type"] == "researcher"
    assert recs[0]["description"] == "find X"


def test_format_tool_input():
    f = SubagentTracker._format_tool_input
    assert f("WebSearch", {"query": "abc"}) == "abc"
    assert f("Write", {"file_path": "/x/y.md"}) == "/x/y.md"
    assert f("Glob", {"pattern": "*.md"}) == "*.md"
    assert f("Bash", {"command": "echo hi"}) == "echo hi"
    assert f("Bash", {"command": "x" * 200}).endswith("...")
