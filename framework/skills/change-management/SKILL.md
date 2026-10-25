---
name: change-management
description: Change / iteration management. Once a product exists, how to handle change requests (new feature / spec change / visual change / bug fix) with impact analysis, scoped re-runs and regression instead of blindly re-running everything. Used by the orchestrator in change mode.
---

# Skill: Change / Iteration Management

Once a product exists, use the same production line for a **scoped re-run** instead of starting from zero.

## Trigger
`sdd-state.json.mode == "change"` and a change request exists (new feature / spec change / visual change / bug fix).

## Steps

### 1. Record the change request
Write it to the product's `change-requests/CR-<n>.md`: request, motivation, expected effect, priority.

### 2. Impact analysis (the core)
Walk the **traceability chain `requirement FR ⇄ scenario ⇄ spec SPEC ⇄ test TEST`** backwards:
- Which **requirements** does the change add or modify?
- Which **scenarios / spec sections / data model / interfaces / UI** does it touch?
- Which **tests** must change or be added?
Output an impact list: affected artifacts + stages.

### 3. Scoped re-run
Re-run **only the affected stages** (sometimes "spec change → implementation change", sometimes just "new scenario → new implementation"); unaffected artifacts stay untouched. The orchestrator dispatches work accordingly.

### 4. Regression testing (mandatory)
qa-test runs the **full suite** (new + existing tests) to confirm the change broke nothing.

### 5. Versioning and release
Bump the semantic version (minor for features, patch for fixes), update the CHANGELOG, and go through the release-preview gate again before releasing.

## Principles
- **Minimal blast radius**: leave everything untouched that can be left untouched, to reduce regression risk and cost.
- **Traceability is the basis**: if the chain is incomplete, repair it first — otherwise the impact analysis cannot be trusted.
- **Iteration is the norm**: a product goes through many change rounds, each following this process.

## Output
`change-requests/CR-<n>.md` + updated affected artifacts + a new version + an `activity-log.md` entry recording the impact list and the decisions.
