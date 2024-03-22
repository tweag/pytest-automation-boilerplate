import os
from requests.models import PreparedRequest

import requests
from requests import auth as requests_auth

import typing

import structlog
from pytest import FixtureRequest

from main.backend.common.utils import utils, helpers, auth as boilerplate_auth
from main.utils import data_manager

logger = structlog.get_logger(__name__)

"""
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------

STEPS AUTHENTICATION

----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
"""


def setup_basic_auth(request: FixtureRequest, username: str, password: str):
    """setup_basic_auth

    Step Behavior
    -------------
    * Get username and password from environment variables
    * Instantiate `HTTPBasicAuth` object with username and password
    * create an attribute `request_auth` of `request.node` object
        and save the object generated at previous step
    """

    username = data_manager.text_formatted(username)
    password = data_manager.text_formatted(password)
    request.node.request_auth = requests_auth.HTTPBasicAuth(username, password)
    logger.info("Step: setup_basic_auth")


def setup_digest_auth(request: FixtureRequest, username: str, password: str):
    """setup_digest_auth

    Step Behavior
    -------------
    * Get username and password from environment variables
    * Instantiate `HTTPDigestAuth` object with username and password
    * create an attribute `request_auth` of `request.node` object
        and save the object generated at previous step
    """

    username = data_manager.text_formatted(username)
    password = data_manager.text_formatted(password)
    request.node.request_auth = requests_auth.HTTPDigestAuth(username, password)
    logger.info("Step: setup_digest_auth")


def setup_bearer_auth(request: FixtureRequest, token: str):
    """setup_bearer_auth

    Step Behavior
    -------------
    * Get username and password from environment variables
    * Instantiate `HTTPBearerAuth` object with username and password
    * create an attribute `request_auth` of `request.node` object
        and save the object generated at previous step
    """

    token = data_manager.text_formatted(token)
    request.node.request_auth = boilerplate_auth.HTTPBearerAuth(token)
    logger.info("Step: setup_bearer_auth")


"""
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------

STEPS REQUEST

----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
"""


def set_request_endpoint(request: FixtureRequest, request_name: str, base_url: str, endpoint: str,
                         with_logs: bool = False):
    """set_request_endpoint

    Step Behavior
    -------------
    * Checks if `request_args` attribute is present for `request.node` object, and if it isn't,
        create one and assign an empty dictionary to it.
    * Checks if the `request_name` key is present in `request.node.request_args` dictionary object,
        and if it isn't, then create a dictionary with `request_name` key and pre-fill with
        default_headers (this is to handle the case where no request specific headers are required)
        and auth values.
    * urlappend Base Url and endpoint and assign it to "url" key of request_args of the named request.
    """

    request.node.base_url = data_manager.text_formatted(base_url)
    helpers.set_request_args_attr(request)
    helpers.create_request_args_for_request(request, request_name)
    request.node.request_args[request_name]["url"] = utils.urlappend(
        helpers.get_base_url(request), data_manager.text_formatted(endpoint)
    )
    if with_logs:
        logger.info(
            "Step: set_request_endpoint - Endpoint Set Successfully with logs.",
            request_name=request_name,
            request_args=request.node.request_args[request_name],
            test_case_name=request.node.name,
        )
    else:
        logger.info(
            "Step: set_request_endpoint - Endpoint Set Successfully.",
            request_name=request_name
        )


def set_request_headers(
    request: FixtureRequest, request_name: str, headers: typing.Union[dict, str], with_logs: bool = False
):
    """set_request_headers

    Step Behavior
    -------------
    * Check for missing url or endpoint (by checking request_args attribute & request_name key in
        request_args). If not raise an exception and abort.
    * Header Key-Value pairs fetched from datatable would be joined with the ones specified as default
        headers and assigned to "headers" key of request's request arguments. Note that, any duplicate
        headers would be overridden here. For example, if "accept" equals "application/json" in default
        headers and the same key is given value of "application/html" in request, the final value would
        be "application/html"
    """

    helpers.raise_for_mising_url_endpoint(request, request_name)
    if isinstance(headers, dict):
        for k, v in headers.items():
            headers[k] = data_manager.text_formatted(v)
    else:
        headers = utils.load_json_file(headers)

    # set headers within request_args[request_name]
    request.node.request_args[request_name]["headers"] = headers

    if with_logs:
        logger.info(
            "Step: set_request_headers - Request Header Set Successfully with logs.",
            request_name=request_name,
            request_args=request.node.request_args[request_name],
            test_name=request.node.name,
        )
    else:
        logger.info(
            "Step: set_request_headers - Request Header Set Successfully.",
            request_name=request_name
        )


