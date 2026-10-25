---
description: Independent evaluation + release (stages 8–9). Usage: /sdd-release <product>
---

# /sdd-release — evaluate and release

1. Delegate stage 8 to **evaluator**: produce `evaluation-report.md` (process monitoring, quality assessment, goal attainment).
2. Delegate stage 9 to **release-manager**:
   - Confirm that all review blockers are resolved.
   - Build / package with the selected stack and produce the releasable artifact.
   - Generate `release-notes.md`, update `CHANGELOG.md`, and set the semantic version and tag.
   - Produce the release checklist (artifacts, rollback plan, known issues).
3. **Human gate**: show the customer a preview and wait for explicit approval before pushing or deploying.

Never deploy to production automatically; irreversible actions are executed only after the customer confirms.
Update `sdd-state.json`: `8-evaluation` and `9-release` done.
