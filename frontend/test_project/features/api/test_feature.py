from os import environ

from main.backend.common.step_definitions.steps_common import *
from assertpy import assert_that
from openai import OpenAI

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
