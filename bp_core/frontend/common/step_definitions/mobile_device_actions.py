
import structlog

from _pytest.fixtures import FixtureRequest
from pytest_bdd import parsers, when, then
from bp_core.backend.common.step_definitions.steps_common import set_request_endpoint, \
    add_json_payload, make_api_request, get_api_response, setup_basic_auth
from bp_core.frontend.common.helpers.selenium_generics import SeleniumGenerics
from bp_core.utils import data_manager

logger = structlog.get_logger(__name__)


# MOBILE Predefined Step
# ID 1201
@when(parsers.re("I turn '(?P<network_status>ON|OFF)' the network connectivity in Browserstack"))
@then(parsers.re("I turn '(?P<network_status>ON|OFF)' the network connectivity in Browserstack"))
def change_network_status(selenium, request: FixtureRequest, network_status: str):
    NETWORK_STATUS = "CHANGE_NETWORK_STATUS_IN_BROWSERSTACK"
    payload = {"networkProfile": "no-network"} if network_status.lower() == "off" else {"networkProfile": "reset"}
    api_response = dict()
    set_request_endpoint(request, base_url="https://api-cloud.browserstack.com/app-automate/sessions/",
                         endpoint=f"{selenium.session_id}/update_network.json", request_name=NETWORK_STATUS)
    selenium_host = request.session.config.option.selenium_host
    BS_USERNAME = selenium_host[0: selenium_host.index(":")]
    BS_PASSWORD = selenium_host[selenium_host.index(":") + 1: selenium_host.index("@")]
    setup_basic_auth(request=request, username=BS_USERNAME, password=BS_PASSWORD)
    add_json_payload(request, json_payload=payload, request_name=NETWORK_STATUS)
    make_api_request(request, api_response, request_type="PUT", request_name=NETWORK_STATUS)
    assert get_api_response(request, api_response, request_name=NETWORK_STATUS).status_code == 200


# MOBILE Predefined Step
# ID 1202
@when("I reset the mobile app")
@then("I reset the mobile app")
def reset_app(selenium_generics: SeleniumGenerics):
    current_context = selenium_generics.get_current_context()
    selenium_generics.reset()
    if selenium_generics.is_android():
        selenium_generics.switch_context(current_context)


# MOBILE Predefined Step
# 1203
@when(parsers.re("I put the mobile app in background for '(?P<seconds>.*)' seconds"),
      converters=dict(seconds=data_manager.text_formatted))
@then(parsers.re("I put the mobile app in background for '(?P<seconds>.*)' seconds"),
      converters=dict(seconds=data_manager.text_formatted))
def background_app(selenium_generics: SeleniumGenerics, seconds: int):
    selenium_generics.background_app(seconds=int(seconds))


@when("I hide the keyboard on mobile app")
@then("I hide the keyboard on mobile app")
def hide_keyboard(selenium_generics: SeleniumGenerics):
    current_context = selenium_generics.get_current_context()
    selenium_generics.background_app()
    if selenium_generics.is_android():
        selenium_generics.switch_context(current_context)
