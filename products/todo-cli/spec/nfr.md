# Non-functional specification · todo-cli

> IDs SPEC-N-xx. Turns the NFRs into concrete, testable mechanisms.

| ID | Category | Metric / requirement | Implementation / verification | Source |
|----|----------|----------------------|-------------------------------|--------|
| SPEC-N-01 | Usability | Every user error gives a clear message on stderr, never a traceback | Unit tests for each error path + manual test | NFR-001 |
| SPEC-N-02 | Reliability | Writes use a temp file + atomic swap; a parse failure never overwrites the original | Tests injecting write failures / corrupt files | NFR-002 |
| SPEC-N-03 | Maintainability | Three decoupled layers: core (business) / storage (I/O) / cli (arguments and output); coverage lines ≥ 80%, core branches ≥ 90% | Coverage report | NFR-003 |
| SPEC-N-04 | Portability | Python standard library only (json / argparse / os / tempfile) | Run in a clean environment + dependency review | NFR-004 |
| SPEC-N-05 | Performance | Each command < 200 ms with ≤ 1000 tasks | Small benchmark script / manual test | NFR-005 |

## Architecture constraints (guidance for stages 5 / 6)
- **Layers**: `core` (pure business logic, no I/O, easiest to test), `storage` (JSON read / write and atomic writes), `cli` (argparse parsing + output formatting).
- core depends on neither storage nor cli, so business rules can be test-driven first.
- The data-file path is injected into storage as a parameter, so tests can use temporary files.
