"""Persistence layer: local JSON read / write. Implements SPEC-D-03 / SPEC-N-02.

Key points (architecture.md ADR-002/003):
- On first run, a missing file is created as an empty list (FR-011).
- Writes go to a temporary file and are swapped in atomically with os.replace,
  so a failure halfway cannot corrupt the original file (NFR-002).
- A parse failure raises StorageCorruptError and never overwrites the original file (NFR-002).
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Union

from todo.core import TodoList, StorageCorruptError

PathLike = Union[str, "os.PathLike[str]"]

DEFAULT_PATH = Path.home() / ".todo.json"
_EMPTY = {"next_id": 1, "tasks": []}


def load(path: PathLike = DEFAULT_PATH) -> TodoList:
    """Load the list; if the file does not exist, create it and return an empty list."""
    p = Path(path)
    if not p.exists():
        _write_atomic(p, _EMPTY)
        return TodoList.from_dict(_EMPTY)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError) as exc:
        raise StorageCorruptError(f"the data file is corrupt: {p}") from exc
    return TodoList.from_dict(data)


def save(path: PathLike, todolist: TodoList) -> None:
    """Write the list atomically."""
    _write_atomic(Path(path), todolist.to_dict())


def _write_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2)
    # write to a temp file in the same directory, then swap atomically, so the original is never half-written
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".todo-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
