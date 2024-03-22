import polling
import structlog

from pytest_bdd import parsers, given, when, then
from pytest_check import check
from bp_core.frontend.common.helpers.app import context_manager
from selenium.common.exceptions import TimeoutException
from assertpy import assert_that
from bp_core.frontend.common.helpers.selenium_generics import SeleniumGenerics
from bp_core.frontend.common.step_definitions.steps_common import MOBILE_SUFFIX
from bp_core.frontend.common.utils.locator_parser import Locators
from bp_core.utils import data_manager

logger = structlog.get_logger(__name__)


# WEB context Predefined Step
@given(parsers.re(r"(With soft assertion '(?P<soft_assert>.*)' )?The attribute '(?P<attribute>.*)' of element '(?P<locator_path>.*)' is the value '(?P<value>.*)'(\s+)?((?:within)\s+(?:')(?P<wait_for>\w+)(?:') seconds)?$"),
    converters=dict(value=data_manager.text_formatted), )
@when(parsers.re(r"(With soft assertion '(?P<soft_assert>.*)' )?The attribute '(?P<attribute>.*)' of element '(?P<locator_path>.*)' is the value '(?P<value>.*)'(\s+)?((?:within)\s+(?:')(?P<wait_for>\w+)(?:') seconds)?$"),
    converters=dict(value=data_manager.text_formatted), )
@then(parsers.re(r"(With soft assertion '(?P<soft_assert>.*)' )?The attribute '(?P<attribute>.*)' of element '(?P<locator_path>.*)' is the value '(?P<value>.*)'(\s+)?((?:within)\s+(?:')(?P<wait_for>\w+)(?:') seconds)?$"),
    converters=dict(value=data_manager.text_formatted), )
def check_property_is(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path, value: str, attribute, wait_for):
    wait_for = int(wait_for) if wait_for else None
    if wait_for:
        try:
            polling.poll(lambda: selenium_generics.get_attribute_of_element(locators.parse_and_get(locator_path, selenium_generics), attribute) == value, step=2, timeout=wait_for)
        except (TimeoutException, polling.TimeoutException):
            pass
    actual_value = selenium_generics.get_attribute_of_element(
        locators.parse_and_get(locator_path, selenium_generics), attribute)
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_value).is_equal_to(value)
    else:
        assert_that(actual_value).is_equal_to(value)


# WEB context Predefined Step
@given(parsers.re(r"(With soft assertion '(?P<soft_assert>.*)' )?The attribute '(?P<attribute>.*)' of element '(?P<locator_path>.*)' is not the value '(?P<value>.*)'(\s+)?((?:within)\s+(?:')(?P<wait_for>\w+)(?:') seconds)?$"),
    converters=dict(value=data_manager.text_formatted), )
@when(parsers.re(r"(With soft assertion '(?P<soft_assert>.*)' )?The attribute '(?P<attribute>.*)' of element '(?P<locator_path>.*)' is not the value '(?P<value>.*)'(\s+)?((?:within)\s+(?:')(?P<wait_for>\w+)(?:') seconds)?$"),
    converters=dict(value=data_manager.text_formatted), )
@then(parsers.re(r"(With soft assertion '(?P<soft_assert>.*)' )?The attribute '(?P<attribute>.*)' of element '(?P<locator_path>.*)' is not the value '(?P<value>.*)'(\s+)?((?:within)\s+(?:')(?P<wait_for>\w+)(?:') seconds)?$"),
    converters=dict(value=data_manager.text_formatted), )
def check_property_is_not(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path, value: str, attribute, wait_for):
    wait_for = int(wait_for) if wait_for else None
    if wait_for:
        try:
            polling.poll(lambda: selenium_generics.get_attribute_of_element(locators.parse_and_get(locator_path, selenium_generics),attribute) != value, step=2, timeout=wait_for)
        except (TimeoutException, polling.TimeoutException):
            pass
    actual_value = selenium_generics.get_attribute_of_element(
        locators.parse_and_get(locator_path, selenium_generics), attribute)
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_value).is_not_equal_to(value)
    else:
        assert_that(actual_value).is_not_equal_to(value)


# WEB context Predefined Step
@given(parsers.re(r"(With soft assertion '(?P<soft_assert>.*)' )?The css attribute '(?P<attribute>.*)' of element '(?P<locator_path>.*)' is the value '(?P<value>.*)'(\s+)?((?:within)\s+(?:')(?P<wait_for>\w+)(?:') seconds)?$"),
    converters=dict(value=data_manager.text_formatted), )
@when(parsers.re(r"(With soft assertion '(?P<soft_assert>.*)' )?The css attribute '(?P<attribute>.*)' of element '(?P<locator_path>.*)' is the value '(?P<value>.*)'(\s+)?((?:within)\s+(?:')(?P<wait_for>\w+)(?:') seconds)?$"),
    converters=dict(value=data_manager.text_formatted), )
@then(parsers.re(r"(With soft assertion '(?P<soft_assert>.*)' )?The css attribute '(?P<attribute>.*)' of element '(?P<locator_path>.*)' is the value '(?P<value>.*)'(\s+)?((?:within)\s+(?:')(?P<wait_for>\w+)(?:') seconds)?$"),
    converters=dict(value=data_manager.text_formatted), )
