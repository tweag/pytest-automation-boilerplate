import datetime
from pytest_bdd import when, parsers, given, then
from main.frontend.common.utils.locator_parser import Locators
from main.frontend.common.helpers.selenium_generics import SeleniumGenerics
import re
from assertpy import assert_that
from selenium.webdriver.common.by import By
from main.frontend.common.helpers.app import context_manager
from pathlib import Path

from main.utils import data_manager

from main.frontend.common.step_definitions.attribute_assertion import \
    element_displayed, wait_for_displayed
from main.frontend.common.step_definitions.click_touch_and_keyboard_actions import click_on_locator
from main.frontend.common.step_definitions.text_assertion_editing import set_element_value, \
    element_equals_text

MOBILE_SUFFIX = "_mob"


@given(parsers.re("I set selenium resolution to '(?P<width>.*)' per '(?P<height>.*)'"),
       converters=dict(width=str, height=str))
def set_selenium_resolution(selenium, width, height):
    selenium.set_window_size(width, height)


@then(parsers.re(
    "I expect element '(?P<locator_path>.*)' has items:(?P<data_table_raw>.*)", flags=re.S))
def items_in_element(selenium_generics: SeleniumGenerics, selenium, locators: Locators, locator_path, data_table_raw):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    data_table_list = data_table_raw.split("|")
    data_table_list = [elem.strip() for elem in data_table_list]
    data_table_list = list(filter(lambda elem: elem != "", data_table_list))
    for i in data_table_list:
        locator = locator.format(i)
        assert_that(
            selenium.find_element(By.XPATH,
                                  locator).is_displayed()
        ).is_true()


@then(parsers.re(
    "I expect '(?P<text>.*)' in common element '(?P<locator_path>.*)' with innertext:(?P<data_table_raw>.*)",
    flags=re.S))
def common_element_with_innertext(selenium_generics: SeleniumGenerics, locators: Locators, text, locator_path,
                                  data_table_raw):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    data_table_list = data_table_raw.split("|")
    data_table_list = [elem.strip() for elem in data_table_list]
    data_table_list = list(filter(lambda elem: elem != "", data_table_list))

    for i in data_table_list:
        locator = locator.format(i)
        actual_text = selenium_generics.get_element_text(locator)
        assert (actual_text == text)


@then(parsers.re(
    "I expect '(?P<locator_path>.*)' elements are displayed with innertext:(?P<data_table_raw>.*)",
    flags=re.S))
def elements_with_innertext(selenium_generics, locators: Locators, locator_path, data_table_raw):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    data_table_list = data_table_raw.split("|")
    data_table_list = [elem.strip() for elem in data_table_list]
    data_table_list = list(filter(lambda elem: elem != "", data_table_list))
    for i in data_table_list:
        locator = locator.format(i)
        assert_that(
            selenium_generics.get_element(locator).is_displayed()
        ).is_true()


@then(parsers.re(
    "I expect '(?P<count>.*)' elements of '(?P<locator_path>.*)' are displayed"),
    converters=dict(count=int, locator_path=str))
def check_elements_count(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, count):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    elements = selenium_generics.get_elements(locator)
    actual_count = len(elements)
    assert (actual_count == count)


@then(parsers.re(
    "I expect element '(?P<locator_path>.*)' is not enabled"),
    converters=dict(locator_path=str))
def element_is_disabled(selenium_generics: SeleniumGenerics, locators: Locators, locator_path):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    ele = selenium_generics.get_element(locator)
    if ele.get_property('disabled'):
        assert True
    else:
        assert False


@then(parsers.re(
    "I expect that element '(?P<locator_path>.*)' is enabled"),
    converters=dict(locator_path=str))
def element_is_disabled(selenium_generics: SeleniumGenerics, locators: Locators, locator_path):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    ele = selenium_generics.get_element(locator)
    if ele.get_property('disabled'):
        assert False
    else:
        assert True


@then(parsers.re(
    "I expect value '(?P<inner_text>.*)' is not enabled for element '(?P<locator_path>.*)'")
)
def element_with_value_is_not_enabled(
    selenium_generics: SeleniumGenerics,
    locators: Locators,
    locator_path: str,
    inner_text: str
):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    locator = locator.format(inner_text)
    ele = selenium_generics.get_element(locator)
    assert selenium_generics.is_enabled(
        ele), f"Element {locator_path} is enabled."


