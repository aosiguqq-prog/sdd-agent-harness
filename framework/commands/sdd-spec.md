---
description: Requirements + full specification (stages 3–4). Usage: /sdd-spec <product>
---

# /sdd-spec — requirements → specification

1. Delegate stage 3 to **requirements-engineer**, producing `requirements.md` (FR / NFR + traceability matrix).
2. Once the gate passes, delegate stage 4 to **spec-architect**:
   - Split into `spec/functional|data|api|ui|nfr.md`; volumes may be written by isolated sub-tasks via `Task`.
   - Use `skills/spec-authoring`.
   - Integrate for consistency and ensure `SPEC-XX` ⇄ `FR-XX` alignment.

Update `sdd-state.json` after each step. When done, suggest `/sdd-implement`.
