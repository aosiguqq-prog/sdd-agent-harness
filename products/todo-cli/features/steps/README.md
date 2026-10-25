# BDD acceptance tests

Planned for the late part of stage 6 (unit U7): run `features/*.feature` with **behave** as the end-to-end acceptance layer.

## Current state: offline fallback
The development environment had no network access, so behave could not be installed. Equivalent substitute:
- `tests/test_cli.py` drives `main()` through the full "parse → core → storage → output" chain
  and covers the core scenarios of all four `.feature` files (add / list / complete / delete, plus the negative cases).
  These CLI tests currently act as the **acceptance layer**.

## To do (once online)
1. `pip install behave`
2. Add step definitions in `steps/*.py`, mapping the Gherkin steps onto CLI calls.
3. Once `behave` passes, replace this note with the real step definitions.

> This lesson was fed back into the framework: see the "offline fallback" section of `framework/stacks/python/stack.md`.