def check_css_property_is(attribute, selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path, value: str, wait_for):
    wait_for = int(wait_for) if wait_for else None
    if wait_for:
        try:
            polling.poll(lambda: selenium_generics.get_css_value(locators.parse_and_get(locator_path, selenium_generics), attribute) == value, step=2, timeout=wait_for)
        except (TimeoutException, polling.TimeoutException):
            pass
    actual_value = selenium_generics.get_css_value(locators.parse_and_get(locator_path, selenium_generics), attribute)
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_value).is_equal_to(value)
    else:
        assert_that(actual_value).is_equal_to(value)


# WEB context Predefined Step
@given(parsers.re(r"(With soft assertion '(?P<soft_assert>.*)' )?The css attribute '(?P<attribute>.*)' of element '(?P<locator_path>.*)' is not the value '(?P<value>.*)'(\s+)?((?:within)\s+(?:')(?P<wait_for>\w+)(?:') seconds)?$"),
    converters=dict(value=data_manager.text_formatted), )
@when(parsers.re(r"(With soft assertion '(?P<soft_assert>.*)' )?The css attribute '(?P<attribute>.*)' of element '(?P<locator_path>.*)' is not the value '(?P<value>.*)'(\s+)?((?:within)\s+(?:')(?P<wait_for>\w+)(?:') seconds)?$"),
    converters=dict(value=data_manager.text_formatted), )
@then(parsers.re(r"(With soft assertion '(?P<soft_assert>.*)' )?The css attribute '(?P<attribute>.*)' of element '(?P<locator_path>.*)' is not the value '(?P<value>.*)'(\s+)?((?:within)\s+(?:')(?P<wait_for>\w+)(?:') seconds)?$"),
    converters=dict(value=data_manager.text_formatted), )
def check_css_property_is_not(attribute, selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path, value: str, wait_for):
    wait_for = int(wait_for) if wait_for else None
    if wait_for:
        try:
            polling.poll(lambda: selenium_generics.get_css_value(locators.parse_and_get(locator_path, selenium_generics), attribute) != value, step=2, timeout=wait_for)
        except (TimeoutException, polling.TimeoutException):
            pass
    actual_value = selenium_generics.get_css_value(locators.parse_and_get(locator_path, selenium_generics), attribute)
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_value).is_not_equal_to(value)
    else:
        assert_that(actual_value).is_not_equal_to(value)


