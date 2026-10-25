---
name: bdd-gherkin
description: Turn requirements into high-quality Gherkin scenarios with BDD. Use for event storming, for writing or reviewing Given-When-Then .feature files, or for establishing a shared business vocabulary.
---

# Skill: BDD and Gherkin

Turn requirements into an "executable specification". This skill provides the method and the quality bar for roles such as intake and gherkin-author.

## Core principles
1. **Behaviour first**: describe what the system does for the user and what value it creates, not how it works inside.
2. **Ubiquitous language**: terms come from the glossary in `discovery.md` and stay consistent throughout.
3. **Declarative**: Given/When/Then describe business actions ("submit valid credentials"), not UI mechanics ("click the login button").
4. **One behaviour per scenario**: do not cram several assertions into one Scenario.

## Gherkin structure
```gherkin
Feature: <one capability, mapping to one or a group of requirements>
  As a <role>
  I want <goal>
  So that <value>

  Background:
    Given <precondition shared by all scenarios>

  Scenario: <happy path describing one concrete behaviour>
    Given <initial context>
    When <triggering event>
    Then <observable outcome>

  Scenario Outline: <data-driven>
    When the amount <amount> is submitted
    Then the result is <result>
    Examples:
      | amount | result   |
      | 100    | accepted |
      | -1     | rejected |
```

## Required coverage
- At least one happy path per core capability.
- Key errors / edge cases / invalid input → negative scenarios.
- Permission- or state-dependent behaviour → scenarios per role / state.

## Quality checklist
- [ ] The scenario title alone says what is being tested
- [ ] No implementation details leak in (API names, buttons, table names)
- [ ] Every Then is an observable, verifiable outcome
- [ ] Terms match the glossary
- [ ] Every scenario can be mapped onto future step definitions

## Event-storming cheat sheet (for the intake stage)
Lay out along a timeline: domain events (orange) → commands (blue) → actors (yellow) → external systems (pink) → read models / screens (green).
Output: event list, command list, scope (in / out), glossary.
