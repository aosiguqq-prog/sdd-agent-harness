"""CLI layer: argparse sub-commands -> core / storage -> formatted output.

Implements SPEC-C-01..07. Exit codes: 0 success / 1 user error / 2 runtime error (e.g. corrupt data file).
Errors go to stderr and never expose a raw traceback (SPEC-N-01 / NFR-001).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from todo import storage
from todo.core import EmptyTextError, TaskNotFoundError, StorageCorruptError

EXIT_OK = 0
EXIT_USER_ERROR = 1
EXIT_RUNTIME_ERROR = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo", description="Command-line to-do list: add / list / done / delete"
    )
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("text", help="task text")

    sub.add_parser("list", help="list all tasks")

    p_done = sub.add_parser("done", help="mark a task as done by id")
    p_done.add_argument("id", type=int, help="task id")

    p_del = sub.add_parser("delete", help="delete a task by id")
    p_del.add_argument("id", type=int, help="task id")

    return parser


def _format_task(task) -> str:
    mark = "[x]" if task.done else "[ ]"
    return f"#{task.id} {mark} {task.text}"


def main(argv: Optional[Sequence[str]] = None, path=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    data_path = Path(path) if path is not None else storage.DEFAULT_PATH

    if not args.command:
        parser.print_help()
        return EXIT_OK

    try:
        todolist = storage.load(data_path)
    except StorageCorruptError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return EXIT_RUNTIME_ERROR
    except OSError as exc:
        print(f"Error: cannot access the data file ({exc.strerror or exc})", file=sys.stderr)
        return EXIT_RUNTIME_ERROR

    try:
        if args.command == "add":
            task = todolist.add(args.text)
            storage.save(data_path, todolist)
            print(f"Added #{task.id}: {task.text}")

        elif args.command == "list":
            tasks = todolist.tasks
            if not tasks:
                print("The list is empty. Add a task with: todo add")
            else:
                for t in tasks:
                    print(_format_task(t))

        elif args.command == "done":
            todolist.complete(args.id)
            storage.save(data_path, todolist)
            print(f"Completed #{args.id}")

        elif args.command == "delete":
            todolist.delete(args.id)
            storage.save(data_path, todolist)
            print(f"Deleted #{args.id}")

    except (EmptyTextError, TaskNotFoundError) as exc:
        # user error: friendly message, exit code 1 (SPEC-N-01 / NFR-001)
        print(f"Error: {exc}", file=sys.stderr)
        return EXIT_USER_ERROR
    except OSError as exc:
        # review finding #1: runtime errors such as a failed disk write never show a raw traceback (NFR-001)
        print(f"Error: cannot save the data ({exc.strerror or exc})", file=sys.stderr)
        return EXIT_RUNTIME_ERROR

    return EXIT_OK


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
