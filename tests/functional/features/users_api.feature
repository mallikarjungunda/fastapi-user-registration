Feature: Users API
  The API supports registering, listing, retrieving, updating, and deleting users.

  Scenario: Manage users through their lifecycle
    Given the API is ready
    When I register a user named "  Ada Lovelace  " with email "Ada@example.com" and password "a-long-test-password"
    Then the response status is 201
    And the response user has name "Ada Lovelace" and email "ada@example.com"
    And the response does not expose password fields
    When I register a user named "Grace Hopper" with email "grace@example.com" and password "another-long-password"
    Then the response status is 201
    When I list users
    Then the response status is 200
    And the response user names are "Ada Lovelace,Grace Hopper"
    When I list users with offset 1 and limit 1
    Then the response status is 200
    And the response user names are "Grace Hopper"
    When I get the first registered user
    Then the response status is 200
    And the response user has name "Ada Lovelace" and email "ada@example.com"
    When I update the first registered user's name to "  Ada Byron  "
    Then the response status is 200
    And the response user has name "Ada Byron" and email "ada@example.com"
    When I delete the first registered user
    Then the response status is 204
    And the response body is empty
    When I get the first registered user
    Then the response status is 404
    And the response error is "User not found"
    When I list users
    Then the response user names are "Grace Hopper"

  Scenario: Reject invalid registration data
    Given the API is ready
    When I register a user named "Ada" with email "not-an-email" and password "a-long-test-password"
    Then the response status is 422

  Scenario: Reject duplicate email addresses regardless of case
    Given the API is ready
    When I register a user named "Ada" with email "ada@example.com" and password "a-long-test-password"
    Then the response status is 201
    When I register a user named "Another Ada" with email "ADA@example.com" and password "a-long-test-password"
    Then the response status is 409
    And the response error is "Email is already registered"

  Scenario: Reject invalid pagination parameters
    Given the API is ready
    When I list users with offset 0 and limit 0
    Then the response status is 422

  Scenario: Return not found for operations on a missing user
    Given the API is ready
    When I get user 999
    Then the response status is 404
    And the response error is "User not found"
    When I update user 999's name to "Updated"
    Then the response status is 404
    And the response error is "User not found"
    When I delete user 999
    Then the response status is 404
    And the response error is "User not found"
