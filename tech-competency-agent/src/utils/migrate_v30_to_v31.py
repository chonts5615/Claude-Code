"""Stub migrator for v3.0 RunState JSON -> v3.1 schema.

This is a placeholder. The hard-cut migration in `src/schemas/competency.py`
means there is no production v3.0 artifact to convert. When real v3.0 RunState
files exist (e.g. archived runs we want to replay against v3.1), implement the
field-by-field mapping here.
"""

from __future__ import annotations

from typing import Any


def migrate_run_state(v30_state: dict[str, Any]) -> dict[str, Any]:
    raise NotImplementedError(
        "v3.0 -> v3.1 RunState migration is not implemented. The hard-cut "
        "decision means no production v3.0 artifacts exist. Implement this "
        "helper when archived v3.0 runs need to be replayed against v3.1."
    )
