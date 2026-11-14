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
- qa-test must write `qa-report.md` (commands, counts, coverage, PASS / FAIL verdict) as a required output of 6-implement; the `claude-cli` driver keeps the tail of stderr in `runs.jsonl` when a call fails (#3; found in RUN-2026-11-08-habit-tracker).
- Feedback loop: the evaluator writes `retrospective.md` (framework findings with evidence, proposals only) as a required output of 8-evaluation; CLAUDE.md and `benchmarks/README.md` describe the triage → issue → fix → CHANGELOG steps (#4; found in RUN-2026-11-08-habit-tracker).
- Assumption checkpoints in conversation mode: after 1-intake and 3-requirements the orchestrator shows the unconfirmed assumptions and continues only after the customer confirms or corrects them; assumptions now carry an ID and a status (#5; found in RUN-2026-11-08-habit-tracker).
- GitHub Pages deployment for static sites: stack-advisor decides `release_target` with a static-site test in 5-architecture; release-manager prepares and runs `framework/templates/deploy/github-pages.yml`, enables Pages, checks the live URL and records it (#10; requested for the next trial run, modelled on the `astrology` product).

### Changed
- The product template's 6-implement now names the TDD relay `test-author+implementer+refactorer+qa-test` and describes the per-unit loop, matching `pipeline.yaml`; the engine runs one pass of each role for now (per-unit loop tracked in #9) (#6; found in RUN-2026-11-08-habit-tracker).
- `claude-cli` driver: installing packages into the system Python is blocked (`--disallowedTools` for `pip`, `python -m pip`, `ensurepip`, `sudo`); roles may install only into the product's own `<product>/.venv` (#8; found in RUN-2026-11-08-habit-tracker).

### Fixed
- The engine no longer erases fields that roles write to `sdd-state.json` (such as `stack`): `save()` re-reads the file and writes back only the fields the engine owns (stage status and gate, `current_stage`, `budget`, `activity`) (#7; found in RUN-2026-11-08-habit-tracker).

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
