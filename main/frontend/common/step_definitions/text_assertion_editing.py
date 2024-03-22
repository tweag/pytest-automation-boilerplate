import os
import typing
import structlog

from pytest_bdd import parsers, given, when, then
from pytest_check import check
from main.frontend.common.helpers.app import context_manager
from selenium.common.exceptions import NoSuchElementException

from assertpy import assert_that
from main.frontend.common.helpers.selenium_generics import SeleniumGenerics
from main.frontend.common.step_definitions.steps_common import MOBILE_SUFFIX
from main.frontend.common.utils.locator_parser import Locators
from main.utils.faker_data import DataUtils
from main.utils import data_manager

logger = structlog.get_logger(__name__)


# WEB & MOBILE contexts Predefined Step
@given(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' text is '(?P<value>.*)'"),
       converters=dict(value=data_manager.text_formatted), )
@when(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' text is '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' text is '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
def element_equals_text(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path,
                        value: str):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    else:
        actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_text).is_equal_to(value)
    else:
        assert_that(actual_text).is_equal_to(value)


# WEB & MOBILE contexts Predefined Step
@given(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' text is not '(?P<value>.*)'"),
       converters=dict(value=data_manager.text_formatted), )
@when(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' text is not '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' text is not '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
def element_not_equals_text(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path,
                            value: str):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    else:
        actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_text).is_not_equal_to(value)
    else:
        assert_that(actual_text).is_not_equal_to(value)


# WEB & MOBILE contexts Predefined Step
@given(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' contains the text '(?P<value>.*)'"),
       converters=dict(value=data_manager.text_formatted), )
@when(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' contains the text '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' contains the text '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
def contains_text(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path, value: str):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    else:
        actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_text).contains(value)
    else:
        assert_that(actual_text).contains(value)


# WEB & MOBILE contexts Predefined Step
@given(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' does not contain the text '(?P<value>.*)'"),
       converters=dict(value=data_manager.text_formatted), )
@when(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' does not contain the text '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' does not contain the text '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
def does_not_contain_text(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path,
                          value: str):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    else:
        actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_text).does_not_contain(value)
    else:
        assert_that(actual_text).does_not_contain(value)


# WEB & MOBILE contexts Predefined Step
@given(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' contains any text"))
@when(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' contains any text"))
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' contains any text"))
def contains_any_text(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    else:
        actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_text).matches(r"(.*?)")
    else:
        assert_that(actual_text).matches(r"(.*?)")


# WEB & MOBILE contexts Predefined Step
@given(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' does not contain any text"))
@when(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' does not contain any text"))
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The (button|element) '(?P<locator_path>.*)' does not contain any text"))
def does_not_contain_any_text(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    else:
        actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_text).matches(r"^$")
    else:
        assert_that(actual_text).matches(r"^$")


# WEB & MOBILE contexts Predefined Step
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?I expect that element '(?P<locator_path1>.*)' contains the same text as element '(?P<locator_path2>.*)'$"))
def check_contains_same_text(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path1,
                             locator_path2, ):
    if MOBILE_SUFFIX in locator_path1 and MOBILE_SUFFIX in locator_path2:
        with context_manager(selenium_generics):
            actual_text1 = selenium_generics.get_element_text(locators.parse_and_get(locator_path1, selenium_generics))
            actual_text2 = selenium_generics.get_element_text(locators.parse_and_get(locator_path2, selenium_generics))
    else:
        actual_text1 = selenium_generics.get_element_text(locators.parse_and_get(locator_path1, selenium_generics))
        actual_text2 = selenium_generics.get_element_text(locators.parse_and_get(locator_path2, selenium_generics))
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_text1).is_equal_to(actual_text2)
    else:
        assert_that(actual_text1).is_equal_to(actual_text2)


# WEB & MOBILE contexts Predefined Step
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?I expect that element '(?P<locator_path1>.*)' does not contain the same text as element '(?P<locator_path2>.*)'$"))
def check_does_not_contain_same_text(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str,
                                     locator_path1, locator_path2, ):
    if MOBILE_SUFFIX in locator_path1 and MOBILE_SUFFIX in locator_path2:
        with context_manager(selenium_generics):
            actual_text1 = selenium_generics.get_element_text(locators.parse_and_get(locator_path1, selenium_generics))
            actual_text2 = selenium_generics.get_element_text(locators.parse_and_get(locator_path2, selenium_generics))
    else:
        actual_text1 = selenium_generics.get_element_text(locators.parse_and_get(locator_path1, selenium_generics))
        actual_text2 = selenium_generics.get_element_text(locators.parse_and_get(locator_path2, selenium_generics))
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_text1).is_not_equal_to(actual_text2)
    else:
        assert_that(actual_text1).is_not_equal_to(actual_text2)


# WEB & MOBILE contexts Predefined Step
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The trimmed text on (button|element) '(?P<locator_path>.*)' is '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
def check_element_equals_text(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path,
                              value: str):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    else:
        actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_text.strip()).is_equal_to(value)
    else:
        assert_that(actual_text.strip()).is_equal_to(value)


# WEB & MOBILE contexts Predefined Step
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The trimmed text on (button|element) '(?P<locator_path>.*)' is not '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
def check_element_not_equals_text(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str,
                                  locator_path, value: str):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    else:
        actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_text.strip()).is_not_equal_to(value)
    else:
        assert_that(actual_text.strip()).is_not_equal_to(value)


