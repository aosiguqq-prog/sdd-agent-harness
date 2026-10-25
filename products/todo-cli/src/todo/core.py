"""Core business logic: pure in-memory operations on the task collection, no file I/O.

Implements SPEC-F-01..04 / SPEC-D-01..02.
Layering per architecture.md ADR-001: core depends on neither storage nor cli, so it can be tested in isolation.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional


class TodoError(Exception):
    """Base class of all business errors in this module."""


class EmptyTextError(TodoError):
    """The task text is empty (SPEC-F-01 / FR-003)."""


class TaskNotFoundError(TodoError):
    """No task exists with the given id (SPEC-F-03/04 / FR-007)."""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"task #{task_id} does not exist")


class StorageCorruptError(TodoError):
    """The data file is corrupt and cannot be parsed (SPEC-N-02 / NFR-002)."""


@dataclass
class Task:
    id: int
    text: str
    done: bool = False


class TodoList:
    """Aggregate root of the to-do list. Ids are assigned monotonically from next_id and never reused (FR-002)."""

    def __init__(self, tasks: Optional[list[Task]] = None, next_id: int = 1) -> None:
        self._tasks: dict[int, Task] = {t.id: t for t in (tasks or [])}
        self._next_id = next_id

    # ---- queries ----
    @property
    def tasks(self) -> list[Task]:
        """Return all tasks in ascending id order (SPEC-F-02 / FR-004)."""
        return [self._tasks[i] for i in sorted(self._tasks)]

    def get(self, task_id: int) -> Task:
        try:
            return self._tasks[task_id]
        except KeyError:
            raise TaskNotFoundError(task_id)

    # ---- commands ----
    def add(self, text: str) -> Task:
        """Add a task (SPEC-F-01 / FR-001/002/003)."""
        text = text.strip()
        if not text:
            raise EmptyTextError("task text must not be empty")
        task = Task(id=self._next_id, text=text, done=False)
        self._tasks[task.id] = task
        self._next_id += 1  # ids are never reused
        return task

    def complete(self, task_id: int) -> Task:
        """Mark as done; idempotent, marking twice is not an error (SPEC-F-03 / FR-006/008)."""
        task = self.get(task_id)
        task.done = True
        return task

    def delete(self, task_id: int) -> None:
        """Delete a task; next_id never goes back, so ids are not reused (SPEC-F-04 / FR-009/002)."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        del self._tasks[task_id]

    # ---- serialisation (supports persistence, SPEC-D-02 / FR-010) ----
    def to_dict(self) -> dict:
        return {
            "next_id": self._next_id,
            "tasks": [asdict(self._tasks[i]) for i in sorted(self._tasks)],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TodoList":
        tasks = [Task(**t) for t in data.get("tasks", [])]
        next_id = data.get("next_id", max((t.id for t in tasks), default=0) + 1)
        return cls(tasks=tasks, next_id=next_id)
