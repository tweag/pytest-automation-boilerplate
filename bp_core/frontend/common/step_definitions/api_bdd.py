import structlog

from _pytest.fixtures import FixtureRequest
from pytest_bdd import parsers, when, then
from pytest_check import check
from bp_core.backend.common.step_definitions.steps_common import set_request_endpoint, set_request_headers, \
    add_json_payload, make_api_request, get_api_response
from bp_core.frontend.common.helpers.app import context_manager
from assertpy import assert_that
from bp_core.frontend.common.helpers.selenium_generics import SeleniumGenerics
from bp_core.frontend.common.step_definitions.steps_common import UI_API_CALL, MOBILE_SUFFIX
from bp_core.utils.bp_storage import BPStorage


logger = structlog.get_logger(__name__)


# WEB context Predefined Step
# ID 1501
@when(parsers.re("I '(?P<request_type>.*)' an API request having base URL '(?P<base_url>.*)' with endpoint '(?P<endpoint>.*)' with headers '(?P<headers>.*)' and payload '(?P<payload>.*)' and store the response value"))
def send_api_request_store_value_bp_storage(selenium_generics: SeleniumGenerics, request: FixtureRequest, request_type: str, base_url: str, endpoint: str, headers: str, payload: str):
    api_response_container = dict()
    set_request_endpoint(request, base_url=base_url, endpoint=endpoint, request_name=UI_API_CALL)
    set_request_headers(request, headers=headers, request_name=UI_API_CALL)
    add_json_payload(request, json_payload=payload, request_name=UI_API_CALL)
    make_api_request(request, api_response_container=api_response_container, request_type=request_type, request_name=UI_API_CALL)
    BPStorage.store_api_bdd_response(get_api_response(request, api_response_container=api_response_container, request_name=UI_API_CALL))


# WEB & MOBILE contexts Predefined Step
# ID 1502
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' has the text equal with the API BDD response key '(?P<key>.*)'"))
def api_contains_text(selenium_generics: SeleniumGenerics, locators, soft_assert: str, locator_path: str, key: str):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    else:
        actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_text).is_equal_to(BPStorage.get_api_bdd_response().json()[key])
    else:
        assert_that(actual_text).is_equal_to(BPStorage.get_api_bdd_response().json()[key])
