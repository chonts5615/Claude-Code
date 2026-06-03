"""Message handling for processing agent responses."""

from typing import Any

# Names under which the SDK surfaces a subagent spawn. Older builds used
# "Task"; current builds (>=0.2) emit the tool-use block as "Agent".
SPAWN_TOOL_NAMES = {"Task", "Agent"}

# Track whether a tool was just used (for formatting purposes).
_tool_just_used = False


def process_assistant_message(msg: Any, tracker: Any, transcript: Any) -> None:
    """Process an AssistantMessage and write its output to the transcript.

    Args:
        msg: The AssistantMessage to process.
        tracker: The SubagentTracker instance.
        transcript: The TranscriptWriter instance.
    """
    global _tool_just_used

    for block in msg.content:
        block_type = type(block).__name__

        if block_type == "TextBlock":
            # Add a newline if a tool was just used, to separate the output.
            if _tool_just_used:
                transcript.write("\n", end="")
                _tool_just_used = False
            transcript.write(block.text, end="")

        elif block_type == "ToolUseBlock":
            # Mark that a tool was used.
            _tool_just_used = True

            # Only subagent-spawn tools are surfaced to the user here; all
            # other tool calls are reported via the tracker hooks.
            if block.name in SPAWN_TOOL_NAMES:
                subagent_type = block.input.get("subagent_type", "subagent")
                description = block.input.get("description", "no description")

                # Log the spawn. Per-subagent run ids (RESEARCHER-1, ...) are
                # minted by the tracker hooks from the SDK's agent_id, so a
                # numbered id is intentionally not used in this announcement.
                tracker.register_subagent_spawn(subagent_type, description)

                # User-facing output.
                transcript.write(
                    f"\n\n[\U0001f680 Spawning {subagent_type} subagent: {description}]\n",
                    end="",
                )
