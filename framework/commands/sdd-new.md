---
description: Initialise a new SDD product (stage 0, bootstrap). Usage: /sdd-new <product> [one-line request]
---

# /sdd-new — create a product and bootstrap the environment

You are running SDD stage 0:

1. Create `products/<product>/` using `products/_template/` as the skeleton.
2. Fill in `PROJECT.md`: product name, one-line request, creation date, current stage = 1-intake.
3. Initialise `sdd-state.json` (all stages `pending`; 1-intake ready to start) and `activity-log.md`.
4. Make sure the product can reach `framework/agents`, `skills` and `commands` (shared root `.claude/` or symlinks).
5. Show the user an overview of the pipeline (from the pipeline section of `framework/ARCHITECTURE.md`) and suggest `/sdd-bdd` as the next step.

Report briefly: what was created, where the product is now, and the next command.
