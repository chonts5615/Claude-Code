"""I/O utilities for strategy workflow."""

import json
from pathlib import Path
from typing import Any, Dict

import yaml


def load_yaml(file_path: Path) -> Dict[str, Any]:
    """
    Load YAML file.

    Args:
        file_path: Path to YAML file

    Returns:
        Parsed YAML content as dictionary
    """
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def save_yaml(data: Dict[str, Any], file_path: Path) -> None:
    """
    Save data to YAML file.

    Args:
        data: Dictionary to save
        file_path: Path to output file
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def load_json(file_path: Path) -> Dict[str, Any]:
    """
    Load JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON content as dictionary
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def save_json(data: Dict[str, Any], file_path: Path, indent: int = 2) -> None:
    """
    Save data to JSON file.

    Args:
        data: Dictionary to save
        file_path: Path to output file
        indent: Indentation level for pretty printing
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=indent, default=str)


def ensure_directory(dir_path: Path) -> Path:
    """
    Ensure directory exists, creating if necessary.

    Args:
        dir_path: Directory path

    Returns:
        The directory path
    """
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path
