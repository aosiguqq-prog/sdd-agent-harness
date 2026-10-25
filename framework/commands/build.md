---
description: Build a new product end to end with the SDD pipeline (greenfield). Usage: /build <one-line request>
---

# /build — one-shot production line

You received a one-line request: **$ARGUMENTS**

Proceed as follows (equivalent to the start-up routing in `CLAUDE.md` §9):

1. Act as the **orchestrator**; first read `CLAUDE.md` and `framework/pipeline/pipeline.yaml`.
2. Choose a product name and create the skeleton under `products/<name>/` from `_template`
   (or run `PYTHONPATH=framework python3 -m engine new <name> --desc "<request>"`).
3. Let the **intake** role clarify the request with the customer until the clarity checklist is met, producing `discovery.md`.
4. Then advance **automatically** through the stages, using the matching role at each step and respecting every gate:
   BDD scenarios → requirements → specification → stack selection → TDD implementation → independent QA → code / security review → independent evaluation.
5. Record every key decision in the product's `activity-log.md`, and update `sdd-state.json` after each step.
6. **Pause and ask the customer** when: requirements are too ambiguous / tests keep failing / review has a blocker / the budget is exceeded / the release-preview gate is reached.
7. After the customer approves the release preview, the **release-manager** publishes (push source to GitHub first).
8. The **evaluator** delivers the final process and product evaluation report.

> Separation of powers: the orchestrator only dispatches — it writes no code and judges no quality; quality is guarded by qa-test and the reviewers.
