# Prompt: generate Gherkin from the discovery document

## Instruction
Read `discovery.md`. For each core capability:
1. Write a `Feature:` with "As a / I want / So that".
2. At least one happy-path `Scenario:` in declarative Given-When-Then.
3. Negative scenarios for key errors and edge cases.
4. `Scenario Outline` + `Examples` for data-driven cases.
5. Use the glossary terms strictly; **no UI mechanics or technical details**.

## Constraints
- One behaviour per scenario.
- Every `Then` is an observable, verifiable outcome.

## Output
`features/<capability>.feature`, following `templates/01-bdd-feature.feature`. Finish with the quality checklist in `skills/bdd-gherkin`.
