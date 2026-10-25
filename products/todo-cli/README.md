# todo-cli

A command-line to-do list — the first end-to-end validation product of the framework. Standard library only.

## Run
```bash
# during development, without installing
PYTHONPATH=src python3 -m todo.cli <command>

# or install it as the `todo` command (preferably inside a venv)
python3 -m venv .venv && source .venv/bin/activate
pip install .
todo <command>
```

## Usage
```bash
todo add "Buy milk"   # add
todo list             # list ([ ] open / [x] done)
todo done 2           # mark task #2 as done
todo delete 1         # delete task #1
```
Data is stored in `~/.todo.json` and survives restarts. Ids are never reused after deletion.

Exit codes: `0` success, `1` user error (empty text, unknown id), `2` runtime error (corrupt or unwritable data file).

## Tests
```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```
31 tests, about 92% line coverage.

## Structure
```
src/todo/core.py     pure business logic (no I/O)
src/todo/storage.py  JSON persistence (atomic writes, corruption protection)
src/todo/cli.py      argparse command-line interface
tests/               unit tests + CLI end-to-end tests (also the acceptance layer)
features/            Gherkin scenarios (acceptance specification)
```

## How it was built
Every artifact in this directory was produced by the pipeline, in order:
[`discovery.md`](discovery.md) → [`features/`](features/) → [`requirements.md`](requirements.md) → [`spec/`](spec/) → [`architecture.md`](architecture.md) → `src/` + `tests/` (TDD) → [`review-report.md`](review-report.md) → [`release-notes.md`](release-notes.md).
Requirement IDs (FR-xxx) are referenced from the scenarios, specs and test comments, so every line of behaviour can be traced back to a requirement.
