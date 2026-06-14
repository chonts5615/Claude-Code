"""Offline tests for process_assistant_message (no SDK/network)."""

import research_agent.utils.message_handler as mh
from research_agent.utils.message_handler import process_assistant_message


class TextBlock:
    def __init__(self, text):
        self.text = text


class ToolUseBlock:
    def __init__(self, id, name, input):
        self.id = id
        self.name = name
        self.input = input


class AssistantMessage:
    def __init__(self, content):
        self.content = content


class FakeTracker:
    def __init__(self):
        self.spawns = []

    def register_subagent_spawn(self, subagent_type, description):
        self.spawns.append((subagent_type, description))


class FakeTranscript:
    def __init__(self):
        self.chunks = []

    def write(self, text, end="", flush=True):
        self.chunks.append(text)

    @property
    def text(self):
        return "".join(self.chunks)


def test_text_block_is_written():
    mh._tool_just_used = False
    tx = FakeTranscript()
    process_assistant_message(AssistantMessage([TextBlock("hello world")]), FakeTracker(), tx)
    assert "hello world" in tx.text


def test_agent_spawn_is_announced():
    mh._tool_just_used = False
    tr, tx = FakeTracker(), FakeTranscript()
    block = ToolUseBlock("t1", "Agent", {"subagent_type": "researcher", "description": "find X"})
    process_assistant_message(AssistantMessage([block]), tr, tx)

    assert tr.spawns == [("researcher", "find X")]
    assert "Spawning researcher subagent: find X" in tx.text


def test_legacy_task_name_is_also_announced():
    mh._tool_just_used = False
    tr, tx = FakeTracker(), FakeTranscript()
    block = ToolUseBlock("t1", "Task", {"subagent_type": "data-analyst", "description": "chart it"})
    process_assistant_message(AssistantMessage([block]), tr, tx)

    assert tr.spawns == [("data-analyst", "chart it")]


def test_non_spawn_tool_blocks_are_not_announced():
    mh._tool_just_used = False
    tr, tx = FakeTracker(), FakeTranscript()
    block = ToolUseBlock("t1", "WebSearch", {"query": "q"})
    process_assistant_message(AssistantMessage([block]), tr, tx)

    assert tr.spawns == []  # surfaced via tracker hooks instead
