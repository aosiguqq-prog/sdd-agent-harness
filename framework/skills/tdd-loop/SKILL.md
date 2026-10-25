---
name: tdd-loop
description: Drive implementation with the red-green-refactor loop while keeping traceability to the spec and scenarios. Use when entering implementation, when writing tests first, or when coordinating the test-author / implementer / refactorer roles.
---

# Skill: The TDD Loop

Let tests drive the implementation to secure code quality and conformance to the spec. Three roles run a relay with **strictly separated duties**.

## Rhythm (per implementation unit)
```
RED      test-author: write one failing test → run → confirm it fails for the right reason
  │
GREEN    implementer: minimal implementation → run → all tests pass
  │
REFACTOR refactorer: small refactoring steps → run after each → always green
  │
  └─ unit done? yes → next unit (back to RED); no → continue
```

## Iron rules
- **Test first**: no product code without a failing test.
- **Small steps**: advance one behaviour at a time.
- **No role mixing**: the test writer does not implement, the implementer does not change test intent, the refactorer adds no features.
- **Stay green**: no refactoring step may turn the suite red.

## Splitting into units
Split the system into independently testable units (functions / modules / use cases) based on `architecture.md`.
Priority: core business rules > edge-case handling > integration > periphery.

## Traceability
- Test names / comments reference FR-xx or the scenario name.
- BDD scenarios serve as **acceptance tests** (end to end), unit tests as **developer tests**; both layers coexist.

## Coverage and gate
- The threshold is defined in `stacks/<profile>/stack.md`.
- Stage-6 gate: all tests green + coverage threshold met + steps for every scenario implemented.

## Connecting to a concrete stack
Test framework, run commands and coverage tool come from the selected `stacks/<profile>/stack.md`; this skill only governs method and rhythm.
