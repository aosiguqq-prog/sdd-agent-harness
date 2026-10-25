# Lesson learned: test fallback when offline / without dependencies

- Date: 2026-06-21
- Source: todo-cli (the first end-to-end validation product)

## What happened
The sandbox's package index was blocked (HTTP 403), so pytest / behave / coverage / ruff could not be installed.

## Decision
Do not block the pipeline; fall back to the Python standard library: `unittest` (tests) + `trace` (coverage) + CLI end-to-end tests (standing in for BDD acceptance).

## Fed back into
- `framework/stacks/python/stack.md` → new "offline / no-dependency fallback" section.

## Generalisation
The test framework is a replaceable *material*; the method (TDD rhythm, coverage gate) is the invariant *capability*.
Every stack profile should define a no-network fallback path.
