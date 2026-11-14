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
| `06-qa-report.md` | 6 | qa-test's gate verdict (required output of 6-implement) |
| `06-review-report.md` | 7 | Review report |
| `evaluation-report.md` | 8 | Process and product evaluation report |
| `08-retrospective.md` | 8 | Framework findings from this run, for human triage into issues |
| `07-release-notes.md` | 9 | Release notes |
| `deploy/github-pages.yml` | 9 | GitHub Actions workflow that deploys a static site to GitHub Pages (copied into the product repository) |
| `activity-log.md` | all | Live activity log written by the orchestrator |
| `decisions.md` | all | The customer's decisions with options and reasons (conversation mode; orchestrator) |

> ID scheme: FR / NFR (requirements) → SPEC-F/D/A/U/N (specs) → TEST (tests), traceable end to end.
