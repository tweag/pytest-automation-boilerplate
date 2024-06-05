import time

import structlog
from pytest_bdd import parsers, given, when, then
from main.frontend.common.helpers.app import context_manager
from selenium.common.exceptions import NoSuchElementException
from main.frontend.common.helpers.selenium_generics import SeleniumGenerics
from main.frontend.common.step_definitions.steps_common import MOBILE_SUFFIX
from main.frontend.common.utils.locator_parser import Locators
from main.utils import data_manager

logger = structlog.get_logger(__name__)


# WEB & MOBILE contexts Predefined Step
@given(parsers.re("I click on (checkbox|button|dropdown|item|element) '(?P<locator_path>.*)'"))
@given(parsers.re("I tap on '(?P<locator_path>.*)'"))
@when(parsers.re("I click on (checkbox|button|dropdown|item|element) '(?P<locator_path>.*)'"))
@when(parsers.re("I tap on '(?P<locator_path>.*)'"))
def click_on_locator(selenium_generics: SeleniumGenerics, locators: Locators, locator_path: str):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            selenium_generics.click(locators.parse_and_get(locator_path, selenium_generics))
    else:
        selenium_generics.click(locators.parse_and_get(locator_path, selenium_generics))


# WEB context Predefined Step - Chrome Only
@given(parsers.re(
    "(I wait for maximum '(?P<wait_seconds>\\d+)' seconds, and )?I click on '(?P<locator_path>.+)'"))
@when(parsers.re(
    "(I wait for maximum '(?P<wait_seconds>\\d+)' seconds, and )?I click on '(?P<locator_path>.+)'"))
def click_element(selenium_generics: SeleniumGenerics, locators: Locators, locator_path: str, wait_seconds):
    waiting_time = int(wait_seconds) if wait_seconds else 20
    selenium_generics.click(locators.parse_and_get(locator_path, selenium_generics), max_wait_time=waiting_time)


# WEB context Predefined Step
@given(parsers.re("I (double click|doubleclick) on '(?P<locator_path>.*)'"))
@when(parsers.re("I (double click|doubleclick) on '(?P<locator_path>.*)'"))
def dbl_click_element(selenium_generics: SeleniumGenerics, locators: Locators, locator_path: str):
    selenium_generics.double_click(locators.parse_and_get(locator_path, selenium_generics))


# WEB context Predefined Step
@given(parsers.re("I click on SVG element '(?P<locator_path>.*)'"))
@when(parsers.re("I click on SVG element '(?P<locator_path>.*)'"))
def click_svg_element(selenium_generics: SeleniumGenerics, locators: Locators, locator_path):
    selenium_generics.click_by_action(locators.parse_and_get(locator_path, selenium_generics))


# WEB context Predefined Step
@given(parsers.re("I click on type:'(?P<element_type>.*)' element with text equal to '(?P<value>.*)'"),
       converters=dict(value=data_manager.text_formatted), )
