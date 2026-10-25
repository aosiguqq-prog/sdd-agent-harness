---
name: requirement-intake
description: Method and clarity checklist for clarifying requirements with the customer. Use when a vague product idea needs to be questioned into shape, or to judge whether requirements are clear enough to start. Mainly used by the intake role.
---

# Skill: Requirement Intake and the Clarity Bar

Turn a one-liner or vague idea into structured, buildable requirements — without asking too little or asking the customer to death.

## Questioning principles
- **Ask only the 3–5 most important questions per round**, in priority order.
- Attach **a default assumption to every question**; if the customer does not answer, proceed with it (and mark it as an assumption in the output).
- First restate what you already understood, then ask what still needs clarifying — it lowers the customer's effort.
- Accept and parse reference files from the customer (colour schemes, styles, feature notes) and fold them into the profile.

## Question dimensions (covering these is enough)
1. **Who and why**: target users, core pain point, usage context.
2. **App type**: CLI / web / mini-app / desktop …
3. **Feature scope**: must-haves vs explicit exclusions (in / out).
4. **Look and feel** (front-end products): colour theme, style, reference sites or files; otherwise "platform recommends".
5. **Technology preference** (if any): language / framework / back end; otherwise "platform recommends".
6. **Success criteria**: what counts as done (measurable where possible).
7. **Constraints**: platform, time, existing systems, data sources.

## Clarity checklist (all must be met to proceed)
- [ ] Target users and roles are clear
- [ ] App type is decided
- [ ] Feature scope in / out is clear
- [ ] Success criteria are measurable
- [ ] Look-and-feel / technology preferences are recorded (or explicitly delegated to the platform)
- [ ] Key constraints and assumptions are listed

## When to stop asking
- Every box is checked, or
- The customer explicitly says "that's it, start" (record the remaining open items as assumptions / open questions for later stages).

## Output
Write `discovery.md` (requirement profile). Open items go into the "open questions / assumptions" list so the orchestrator can decide whether to come back to them later.
