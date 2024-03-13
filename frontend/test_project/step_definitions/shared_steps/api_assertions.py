from assertpy import assert_that
from pytest_bdd import then, parsers


@then(parsers.re("I expect the HTTP response code of '(?P<request_type>.*)' to be '(?P<status_code>.*)'"),
      converters=dict(status_code=int, request_type=str))
def validate_status_code(context, request_type, status_code):
    if request_type == "POST":
        assert_that(context["post_status_code"]).is_equal_to(status_code)
    elif request_type == "GET":
        assert_that(context["get_status_code"]).is_equal_to(status_code)
    elif request_type == "PUT":
        assert_that(context["put_status_code"]).is_equal_to(status_code)
    elif request_type == "DELETE":
        assert_that(context["delete_status_code"]).is_equal_to(status_code)


@then(parsers.re("I expect the response body of '(?P<request_type>.*)' to be empty"))
@then(parsers.re("I expect the response body of '(?P<request_type>.*)' to be non-empty"))
def validate_response_body(context, request_type):
    if request_type == "POST":
        assert_that(context["post_response"]).is_not_equal_to(None)
    elif request_type == "GET":
        assert_that(context["get_response"]).is_not_equal_to(None)
    elif request_type == "PUT":
        assert_that(context["put_response"]).is_not_equal_to(None)
    elif request_type == "DELETE":
        assert_that(context["delete_response"]).is_empty()