def add_url_path_parameters(request: FixtureRequest, request_name: str, path_params: typing.Union[str, list],
                            with_logs: bool = False):
    """add_url_path_parameter

    Note that this step depends on the current state of the url value, and would do a ordered modification of
    the url. This step has to be done only after setting base url and endpoint. As an example, if you have a test
    url like this: https://httpbin.org/delay/4/2. then, base url would be `https://httpbin.org` and endpoint would
    be `delay` and the first url parameter would be 4 and second one would be 2, should be called in order.

    Step Behavior
    -------------
    * Check for missing url or endpoint (by checking request_args attribute & request_name key in
        request_args). If not raise an exception and abort.
    * urlappend the existing url and the url parameter for the specified request.
    """

    helpers.raise_for_mising_url_endpoint(request, request_name)
    if isinstance(path_params, list):
        for elem in path_params:
            request.node.request_args[request_name]["url"] = utils.urlappend(
                request.node.request_args[request_name]["url"],
                data_manager.text_formatted(elem),
            )
    else:
        request.node.request_args[request_name]["url"] = utils.urlappend(
            request.node.request_args[request_name]["url"],
            data_manager.text_formatted(path_params),
        )

    if with_logs:
        logger.info(
            "Step: add_url_path_parameter - Url Parameter Added Successfully to the request url with logs.",
            request_name=request_name,
            request_args=request.node.request_args[request_name],
            test_name=request.node.name
        )
    else:
        logger.info(
            "Step: add_url_path_parameter - Url Parameter Added Successfully to the request url.",
            request_name=request_name
        )


def add_url_query_parameters(request: FixtureRequest, request_name: str, query_params: typing.Union[dict, str],
                             with_logs: bool = False):
    """add_url_query_parameters

    Note that this step depends on the current state of the url value, and would do a ordered modification of
    the url. This step has to be done only after setting base url and endpoint. As an example, if you have a test
    url like this: https://httpbin.org/delay/4/2. then, base url would be `https://httpbin.org` and endpoint would
    be `delay` and the first url parameter would be 4 and second one would be 2, should be called in order.

    Step Behavior
    -------------
    * Check for missing url or endpoint (by checking request_args attribute & request_name key in
        request_args). If not raise an exception and abort.
    """

    helpers.raise_for_mising_url_endpoint(request, request_name)
    if isinstance(query_params, dict):
        for k, v in query_params.items():
            query_params[k] = data_manager.text_formatted(v)
    else:
        query_params = utils.load_json_file(query_params)

    req = PreparedRequest()
    req.prepare_url(request.node.request_args[request_name]["url"], query_params)
    request.node.request_args[request_name]["url"] = req.url

    if with_logs:
        logger.info(
            "Step: add_url_query_parameters - Url Parameters Added Successfully to the request url with logs.",
            request_name=request_name,
            request_args=request.node.request_args[request_name],
            test_name=request.node.name
        )
    else:
        logger.info(
            "Step: add_url_query_parameters - Url Parameter Added Successfully to the request url.",
            request_name=request_name
        )


def add_params_parameters(
    request: FixtureRequest, request_name: str, params: typing.Union[dict, str], with_logs: bool = False
):
    """add_params_parameters

    Step Behavior
    -------------
    * Check for missing url or endpoint (by checking request_args attribute & request_name key in
        request_args). If not raise an exception and abort.
    * Add query params passed in the step as "params" in request arguments.
    """

    helpers.raise_for_mising_url_endpoint(request, request_name)
    if isinstance(params, dict):
        for k, v in params.items():
            params[k] = data_manager.text_formatted(v)
    else:
        params = utils.load_json_file(params)

    request.node.request_args[request_name]["params"] = params

    if with_logs:
        logger.info(
            "Step: add_params_parameters - Query Parameters Added Successfully to the request args with logs.",
            request_name=request_name,
            request_args=request.node.request_args[request_name],
            test_name=request.node.name
        )
    else:
        logger.info(
            "Step: add_params_parameters - Query Parameters Added Successfully to the request args.",
            request_name=request_name
        )


def add_json_payload(
    request: FixtureRequest, request_name: str, json_payload: typing.Union[dict, str], with_logs: bool = False
):
    """add_json_payload

    Step Behavior
    -------------
    * Check for missing url or endpoint (by checking request_args attribute & request_name key in
        request_args). If not raise an exception and abort.
    * Add payload passed in the step as "data" in request arguments.
    """

    helpers.raise_for_mising_url_endpoint(request, request_name)
    if isinstance(json_payload, dict):
        # the first use case of adding payload as datatable
        payload = json_payload
    else:
        # second use case where user specifies json file
        payload = utils.load_json_file(json_payload)

    request.node.request_args[request_name]["json"] = payload

    if with_logs:
        logger.info(
            "Step: add_json_payload - Json Payload Added Successfully to the request args with logs.",
            request_name=request_name,
            request_args=request.node.request_args[request_name],
            test_name=request.node.name
        )
    else:
        logger.info(
            "Step: add_json_payload - Json Payload Added Successfully to the request args.",
            request_name=request_name
        )


