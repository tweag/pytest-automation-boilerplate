from os import environ

from main.backend.common.step_definitions.steps_common import *
from assertpy import assert_that
from openai import OpenAI
from hypothesis import given
import hypothesis.strategies as st

import pytest

from main.frontend.common.step_definitions import open_base_url, maximize, page_title

logger = structlog.get_logger(__name__)
client = OpenAI(api_key=environ.get("OPEN_KEY"))

API_POST_CALL = "post_call"
DELETE_ENDPOINT = "/posts/1"
POST_ENDPOINT = "/posts"


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.api
@pytest.mark.apitest
@pytest.mark.test_name("Verify post call")
def test_send_post_request(request, api_response_container):
    logger.info(
        "Scenario is started",
        request_name=API_POST_CALL,
        test_case_name=request.node.name,
    )
    set_request_endpoint(request, request_name=API_POST_CALL, base_url='{%API_BASE_URL%}', endpoint=POST_ENDPOINT)
    set_request_headers(request, request_name=API_POST_CALL, headers="./test_data/api/payloads/sample/headers.json")
    add_json_payload(request, request_name=API_POST_CALL, json_payload="./test_data/api/payloads/post_payload_1.json")
    make_api_request(request, api_response_container, request_name=API_POST_CALL, request_type='POST')

    response = get_api_response(request, api_response_container, request_name=API_POST_CALL)
    assert response.status_code == 201 and response.reason == 'Created' and response.ok is True
    logger.info(
        "Scenario is completed successfully",
        request_name=API_POST_CALL,
        test_case_name=request.node.name,
    )


# A sample test to verify the open API call
@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.openapi
@pytest.mark.test_name("Verify open api call")
def test_search_text():
    prompt = "get a header from chatgpt"
    response_message = search_text(prompt)
    expected_message = "ChatGPT"
    assert_that(response_message).contains(expected_message)


def search_text(text: str):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.propertytest1
@pytest.mark.test_name("Verify values are equal")
@given(st.integers(), st.integers())
def test_ints_are_commutative(x, y):
    assert x + y == y + x
    print(f"Test passed for x={x} and y={y}")


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.propertytest
@pytest.mark.test_name("Verify reversing twice gives same list")
@given(st.lists(st.integers()))
def test_reversing_twice_gives_same_list(xs):
    ys = list(xs)
    reversed_list = list(reversed(ys))
    reversed_back = list(reversed(reversed_list))
    assert xs == reversed_back
    print(f"Test passed for xs={xs} and reversed_back={reversed_back}")


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.propertytest1
@pytest.mark.test_name("Verify look tuples work too")
@given(st.tuples(st.booleans(), st.text()))
def test_look_tuples_work_too(t):
    # A tuple is generated as the one you provided, with the corresponding
    # types in those positions.
    assert len(t) == 2
    assert isinstance(t[0], bool)
    assert isinstance(t[1], str)
