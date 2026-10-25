# Requirements · todo-cli

> Stage 3 artifact. Every requirement has a unique ID and is traceable and verifiable.

## 1. Functional requirements (FR)

| ID | Requirement | Priority | Acceptance criteria | Source scenario |
|----|-------------|----------|---------------------|-----------------|
| FR-001 | The user can add a task with text; the system assigns a unique id and sets it to open | Must | After adding, the list has +1 task with the right text, status open and a unique id | add_task: add a task |
| FR-002 | Ids increase monotonically and are never reused after deletion | Must | Consecutive adds give increasing ids; after deleting an id, a new task gets a larger one | add_task: ids increase / delete_task: id not reused |
| FR-003 | The system rejects tasks with empty text and says why | Must | Empty text is rejected with a message; the list is unchanged | add_task: reject empty text |
| FR-004 | The user can view all tasks, each with id, text and status, open and done distinguishable | Must | All entries listed with complete fields and distinguishable status | list_tasks: list open and done tasks |
| FR-005 | Viewing an empty list shows a friendly message and no entries | Should | An "empty list" message is shown | list_tasks: empty list |
| FR-006 | The user can mark a task as done by id | Must | The given task's status becomes done | complete_task: mark as done |
| FR-007 | Completing / deleting an unknown id gives a friendly message and changes no data | Must | A "does not exist" message; other data unchanged | complete_task / delete_task: unknown id |
| FR-008 | Marking a done task again is not an error; it stays done | Should | No error, status unchanged | complete_task: mark again |
| FR-009 | The user can delete a task by id; other tasks and their ids are unchanged | Must | The list has −1 task, the target is gone, other ids unchanged | delete_task: delete a task |
| FR-010 | All changes are persisted to a local JSON file and survive a restart | Must | After a process restart the list is identical | discovery: data persisted |
| FR-011 | If the data file does not exist, it is created on first run | Must | First run does not fail and creates the data file | discovery: open question → default |

## 2. Non-functional requirements (NFR)

| ID | Category | Requirement (measurable) | Acceptance criteria |
|----|----------|--------------------------|---------------------|
| NFR-001 | Usability | Every error (empty text, unknown id, empty list) gives a clear message; no raw tracebacks | Only friendly messages are seen on every error path |
| NFR-002 | Reliability | Reading / writing the data file must never lose existing data because of a single failure | A failed write leaves the original file intact |
| NFR-003 | Maintainability | Business logic decoupled from CLI and storage; line coverage ≥ 80%, core branch coverage ≥ 90% | Coverage report meets the thresholds |
| NFR-004 | Portability | Python standard library only; no network or extra services | Runs directly in a clean environment |
| NFR-005 | Performance | Each command responds in < 200 ms at normal scale (≤ 1000 tasks) | Local manual test / benchmark |

## 3. Constraints and assumptions
- Constraints: Python 3.11+; standard library only (json, argparse, …).
- Assumptions: single user, single machine, no concurrent writes; data file defaults to `~/.todo.json`.

## 4. Traceability matrix (FR ⇄ scenario)

| Requirement | Related scenarios |
|-------------|-------------------|
| FR-001 | add_task: add a task |
| FR-002 | add_task: ids increase; delete_task: id not reused |
| FR-003 | add_task: reject empty text |
| FR-004 | list_tasks: list open and done tasks |
| FR-005 | list_tasks: empty list |
| FR-006 | complete_task: mark as done |
| FR-007 | complete_task / delete_task: unknown id |
| FR-008 | complete_task: mark again |
| FR-009 | delete_task: delete a task |
| FR-010 | discovery: data persisted |
| FR-011 | discovery: open question (default: create automatically) |

## 5. Open questions
- [ ] Is a `clear` (delete everything) command needed? **Default assumption**: not in the first version (out of scope).
- [ ] Should the data-file path be overridable via an environment variable? **Default assumption**: fixed default path in the first version, with room to extend.
