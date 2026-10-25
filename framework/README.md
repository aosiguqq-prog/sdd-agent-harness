# framework/ — the reusable core

This is the "factory" of the platform. Every product is built from the roles, skills and templates defined here.

## Directory map

| Directory | What it is | Analogy |
|-----------|------------|---------|
| `pipeline/` | Declarative pipeline (stages / roles / gates) in `pipeline.yaml` | The factory floor plan |
| `agents/` | Sub-agent role definitions — *who* does the work | Workers at each station |
| `commands/` | `/sdd-*` slash commands — entry points into the pipeline | Start buttons |
| `skills/` | SDD-specific methods and procedures — *how* the work is done | Workers' manuals and tools |
| `templates/` | Templates for every artifact (Gherkin, specs, reports, …) | Blank forms |
| `prompts/` | Reusable prompt library | Standard scripts |
| `stacks/` | Pluggable technology-stack profiles | Production-line configurations |
| `gates/` | Quality gates and Definition of Done | Inspection standards |
| `hooks/` | Guard layer: scripts triggered automatically at fixed points | Automatic inspection probes |
| `engine/` | Deterministic runner (state machine, gates, budget, resume) | The conveyor belt |

## Wiring the framework into a product

The repository root ships a shared `.claude/` (settings + hooks), so every product under `products/*` uses the same core — change it once, every product picks it up. Alternatively, symlink or copy `framework/agents`, `framework/commands` and `framework/skills` into a product's own `.claude/`.

## Extending

- New stage → edit `pipeline/pipeline.yaml` and add the matching `agents/*.md`.
- New stack → copy `stacks/_generic/` to `stacks/<name>/` and fill it in.
- A prompt that proved useful → put it in `prompts/` and reference it from the role definition.
