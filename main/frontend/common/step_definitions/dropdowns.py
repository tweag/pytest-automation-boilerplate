"""
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
"""
import time
import structlog
import re

from pytest_bdd import parsers, given, when, then
from pytest_check import check
from main.frontend.common.helpers.app import context_manager
from selenium.common.exceptions import NoSuchElementException

from assertpy import assert_that
from main.frontend.common.helpers.selenium_generics import SeleniumGenerics
from main.frontend.common.step_definitions.steps_common import MOBILE_SUFFIX
from main.frontend.common.utils.locator_parser import Locators
from main.utils.gherkin_utils import data_table_vertical_converter
from main.utils import data_manager

logger = structlog.get_logger(__name__)


# WEB & MOBILE contexts Predefined Step
# ID 701
@given(parsers.re("I select the value '(?P<value>.*)' from dropdown '(?P<locator_path>.*)'"),
    converters=dict(value=data_manager.text_formatted), )
@when(parsers.re("I select the value '(?P<value>.*)' from dropdown '(?P<locator_path>.*)'"),
    converters=dict(value=data_manager.text_formatted), )
def select_dropdown_by_value(selenium_generics: SeleniumGenerics, value: str, locators: Locators, locator_path):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            selenium_generics.select_dropdown_value(locators.parse_and_get(locator_path, selenium_generics), value)
    else:
        selenium_generics.select_dropdown_value(locators.parse_and_get(locator_path, selenium_generics), value)


# WEB & MOBILE contexts Predefined Step
# ID 702
@given(parsers.re("I select the value at index '(?P<index>.*)' from dropdown '(?P<locator_path>.*)'"),
    converters=dict(index=data_manager.text_formatted), )
@when(parsers.re("I select the value at index '(?P<index>.*)' from dropdown '(?P<locator_path>.*)'"),
    converters=dict(index=data_manager.text_formatted), )
def select_dropdown_by_index(selenium_generics: SeleniumGenerics, index: int, locators: Locators, locator_path):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            selenium_generics.select_dropdown_value_at_index(locators.parse_and_get(locator_path, selenium_generics),
                                                             int(index))
    else:
        selenium_generics.select_dropdown_value_at_index(locators.parse_and_get(locator_path, selenium_generics),
                                                         int(index))


# WEB context Predefined Step
# ID 703
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect the selected dropdown '(?P<locator_path>.*)' text is '(?P<value>.*)'"),
    converters=dict(value=data_manager.text_formatted), )
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect the selected dropdown '(?P<locator_path>.*)' text is '(?P<value>.*)'"),
    converters=dict(value=data_manager.text_formatted), )
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect the selected dropdown '(?P<locator_path>.*)' text is '(?P<value>.*)'"),
    converters=dict(value=data_manager.text_formatted), )
def get_selected_dropdown_text(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path, value: str):
    actual_text = selenium_generics.get_first_selected_option(
        locators.parse_and_get(locator_path, selenium_generics)).text
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_text).is_equal_to(value)
    else:
        assert_that(actual_text).is_equal_to(value)


# ID 704
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect that drop-down list '(?P<locator_path>.*)' contains the values:(?P<table_values>.*)", flags=re.S),
    converters=dict(table_values=data_table_vertical_converter))
def check_dropdown_contains_values(selenium_generics, locators, soft_assert, locator_path, table_values):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            selenium_generics.contains_expected_and_ui_values(
                locators.parse_and_get(locator_path, selenium_generics), table_values)
    else:
        selenium_generics.contains_expected_and_ui_values(
            locators.parse_and_get(locator_path, selenium_generics), table_values)


# ID 705
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect that drop-down list '(?P<locator_path>.*)' does not contains the values:(?P<table_values>.*)", flags=re.S),
    converters=dict(table_values=data_table_vertical_converter))
def check_dropdown_not_contains_values(selenium_generics, locators, soft_assert, locator_path, table_values):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            selenium_generics.does_not_contains_expected_and_ui_values(
                locators.parse_and_get(locator_path, selenium_generics), table_values)
    else:
        selenium_generics.does_not_contains_expected_and_ui_values(
            locators.parse_and_get(locator_path, selenium_generics), table_values)


# ID 706
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect that drop-down list '(?P<locator_path>.*)' has in that specific order, only the values:(?P<table_values>.*)", flags=re.S),
    converters=dict(table_values=data_table_vertical_converter))
