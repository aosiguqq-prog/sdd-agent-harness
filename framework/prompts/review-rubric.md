# Prompt: review rubric

Reviewers check each item and assign a severity: 🔴 blocker / 🟡 major / 🟢 suggestion. **Read-only.**

## Code review dimensions
1. **Correctness**: does it implement the spec; are edge cases and errors handled completely?
2. **Spec conformance**: is every SPEC-x implemented; are there unauthorised deviations?
3. **Readability**: naming, structure, comments, complexity.
4. **Maintainability**: duplication, coupling, testability.
5. **Test quality**: do the tests really cover behaviour; any brittle or meaningless assertions?

## Security review dimensions
1. Input validation / injection
2. Authentication and authorisation
3. Sensitive data and secret management
4. Encryption and transport security
5. Dependencies and supply chain
6. Information leakage in errors / insecure defaults

## Output
Fill `templates/06-review-report.md`: severity / location / reason / suggested fix for each issue.
All blockers must be resolved to pass the stage-7 gate. Distinguish objective defects from style preferences.
