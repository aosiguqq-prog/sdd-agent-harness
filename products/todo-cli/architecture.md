# Architecture and stack selection · todo-cli

> Stage 5 artifact (stack-advisor).

## Selected stack
- Profile: `framework/stacks/python`
- Language: Python 3.11+, standard library only
- Rationale (with reference to the NFRs):
  - NFR-004 requires zero external dependencies → the standard-library `json` / `argparse` / `os` / `tempfile` cover every need.
  - A single-machine CLI with no web or concurrency needs requires no framework.
  - The pytest + behave test chain is mature and suits TDD / BDD.

## Candidate comparison
| Candidate | Fit | Familiarity / ecosystem | Risk | Verdict |
|-----------|-----|-------------------------|------|---------|
| Python standard library (argparse) | high | high | low | ✅ selected |
| Python + Typer / Click | medium | high | one extra dependency, violates NFR-004 | no |
| Node.js + commander | medium | medium | extra burden unrelated to the goal of validating the pipeline | no |

## Architecture decision records (ADR)

### ADR-001 Three layers (core / storage / cli)
- Context: NFR-003 demands high maintainability and testability; TDD needs business logic that can be tested without file I/O.
- Decision: three layers — `core` holds pure business logic (operates on the in-memory task collection, never touches disk), `storage` handles JSON read / write and atomic writes, `cli` handles argparse parsing and output formatting.
- Trade-off: a single file would be shorter but harder to test and maintain; layers mean a few more files, but each can be test-driven independently.
- Consequence: core is fully unit-testable without any files, so the coverage target is easy to reach.

### ADR-002 Persist next_id so ids are never reused
- Decision: store `next_id` in the data file instead of computing `max(id) + 1`, so ids are not reused even after deletion (FR-002).

### ADR-003 Atomic writes
- Decision: `storage` writes to a temporary file and swaps it in with `os.replace` (NFR-002).

## Modules and directory structure
```
products/todo-cli/
├── src/todo/
│   ├── __init__.py
│   ├── core.py        # TodoList: add / list / complete / delete (pure logic, in memory)
│   ├── storage.py     # load / save JSON, atomic writes, created on first run
│   └── cli.py         # argparse sub-commands → core / storage → formatted output
├── tests/
│   ├── test_core.py        # business-logic unit tests (where most of the TDD happens)
│   ├── test_storage.py     # read / write / atomicity / corruption handling
│   └── test_cli.py         # command parsing and output (data file injected via a temp path)
├── features/          # Gherkin from stage 2
│   └── steps/         # behave step definitions (acceptance tests, late stage 6)
├── pyproject.toml     # project metadata + entry point todo = todo.cli:main
└── README.md
```

## Implementation units (fed to the stage-6 TDD loop, in order)
1. **U1 core.add** (FR-001/002/003)
2. **U2 core.list / queries** (data side of FR-004/005)
3. **U3 core.complete** (FR-006/007/008)
4. **U4 core.delete** (FR-007/009, including id non-reuse FR-002)
5. **U5 storage** (FR-010/011: atomic writes, automatic creation, corruption handling)
6. **U6 cli** (SPEC-C-01..07: parsing, output format, exit codes, stderr)
7. **U7 behave acceptance**: wire the four `.feature` files to step definitions and get them green end to end.

## Test and coverage strategy
- Unit / integration: pytest; run `pytest --cov=src --cov-report=term-missing`
- Thresholds: lines ≥ 80%, core branches ≥ 90% (NFR-003)
- Acceptance: behave runs `features/*.feature` as the BDD acceptance layer
- Quality: `ruff check` + `ruff format` + `mypy src`

> Note from implementation: the environment was offline, so the stack's offline fallback was used — `unittest` instead of pytest, `trace` for coverage, and CLI end-to-end tests in place of behave (see `features/steps/README.md`).