def add_files_payload(
    request: FixtureRequest, request_name: str, files_payload: dict, with_logs: bool = False
):
    """add_files_payload

    Step Behavior
    -------------
    * Check for missing url or endpoint (by checking request_args attribute & request_name key in
        request_args). If not raise an exception and abort.
    * Add payload passed in the step as "files" in request arguments.
    """

    helpers.raise_for_mising_url_endpoint(request, request_name)
    request.node.request_args[request_name]["files"] = files_payload

    if with_logs:
        logger.info(
            "Step: add_files_payload - Files Payload Added Successfully to the request args with logs.",
            request_name=request_name,
            request_args=request.node.request_args[request_name],
            test_name=request.node.name
        )
    else:
        logger.info(
            "Step: add_files_payload - Files Payload Added Successfully to the request args.",
            request_name=request_name
        )


def add_data_payload(
    request: FixtureRequest, request_name: str, data_payload: typing.Union[dict, str], with_logs: bool = False
):
    """add_data_payload

    Step Behavior
    -------------
    * Check for missing url or endpoint (by checking request_args attribute & request_name key in
        request_args). If not raise an exception and abort.
    * Add payload passed in the step as "data" in request arguments.
    """

    helpers.raise_for_mising_url_endpoint(request, request_name)
    if isinstance(data_payload, dict):
        # the first use case of adding payload as datatable
        payload = data_payload
    else:
        # second use case where user specifies json file
        payload = utils.load_json_file(data_payload)

    request.node.request_args[request_name]["data"] = payload

    if with_logs:
        logger.info(
            "Step: add_data_payload - Data Payload Added Successfully to the request args with logs.",
            request_name=request_name,
            request_args=request.node.request_args[request_name],
            test_name=request.node.name
        )
    else:
        logger.info(
            "Step: add_data_payload - Data Payload Added Successfully to the request args.",
            request_name=request_name
        )


def make_api_request(
    request: FixtureRequest,
    api_response_container: dict,
    request_name: str,
    request_type: str,
    with_logs: bool = False
):
    """make_api_request

    Step Behavior
    -------------
    * Check for url and endpoint & request args for the request name
    * Make request using the request_args value for the named request, and
        Save the Response in api_response_container
    """

    helpers.raise_for_mising_url_endpoint(request, request_name)
    request_type = request_type.upper()
    request_args = request.node.request_args[request_name]
    if not hasattr(request.node, "request_auth"):
        request_args["auth"] = None
    else:
        request_args["auth"] = request.node.request_auth
    if request.node.name not in api_response_container:
        api_response_container[request.node.name] = dict()
    response = helpers.request_type_map.get(
        request_type, helpers.request_type_not_implemented
    )(**request_args)
    api_response_container[request.node.name][request_name] = response

    if with_logs:
        logger.info(
            "Step: make_api_request - Request Successfully made to the server with logs.",
            request_args=request_args,
            response_status_code=response.status_code,
            response_text=response.text or None
        )
    else:
        logger.info(
            "Step: make_api_request - Request Successfully made to the server.",
            request_name=request_name
        )


def set_env_variables(
    request: FixtureRequest,
    api_response_container: dict,
    request_name: str,
    env_variables: dict,
    with_logs: bool = False
):
    """set_env_variable

    This step has to be called only after sending the request out. Note that, the environment variables
    will be set only if the status code is < 400. This step has to be used in conjunction with verbose
    request mode.

    `env_variables: dict` (Required)
        key-value pairs of environment variable(s).
    `name_of_request` (Required)
        user friendly name for the request

    Step Behavior
    -------------
    * Check for url and endpoint & request args for the request name
    * Check for response in api_response_container
    * Set Environment Variables based on provided key-value pairs.
    """

    helpers.raise_for_mising_url_endpoint(request, request_name)
    helpers.raise_for_missing_response(request, request_name, api_response_container)

    response = api_response_container[request.node.name][request_name]

    if response.ok:
        for name, value in env_variables.items():
            os.environ[name] = str(value)
            if with_logs:
                logger.info(
                    "Step: set_env_variables - Environment Variable added successfully with logs.",
                    var_name=name,
                    value=value,
                )
            else:
                logger.info(
                    "Step: set_env_variables - Environment Variable added successfully.",
                    var_name=name
                )


"""
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------

STEPS RESPONSE

----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
"""


def get_api_response(
    request: FixtureRequest,
    api_response_container: dict,
    request_name: str,
    with_logs: bool = False
) -> requests.Response:
    """get_api_response

    Step Behavior
    -------------
    * As a prereqisite, assert that the named request is present in api_response_container.
    * If present, check for the status code and verify if it matches expected status code.
    """

    assert (
        request.node.name in api_response_container
    ), "Looks like no requests has been passed during this test!!"
    assert (
        request_name in api_response_container[request.node.name]
    ), f"There is no response present with name {request_name}"

    if with_logs:
        logger.info("Step: get_api_response - API response container: ", api_response_container=
        "Message: " + str(api_response_container[request.node.name][request_name].reason) +
        ", Status code: " + str(api_response_container[request.node.name][request_name].status_code) +
        ", Data: " + api_response_container[request.node.name][request_name].text)
    else:
        logger.info("Step: get_api_response")
    return api_response_container[request.node.name][request_name]
