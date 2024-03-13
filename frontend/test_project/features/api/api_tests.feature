@nondestructive @automated @api
Feature: Test HTTP methods for a REST API

    Background:
        Given I set api base url '{%API_BASE_URL%}'
        And I set the header param request content type as 'application/json'

    @api_smoke @critical
    Scenario Outline: Test POST Call
        Given I set the POST endpoint to '/posts' for creating posts
        When I send a POST HTTP request with '<payload>'
        Then I expect the HTTP response code of 'POST' to be '201'
        And I expect the response body of 'POST' to be non-empty
        Examples:
            | payload             |
            | post_payload_1.json |
            | post_payload_2.json |

    @api_smoke @blocker
    Scenario: Test GET Call
        Given I set the GET endpoint to '/posts' for fetching posts
        When I send a GET HTTP request
        # Failing the test on purpose to see the failure in the report
        Then I expect the HTTP response code of 'GET' to be '200'
        And I expect the response body of 'GET' to be non-empty

    @api_smoke
    Scenario Outline: Test UPDATE call
        Given I set the UPDATE endpoint to '/posts/1' for updating posts
        When I send a PUT HTTP request with '<payload>'
        Then I expect the HTTP response code of 'PUT' to be '200'
        And I expect the response body of 'PUT' to be non-empty
        Examples:
            | payload            |
            | put_payload_1.json |
            | put_payload_2.json |

    @api_smoke
    Scenario: Test DELETE Call
        Given I set the DELETE endpoint to '/posts/1' for deleting posts
        When I send a DELETE HTTP request
        Then I expect the HTTP response code of 'DELETE' to be '200'
        And I expect the response body of 'DELETE' to be empty
