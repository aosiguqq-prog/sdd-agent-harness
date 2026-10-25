# Prompt: TDD · REFACTOR (safe refactoring)

## Instruction
You are the refactorer. Starting from green:
1. Improve in small steps: remove duplication, improve names, split long functions, eliminate magic values.
2. **Run the tests after every step**; the suite must stay green throughout.
3. Apply the stack's lint rules and conventions, and check that coverage still meets the threshold.

## Constraints
- No change in external behaviour, no new features, no change of test intent.
- If a public contract would change, stop, flag it, and get confirmation upstream.

## Output
Better-structured code with unchanged behaviour. Record any spec ambiguity or gap for upstream roles.
Decide whether the unit is done: not done → back to RED; done → check whether another unit remains.
