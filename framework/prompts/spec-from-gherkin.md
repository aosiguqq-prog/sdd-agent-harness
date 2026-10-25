# Prompt: generate specs from requirements + scenarios

## Instruction
Input: `requirements.md` and `features/`. For each requirement:
1. Assign it to the matching spec volume (functional / data / API / UI / non-functional).
2. Write SPEC-x entries with the matching template: source requirement, precise description, business rules, edge cases and errors, **acceptance / test points**.
3. Embed or reference the Gherkin scenarios as the acceptance basis.

## Constraints (no ambiguity)
- Banned vague words: "friendly", "as far as possible", "fast", "etc.". Write thresholds for anything measurable.
- Every spec item must be testable with at least one test.
- Cross-volume references must be consistent (one name per entity / interface).

## Output
`spec/*.md` + an index + a traceability matrix (SPEC ⇄ FR ⇄ scenario).
