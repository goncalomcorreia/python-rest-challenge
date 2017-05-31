Feature: Loan applications API
  REST API for integration with loan application frontends built by
  client IT departments.

  Scenario: Add a new loan application
    Given the webserver is available
    And a valid application is generated
    When the endpoint POST /application is called
    Then the application is returned with an id
    Then status 200 is returned
    And the loan exists in the database

  Scenario: Attempt to add application with missing field
    Given the webserver is available
    And an application with age missing is generated
    When the endpoint POST /application is called
    Then status 422 is returned
    And an error message saying age is missing is returned

  Scenario: Attempt to add application with incorrect type
    Given the webserver is available
    And an application with age as a string is generated
    When the endpoint POST /application is called
    Then status 422 is returned
    And an error message saying age has wrong type is returned

  Scenario: Fetch an application by ID
    Given the webserver is available
    And an application exists in the database with id specialid
    When GET /application/specialid is called
    Then status 200 is returned
    And the correct application is returned

  Scenario: Update an application by ID
    Given the webserver is available
    And an application exists in the database with id specialid
    When PATCH /application/specialid is called to update age
    Then status 200 is returned
    And the updated age is recorded in the database

  Scenario: Delete an application by ID
    Given the webserver is available
    And an application exists in the database with id specialid
    When DELETE /application/specialid
    Then status 200 is returned
    And the application with id specialid is no longer in the database
