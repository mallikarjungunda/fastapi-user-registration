Feature: Root API
  The service exposes a simple root endpoint.

  Scenario: Get the root greeting
    Given the API is ready
    When I request the root endpoint
    Then the response status is 200
    And the response message is "Hello"
