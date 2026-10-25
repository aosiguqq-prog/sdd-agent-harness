Feature: View the task list
  As a terminal user
  I want to see all tasks and their status
  So that I can decide what to do next

  Scenario: List open and done tasks
    Given the list contains an open task "Buy milk"
    And the list contains a done task "Pay rent"
    When the user views the list
    Then the system lists all 2 tasks
    And each task shows its id, text and status
    And open and done tasks can be told apart

  Scenario: A friendly message for an empty list
    Given the list is empty
    When the user views the list
    Then the system says the list is empty
    And no task entries are shown
