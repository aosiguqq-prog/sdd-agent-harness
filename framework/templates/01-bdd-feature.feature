Feature: <capability, mapping to one or a group of requirements>
  As a <role>
  I want <goal>
  So that <value>

  Background:
    Given <precondition shared by all scenarios>

  Scenario: <happy path: one concrete successful behaviour>
    Given <initial context>
    When <triggering business event>
    Then <observable, verifiable outcome>

  Scenario: <negative case: key error or edge case>
    Given <error precondition>
    When <triggering action>
    Then <the correct rejection / message from the system>

  Scenario Outline: <data-driven behaviour>
    When the input is <input>
    Then the result is <result>
    Examples:
      | input       | result   |
      | valid value | success  |
      | edge value  | rejected |
