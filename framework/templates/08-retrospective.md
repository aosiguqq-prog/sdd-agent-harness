# Retrospective · <product>

> Stage 8 artifact, written by the **evaluator** next to `evaluation-report.md`.
> Purpose: turn what went wrong **with the framework** in this run into proposals a human can triage into `harness-feedback` issues.
> The evaluator only proposes. It never edits the framework; a human decides what to accept.

- Run ID: `RUN-<YYYY-MM-DD>-<product>`
- Mode: conversation / headless (`claude-cli`)
- Framework commit: <git rev-parse --short HEAD>
- Date and time: <YYYY-MM-DD HH:MM> (real time, see CLAUDE.md)

## 1. Run at a glance
| Item | Value | Source |
|------|-------|--------|
| Stages completed | x / 9 | `sdd-state.json` |
| Human interventions (count, and why each) | | `activity-log.md` (PAUSED entries, manual fixes) |
| AI calls / total turns / minutes | | `runs.jsonl` (headless only; write "n/a" in conversation mode) |
| Gate failures or rework | | `activity-log.md` |
| Size class and exceptions | | `discovery.md`, artifacts' "Size exceptions" |
| Assumptions made without human review | | artifacts' "Assumptions" sections |

## 2. Framework findings
One block per finding. Only problems whose cause is **in the framework** (rules, roles, skills, templates, gates, hooks, engine, stacks).

### F-1 <short title>
- Where: stage / role
- What happened:
- Evidence: <file and line, log entry, runs.jsonl row, test output>
- Layer: role / skill / template / gate / hook / engine-driver / stack
- Impact: high / medium / low — <what it cost: rework, turns, human time, risk>
- Proposed change:

### F-2 …

## 3. Not framework problems
Problems specific to this product (fix them in the product, not the framework), each with one line on why it is product-specific.
- …

## 4. What worked
Rules or roles that clearly helped, so they are kept when the framework changes.
- …

## 5. Triage (filled in by the human)
| Finding | Decision | Issue / reason |
|---------|----------|----------------|
| F-1 | accept / reject | #<n> / <reason> |