@when(parsers.re("I click on type:'(?P<element_type>.*)' element with text equal to '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
def click_on_text(selenium_generics: SeleniumGenerics, element_type, value: str):
    selenium_generics.click(f"//{element_type}[normalize-space()='{value}']")


# WEB context Predefined Step
@given(parsers.re("I click on type:'(?P<element_type>.*)' that contains the text:'(?P<value>.*)'"),
       converters=dict(value=data_manager.text_formatted), )
@when(parsers.re("I click on type:'(?P<element_type>.*)' that contains the text:'(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
def click_on_partial_text(selenium_generics: SeleniumGenerics, element_type, value: str):
    selenium_generics.click(f"//{element_type}[contains(normalize-space(),'{value}')]")


# WEB contexts Predefined Step
@given(parsers.re(
    "I click on element with visible text '(?P<visibility_option>EQUALS|CONTAINS|STARTS_WITH|ENDS_WITH)' '(?P<value>.*)'"),
       converters=dict(value=data_manager.text_formatted), )
@when(parsers.re(
    "I click on element with visible text '(?P<visibility_option>EQUALS|CONTAINS|STARTS_WITH|ENDS_WITH)' '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
def click_on_element_by_visible_text(selenium_generics: SeleniumGenerics, locators, visibility_option: str, value: str):
    locator = locators.get_element_by_text(value, visibility_option)
    num_of_elements = len(selenium_generics.get_elements(locator))
    if num_of_elements == 1:
        selenium_generics.click(locator)
    else:
        raise NoSuchElementException(f"Element cannot be uniquely identified. Found: {num_of_elements} elements")


# MOBILE context Predefined Step
@given(parsers.re("I long tap on element '(?P<locator>.*)'"))
@when(parsers.re("I long tap on element '(?P<locator>.*)'"))
def long_tap(selenium_generics: SeleniumGenerics, locators: Locators, locator: str):
    with context_manager(driver=selenium_generics):
        selenium_generics.long_tap(selenium_generics, locators.parse_and_get(locator, selenium_generics))


# MOBILE contexts Predefined Step
@given(parsers.re(
    "I tap '(?P<corner>BOTTOM_LEFT|BOTTOM_RIGHT|TOP_LEFT|TOP_RIGHT)' corner of element '(?P<locator_path>.*)'"))  # noqa
@when(parsers.re(
    "I tap '(?P<corner>BOTTOM_LEFT|BOTTOM_RIGHT|TOP_LEFT|TOP_RIGHT)' corner of element '(?P<locator_path>.*)'"))  # noqa
def click_element_corner(selenium_generics: SeleniumGenerics, locators: Locators, corner: str, locator_path: str):
    """
    Taps the <corner> of the given element, in the given context
    """
    locator = locators.parse_and_get(locator_path, selenium_generics)
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            selenium_generics.tap_corner_of_element(selenium_generics, corner, locator)
    else:
        selenium_generics.tap_corner_of_element(selenium_generics, corner, locator)


# MOBILE context Predefined Step
@given(parsers.re(
    "On '(?P<platform>Android|iOS)' I tap on the x='(?P<x_value>.*)' % and y='(?P<y_value>.*)' % of element '(?P<locator_path>.*)'"))
@when(parsers.re(
    "On '(?P<platform>Android|iOS)' I tap on the x='(?P<x_value>.*)' % and y='(?P<y_value>.*)' % of element '(?P<locator_path>.*)'"))
def tap_with_percentage(selenium_generics: SeleniumGenerics, locators, platform: str, x_value: int, y_value: int,
                        locator_path):
    if selenium_generics.driver.capabilities['platformName'].lower() == platform.lower():
        if MOBILE_SUFFIX in locator_path:
            with context_manager(selenium_generics):
                locator = locators.parse_and_get(locator_path, selenium_generics)
                selenium_generics.tap_with_percentage(selenium_generics, locator, x_value, y_value)


# ANDROID MOBILE context Predefined Step
@given("On android, I tap on back navigation")
@when("On android, I tap on back navigation")
def tap_back_nav(selenium_generics: SeleniumGenerics):
    if selenium_generics.is_android():
        with context_manager(driver=selenium_generics):
            selenium_generics.back()


# iOS MOBILE context Predefined Step
@given(parsers.re("On iOS, I navigate back to app after clicking on '(?P<locator>.*)'"))
@when(parsers.re("On iOS, I navigate back to app after clicking on '(?P<locator>.*)'"))
def navigate_back_to_app(selenium_generics: SeleniumGenerics, locators: Locators, locator: str):
    if not selenium_generics.is_android():
        with context_manager(driver=selenium_generics):
            selenium_generics.click(locators.parse_and_get(locator, selenium_generics))


# WEB context Predefined Step
@given(parsers.re("I press '(?P<key>.*)'"))
@when(parsers.re("I press '(?P<key>.*)'"))
def press_key_not_focused_on_element(selenium_generics: SeleniumGenerics, key: str):
    logger.info("Pressing Key", key=key)
    selenium_generics.press_key(key)


# WEB context Predefined Step
@given(parsers.re("I focus over '(?P<locator_path>.*)' then I press '(?P<key>.*)'"))
@when(parsers.re("I focus over '(?P<locator_path>.*)' then I press '(?P<key>.*)'"))
def press_key_on_element(selenium_generics: SeleniumGenerics, locator_path: str, key: str, locators: Locators):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    logger.info("Pressing Key", locator=locator, key=key)
    selenium_generics.press_key_on_element(locator, key)


# WEB context Predefined Step
@when(parsers.re("I click item '(?P<inner_text>.*)' for element '(?P<locator_path>.*)'"),
      converters=dict(inner_text=data_manager.text_formatted), )
def add_item_for_element(selenium_generics: SeleniumGenerics, locators: Locators, inner_text: str, locator_path: str):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    locator = locator.format(inner_text)
    selenium_generics.click(locator)


@when(parsers.re("I set value '(?P<value>.*)' for item '(?P<inner_text>.*)' on element '(?P<locator_path>.*)'"),
      converters=dict(inner_text=data_manager.text_formatted), )
def add_item_for_element(selenium_generics: SeleniumGenerics, locators: Locators, value: str, inner_text: str,
                         locator_path: str):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    locator = locator.format(inner_text)
    selenium_generics.enter_text(locator, value)


@given(parsers.re("I pause for '(?P<seconds>.*)' s"), converters=dict(seconds=int))
@when(parsers.re("I pause for '(?P<seconds>.*)' s"), converters=dict(seconds=int))
def pause_execution(seconds: int):
    time.sleep(seconds)
