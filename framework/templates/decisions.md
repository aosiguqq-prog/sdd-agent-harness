# Decision record · <product>

> Written by the orchestrator in conversation mode, at any stage. One entry for each decision the **customer** makes
> that changes the product's scope, design, technology, release, or what may be changed later.
> The artifact that the decision changes (requirements, spec, architecture …) is still updated by its owning role;
> this file keeps the *why*, so a later change can see what was considered and what it would undo.
>
> Record: the customer chose between options, overruled a proposal, changed or dropped a feature, accepted a trade-off.
> Do not record: wording fixes, small details with no alternatives, choices the roles make on their own
> (those are assumptions in the artifacts, or ADRs in `architecture.md`).

## Index
| ID | Date | Stage | Decision | Status |
|----|------|-------|----------|--------|
| DEC-001 | YYYY-MM-DD | 1-intake | <one line> | accepted |

---

## DEC-001 <short title>
- Date / stage: YYYY-MM-DD HH:MM · <stage>
- Decided by: customer (<how: answered a question / reviewed an artifact / own initiative>)
- Context: <what situation or question led to the decision>
- Options considered:
  1. <option> — <pros / cons>
  2. <option> — <pros / cons>
- Decision: <what was chosen>
- Reason: <the customer's reason, in their words where possible; sources they checked, if any>
- Consequences: <what this changes, what it rules out, any cost accepted>
- Affects: <artifacts and IDs updated, e.g. requirements.md FR-03, architecture.md ADR-002>
- Status: accepted  <!-- later: superseded by DEC-00x, with the date -->

<!-- A decision is never edited away. To change it, add a new entry and mark the old one "superseded by DEC-00x". -->
