# Changelog

Changes to the **framework itself** (rules, roles, skills, hooks, engine).
Each product keeps its own CHANGELOG inside its folder.

Every entry links the problem that motivated it: the `harness-feedback` issue number, and the run ID where it was found
(see `benchmarks/runs/`). A run can come from a released product or from an **unreleased trial**; the run record says which.

Entry format: `- <what changed> (#<issue>; found in RUN-<date>-<product>)`

## Unreleased

### Added
- Issue template and `harness-feedback` label for recording problems found while building products.
- This CHANGELOG for the framework.
- `benchmarks/` with the first run record, `RUN-2026-11-08-habit-tracker` (unreleased trial).
- Size budget: intake sets a product size (S / M / L) and every stage stays within its caps (`framework/gates/size-budget.md`); exceptions must be justified (#1; found in RUN-2026-11-08-habit-tracker).
- Real timestamps in activity logs: the prompt hook and the headless task give roles the current time, and CLAUDE.md forbids guessing it (#2; found in RUN-2026-11-08-habit-tracker).

## 2026-11-07

### Added
- `claude-cli` driver: runs each role through Claude Code in headless mode (`claude -p`) with a turn limit, a timeout and a fixed tool allow-list, and appends per-call metrics to `<product>/runs.jsonl`.
- Three offline tests for the driver (9 engine tests in total).

## 2026-10-29

### Added
- GitHub Actions CI: lint (pyflakes rules via ruff) and the engine and `todo-cli` tests on Python 3.10 and 3.12.

### Fixed
- Removed unused imports and an unused variable reported by the linter.

## 2026-10-25

### Added
- Initial public release: pipeline, 14 roles, skills, commands, templates, hooks, gates, deterministic engine, and the `todo-cli` sample product.
