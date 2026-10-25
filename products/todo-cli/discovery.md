# Discovery · todo-cli

> Stage 1 artifact. Clarifies a one-line request into a bounded, unambiguous shared understanding.

## Background and goals
- **Problem**: record and manage daily tasks quickly in the terminal, without opening a GUI app.
- **What success looks like**: the user can add a task, view the list, mark a task done and delete a task with short commands, and the data is still there after a restart.

## Users and roles
| Role | Description | Cares about |
|------|-------------|-------------|
| Terminal user | An individual who is comfortable with the command line | Short commands, clear feedback, no data loss |

## Core business events (event storming)
- **Task added**: the user submits task text → the system stores it in the list and assigns an id.
- **List viewed**: the user asks to see the list → the system shows every task and its status (open / done).
- **Task completed**: the user marks a task done by id → its status becomes done.
- **Task deleted**: the user deletes a task by id → it is removed from the list.
- **Data persisted**: after any change, the list is written to a local JSON file so nothing is lost on restart.

## Scope
- ✅ **In scope (first version)**:
  1. Add a task (`add`)
  2. List tasks (`list`, distinguishing open / done)
  3. Mark as done (`done <id>`)
  4. Delete a task (`delete <id>`)
  5. Local JSON-file persistence
- ❌ **Out of scope (explicitly not in the first version)**: priorities, due dates, tags, search, sub-tasks, multiple lists, reminders, sync / cloud, undo.

## Ubiquitous language · glossary
| Term | Meaning |
|------|---------|
| Task | One thing the user has to do: text, id, completion status |
| Id | The stable identifier of a task, used to complete / delete it |
| Status | One of two task states: open / done |
| List | The collection of all current tasks, persisted in a local JSON file |

## Interaction and storage decisions (confirmed at this stage)
- **Interaction**: sub-command CLI, e.g. `todo add "Buy milk"`, `todo list`, `todo done 3`, `todo delete 3`.
- **Storage**: local JSON file (default `~/.todo.json`, configurable later).

## Key risks and open questions
- [ ] Id strategy: are ids reused after deletion? **Default assumption**: ids increase monotonically and are never reused (more stable, better for traceability).
- [ ] Empty list / unknown id: needs a friendly message (to be refined in requirements / spec).
- [ ] Missing or corrupt JSON file: created automatically on first run; handling of corruption to be refined in the spec.
