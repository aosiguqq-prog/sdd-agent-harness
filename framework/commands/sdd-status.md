---
description: Show the current SDD progress of a product and the next step. Usage: /sdd-status <product>
---

# /sdd-status — progress board

1. Read `products/<product>/sdd-state.json`.
2. Show a table with each stage's status, whether its gate passed, and whether its artifacts exist.
3. Point out the **current stage**, **pending gates**, and the **recommended next command**.
4. If the traceability chain (FR ⇄ scenario ⇄ spec ⇄ test) is broken anywhere, list the gaps explicitly.

Read-only; modifies no files.
