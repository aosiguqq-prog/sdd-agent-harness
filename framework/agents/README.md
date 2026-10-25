# agents/ — sub-agent role library

Each file defines one independent AI role in Claude Code sub-agent format. Switching roles means switching context, which keeps each role's context clean.

| Role | Stage | Responsibility |
|------|-------|----------------|
| `intake` | 1 | The only role that talks to the customer; clarifies the request until it meets the clarity bar |
| `orchestrator` | all | Pipeline controller: dispatches work, decides when to advance, enforces gates and budget, writes the activity log |
| `gherkin-author` | 2 | Writes Given-When-Then scenarios |
| `requirements-engineer` | 3 | Derives numbered, traceable requirements |
| `spec-architect` | 4 | Splits the specification into volumes and integrates them |
| `stack-advisor` | 5 | Selects the tech stack and records architecture decisions |
| `test-author` | 6 · RED | Writes failing tests only |
| `implementer` | 6 · GREEN | Minimal implementation to turn tests green |
| `refactorer` | 6 · REFACTOR | Improves structure while keeping everything green |
| `qa-test` | 6 | Independent QA: full test run, coverage gate, regression in change mode |
| `code-reviewer` | 7 | Code review (read-only) |
| `security-reviewer` | 7 | Security review (read-only) |
| `evaluator` | 8 | Independent evaluation of the product and the process |
| `release-manager` | 9 | Build, versioning, release notes, publishing |

## Conventions
- Every role definition contains: responsibility, method, **output contract**, boundaries, and a wrap-up step (update `sdd-state.json`).
- Roles hand over work **only through files**, never through implicit memory.
- `tools` / `model` in the frontmatter can be adjusted as needed; roles that write tests, code or reviews get `Bash` so they can run the test suite.
