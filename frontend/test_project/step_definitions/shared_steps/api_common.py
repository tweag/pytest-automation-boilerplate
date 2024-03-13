import os

import pytest
from pytest_bdd import given, parsers

DELETE_ENDPOINT = "/posts/1"
POST_ENDPOINT = "/posts"


@pytest.fixture
@given(parsers.re("I set api base url '(?P<api_base_url>.*)'"),
       converters=dict(api_base_url=str))
def set_rest_api_base_url(api_base_url):
    return api_base_url


@pytest.fixture
@given(parsers.re("I set the header param request content type as '(?P<header_content_type>.*)'"),
       converters=dict(header_content_type=str))
def set_headers(header_content_type):
    return {"Content-type": f"{header_content_type}; charset=UTF-8"}


@pytest.fixture
@given(parsers.re("I set the GET endpoint to '(?P<endpoint_url>.*)' for fetching posts"),
       converters=dict(endpoint_url=str))
@given(parsers.re("I set the POST endpoint to '(?P<endpoint_url>.*)' for creating posts"),
       converters=dict(endpoint_url=str))
def set_post_endpoint(set_rest_api_base_url):
    api_endpoint = set_rest_api_base_url + POST_ENDPOINT
    return api_endpoint


@pytest.fixture
@given(parsers.re("I set the DELETE endpoint to '(?P<endpoint_url>.*)' for deleting posts"),
       converters=dict(endpoint_url=str))
@given(parsers.re("I set the UPDATE endpoint to '(?P<endpoint_url>.*)' for updating posts"),
       converters=dict(endpoint_url=str))
def set_delete_endpoint(set_rest_api_base_url):
    api_endpoint = set_rest_api_base_url + DELETE_ENDPOINT
    return api_endpoint
