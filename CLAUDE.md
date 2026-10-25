# CLAUDE.md — global working rules (every role, at all times)

This repository is an **autonomous development production line (agent harness)**: you, the customer, provide a rough product idea, and a set of AI roles with separated duties drive it autonomously from requirements to release. This file is the ground rules that apply to every role at all times.

---

## 1. Blackboard protocol (most important)
All roles **collaborate through files, never through chat memory**. The shared memory ("blackboard") is, in each product folder:
- `sdd-state.json` — progress, gates, stack, mode, budget, to-dos, activity pointer (the single source of truth)
- the stage artifacts (discovery.md / features / requirements.md / spec / src / tests / …)
- `activity-log.md` — the live activity log

Rules:
1. **Read before acting**: read `sdd-state.json` and the artifacts you need — **only what this step needs**, never the whole context.
2. **Write back after acting**: update your artifacts + `sdd-state.json` + append one entry to `activity-log.md`.
3. Roles **never talk to each other directly**; every hand-over goes through files, scheduled by the orchestrator.

## 2. Where rules live (look here to find or add a rule)
| Kind of rule | Location |
|---|---|
| Global conventions | this `CLAUDE.md` |
| A role's identity / responsibilities / boundaries | `framework/agents/<role>.md` |
| Reusable methods / craft | `framework/skills/<name>/SKILL.md` |
| Rules that must be enforced and cannot be skipped | `framework/hooks/` |
| Deterministic control logic (budget / resume / dispatch) | engine code (`framework/engine/`) |

## 3. Autonomy policy
- **Avoid interrupting**: advance automatically and record everything in `activity-log.md`.
- **The only mandatory human gate is the release preview**: stop before release, let the customer preview the result and decide.
- **Stop and ask a human** when: requirements are too ambiguous / tests keep failing / review has a blocker / the budget is exceeded.

## 4. Separation of powers
- Whoever **decides to advance** (the orchestrator), whoever **guards quality** (qa-test, code / security review) and whoever **does the work** (production roles) are kept separate and never combined — no one approves their own work.

## 5. Two modes
- **greenfield**: run the full pipeline.
- **change**: change request → impact analysis over the traceability chain → re-run only the affected stages → regression tests → new version → release again.
- The mode is recorded in `sdd-state.json` (`mode`); the method is in `skills/change-management`.

## 6. Traceability (quality red line)
Always maintain `requirement FR/NFR ⇄ scenario ⇄ spec SPEC ⇄ test TEST`. Any broken link fails the gate; the chain is also the basis of impact analysis in change mode.

## 7. Safety and budget
- Automatically executed commands are constrained by the guard rails in `framework/hooks` (dangerous-command blocking, post-edit quality checks).
- When a quota or budget limit is hit: **save, stop gracefully, resume later** — never force through.

## 8. Roles (see framework/agents/)
intake · orchestrator · gherkin-author / requirements-engineer / spec-architect / stack-advisor · test-author / implementer / refactorer · independent qa-test · code-reviewer · security-reviewer · evaluator · release-manager.

## 9. Start-up routing (default behaviour when the customer says "build X")
- When the customer asks to **create / develop / build** a product (app, program, tool, website …): **do not jump straight into code**. Switch to the orchestrator role and follow this file and `framework/pipeline/pipeline.yaml` (intake first → advance stage by stage → stop before release for confirmation), working under `products/<name>/` and logging everything to `activity-log.md`.
- When the customer asks to add a feature / change the spec / change the look / fix a bug in an **existing product**: use **change mode** (`framework/skills/change-management`) — impact analysis, scoped re-run, regression, new version.
- The only exception: the customer **explicitly says "just write it, skip the process"**.
- Shortcut: `/build <one-line request>` starts a greenfield run in one go.
