# Review report · todo-cli

> Stage 7 artifact. Code review (code-reviewer) + security review (security-reviewer).
> Severity: 🔴 blocker / 🟡 major / 🟢 suggestion.

## Conclusion
- Blockers: **0** (gate passes)
- Conformance to spec: **pass** (all 11 FRs and every SPEC section have a matching implementation and tests)
- Security check: **pass** (no high-risk items)
- Tests: 28 all green, line coverage 90.8% (before the fixes below)

## Code review
| # | Severity | Location | Issue | Resolution |
|---|----------|----------|-------|------------|
| 1 | 🟡 | cli.py: save path | A failed disk write (OSError, e.g. read-only or disk full) was not caught and would show a raw traceback, violating SPEC-N-01 / NFR-001 | **Fixed in this round**: catch OSError → friendly message + exit code 2 |
| 2 | 🟡 | cli.py:55-59 | CLI handling of a corrupt data file (exit code 2) had no test | **Fixed in this round**: test added |
| 3 | 🟡 | cli.py:51-53 | Printing help when no sub-command is given had no test | **Fixed in this round**: test added |
| 4 | 🟢 | storage.py:51-54 | The failure branch of temp-file cleanup has no test (hard to trigger) | Accepted, recorded for reference |
| 5 | 🟢 | core.py | Business logic is clear, well layered, consistently named | No change needed |

## Security review
| # | Severity | Category | Assessment |
|---|----------|----------|------------|
| S1 | 🟢 | Injection | No shell / SQL execution; text is stored in JSON as-is, no injection surface |
| S2 | 🟢 | Deserialisation | Only `json.loads` (safe); no pickle / eval |
| S3 | 🟢 | File writes | Atomic writes (tempfile + os.replace); a corrupt file is never overwritten |
| S4 | 🟢 | Sensitive data | No secrets, credentials or personal data involved |
| S5 | 🟢 | Supply chain | Zero third-party dependencies, no supply-chain risk |

## To-do (back to the implementer, then re-review)
- [x] Fix #1: CLI catches OSError and shows a friendly message
- [x] Test #2: corrupt file → exit code 2
- [x] Test #3: no command → print help, exit code 0