# WEB & MOBILE contexts Predefined Step
@given(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' text value is '(?P<comparison_value>EQUAL|LESS_THAN|LESS_THAN_OR_EQUAL|GREATER_THAN|GREATER_THAN_OR_EQUAL)' to '(?P<value>.*)'"),
       converters=dict(value=data_manager.text_formatted))
@when(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' text value is '(?P<comparison_value>EQUAL|LESS_THAN|LESS_THAN_OR_EQUAL|GREATER_THAN|GREATER_THAN_OR_EQUAL)' to '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted))
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' text value is '(?P<comparison_value>EQUAL|LESS_THAN|LESS_THAN_OR_EQUAL|GREATER_THAN|GREATER_THAN_OR_EQUAL)' to '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted))
def compare_numbers(selenium_generics: SeleniumGenerics, locators: Locators, locator_path: str, soft_assert: str,
                    comparison_value: str, value: str):
    comparison_values = dict(EQUAL=lambda number_1, number_2: assert_that(number_1).is_equal_to(number_2),
                             LESS_THAN=lambda number_1, number_2: assert_that(number_1).is_less_than(number_2),
                             LESS_THAN_OR_EQUAL=lambda number_1, number_2: assert_that(
                                 number_1).is_less_than_or_equal_to(number_2),
                             GREATER_THAN=lambda number_1, number_2: assert_that(number_1).is_greater_than(number_2),
                             GREATER_THAN_OR_EQUAL=lambda number_1, number_2: assert_that(
                                 number_1).is_greater_than_or_equal_to(number_2))
    number_value = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics))

    if number_value.isnumeric() and number_value.strip().isdigit():
        number_value = int(number_value.strip())
    else:
        raise ValueError(f"Given number_value: {number_value} is not in a numeric integer value")

    compare_function = comparison_values[comparison_value]

    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            if soft_assert is not None and soft_assert.lower() == 'true':
                with check:
                    compare_function(number_value, int(value))
            else:
                compare_function(number_value, int(value))
    else:
        if soft_assert is not None and soft_assert.lower() == 'true':
            with check:
                compare_function(number_value, int(value))
        else:
            compare_function(number_value, int(value))


# WEB context Predefined Step
@given(parsers.re("I add text '(?P<value>.*)' to field '(?P<locator_path>.*)'"),
       converters=dict(value=data_manager.text_formatted), )
@when(parsers.re("I add text '(?P<value>.*)' to field '(?P<locator_path>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
def add_element_value(selenium_generics: SeleniumGenerics, value: str, locators: Locators, locator_path: str):
    selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), f"{value}")


# WEB & MOBILE contexts Predefined Step
@given(parsers.re("I set text '(?P<value>.*)' to field '(?P<locator_path>.*)'"),
       converters=dict(value=data_manager.text_formatted), )
@when(parsers.re("I set text '(?P<value>.*)' to field '(?P<locator_path>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
def set_element_value(selenium_generics: SeleniumGenerics, value: str, locators: Locators, locator_path):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), value)
    else:
        selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), value)


# WEB & MOBILE contexts Predefined Step
@given(parsers.re("I clear text from field '(?P<locator_path>.*)'"))
@when(parsers.re("I clear text from field '(?P<locator_path>.*)'"))
def clear_text(selenium_generics: SeleniumGenerics, locators: Locators, locator_path: str):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            selenium_generics.clear_text(locators.parse_and_get(locator_path, selenium_generics))
    else:
        selenium_generics.clear_text(locators.parse_and_get(locator_path, selenium_generics))


# WEB context Predefined Step
@given(parsers.re("I clear text using keys from field '(?P<locator_path>.*)'"))
@when(parsers.re("I clear text using keys from field '(?P<locator_path>.*)'"))
def clear_text_actions(selenium_generics: SeleniumGenerics, locators: Locators, locator_path: str):
    selenium_generics.clear_text_using_keys(locators.parse_and_get(locator_path, selenium_generics))


