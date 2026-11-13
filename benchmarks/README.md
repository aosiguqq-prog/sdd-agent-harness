# benchmarks/

Evidence from runs of the framework, so that changes to the framework can be compared run against run.

- `runs/<date>-<product>/` holds one **run record**: a `README.md` summary (run ID, framework commit, status, metrics, human interventions, outcome) and frozen copies of the product's evidence files.
- A run gets a record whether or not its product is released. **Unreleased trial** runs are marked as such in the record's status.
- Problems found in a run are filed as `harness-feedback` issues that cite the run ID; the fix is recorded in the root `CHANGELOG.md` with the issue number.

Trace: run record → issue → commit → CHANGELOG entry → next run record (to check the effect).

## After a run
1. Read the evaluator's `retrospective.md` in the product folder.
2. Triage each finding: accept or reject (with a reason). Fill in its section 5.
3. File accepted findings as `harness-feedback` issues (same shape as the findings).
4. Copy the evidence into `runs/<date>-<product>/`: `README.md` summary, `runs.jsonl` (headless), `activity-log.md`, `evaluation-report.md`, `retrospective.md`, and any other file an issue cites.
5. Fix each issue with a commit that says `fixes #<n>` and add a line to the root `CHANGELOG.md`.
