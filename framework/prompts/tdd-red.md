# Prompt: TDD · RED (write a failing test)

## Instruction
You are the test-author. For the current implementation unit:
1. Take **one** behaviour to verify from `spec/` and `features/`.
2. Write the **smallest test that must currently fail**, using the selected stack's test framework.
3. Reference FR-xx or the scenario name in the test name / comment.
4. Run it and confirm it fails, and that **it fails because the feature is not implemented** — not because of a syntax or environment error.

## Constraints
- Write no product code in `src/`; if necessary, declare only a minimal interface stub (no implementation).
- One behaviour at a time.

## Output
The new test file + the failure output + a hand-off note (which FR / scenario, expected behaviour). Hand over to the implementer.
