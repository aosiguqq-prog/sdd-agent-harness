Feature: Mark a task as done
  As a terminal user
  I want to mark finished tasks as done
  So that I can see clearly what is left

  Background:
    Given the list contains an open task "Buy milk" with id 1

  Scenario: Successfully mark a task as done
    When the user marks task 1 as done
    Then task 1 has the status done

  Scenario: A friendly message for an unknown id
    When the user marks task 999 as done
    Then the system says that the id does not exist
    And the status of the existing tasks is unchanged

  Scenario: Marking a done task again is not an error
    Given task 1 is already done
    When the user marks task 1 as done again
    Then task 1 still has the status done
    And the system reports no error
