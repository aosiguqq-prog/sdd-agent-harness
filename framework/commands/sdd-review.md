---
description: Code + security review (stage 7). Usage: /sdd-review <product>
---

# /sdd-review — parallel review

Delegate to two read-only roles in parallel, both using `prompts/review-rubric.md`:

1. **code-reviewer** → correctness, readability, conformance to the spec.
2. **security-reviewer** → security risks (may use the built-in `security-review` command as input).

Merge both results into `review-report.md`, sorted by severity.
- **Blockers** found: hand the fixes back to `implementer` / `refactorer`, then review again.
- No blockers: the stage-7 gate passes; suggest `/sdd-release`.

Update `sdd-state.json`.
