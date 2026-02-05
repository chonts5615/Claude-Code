"""Logging utilities for strategy workflow."""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    structured: bool = False
) -> None:
    """
    Set up logging configuration.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional path to log file
        structured: Whether to use structured JSON logging
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Format string
    if structured:
        fmt = '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}'
    else:
        fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    # Configure handlers
    handlers = [logging.StreamHandler(sys.stdout)]

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))

    # Apply configuration
    logging.basicConfig(
        level=log_level,
        format=fmt,
        handlers=handlers,
        force=True
    )

    # Quiet noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name.

    Args:
        name: Logger name (usually module name)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
