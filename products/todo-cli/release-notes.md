# Release notes · todo-cli v0.1.0

> Release-stage artifact (release-manager).

## Version
- Version: v0.1.0 (semantic versioning, first usable version)
- Date: 2026-06-21
- Tag: `v0.1.0`

## What's in this release (first version)
- New `add`: add a task, id assigned automatically (FR-001/002/003)
- New `list`: view the list, open `[ ]` vs done `[x]` (FR-004/005)
- New `done`: mark as done by id, idempotent (FR-006/007/008)
- New `delete`: delete by id; ids are never reused (FR-007/009)
- Local JSON persistence, created on first run, atomic writes against corruption (FR-010/011)

## Quality
- Tests: 31, all green (core / storage / cli / error paths)
- Coverage: 92.3% (core 92.9% / cli 95.3% / storage 85.7%), meets NFR-003
- Security: zero third-party dependencies, no injection surface, atomic writes (review: 0 blockers)

## Install and use
```bash
pip install .          # creates the todo command
todo add "Buy milk"
todo list
todo done 1
todo delete 1
```
Without installing, during development: `PYTHONPATH=src python3 -m todo.cli <command>`

## Known issues and limitations
- The first version has no priorities, due dates, tags, search or undo (out of scope, see requirements.md).
- In the offline sandbox, building a wheel was limited by an old setuptools; it works with a modern local toolchain.
- BDD acceptance is currently covered by CLI end-to-end tests; behave will be wired in once online (see features/steps/README.md).

## Upgrade / rollback
- Upgrade: first version, no upgrade path.
- Rollback: `pip uninstall todo-cli`; the data file `~/.todo.json` is kept.

## Verification
- All tests pass; CLI end-to-end smoke test correct (add / delete / complete / list, ids not reused, friendly errors).
