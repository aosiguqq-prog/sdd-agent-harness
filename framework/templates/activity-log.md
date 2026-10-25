# Activity log · <product>

> Appended live by the orchestrator, so the customer can see at any time where the line is, what was decided, and why.
> One entry per step, appended at the end in chronological order.

Format: `[time] [stage] [role] decision / action — reason (status / budget)`

---

- [YYYY-MM-DD HH:MM] [0-bootstrap] [orchestrator] Created the product skeleton — new product (steps 1/200)
- [YYYY-MM-DD HH:MM] [1-intake] [intake] Asked the customer 3 clarifying questions — profile lacked feature scope / look-and-feel (steps 3/200)
- [YYYY-MM-DD HH:MM] [1-intake] [orchestrator] Gate passed, moving to 2-bdd — clarity checklist met (steps 4/200)
- ...

<!-- Pauses are logged too, for example: -->
<!-- - [..] [6-implement] [orchestrator] PAUSED: tests failed 3 times in a row — safety condition fired, waiting for a human -->
<!-- - [..] [9-release] [orchestrator] PAUSED: release preview — the only mandatory human gate, waiting for the customer -->
