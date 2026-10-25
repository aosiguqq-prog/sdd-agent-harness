---
name: spec-authoring
description: Write a complete, unambiguous, testable and traceable specification (functional / data / API / UI / non-functional). Use when turning requirements and scenarios into a formal specification, splitting or integrating spec volumes, or reviewing spec quality.
---

# Skill: Specification Authoring

Expand "requirements + scenarios" into a **complete specification** that a developer can implement from and a tester can verify against.

## Volume structure (tailor per project)
| Volume | Content | ID prefix |
|--------|---------|-----------|
| `spec/functional.md` | Behaviour, business rules, state machines, flows | SPEC-F-xx |
| `spec/data.md` | Domain model, entities / fields / constraints, data dictionary, ER | SPEC-D-xx |
| `spec/api.md` | Interface contracts: endpoints / methods / inputs / outputs / error codes | SPEC-A-xx |
| `spec/ui.md` | Screens, components, interactions, states, empty / error / loading states | SPEC-U-xx |
| `spec/nfr.md` | Performance, security, availability, maintainability, compliance | SPEC-N-xx |

## How to write each spec item
- **Unique ID** + title
- **Source**: the FR-xx / scenario it satisfies
- **Description**: precise and unambiguous (avoid "etc.", "as far as possible", "user-friendly")
- **Acceptance / test points**: what counts as a correct implementation
- **Edge cases and errors**: invalid input, extreme values, concurrency

## Quality bar (INVEST + testable)
- Unambiguous: everyone reads the same sentence the same way
- Testable: every item can be turned into at least one test
- Complete: covers every requirement, with nothing left dangling
- Consistent: volumes do not contradict each other (the architect integrates and checks)
- Traceable: SPEC-xx ⇄ FR-xx ⇄ scenario ⇄ test

## Split-authoring workflow (for the architect)
1. List the requirements → assign each to a volume.
2. Start an isolated sub-task per volume (separate context), passing only the relevant requirements and scenarios.
3. Once all are in, **integrate for consistency**: terminology, IDs, cross-volume references, contradictions.
4. Generate the spec index and the traceability matrix.
