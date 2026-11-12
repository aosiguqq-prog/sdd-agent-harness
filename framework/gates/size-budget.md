# Size budget

Every product gets a **size class** at intake. The class caps how much each stage may produce, so a one-line request does not grow into an enterprise system (issue #1).

Principles: **MVP first, YAGNI.** Build the smallest product that meets the success criteria; anything more is a later change request.

## Size classes

| | **S** — small tool, exercise, prototype | **M** — ordinary application | **L** — production product |
|---|---|---|---|
| Typical request | a one-line idea, a CLI tool, a demo | a web app with a few user roles | a system with real users, integrations and operations |
| Capabilities (features in scope) | ≤ 5 | ≤ 10 | no fixed cap; deliver in phases |
| Functional requirements (FR) | ≤ 10 | ≤ 30 | justify |
| BDD scenarios | ≤ 20 | ≤ 60 | justify |
| Non-functional requirements (NFR) | ≤ 5, only those the request asks for or that protect user data | ≤ 10 | justify |
| ADRs | ≤ 3 | ≤ 6 | justify |
| Test layers | unit + one acceptance test per scenario | + integration | + the NFR suites the product needs |
| Fuzz / load / benchmark / crash-injection suites | only if the request asks | only for NFRs that require them | as needed |

## How the size is set
- **Conversation mode:** intake asks the customer, with a recommended class as the default answer.
- **Headless mode (no human):** use the size the request states; if it states none, use **S**.
- The class is recorded in the "Product size" section of `discovery.md`. Every later role reads it there.

## Exceeding the budget
A role may exceed a cap only when the request or a success criterion needs it. Record each exception in the artifact under **"Size exceptions"**: what exceeds the cap, by how much, and which requirement makes it necessary. An exception without a reason fails the gate.
