---
description: Run intake + BDD scenarios (stages 1–2). Usage: /sdd-bdd <product>
---

# /sdd-bdd — intake → Gherkin scenarios

Orchestrate two roles in sequence:

1. Delegate stage 1 to **intake**, producing `discovery.md`.
   - Use `skills/requirement-intake`, `prompts/clarify-requirements.md` and `prompts/event-storming.md`.
   - Gate 1: the clarity checklist is met (or the customer explicitly says "go").
2. Once the gate passes, delegate stage 2 to **gherkin-author**, producing `features/*.feature`.
   - Use `skills/bdd-gherkin`.
   - Gate 2: every core capability has a happy path, and key errors have negative scenarios.

Update `sdd-state.json` after each step. When done, suggest `/sdd-spec`.
