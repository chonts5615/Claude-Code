"""Ensure the package root is importable when running tests without an install."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
