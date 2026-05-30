"""Transcript handling for conversation history."""

import logging
from datetime import datetime
from pathlib import Path


def setup_session() -> tuple[Path, Path]:
    """Set up the session directory and transcript file.

    Creates a session folder in logs/ with a timestamp, containing both the
    transcript and the detailed tool-call logs.

    Returns:
        Tuple of (transcript_file_path, session_dir_path).
    """
    # Create the session directory.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = Path("logs") / f"session_{timestamp}"
    session_dir.mkdir(parents=True, exist_ok=True)

    # Transcript file lives inside the session directory.
    transcript_file = session_dir / "transcript.txt"

    # Suppress noisy HTTP debug logs from urllib3.
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

    return transcript_file, session_dir


class TranscriptWriter:
    """Helper to write output to both the console and a transcript file."""

    def __init__(self, transcript_file: Path):
        self.file = open(transcript_file, "w", encoding="utf-8")

    def write(self, text: str, end: str = "", flush: bool = True) -> None:
        """Write text to both the console and the transcript."""
        print(text, end=end, flush=flush)
        self.file.write(text + end)
        if flush:
            self.file.flush()

    def write_to_file(self, text: str, flush: bool = True) -> None:
        """Write text to the transcript file only (not the console)."""
        self.file.write(text)
        if flush:
            self.file.flush()

    def close(self) -> None:
        """Close the transcript file."""
        self.file.close()

    def __enter__(self) -> "TranscriptWriter":
        return self

    def __exit__(self, *_args: object) -> bool:
        self.close()
        return False
