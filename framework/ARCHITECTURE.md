# Architecture and design rationale

## 1. In one sentence

Turn "humans + AI building software together" into **a gated production line**: each station (stage) is owned by **a dedicated AI role (sub-agent)**, inputs and outputs are **structured files**, and the human only makes decisions at a few key gates.

## 2. Why it is designed this way

| Goal | How the framework addresses it |
|------|--------------------------------|
| Keep control over what the AI builds | Every stage produces **human-readable files** (Gherkin, specs, tests) and passes through a **gate** before the next stage |
| Raise code quality | Mandatory **TDD (red-green-refactor)** plus independent **QA, code-review and security-review** roles |
| Avoid context pollution | Each stage runs in its own sub-agent with only the context it needs |
| Let the process evolve | The process is declared in `pipeline.yaml`, decoupled from execution logic |
| Stay technology-agnostic | Stacks are pluggable `stacks/<profile>`; the spec layer is separated from the implementation layer |

## 3. Pipeline overview

```
Stage            Role (sub-agent)                Main artifacts                      Gate
────────────────────────────────────────────────────────────────────────────────────────────
0 bootstrap      orchestrator                    product skeleton, sdd-state.json    auto
1 intake         intake                          discovery.md (requirement profile)  auto / pause if ambiguous
2 bdd            gherkin-author                  features/*.feature                  auto
3 requirements   requirements-engineer           requirements.md (FR / NFR)          auto
4 spec           spec-architect (+ sub-tasks)    spec/*.md                           auto
5 architecture   stack-advisor                   architecture.md + chosen stack      auto
6 implement      test-author → implementer →     src/, tests/ (all green)            auto
                 refactorer (loop), verified by qa-test
7 review         code-reviewer ‖ security-reviewer  review-report.md                 auto / pause on blocker
8 evaluation     evaluator                       evaluation-report.md                auto
9 release        release-manager                 release-notes.md, CHANGELOG.md      HUMAN (release preview)
────────────────────────────────────────────────────────────────────────────────────────────
```

> Stages are not fixed: `pipeline.yaml` can add or remove stages, adjust gates, or run stations in parallel.

## 4. Asset model (four layers + a guard layer)

```
┌─ Orchestration (commands/)  ── /sdd-* commands: the human entry points
├─ Roles (agents/)            ── sub-agents: *who* does the work; responsibilities, boundaries, output contracts
├─ Capabilities (skills/)     ── *how* the work is done: methods any role can invoke
├─ Materials (templates/ prompts/ stacks/ gates/) ── templates, prompts, stack profiles, quality standards
└─ Guard layer (hooks/)       ── cross-cutting automation that runs at fixed points and turns soft rules into hard ones
```

Design principle: **roles invoke capabilities, capabilities consume materials, the pipeline orchestrates roles.** Each layer can be replaced independently.

### Guard layer (hooks)
The first four layers are rules the model *reads* (soft constraints), and a model can skip them. The guard layer uses native Claude Code hooks to **run scripts automatically** at fixed points, turning the critical rules into constraints that cannot be bypassed. Three rules: fail open (a broken hook never blocks the work), language-agnostic (the file → command mapping comes from external config), and individually switchable.

| When | Hook | Effect |
|------|------|--------|
| A request arrives, before any action | UserPromptSubmit | Forces a skill assessment (YES/NO) and a check of the current stage, preventing skipped steps |
| After every file write / edit | PostToolUse (Write/Edit) | Runs the configured lint / type / syntax checks and feeds failures back for fixing |
| Session start | SessionStart | Injects the SDD progress of every product, so work can resume across sessions |
| Before running a command | PreToolUse (Bash) | Blocks high-risk destructive commands |

See `framework/hooks/README.md`. The wiring lives in `.claude/settings.json` at the repository root.

## 5. State machine: where is the product now?

Each product has an `sdd-state.json` recording the current stage, the status of each artifact, gate results, mode and budget.
Every role reads it before starting and updates it when done — that is what keeps contexts clean while the whole line stays traceable.

```json
{
  "product": "todo-cli",
  "mode": "greenfield",
  "current_stage": "4-spec",
  "stack": null,
  "budget": {"max_steps": 200, "used_steps": 9},
  "stages": {
    "1-intake":       {"status": "done", "gate_passed": true},
    "2-bdd":          {"status": "done", "gate_passed": true},
    "3-requirements": {"status": "done", "gate_passed": true},
    "4-spec":         {"status": "in_progress", "gate_passed": false}
  }
}
```

## 6. Relationship to Claude Code

- The core uses **native Claude Code mechanisms**: `agents/` (sub-agents), `skills/` (SKILL.md), `commands/` (slash commands), `CLAUDE.md` and hooks — it runs as-is inside Claude Code.
- The process logic is written as tool-agnostic Markdown / YAML, so the assets carry over if execution moves to a custom engine or a GUI.
- The deterministic half (state machine, gates, budget, resume) lives in `framework/engine/` as plain Python.

## 7. Roadmap (from core to app)

1. **Now**: a working CLI core, validated end to end on small sample products.
2. **Next**: connect the engine to a real AI driver and run the line unattended within budget; standardise stack scaffolds; benchmark framework changes against the sample products.
3. **Later**: a GUI / orchestration service on top of the core that turns `sdd-state.json` and the gates into a visual board. The core API stays the same; only the "face" changes.
