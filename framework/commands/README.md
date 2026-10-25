# commands/ — pipeline entry points (slash commands)

The "buttons" a human presses to start the pipeline. Commands **orchestrate**: they decide which role gets the work, what it must produce, and where to stop at a gate.

| Command | Stages | Purpose |
|---------|--------|---------|
| `/build <request>` | 0–9 | **One shot**: run the whole line from request to release (greenfield entry point) |
| `/sdd-new <name>` | 0 | Create the product skeleton and initialise state |
| `/sdd-bdd <name>` | 1–2 | Intake → Gherkin scenarios |
| `/sdd-spec <name>` | 3–4 | Requirements → specification |
| `/sdd-implement <name>` | 5–6 | Stack selection → TDD implementation |
| `/sdd-review <name>` | 7 | Code + security review |
| `/sdd-release <name>` | 8–9 | Independent evaluation → release |
| `/sdd-status <name>` | — | Show progress and the next step |

## Design choices
- One command may span several adjacent stages, but **it stops at every gate** that requires a decision, so the human stays in control.
- Commands contain no business logic; the logic lives in roles and skills, so the execution substrate can be swapped later.
- Commands treat `pipeline/pipeline.yaml` as the single source of truth for the process.
