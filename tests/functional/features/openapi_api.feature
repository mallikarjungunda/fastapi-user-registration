Feature: OpenAPI documentation
  The generated schema documents the public API endpoints.

  Scenario: Inspect documented API routes
    Given the API is ready
    When I request the OpenAPI document
    Then the response status is 200
    And the OpenAPI document lists the root and users endpoints
