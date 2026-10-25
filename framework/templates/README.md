# templates/ — artifact templates

Standard templates for each stage's artifacts. Roles fill them in, so artifacts look the same and stay traceable across products.

| File | Stage | Used for |
|------|-------|----------|
| `00-discovery.md` | 1 | Discovery / requirement profile |
| `01-bdd-feature.feature` | 2 | Gherkin scenario skeleton |
| `02-requirements.md` | 3 | Requirements |
| `03-spec-functional.md` | 4 | Functional spec |
| `03-spec-data.md` | 4 | Data spec |
| `03-spec-api.md` | 4 | Interface spec |
| `03-spec-ui.md` | 4 | UI / interaction spec |
| `03-spec-nfr.md` | 4 | Non-functional spec |
| `04-architecture.md` | 5 | Architecture and stack selection |
| `06-review-report.md` | 7 | Review report |
| `evaluation-report.md` | 8 | Process and product evaluation report |
| `07-release-notes.md` | 9 | Release notes |
| `activity-log.md` | all | Live activity log written by the orchestrator |

> ID scheme: FR / NFR (requirements) → SPEC-F/D/A/U/N (specs) → TEST (tests), traceable end to end.
