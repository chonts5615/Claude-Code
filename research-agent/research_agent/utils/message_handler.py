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

    # Update the tracker context with the parent_tool_use_id from the message.
    # When a subagent produces a message, parent_tool_use_id points at the Task
    # tool call that spawned it; for the lead agent it is None.
    parent_id = getattr(msg, "parent_tool_use_id", None)
    tracker.set_current_context(parent_id)

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
                subagent_type = block.input.get("subagent_type", "unknown")
                description = block.input.get("description", "no description")
                prompt = block.input.get("prompt", "")

                # Register with the tracker and get the subagent ID back.
                subagent_id = tracker.register_subagent_spawn(
                    tool_use_id=block.id,
                    subagent_type=subagent_type,
                    description=description,
                    prompt=prompt,
                )

                # User-facing output with the subagent ID.
                transcript.write(
                    f"\n\n[\U0001f680 Spawning {subagent_id}: {description}]\n",
                    end="",
                )
