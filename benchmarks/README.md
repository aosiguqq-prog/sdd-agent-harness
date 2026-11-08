# benchmarks/

Evidence from runs of the framework, so that changes to the framework can be compared run against run.

- `runs/<date>-<product>/` holds one **run record**: a `README.md` summary (run ID, framework commit, status, metrics, human interventions, outcome) and frozen copies of the product's evidence files.
- A run gets a record whether or not its product is released. **Unreleased trial** runs are marked as such in the record's status.
- Problems found in a run are filed as `harness-feedback` issues that cite the run ID; the fix is recorded in the root `CHANGELOG.md` with the issue number.

Trace: run record → issue → commit → CHANGELOG entry → next run record (to check the effect).
