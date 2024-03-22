"""helpers.py

API step definitions related utility functions
"""
from pytest import FixtureRequest
from functools import partial
from typing import Union

import requests
import structlog
from requests.auth import AuthBase

from main.utils.exceptions import ApiException

logger = structlog.get_logger(__name__)


class BaseUrlNotSetError(Exception):
    """Exception to be raised when Base URL is not set for a request"""


def request_type_not_implemented(*args, **kwargs):
    raise NotImplementedError


def set_request_args_attr(request: FixtureRequest):
    """set_request_args_attr

    Function to set `request_args` attribute to a test case, a.k.a `request.node` object

    Arguments
    ---------
    `request: FixtureRequest`

    Returns
    -------
    None
    """
    if not hasattr(request.node, "request_args"):
        setattr(request.node, "request_args", {})
    logger.info("Helper: set_request_args_attr")


def create_request_args_for_request(request: FixtureRequest, request_name: str):
    """create_request_args_for_request

    Function to create request arguments dictionary for a named request for a particular
    test case (`request.node` object represents a test case).

    Arguments
    ---------
    `request: FixtureRequest`
    `request_name: str`

    Returns
    -------
    None
    """
    if request_name not in request.node.request_args:
        request.node.request_args[request_name] = {
            "headers": get_default_headers(request),
            "auth": get_request_auth(request),
        }
    logger.info("Helper: create_request_args_for_request")


def get_base_url(request: FixtureRequest) -> str:
    """get_base_url

    Check if a test case / request.node object has an attribute of base_url. If it isn't,
    raise an exception indicating the same. This is used in steps to set request endpoint,
    in which exception would be raised if endpoint is attempted to set before setting base url

    Arguments
    ---------
    `request: FixtureRequest`

    Returns
    -------
    `request.node.base_url: str`

    Raises
    ------
    `BaseUrlNotSetError`
    """
    if not hasattr(request.node, "base_url"):
        raise BaseUrlNotSetError(
            f"Base Url is not set for test case: {request.node.name}."
            " Set Base Url as a prerequisite using .local.env file, step definition or environment variable"
        )
    logger.info("Helper: get_base_url")
    return request.node.base_url


def get_default_headers(request: FixtureRequest) -> dict:
    """get_default_headers

    Gets default header dictionary if set, for a test case. If not, return empty dict.

    Arguments
    ---------
    `request: FixtureRequest`

    Returns
    -------
    `request.node.default_headers | dict() : dict`
    """
    logger.info("Helper: get_default_headers")
    if hasattr(request.node, "default_headers"):
        return request.node.default_headers
    return dict()


def raise_for_mising_url_endpoint(request: FixtureRequest, request_name: str):
    """raise_for_mising_url_endpoint

    Url &/ endpoint has to be set first in a test case for a named request, and only then
    request headers, url params, query params and payload has to be set. By design,
    request_args for a request is created during the url/endpoint creation steps. This
    functions checks for the presence of request arguments to indicate if url and/or endpoint
    is set for a particular request.

    Arguments
    ---------
    `request: FixtureRequest`
    `request_name: str`

    Returns
    -------
    None

    Raises
    ------
    `Exception`
        When request_args is not found for a test case object, or request_name is not available
        in request arguments dict.
    """
    if (not hasattr(request.node, "request_args")) or (
        request_name not in request.node.request_args
    ):
        raise ApiException("Looks like endpoint is not set. Set URL and Endpoint prior to setting headers!!")


def raise_for_missing_response(
    request: FixtureRequest, request_name: str, api_response_container: dict
):
    """raise_for_missing_response

    After a request is passed, the corresponding response is saved in a dictionary (pytest fixture)
    called api_response_container, which will be used for subsequent verification and other test steps.
    This function checks & raises an exception in case concerned test case or request is not found in
    the container

    Arguments
    ---------
    `request: FixtureRequest`
    `request_name: str`
    `api_response_container: dict`

    Returns
    -------
    None

    Raises
    ------
    `Exception`
    """
    if request.node.name not in api_response_container:
        raise ApiException("Looks like no requests has been passed during this test!!")
    if request_name not in api_response_container[request.node.name]:
        raise ApiException(f"There is no response present with name {request_name}")


def get_request_auth(request: FixtureRequest):
    """get_request_auth

    Authentication is set common to a particular test case (not at request level). This function
    checks if an authentication is setup and returns the same (or None)

    Arguments
    ---------
    `request: FixtureRequest`

    Returns
    -------
    `request.node.request_auth | None`
    """
    logger.info("Helper: get_request_auth")
    if not hasattr(request.node, "request_auth"):
        return None
    return request.node.request_auth


def api_request(
    *,
    method: str,
    url: str,
    headers: dict,
    params: Union[dict, None] = None,
    json: Union[dict, None] = None,
    auth: Union[AuthBase, None] = None,
    **var_req_args,
) -> requests.Response:
    """Send API Requests

    Positional Arguments
    --------------------
    None

    Keyword-only Arguments
    ----------------------
    `method: str` (Required)
        HTTP Request Method - GET, POST, PUT, PATCH, DELETE, etc.
    `url: str` (Required)
        Server Url Endpoint to communicate with. E.g.:- https://httpbin.org/get
    `headers: dict` (Required)
        key, value pairs of header values to be passed along with request like "accept": "application/json", etc.
    `params: dict | None` (Optional. Defaulted to None)
        Query Parameters as key, value pairs.
    `json: dict | None` (Optional. Defaulted to None)
        Payload that has to be sent to the server as dict.
    `auth: AuthBase | None` (Optional. Defaulted to None)
        Authentication Model for API. Like, Basic Authentication (HTTPBasicAuth), etc.
    `**var_req_args`
        Variable Request Args, corresponding to applicable arguments accepted `requests.request` method.
        For ex: `timeout`, etc.

    Returns
    -------
    `requests.Response` Object.

    Raises
    ------
    `requests.exceptions.RequestException`
        This exception is raised in case of any exceptions raised by requests module, except HTTPError.
    `Exception`
        Generic Exception (Catch-all) that is non-requests.


    """
    return_res = None
    params = params or None
    json = json or None
    try:
        logger.info(
            "Helper: api_request - Preparing to send API request"
        )
        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=json,
            headers=headers,
            auth=auth,
            **var_req_args,
        )
        response.raise_for_status()
        return_res = response
    except requests.exceptions.HTTPError as http_err:
        logger.warning(
            "Helper: api_request - Received HTTP Error (Status Code >= 400)"
        )
        return_res = http_err.response
    except requests.exceptions.RequestException:
        logger.error(
            "Helper: api_request - Server Side Error Observed (non-http error)"
        )
        raise
    except Exception:
        logger.error("Helper: api_request - Non-Requests Exception Occurred.")
        raise
    return return_res


# Note: to understand `partial` usage, please read:
# https://docs.python.org/3/library/functools.html#functools.partial
request_type_map = {
    "GET": partial(api_request, method="GET"),
    "POST": partial(api_request, method="POST"),
    "PUT": partial(api_request, method="PUT"),
    "PATCH": partial(api_request, method="PATCH"),
    "DELETE": partial(api_request, method="DELETE"),
}
