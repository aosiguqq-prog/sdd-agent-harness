# Data specification · todo-cli

> IDs SPEC-D-xx. Domain model and data dictionary.

## Domain model
A single entity, **Task**; the collection is persisted as a local JSON file.

## Entity dictionary

### SPEC-D-01 Task
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| id | int | yes | ≥ 1, monotonically increasing, globally unique, never reused after deletion | Task id (FR-002) |
| text | str | yes | non-empty after stripping surrounding whitespace | Task text (FR-001/003) |
| done | bool | yes | default false | Completion status (FR-006) |

- **Invariants**:
  - `id` is unique and never reused for the lifetime of the file (relies on `next_id` in SPEC-D-02).
  - `text` must not be empty after `strip()`.

### SPEC-D-02 Storage file structure
Local JSON file (default `~/.todo.json`), root object:
```json
{
  "next_id": 4,
  "tasks": [
    { "id": 1, "text": "Buy milk", "done": false },
    { "id": 3, "text": "Pay rent", "done": true }
  ]
}
```
- `next_id`: the next id to assign; incremented after every add (guarantees non-reuse, FR-002).
- `tasks`: array of tasks, stored in ascending id order.

## Data lifecycle / persistence rules (SPEC-D-03)
- **First run**: if the file does not exist, create it as `{"next_id": 1, "tasks": []}` (FR-011).
- **Write after every change**: persist immediately after a successful add / done / delete (FR-010).
- **Safe writes**: write to a temporary file, then swap it in atomically (`os.replace`), so a failure halfway cannot corrupt the original (NFR-002).
- **Corruption**: if JSON parsing fails, report the corrupt file and stop; never overwrite the original (NFR-001/002).
- **Encoding**: UTF-8 with `ensure_ascii=False`, so non-ASCII text is stored as-is.
