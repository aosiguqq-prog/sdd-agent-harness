# Functional specification · todo-cli

> IDs SPEC-F-xx, each mapping to requirements and scenarios. Describes what the system must do — testable and unambiguous.

## Overview
Single-user, single-machine command-line task management: add / view / change status / delete tasks, with persistence.

## Function list
| ID | Function | Requirements | Scenarios |
|----|----------|--------------|-----------|
| SPEC-F-01 | Add a task | FR-001/002/003 | add_task |
| SPEC-F-02 | View the list | FR-004/005 | list_tasks |
| SPEC-F-03 | Mark as done | FR-006/007/008 | complete_task |
| SPEC-F-04 | Delete a task | FR-007/009 | delete_task |
| SPEC-F-05 | Persistence and initialisation | FR-010/011 | discovery |

## Detailed specification

### SPEC-F-01 Add a task
- **Source**: FR-001/002/003
- **Input**: task text
- **Main flow**:
  1. `strip()` the text.
  2. If the result is empty → reject with the error "task text must not be empty"; the list is unchanged.
  3. Otherwise take the current `next_id` as the new id and append `{id, text, done: false}`.
  4. `next_id += 1` (increasing, never reused).
  5. Persist. Report success, including the assigned id.
- **Business rule**: ids come from `next_id`; used ids are never recycled.
- **Test points**: count +1, correct fields, status open, unique increasing id; empty text rejected with the count unchanged.

### SPEC-F-02 View the list
- **Source**: FR-004/005
- **Main flow**:
  1. Read all tasks.
  2. Empty → show the friendly "list is empty" message.
  3. Not empty → print each task in ascending id order: id, status marker, text.
- **Status markers**: open `[ ]`, done `[x]` (see CLI spec SPEC-C-06).
- **Test points**: all entries listed with complete fields and distinguishable status; empty list shows the message and no entries.

### SPEC-F-03 Mark as done
- **Source**: FR-006/007/008
- **Input**: id
- **Main flow**:
  1. Look up the task by id.
  2. Not found → error "task #{id} does not exist"; data unchanged.
  3. Found → set `done` to true (if already true, keep it and report no error).
  4. Persist. Report success.
- **Test points**: target becomes done; unknown id gives a message and changes nothing; marking twice is not an error and keeps the status.

### SPEC-F-04 Delete a task
- **Source**: FR-007/009
- **Input**: id
- **Main flow**:
  1. Look up the task by id.
  2. Not found → error "task #{id} does not exist"; data unchanged.
  3. Found → remove it from the tasks; **leave `next_id` untouched** (ids are not reused).
  4. Persist. Report success.
- **Test points**: count −1, target gone, other ids unchanged; unknown id gives a message with the count unchanged; a task added after deletion gets an id greater than the deleted one.

### SPEC-F-05 Persistence and initialisation
- **Source**: FR-010/011
- **Rules**: see data spec SPEC-D-03 (created on first run, written after every change, atomic writes, corrupt files never overwritten).
- **Test points**: data identical after a process restart; first run creates the file without errors.

## General error handling (SPEC-F-06)
Every user-facing error returns a short, clear message; raw tracebacks are never shown to the user (NFR-001).
Error classes: empty text, unknown id, corrupt data file.
