# Specification index · todo-cli

> Stage 4 artifact (integrated by the spec-architect). The product has no GUI, so the interface spec and the UI spec are merged into a CLI spec.

| Volume | File | Covers |
|--------|------|--------|
| Functional spec | `functional.md` | SPEC-F-01..06 |
| Data spec | `data.md` | SPEC-D-01..03 |
| CLI spec (interface + UI) | `cli.md` | SPEC-C-01..07 |
| Non-functional spec | `nfr.md` | SPEC-N-01..05 |

## Traceability matrix (requirement ⇄ spec)
| Requirement | Spec |
|-------------|------|
| FR-001 add | SPEC-F-01 / SPEC-C-01 / SPEC-D-01 |
| FR-002 ids not reused | SPEC-F-01/04 / SPEC-D-01/02 |
| FR-003 reject empty text | SPEC-F-01 / SPEC-C-01 |
| FR-004 view list | SPEC-F-02 / SPEC-C-02 |
| FR-005 empty-list message | SPEC-F-02 / SPEC-C-02 |
| FR-006 mark as done | SPEC-F-03 / SPEC-C-03 |
| FR-007 unknown-id message | SPEC-F-03/04 / SPEC-C-03/04 |
| FR-008 idempotent completion | SPEC-F-03 / SPEC-C-03 |
| FR-009 delete | SPEC-F-04 / SPEC-C-04 |
| FR-010 persistence | SPEC-F-05 / SPEC-D-03 |
| FR-011 automatic creation | SPEC-F-05 / SPEC-D-03 |
| NFR-001..005 | SPEC-N-01..05 |

> Consistency check (architect): terminology is uniform (task / id / status / list); field names are consistent (id / text / done);
> no contradictions between volumes; every requirement has a spec item, nothing is left dangling.
