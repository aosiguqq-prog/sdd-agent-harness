# Definition of Done and quality gates

A gate is an objective condition that must hold before the next stage starts. **No gate, no progress.**
Gates are either `auto` (checked by a checklist / machine) or `human` (needs a person to confirm).

## General DoD (every stage)

- The artifact is written to its agreed location in the product directory
- `sdd-state.json` is updated (stage status, gate result)
- The artifact is unambiguous and can be consumed directly by the next role

## Gate highlights per stage

| Stage | Key gate | Judged by |
|-------|----------|-----------|
| 1 intake | Clarity checklist met; scope (in / out) clear; product size set; conversation mode: assumptions confirmed by the customer | auto (pause if ambiguous) + **customer** in conversation mode |
| 2 BDD | Happy path for every core capability, negative scenarios for errors; scenario count within the size budget | auto |
| 3 requirements | Every requirement traceable to a scenario; NFRs complete; FR / NFR counts within the size budget; conversation mode: assumptions confirmed by the customer | auto + **customer** in conversation mode |
| 4 specification | Unambiguous, testable, aligned with requirements both ways | auto |
| 5 architecture | Selection justified (ADR); directory layout final | auto |
| 6 implementation | All green + coverage threshold + every scenario covered; `qa-report.md` written with verdict PASS | qa-test |
| 7 review | No blockers; implementation ≈ spec; security passed | reviewers |
| 8 evaluation | Process, quality and goal attainment assessed; `retrospective.md` lists framework findings with evidence | evaluator |
| 9 release | Customer previewed and approved; build OK; version set | **human** |

## Size budget (hard constraint)

Every stage stays within the caps of the product's size class (`size-budget.md`). Exceeding a cap is allowed only with a recorded reason under "Size exceptions"; an unexplained excess fails the gate.

## Traceability matrix (hard constraint)

Maintain one chain end to end:

```
requirement FR-XX  ⇄  scenario  ⇄  spec section SPEC-XX  ⇄  test case TEST-XX
```

Any broken link fails the gate. Keep the traceability table at the end of `requirements.md`.

## Coverage thresholds

Defined per `stacks/<profile>/stack.md` (may differ by language / project). Default recommendation:
- Line coverage ≥ 80%, branch coverage of core business logic ≥ 90%.
