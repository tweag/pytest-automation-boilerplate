
import structlog

from _pytest.fixtures import FixtureRequest
from pytest_bdd import parsers, when, then
from bp_core.backend.common.step_definitions.steps_common import set_request_endpoint, \
    add_json_payload, make_api_request, get_api_response, setup_basic_auth
from bp_core.frontend.common.helpers.selenium_generics import SeleniumGenerics
from bp_core.utils import data_manager

logger = structlog.get_logger(__name__)


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
