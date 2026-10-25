Feature: Add a task
  As a terminal user
  I want to record a task quickly
  So that I don't have to worry about forgetting it

  Background:
    Given the list is empty

  Scenario: Successfully add a task
    When the user adds a task with the text "Buy milk"
    Then the list contains 1 task
    And that task's text is "Buy milk"
    And that task's status is open
    And that task has a unique id

  Scenario: Ids increase and are not reused when adding several tasks
    When the user adds "Buy milk" and then "Pay rent"
    Then the list contains 2 tasks
    And the two tasks have different ids
    And the later task's id is greater than the earlier one's

  Scenario: Reject a task with empty text
    When the user adds a task with empty text
    Then the system rejects the operation
    And it says the task text must not be empty
    And the list contains 0 tasks
