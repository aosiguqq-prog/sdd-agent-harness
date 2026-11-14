# Architecture and stack selection · <product>

> Stage 5 artifact.

## Selected stack
- Profile: `stacks/<profile>`
- Rationale (with reference to the NFRs):

## Release target
- Target: `github-pages` (static site) / `github-repo` (source only)
- Static-site test (all must hold for `github-pages`): output is files only · no own back end · no run-time secret · external APIs work from the browser without a proxy
- For `github-pages`: base path `/<repo>/`, routing (hash routes or `404.html` fallback)

## Candidate comparison
| Candidate | Fit | Ecosystem / familiarity | Risk | Verdict |
|-----------|-----|-------------------------|------|---------|

## Architecture decision records (ADR)
### ADR-001 <decision title>
- Context:
- Decision:
- Trade-offs / rejected alternatives:
- Consequences:

## Modules and directory structure
```
<planned source tree>
```

## Test and coverage strategy
- Unit / integration / end-to-end layers:
- Coverage thresholds:
- How BDD scenarios are wired in as acceptance tests:
