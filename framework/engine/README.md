# engine/ — the production-line runner

The engine owns the **deterministic half** of the line: state machine, stage progression, gates, budget, pause / resume and the activity log.
Actually producing a stage's artifacts is delegated to a pluggable **driver**. Standard library only.

| Driver | What it does | Needs |
|--------|--------------|-------|
| `manual` (default) | Calls no AI. A stage passes when its artifacts exist; otherwise the line pauses until a human — or Claude Code in an interactive session — produces them | nothing |
| `claude` | Drives each role as an AI agent through the Claude Agent SDK, which writes the artifacts back to files | `pip install claude-agent-sdk`, `ANTHROPIC_API_KEY` |

## Usage (from the repository root)
```bash
PYTHONPATH=framework python3 -m engine new <product> --desc "one-line request"
PYTHONPATH=framework python3 -m engine status <product>
PYTHONPATH=framework python3 -m engine run <product> [--max N] [--approve-release] [--driver manual|claude]
PYTHONPATH=framework python3 -m engine resume <product>
```

## Run loop
```
find the first unfinished stage
  ├─ human gate and not approved → pause
  ├─ budget exhausted / --max reached → pause (resumable)
  ├─ driver.run_stage() → done: mark complete, log, continue
  │                       paused / blocked: log, stop and wait for the missing artifacts
  └─ nothing left → completed
```
Every step increments the budget (`budget.used_steps`), appends to `activity-log.md` and saves the state atomically — the line can be stopped at any point and resumed later.

## Design choices
- **Deterministic control in code, judgement in agents.** Advancing, gating and budgeting are plain code that can be unit-tested; the AI only does the creative work inside a stage.
- **The state file is the single source of truth.** The engine reads only the ordered `stages` in `sdd-state.json`, so it has zero dependencies and is portable.
- **Cost control by construction.** A hard step budget, a per-run `--max`, a per-agent turn limit, and the mandatory human release gate keep unattended runs bounded.

## Tests
```bash
PYTHONPATH=framework python3 -m unittest engine.tests.test_engine
```
Six offline tests cover: pausing on missing artifacts, advancing when they appear, the human gate, budget exhaustion, the activity log, and resume consistency.

## Limits (stated honestly)
- The engine judges only whether artifacts **exist**, not their quality; quality is guarded by the qa-test and reviewer roles.
- The `claude` driver has not yet been exercised end to end; so far the sample products were produced stage by stage in interactive Claude Code sessions, with the engine tracking state. A driver that runs Claude Code in headless mode (`claude -p`) is planned as a lower-cost alternative.
