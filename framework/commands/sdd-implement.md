---
description: Stack selection + TDD implementation (stages 5–6). Usage: /sdd-implement <product>
---

# /sdd-implement — stack selection → TDD implementation

1. Delegate stage 5 to **stack-advisor**: select `stacks/<profile>`, produce `architecture.md`, and write the stack back to the state file.
2. Then split the work into **implementation units** according to `architecture.md`, and run the TDD loop (`skills/tdd-loop`) for each unit:
   - **test-author** (RED) → write a failing test and confirm it fails
   - **implementer** (GREEN) → minimal implementation until everything is green
   - **refactorer** (REFACTOR) → improve structure while staying green
   - Repeat until the unit is done, then move to the next unit.
3. **qa-test** verifies the stage-6 gate independently: all tests pass + coverage threshold met + every scenario covered.

Update `sdd-state.json` after each unit. When done, suggest `/sdd-review`.
