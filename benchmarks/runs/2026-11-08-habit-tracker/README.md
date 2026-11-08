# Run record: RUN-2026-11-08-habit-tracker

| Field | Value |
|---|---|
| Run ID | `RUN-2026-11-08-habit-tracker` |
| Product | habit-tracker (trial product, kept outside this repository) |
| Request | "a command-line habit tracker" |
| Status | **Unreleased trial** — stopped at the release gate on purpose; the product is not published |
| Framework version | commit `1ddc4c4` |
| Driver | `claude-cli` (`claude -p`), max turns 30 (60 for the second 6-implement call) |
| Date | 2026-11-08 |

## Metrics (from `runs.jsonl`)
Cost is Claude Code's client-side estimate; the run used a subscription, so nothing was billed per call.

| Stage | Role | Turns | Minutes | Est. cost (USD) | Result |
|---|---|---|---|---|---|
| 1-intake | intake | 9 | 0.9 | 0.4 | ok |
| 2-bdd | gherkin-author | 24 | 3.2 | 0.99 | ok |
| 3-requirements | requirements-engineer | 21 | 3.6 | 1.05 | ok |
| 4-spec | spec-architect | 23 | 8.4 | 2.18 | ok |
| 5-architecture | stack-advisor | 20 | 3.3 | 1.01 | ok |
| 6-implement | implementer | 31 | 12.9 | 4.01 | error: error_max_turns |
| 6-implement | implementer | 45 | 5.3 | 2.04 | ok |
| 6-implement | qa-test | 73 | 10.7 | 2.77 | error: success |
| 7-review | code-reviewer | 54 | 4.5 | 1.61 | ok |
| 7-review | security-reviewer | 16 | 2.0 | 0.75 | ok |
| 8-evaluation | evaluator | 19 | 3.1 | 1.01 | ok |
| **Total** | 11 calls | 335 | 58.0 | 17.82 | |

## Human interventions
1. 6-implement hit the turn limit; re-run with `SDD_MAX_TURNS=60`.
2. qa-test exited with code 1 but reported `success`; a human checked that all 249 tests pass and marked the stage done with the `manual` driver.

## Outcome
- 249 tests green, core line coverage 99.3 %, review: 0 blockers / 3 majors, security: no findings.
- Evaluation: goal attained; release recommended after two small fixes (README, delete prompt).
- Not released: the product was built only to exercise the framework.

## Files in this record
Copies of the product's evidence, frozen at the end of the run: `runs.jsonl`, `activity-log.md`, `discovery.md`, `review-report.md`, `evaluation-report.md`.

## Problems found
See the `harness-feedback` issues that link to this run ID.