def check_dropdown_equal_values(selenium_generics, locators, soft_assert, locator_path, table_values):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            selenium_generics.compare_expected_and_ui_values_with_order(
                locators.parse_and_get(locator_path, selenium_generics), table_values)
    else:
        selenium_generics.compare_expected_and_ui_values_with_order(
            locators.parse_and_get(locator_path, selenium_generics), table_values)


# WEB context Predefined Step
# ID 707
@given(parsers.re(r"I select an item index '(?P<index>.*)' from a searchable dropdown with '(?P<type>label|placeholder|visible text)' '(?P<label>.*)' and search text '(?P<text>.*)'(\s+)?((?:with wait time)\s+(?:')(?P<timeout>.*)(?:') seconds)?$"),
      converters=dict(label=data_manager.text_formatted, text=data_manager.text_formatted))
@when(parsers.re(r"I select an item index '(?P<index>.*)' from a searchable dropdown with '(?P<type>label|placeholder|visible text)' '(?P<label>.*)' and search text '(?P<text>.*)'(\s+)?((?:with wait time)\s+(?:')(?P<timeout>.*)(?:') seconds)?$"),
      converters=dict(label=data_manager.text_formatted, text=data_manager.text_formatted))
def select_item_from_searchable_dropdown(selenium_generics: SeleniumGenerics, locators, index: str, label: str, text: str, timeout: str, type: str):
    def _select_element_from_dropdown_by_index(idx, dropdown_element_locator):
        num_of_elements = len(selenium_generics.get_elements(locator=dropdown_element_locator))
        if num_of_elements == 1:
            selenium_generics.enter_text(locator=locator, text_to_enter=text)
            time.sleep(int(timeout))
            for _ in range(int(idx)):
                selenium_generics.press_key("ARROW_DOWN")
                time.sleep(1)
            selenium_generics.press_key("RETURN")
        else:
            raise NoSuchElementException(f"Element cannot be uniquely identified. Found: {num_of_elements} elements")

    timeout = timeout if timeout else 10  # timeout until searchable dropdown appears
    if type == 'visible text':
        locator = locators.get_searchable_dropdown_by_visible_text(label)
        _select_element_from_dropdown_by_index(idx=index, dropdown_element_locator=locator)
    elif type == 'placeholder':
        locator = locators.get_element_by_attribute(type, label)
        _select_element_from_dropdown_by_index(idx=index, dropdown_element_locator=locator)
    elif type == 'label':
        locator = locators.get_searchable_dropdown_by_visible_text(value=label, attr="label")
        _select_element_from_dropdown_by_index(idx=index, dropdown_element_locator=locator)
    else:
        raise ValueError(f"Provide either 'placeholder', 'label' or 'visible text. Provided selector type: {type}")


# WEB context Predefined Step
# ID 708
@given(parsers.re(r"I select by visible text (?:')(?P<value>.*)(?:') from dropdown (whose placeholder is equal to (?:')(?P<placeholder>.*)(?:'))?(\s+)?((?:with the parent)\s+(?:')(?P<label>.*)(?:') label)?$"),
       converters=dict(value=data_manager.text_formatted,))
@when(parsers.re(r"I select by visible text (?:')(?P<value>.*)(?:') from dropdown (whose placeholder is equal to (?:')(?P<placeholder>.*)(?:'))?(\s+)?((?:with the parent)\s+(?:')(?P<label>.*)(?:') label)?$"),
       converters=dict(value=data_manager.text_formatted,))
def select_by_visible_text_from_dropdown(selenium_generics: SeleniumGenerics, locators, value: str, placeholder: str, label: str):
    if placeholder:
        locator = locators.get_dropdown_option(placeholder)
        num_of_elements = len(selenium_generics.get_elements(locator))
        if num_of_elements == 1:
            selenium_generics.select_by_visible_text(select_locator=locator, text=value)
        else:
            raise NoSuchElementException(f"Element cannot be uniquely identified. Found: {num_of_elements} elements")
    elif label:
        locator = locators.get_select_element_by_parent_label(label)
        num_of_elements = len(selenium_generics.get_elements(locator))
        if num_of_elements == 1:
            selenium_generics.select_by_visible_text(select_locator=locator, text=value)
        else:
            raise NoSuchElementException(f"Element cannot be uniquely identified. Found: {num_of_elements} elements")
    else:
        raise ValueError(f"Provide either 'placeholder' or 'label'. Provided placeholder: {placeholder}; label: {label}")


# WEB context Predefined Step
# ID 709
@given(parsers.re("I select the option at index '(?P<index>.*)' element '(?P<locator_path>.*)'"),
    converters=dict(index=data_manager.text_formatted), )