# WEB & MOBILE contexts Predefined Step
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?There is an element '(?P<locator_path>.*)' on the page"))
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is displayed"))
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?There is an element '(?P<locator_path>.*)' on the page"))
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is displayed"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?There is an element '(?P<locator_path>.*)' on the page"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is displayed"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect that element '(?P<locator_path>.*)' (is displayed|exists)"))
def element_displayed(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            if soft_assert is not None and soft_assert.lower() == 'true':
                with check:
                    assert selenium_generics.is_element_visible(locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is not visible."
            else:
                assert selenium_generics.is_element_visible(
                    locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is not visible."
    else:
        if soft_assert is not None and soft_assert.lower() == 'true':
            with check:
                assert selenium_generics.is_element_visible(locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is not visible."
        else:
            assert selenium_generics.is_element_visible(
                locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is not visible."


# WEB & MOBILE contexts Predefined Step
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?There is no element '(?P<locator_path>.*)' on the page"))
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is not displayed"))
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?There is no element '(?P<locator_path>.*)' on the page"))
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is not displayed"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?There is no element '(?P<locator_path>.*)' on the page"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is not displayed"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect that element '(?P<locator_path>.*)' (is not displayed|does not exist)"))
def element_not_displayed(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            if soft_assert is not None and soft_assert.lower() == 'true':
                with check:
                    assert selenium_generics.is_element_invisible(locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is visible."
            else:
                assert selenium_generics.is_element_invisible(
                    locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is visible."
    else:
        if soft_assert is not None and soft_assert.lower() == 'true':
            with check:
                assert selenium_generics.is_element_invisible(locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is visible."
        else:
            assert selenium_generics.is_element_invisible(
                locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is visible."


# WEB & MOBILE contexts Predefined Step
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect that element '(?P<locator_path>.*)' appears exactly '(?P<occurrence_count>.*)' times"),
    converters=dict(occurrence_count=data_manager.text_formatted), )
def check_element_exists(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path, occurrence_count: int, ):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            if soft_assert is not None and soft_assert.lower() == 'true':
                with check:
                    assert (len(selenium_generics.get_elements(locators.parse_and_get(locator_path, selenium_generics))) == int(occurrence_count))
            else:
                assert (len(selenium_generics.get_elements(
                    locators.parse_and_get(locator_path, selenium_generics))) == int(occurrence_count))
    else:
        if soft_assert is not None and soft_assert.lower() == 'true':
            with check:
                assert (len(selenium_generics.get_elements(locators.parse_and_get(locator_path, selenium_generics))) == int(occurrence_count))
        else:
            assert (len(selenium_generics.get_elements(
                locators.parse_and_get(locator_path, selenium_generics))) == int(occurrence_count))


# WEB & MOBILE contexts Predefined Step
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect that element '(?P<locator_path>.*)' does not appear exactly '(?P<occurrence_count>.*)' times"),
    converters=dict(occurrence_count=data_manager.text_formatted), )
def check_element_not_exists(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path, occurrence_count: int, ):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            if soft_assert is not None and soft_assert.lower() == 'true':
                with check:
                    assert (len(selenium_generics.get_elements(locators.parse_and_get(locator_path, selenium_generics))) != int(occurrence_count))
            else:
                assert (len(selenium_generics.get_elements(
                    locators.parse_and_get(locator_path, selenium_generics))) != int(occurrence_count))
    else:
        if soft_assert is not None and soft_assert.lower() == 'true':
            with check:
                assert (len(selenium_generics.get_elements(locators.parse_and_get(locator_path, selenium_generics))) != int(occurrence_count))
        else:
            assert (len(selenium_generics.get_elements(
                locators.parse_and_get(locator_path, selenium_generics))) != int(occurrence_count))


# WEB & MOBILE contexts Predefined Step
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect that element '(?P<locator_path>.*)' becomes visible within '(?P<wait_for>.*)' seconds"),
    converters=dict(wait_for=data_manager.text_formatted), )
def wait_for_displayed(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path: str, wait_for: int, ):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            if soft_assert is not None and soft_assert.lower() == 'true':
                with check:
                    assert selenium_generics.is_element_visible(locators.parse_and_get(locator_path, selenium_generics), int(wait_for))
            else:
                assert selenium_generics.is_element_visible(locators.parse_and_get(locator_path, selenium_generics), int(wait_for))
    else:
        if soft_assert is not None and soft_assert.lower() == 'true':
            with check:
                assert selenium_generics.is_element_visible(locators.parse_and_get(locator_path, selenium_generics), int(wait_for))
        else:
            assert selenium_generics.is_element_visible(locators.parse_and_get(locator_path, selenium_generics), int(wait_for))


@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect that element '(?P<locator_path>.*)' becomes invisible within '(?P<wait_for>.*)' seconds"),
    converters=dict(wait_for=data_manager.text_formatted), )
def wait_for_not_displayed(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path: str, wait_for: int):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            if soft_assert is not None and soft_assert.lower() == 'true':
                with check:
                    assert selenium_generics.is_element_invisible(locators.parse_and_get(locator_path, selenium_generics), int(wait_for))
            else:
                assert selenium_generics.is_element_invisible(locators.parse_and_get(locator_path, selenium_generics),
                                                              int(wait_for))
    else:
        if soft_assert is not None and soft_assert.lower() == 'true':
            with check:
                assert selenium_generics.is_element_invisible(locators.parse_and_get(locator_path, selenium_generics), int(wait_for))
        else:
            assert selenium_generics.is_element_invisible(locators.parse_and_get(locator_path, selenium_generics),
                                                          int(wait_for))


# WEB context Predefined Step

@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect that element '(?P<locator_path>.*)' is within the viewport"))
def check_within_viewport(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert:str, locator_path: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics._is_in_viewport(locators.parse_and_get(locator_path, selenium_generics))
    else:
        assert selenium_generics._is_in_viewport(locators.parse_and_get(locator_path, selenium_generics))


# WEB context Predefined Step
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect that element '(?P<locator_path>.*)' is not within the viewport"))
def check_within_viewport(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert not selenium_generics._is_in_viewport(locators.parse_and_get(locator_path, selenium_generics))
    else:
        assert not selenium_generics._is_in_viewport(locators.parse_and_get(locator_path, selenium_generics))


@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is enabled"))
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is enabled"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is enabled"))
def element_enabled(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            if soft_assert is not None and soft_assert.lower() == 'true':
                with check:
                    assert selenium_generics.is_enabled(locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is not enabled."
            else:
                assert selenium_generics.is_enabled(
                    locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is not enabled."
    else:
        if soft_assert is not None and soft_assert.lower() == 'true':
            with check:
                assert selenium_generics.is_enabled(locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is not enabled."
        else:
            assert selenium_generics.is_enabled(locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is not enabled."


# WEB & MOBILE contexts Predefined Step
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is not enabled"))
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is not enabled"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is not enabled"))
def element_not_enabled(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            if soft_assert is not None and soft_assert.lower() == 'true':
                with check:
                    assert not selenium_generics.is_enabled(locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is enabled."
    else:
        if soft_assert is not None and soft_assert.lower() == 'true':
            with check:
                assert not selenium_generics.is_enabled(locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is enabled."


# WEB context Predefined Step
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is selected"))
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is selected"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is selected"))
def element_selected(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.is_selected(locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is not selected."
    else:
        assert selenium_generics.is_selected(
            locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is not selected."


# WEB context Predefined Step
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is not selected"))
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is not selected"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' is not selected"))
def element_not_selected(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert not selenium_generics.is_selected(locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is selected."
    else:
        assert not selenium_generics.is_selected(
            locators.parse_and_get(locator_path, selenium_generics)), f"Element {locator_path} is selected."

