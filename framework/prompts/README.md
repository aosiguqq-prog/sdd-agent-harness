# prompts/ — reusable prompt library

Frequently used, refined prompts. Role definitions reference them by file name instead of rewriting them each time.

| File | Purpose | Main users |
|------|---------|------------|
| `clarify-requirements.md` | Question framework for clarifying requirements | intake, requirements-engineer |
| `event-storming.md` | Event-storming guide | intake |
| `gherkin-from-requirements.md` | Generate Gherkin from discovery | gherkin-author |
| `spec-from-gherkin.md` | Generate specs from requirements + scenarios | spec-architect |
| `tdd-red.md` | Write a failing test | test-author |
| `tdd-green.md` | Minimal implementation | implementer |
| `tdd-refactor.md` | Safe refactoring | refactorer |
| `review-rubric.md` | Review scoring rubric | code-reviewer, security-reviewer |

> Convention: a prompt is written as "an instruction that can be fed to the model directly + output-format constraints", and names the expected artifact.
