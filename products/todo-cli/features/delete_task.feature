Feature: Delete a task
  As a terminal user
  I want to delete tasks I no longer need
  So that the list stays tidy

  Background:
    Given the list contains "Buy milk" (id 1) and "Pay rent" (id 2)

  Scenario: Successfully delete a task
    When the user deletes task 1
    Then the list contains 1 task
    And the list no longer contains task 1
    And task 2 still exists with the same id

  Scenario: A friendly message when deleting an unknown id
    When the user deletes task 999
    Then the system says that the id does not exist
    And the list still contains 2 tasks

  Scenario: A deleted id is not reused by a new task
    Given the user has deleted task 2
    When the user adds a task with the text "Buy bread"
    Then the new task's id is greater than 2