@then(parsers.re(
    "I expect value '(?P<inner_text>.*)' is enabled for element '(?P<locator_path>.*)'")
)
def element_with_value_is_enabled(
    selenium_generics: SeleniumGenerics,
    locators: Locators,
    locator_path: str,
    inner_text: str
):
    value = data_manager.text_formatted(inner_text)
    locator = locators.parse_and_get(locator_path, selenium_generics)
    locator = locator.format(value)
    ele = selenium_generics.get_element(locator)
    assert selenium_generics.is_enabled(
        ele), f"Element {locator_path} is not enabled."


@when(parsers.re(
    "I click item '(?P<inner_text>.*)' for element '(?P<locator_path>.*)'")
)
def add_item_for_element(
    selenium_generics: SeleniumGenerics,
    locators: Locators,
    locator_path: str,
    inner_text: str
):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    locator = locator.format(inner_text)
    selenium_generics.click(locator)


@then(parsers.re(
    "I expect that the element '(?P<locator_path>.*)' is highlighted")
)
def element_with_value_is_not_enabled(
    selenium_generics: SeleniumGenerics,
    locators: Locators,
    locator_path
):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    backcolor = selenium_generics.get_css_value(locator, 'background-color')
    default_backcolor = "rgba(0, 0, 0, 0)"
    assert backcolor != default_backcolor


@when(parsers.re(
    "I switch to newly opened tab")
)
def switch_to_new_tab(
    selenium
):
    new_tab = selenium.window_handles[1]
    selenium.switch_to.window(new_tab)


@when(parsers.re(
    "I refresh page")
)
def switch_to_new_tab(
    selenium
):
    selenium.refresh()


@when(parsers.re(
    "I switch to parent tab")
)
def switch_to_new_tab(
    selenium
):
    parent_tab = selenium.window_handles[0]
    selenium.switch_to.window(parent_tab)


@when(parsers.re(
    "I close the browser")
)
def close_browser(
    selenium
):
    selenium.close()


@then(parsers.re(
    "I expect that item '(?P<inner_text>.*)' for element '(?P<locator_path>.*)' is displayed")
)
def element_visible_on_page(
    selenium_generics: SeleniumGenerics,
    locators: Locators,
    locator_path: str,
    inner_text: str
):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    locator = locator.format(inner_text)
    assert selenium_generics.is_element_visible(locator)


@then(parsers.re(
    "I expect '(?P<locator_path>.*)' elements are present with innertext:(?P<data_table_raw>.*)",
    flags=re.S))
def elements_with_innertext_in_dom(selenium_generics: SeleniumGenerics, locators: Locators, locator_path,
                                   data_table_raw):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    data_table_list = data_table_raw.split("|")
    data_table_list = [elem.strip() for elem in data_table_list]
    data_table_list = list(filter(lambda elem: elem != "", data_table_list))
    for i in data_table_list:
        locator = locator.format(i)
        assert_that(
            selenium_generics.is_element_present_on_dom(locator)
        ).is_true()


@then(parsers.re(
    "The element with inner text '(?P<inner_text>.*)' and element '(?P<locator_path>.*)' has text '(?P<text>.*)'"),
    converters=dict(inner_text=data_manager.text_formatted, text=data_manager.text_formatted), )
def element_with_innertext_equals_text(selenium_generics: SeleniumGenerics, locators: Locators, locator_path,
                                       inner_text, text):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    locator = locator.format(inner_text)
    actual_text = selenium_generics.get_element_text(locator)
    assert_that(actual_text).contains(text)


# WEB File Attachment
@given(parsers.re("I attach file '(?P<file_path>.*)' to input field '(?P<locator_path>.*)'"),
       converters=dict(text=data_manager.text_formatted), )
@when(parsers.re("I attach file '(?P<file_path>.*)' to input field '(?P<locator_path>.*)'"),
      converters=dict(text=data_manager.text_formatted), )
def attach_file(selenium_generics: SeleniumGenerics, file_path: str, locators: Locators, locator_path):
    relative_path = Path(file_path)
    if relative_path and relative_path.absolute().is_file():
        full_path = relative_path.absolute().as_posix()
        selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), full_path)
    else:
        raise FileNotFoundError(f"The file {file_path}' is not a valid path to a file")


@when(parsers.re("I set text with current_timestamp '(?P<text>.*)' to field '(?P<locator_path>.*)'"),
      converters=dict(text=data_manager.text_formatted), )
def set_element_value_with_timestamp(selenium_generics: SeleniumGenerics, text: str, locators: Locators, locator_path):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics),
                                         text + str(datetime.datetime.now()))
    else:
        selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics),
                                     text + str(datetime.datetime.now()))


@given('I open the mobile application')
def open_mobile_app():
    print("ToDo - Open mobile application")