# WEB context Predefined Step
@given(parsers.re(
    "(?P<gap_str>With gap of (?P<gap_seconds>\\d+) seconds, )?I type text '(?P<text>.+)' in the input field '(?P<locator_path>.+)'"),
    converters=dict(text=data_manager.text_formatted))
@when(parsers.re(
    "(?P<gap_str>With gap of (?P<gap_seconds>\\d+) seconds, )?I type text '(?P<text>.+)' in the input field '(?P<locator_path>.+)'"),
    converters=dict(text=data_manager.text_formatted))
def step_realistic_typing(selenium_generics: SeleniumGenerics, locators: Locators,
                          gap_seconds: typing.Union[float, None], text: str, locator_path: str, ):
    func = selenium_generics.simulate_realistic_typing
    gap_seconds = float(gap_seconds or func.__kwdefaults__["gap_seconds"])
    func(locators.parse_and_get(locator_path, selenium_generics), text, gap_seconds=gap_seconds)


# WEB context Predefined Step
# ID 417
@given(parsers.re(
    "I add text '(?P<text>.*)' in input field whose attribute '(?P<attribute>.*)' is equal to '(?P<value>.*)'"),
       converters=dict(text=data_manager.text_formatted), )
@when(parsers.re(
    "I add text '(?P<text>.*)' in input field whose attribute '(?P<attribute>.*)' is equal to '(?P<value>.*)'"),
      converters=dict(text=data_manager.text_formatted), )
def add_text_based_on_attribute(selenium_generics: SeleniumGenerics, locators, text: str, attribute: str, value: str):
    locator = locators.get_element_by_attribute(attribute, value)
    num_of_elements = len(selenium_generics.get_elements(locator))
    if num_of_elements == 1:
        selenium_generics.clear_text(locator)
        selenium_generics.enter_text(locator, text)
    else:
        raise NoSuchElementException(f"Element cannot be uniquely identified. Found: {num_of_elements} elements")


# WEB & MOBILE contexts Predefined Step
# ID 418, 805
@given(parsers.re(
    r"I add random string of length (?:')(?P<length>.*)(?:') composed of (?:')(?P<character_type>alphabetic characters|numeric characters|alphabetic and numeric characters)(?:') to field (?:')(?P<locator_path>.*)(?:')(\s+)?((?:and save as)\s+(?:')(?P<storage_var>\w+)(?:') environment variable)?$"))
@when(parsers.re(
    r"I add random string of length (?:')(?P<length>.*)(?:') composed of (?:')(?P<character_type>alphabetic characters|numeric characters|alphabetic and numeric characters)(?:') to field (?:')(?P<locator_path>.*)(?:')(\s+)?((?:and save as)\s+(?:')(?P<storage_var>\w+)(?:') environment variable)?$"))
def set_random_element_value(selenium_generics: SeleniumGenerics, length: str, character_type: str, locators: Locators,
                             locator_path, storage_var):
    storage_var = storage_var if storage_var else None
    if length.isdigit():
        random_string = DataUtils.get_random_text(length=int(length), source=character_type)
        if MOBILE_SUFFIX in locator_path:
            with context_manager(selenium_generics):
                selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), random_string)
        else:
            selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), random_string)
        if storage_var:
            os.environ[storage_var] = random_string
    else:
        raise ValueError(f"Wrong length value: {length}")


# WEB & MOBILE contexts Predefined Step
# ID 419
@given(
    parsers.re(r"I add a random email to field '(?P<locator_path>.*)'((\s+)?with (?:')(?P<domain>.*)(?:') domain)?$"),
    converters=dict(domain=data_manager.text_formatted), )
@when(parsers.re(r"I add a random email to field '(?P<locator_path>.*)'((\s+)?with (?:')(?P<domain>.*)(?:') domain)?$"),
      converters=dict(domain=data_manager.text_formatted), )
def set_random_email_value(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, domain: str):
    domain = domain if domain else "gmail.com"
    random_email = DataUtils().get_random_email(domain=domain)

    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), random_email)
    else:
        selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), random_email)


# WEB & MOBILE contexts Predefined Step
@given(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' text after removing new lines is '(?P<value>.*)'"),
    converters=dict(value=data_manager.text_formatted), )
@when(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' text after removing new lines is '(?P<value>.*)'"),
    converters=dict(value=data_manager.text_formatted), )
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The element '(?P<locator_path>.*)' text after removing new lines is '(?P<value>.*)'"),
    converters=dict(value=data_manager.text_formatted), )
def element_equals_text(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path,
                        value: str):
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics)) \
                .replace("\n", "")
    else:
        actual_text = selenium_generics.get_element_text(locators.parse_and_get(locator_path, selenium_generics)) \
            .replace("\n", "")
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(actual_text).is_equal_to(value)
    else:
        assert_that(actual_text).is_equal_to(value)