@when(parsers.re("I select the option at index '(?P<index>.*)' element '(?P<locator_path>.*)'"),
    converters=dict(index=data_manager.text_formatted), )
def select_option_by_index(selenium_generics: SeleniumGenerics, index: int, locators: Locators, locator_path):
    selenium_generics.select_by_index(locators.parse_and_get(locator_path, selenium_generics), int(index))


# WEB context Predefined Step
# ID 710
@given(parsers.re("I select the option '(?P<option>.*)' by value for element '(?P<locator_path>.*)'"),
    converters=dict(option=data_manager.text_formatted), )
@when(parsers.re("I select the option '(?P<option>.*)' by value for element '(?P<locator_path>.*)'"),
    converters=dict(option=data_manager.text_formatted), )
def select_option_by_value(selenium_generics: SeleniumGenerics, option: str, locators: Locators, locator_path):
    selenium_generics.select_by_value(locators.parse_and_get(locator_path, selenium_generics), option)


# WEB context Predefined Step
# ID 711
@given(parsers.re("I select the option '(?P<option>.*)' by visible text for element '(?P<locator_path>.*)'"),
    converters=dict(option=data_manager.text_formatted), )
@when(parsers.re("I select the option '(?P<option>.*)' by visible text for element '(?P<locator_path>.*)'"),
    converters=dict(option=data_manager.text_formatted), )
def select_option_by_visible_text(selenium_generics: SeleniumGenerics, option: str, locators: Locators, locator_path):
    selenium_generics.select_by_visible_text(locators.parse_and_get(locator_path, selenium_generics), option)


# WEB context Predefined Step
# ID 712
@given(parsers.re("I deselect the option at index '(?P<index>.*)' element '(?P<locator_path>.*)'"),
    converters=dict(index=data_manager.text_formatted), )
@when(parsers.re("I deselect the option at index '(?P<index>.*)' element '(?P<locator_path>.*)'"),
    converters=dict(index=data_manager.text_formatted), )
def deselect_option_index(selenium_generics: SeleniumGenerics, index: int, locators: Locators, locator_path):
    selenium_generics.deselect_by_index(locators.parse_and_get(locator_path, selenium_generics), int(index))


# WEB context Predefined Step
# 713
@given(parsers.re("I deselect the option '(?P<option>.*)' by value for element '(?P<locator_path>.*)'"),
    converters=dict(option=data_manager.text_formatted), )
@when(parsers.re("I deselect the option '(?P<option>.*)' by value for element '(?P<locator_path>.*)'"),
    converters=dict(option=data_manager.text_formatted), )
def deselect_option_by_value(selenium_generics: SeleniumGenerics, option: str, locators: Locators, locator_path: str, ):
    selenium_generics.deselect_by_value(locators.parse_and_get(locator_path, selenium_generics), option)


# WEB context Predefined Step
# 714
@given(parsers.re("I deselect the option '(?P<option>.*)' by visible text for element '(?P<locator_path>.*)'"),
    converters=dict(option=data_manager.text_formatted), )
@when(parsers.re("I deselect the option '(?P<option>.*)' by visible text for element '(?P<locator_path>.*)'"),
    converters=dict(option=data_manager.text_formatted), )
def deselect_option_by_visible_text(selenium_generics: SeleniumGenerics, option: str, locators: Locators,
                                    locator_path: str, ):
    selenium_generics.deselect_by_visible_text(locators.parse_and_get(locator_path, selenium_generics), option)


# WEB context Predefined Step
# 715
@given(parsers.re("I select the radio option whose attribute '(?P<option_attribute>.*)' is equal to '(?P<text>.*)' from the parent attribute '(?P<parent_attribute>.*)' and value '(?P<value>.*)'"),
       converters=dict(text=data_manager.text_formatted), )
@when(parsers.re("I select the radio option whose attribute '(?P<option_attribute>.*)' is equal to '(?P<text>.*)' from the parent attribute '(?P<parent_attribute>.*)' and value '(?P<value>.*)'"),
       converters=dict(text=data_manager.text_formatted), )
def select_radio_option_from_parent_attribute(selenium_generics: SeleniumGenerics, locators, option_attribute: str, text: str, parent_attribute: str, value: str):
    locator = locators.get_radio_option_from_parent(option_attribute, text, parent_attribute, value)
    num_of_elements = len(selenium_generics.get_elements(locator))
    if num_of_elements == 1:
        selenium_generics.click(locator)
    else:
        raise NoSuchElementException(f"Element cannot be uniquely identified. Found: {num_of_elements} elements")
