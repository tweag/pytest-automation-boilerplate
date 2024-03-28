"""
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
"""
import os
import typing
import structlog

from pathlib import Path
from pytest_bdd import parsers, given, when, then
from pytest_check import check
from main.frontend.common.utils.containers import WindowSize
from assertpy import assert_that
from main.frontend.common.helpers.selenium_generics import SeleniumGenerics
from main.frontend.common.utils.locator_parser import Locators
from main.utils import data_manager
from main.utils.utils import remote_execute_cmd_commands

logger = structlog.get_logger(__name__)


# WEB context Predefined Step
# ID 101, 102
@given(parsers.re("The browser resolution is '(?P<width>.*)' per '(?P<height>.*)'"),
       converters=dict(width=data_manager.text_formatted, height=data_manager.text_formatted), )
@given(parsers.re("My screen resolution is '(?P<width>.*)' by '(?P<height>.*)' pixels"),
       converters=dict(width=data_manager.text_formatted, height=data_manager.text_formatted), )
@when(parsers.re("The browser resolution is '(?P<width>.*)' per '(?P<height>.*)'"),
      converters=dict(width=data_manager.text_formatted, height=data_manager.text_formatted), )
@when(parsers.re("My screen resolution is '(?P<width>.*)' by '(?P<height>.*)' pixels"),
      converters=dict(width=data_manager.text_formatted, height=data_manager.text_formatted), )
def window_size(width: int, height: int, selenium_generics: SeleniumGenerics):
    selenium_generics.set_window_size(WindowSize(int(width), int(height)))


# WEB context Predefined Step
# ID 103
@given("Browser is maximized")
@when("Browser is maximized")
def maximize(selenium_generics: SeleniumGenerics):
    selenium_generics.maximize_window()


# WEB context Predefined Step
# ID 104
@given(parsers.re("I am on the (url|page|site) '(?P<page_url>.*)'"),
       converters=dict(page_url=data_manager.text_formatted), )
@when(parsers.re("I am on the (url|page|site) '(?P<page_url>.*)'"),
      converters=dict(page_url=data_manager.text_formatted), )
def open_webpage(selenium_generics: SeleniumGenerics, base_url: str, page_url: str):
    selenium_generics.navigate_to_url(f"{base_url}{page_url}")


@given(parsers.re("I set web base url '(?P<base_url>.*)'"),
       converters=dict(base_url=data_manager.text_formatted), )
def open_base_url(selenium_generics: SeleniumGenerics, base_url):
    selenium_generics.navigate_to_url(base_url)


# WEB context Predefined Step
# ID 105
@given(parsers.re("I navigate to external page '(?P<url>.*)'"),
       converters=dict(url=data_manager.text_formatted), )
@when(parsers.re("I navigate to external page '(?P<url>.*)'"),
      converters=dict(url=data_manager.text_formatted), )
def navigate_to_external_page(selenium_generics: SeleniumGenerics, url: str):
    selenium_generics.navigate_to_url(url)


# WEB context Predefined Step
# ID 106
@given(parsers.re("I get current browser url and store it to '(?P<env_var>.*)'"))
@when(parsers.re("I get current browser url and store it to '(?P<env_var>.*)'"))
@then(parsers.re("I get current browser url and store it to '(?P<env_var>.*)'"))
def store_url_env_var(selenium_generics, env_var: str):
    os.environ[env_var] = selenium_generics.current_url


# WEB context Predefined Step
# ID 107
@given("I navigate back to the previous page")
@when("I navigate back to the previous page")
@then("I navigate back to the previous page")
def navigate_to_previous_page(selenium_generics: SeleniumGenerics):
    selenium_generics.one_page_backward()


# WEB context Predefined Step
# ID 108
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The title is '(?P<title>.*)'"),
       converters=dict(title=data_manager.text_formatted), )
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The title is '(?P<title>.*)'"),
      converters=dict(title=data_manager.text_formatted), )
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The title is '(?P<title>.*)'"),
      converters=dict(title=data_manager.text_formatted), )
def page_title(selenium_generics: SeleniumGenerics, soft_assert: str, title: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.does_title_equals(title), f"Title Mismatch: {selenium_generics.title} vs {title}"
    else:
        assert selenium_generics.does_title_equals(title), f"Title Mismatch: {selenium_generics.title} vs {title}"


# WEB context Predefined Step
# ID 109
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The title is not '(?P<title>.*)'"),
       converters=dict(title=data_manager.text_formatted), )
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The title is not '(?P<title>.*)'"),
      converters=dict(title=data_manager.text_formatted), )
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The title is not '(?P<title>.*)'"),
      converters=dict(title=data_manager.text_formatted), )
def page_title_is_not(selenium_generics: SeleniumGenerics, soft_assert: str, title: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert not selenium_generics.does_title_equals(
                title), f"Title Mismatch: {selenium_generics.title} vs {title}"
    else:
        assert not selenium_generics.does_title_equals(title), f"Title Mismatch: {selenium_generics.title} vs {title}"


# WEB context Predefined Step
# ID 110
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect that the title contains '(?P<title>.*)'"),
      converters=dict(title=data_manager.text_formatted), )
def check_title_contains(selenium_generics: SeleniumGenerics, soft_assert: str, title: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.does_title_contains(title), f"Mismatch: {title} not in {selenium_generics.title}"
    else:
        assert selenium_generics.does_title_contains(title), f"Mismatch: {title} not in {selenium_generics.title}"


# WEB context Predefined Step
# ID 111
@then(
    parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect that the title does not contain '(?P<title>.*)'"),
    converters=dict(title=data_manager.text_formatted), )
def check_title_not_contains(selenium_generics: SeleniumGenerics, soft_assert: str, title: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert not selenium_generics.does_title_contains(title), f"Mismatch: {title} in {selenium_generics.title}"
    else:
        assert not selenium_generics.does_title_contains(title), f"Mismatch: {title} in {selenium_generics.title}"


# WEB context Predefined Step
# ID 112
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The page url is '(?P<url>.*)'"),
       converters=dict(url=data_manager.text_formatted), )
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The page url is '(?P<url>.*)'"),
      converters=dict(url=data_manager.text_formatted), )
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The page url is '(?P<url>.*)'"),
      converters=dict(url=data_manager.text_formatted), )
def given_page_url_is(selenium_generics: SeleniumGenerics, soft_assert: str, url: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.does_url_equals(url), f"URL mismatch: {selenium_generics.current_url} vs {url}"
    else:
        assert selenium_generics.does_url_equals(url), f"URL mismatch: {selenium_generics.current_url} vs {url}"


# WEB context Predefined Step
# ID 113
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The page url is not '(?P<url>.*)'"),
       converters=dict(url=data_manager.text_formatted), )
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The page url is not '(?P<url>.*)'"),
      converters=dict(url=data_manager.text_formatted), )
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The page url is not '(?P<url>.*)'"),
      converters=dict(url=data_manager.text_formatted), )
def given_page_url_is_not(selenium_generics: SeleniumGenerics, soft_assert: str, url: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.does_url_not_equals(url), f"URL mismatch: {selenium_generics.current_url} vs {url}"
    else:
        assert selenium_generics.does_url_not_equals(url), f"URL mismatch: {selenium_generics.current_url} vs {url}"


# WEB context Predefined Step
# ID 114
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The page (path is|url contains) '(?P<url>.*)'"),
      converters=dict(url=data_manager.text_formatted), )
def check_page_url_contains(selenium_generics: SeleniumGenerics, soft_assert: str, url: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.does_current_url_contains(url)
    else:
        assert selenium_generics.does_current_url_contains(url)


# WEB context Predefined Step
# ID 115
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The page (path is not|url does not contain) '(?P<url>.*)'"),
      converters=dict(url=data_manager.text_formatted), )
def check_page_url_not_contains(selenium_generics: SeleniumGenerics, soft_assert: str, url: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert not selenium_generics.does_current_url_contains(url)
    else:
        assert not selenium_generics.does_current_url_contains(url)


# WEB context Predefined Step
# ID 116
@given(parsers.re("I refresh the current page"))
@when(parsers.re("I refresh the current page"))
def refresh_page(selenium_generics: SeleniumGenerics):
    selenium_generics.refresh_page()


# WEB context Predefined Step
# ID 117
@given(parsers.re("There is just one (browser tab|window) open"))
@when(parsers.re("There is just one (browser tab|window) open"))
def close_all_but_first_tab(selenium_generics: SeleniumGenerics):
    windows = selenium_generics.window_handles
    windows_to_close = windows[1:]
    while windows_to_close:
        selenium_generics.switch_to_known_window(windows_to_close.pop())
        selenium_generics.close_active_window()


# WEB context Predefined Step
# ID 118
@given(parsers.re("I open new tab with url '(?P<page_url>.*)'"),
       converters=dict(page_url=data_manager.text_formatted), )
@when(parsers.re("I open new tab with url '(?P<page_url>.*)'"),
      converters=dict(page_url=data_manager.text_formatted), )
def open_specific_tab(selenium_generics: SeleniumGenerics, base_url: str, page_url: str):
    selenium_generics.open_new_tab(f"{base_url}{page_url}")


# WEB context Predefined Step
# ID 119
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The url '(?P<url>.*)' is opened in a new (tab|window)"),
      converters=dict(url=data_manager.text_formatted), )
def check_is_opened_in_new_window(selenium_generics: SeleniumGenerics, soft_assert: str, url: str):
    selenium_generics.switch_to_last_window()
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.does_url_equals(url)
    else:
        assert selenium_generics.does_url_equals(url)


# WEB context Predefined Step
# ID 120
@given(parsers.re("I close the last opened window"))
@given(parsers.re("I close the last opened tab"))
@when(parsers.re("I close the last opened window"))
@when(parsers.re("I close the last opened tab"))
def close_last_opened_window(selenium_generics: SeleniumGenerics):
    selenium_generics.close_last_window()


# WEB context Predefined Step
# ID 121
@given(parsers.re("I focus the last opened window"))
@given(parsers.re("I focus the last opened tab"))
@when(parsers.re("I focus the last opened window"))
@when(parsers.re("I focus the last opened tab"))
def switch_to_last(selenium_generics: SeleniumGenerics):
    selenium_generics.switch_to_last_window()


# WEB context Predefined Step
# ID 122
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?There are '(?P<count>.*)' (tabs|windows) currently opened"),
      converters=dict(count=data_manager.text_formatted))
def check_number_of_tabs(selenium_generics: SeleniumGenerics, soft_assert: str, count: int):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.num_of_windows == int(count)
    else:
        assert selenium_generics.num_of_windows == int(count)


# WEB context Predefined Step
# ID 123
@given(parsers.re("I close the current opened tab"))
@when(parsers.re("I close the current opened tab"))
def close_current_opened_tab(selenium_generics: SeleniumGenerics):
    selenium_generics.close_active_window()


# WEB context Predefined Step
# ID 124
@given(parsers.re("I switch to tab with (url|number) '(?P<value>.*)'"),
       converters=dict(value=data_manager.text_formatted), )
@when(parsers.re("I switch to tab with (url|number) '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
def switch_specific_tab(selenium_generics: SeleniumGenerics, base_url: str, value: typing.Union[str, int]):
    if value.isdigit():
        selenium_generics.switch_to_window_by_position(int(value))
    else:
        selenium_generics.switch_tab_by_url(f"{base_url}{value}")


# WEB context Predefined Step
@given(parsers.re("I close the tab with (url|number) '(?P<value>.*)'"),
       converters=dict(value=data_manager.text_formatted), )
@when(parsers.re("I close the tab with (url|number) '(?P<value>.*)'"),
      converters=dict(value=data_manager.text_formatted), )
def close_specific_tab(selenium_generics: SeleniumGenerics, base_url: str, value: typing.Union[str, int]):
    if value.isdigit():
        selenium_generics.close_window_by_position(int(value))
    else:
        selenium_generics.close_window_by_url(f"{base_url}{value}")


# WEB context Predefined Step
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?A new (tab|window) is opened"))
def check_new_window(selenium_generics: SeleniumGenerics, soft_assert: str):
    # todo: refactor this method in future releases as appropriate
    # error case: how does this verify the scenario where there is already more than one tab opened prior to this step.
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.num_of_windows > 1
    else:
        assert selenium_generics.num_of_windows > 1


# WEB context Predefined Step
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?A new (tab|window) is not opened"))
def check_no_new_window(selenium_generics: SeleniumGenerics, soft_assert: str):
    # todo: refactor this method in future releases as appropriate
    # error case: how does this verify the scenario where there is already more than one tab opened prior to this step.
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.num_of_windows == 1
    else:
        assert selenium_generics.num_of_windows == 1


# WEB context Predefined Step
@given(parsers.re("I switch to iframe '(?P<locator_path>.*)'"))
@when(parsers.re("I switch to iframe '(?P<locator_path>.*)'"))
def switch_to_iframe(selenium_generics: SeleniumGenerics, locators: Locators, locator_path: str):
    selenium_generics.switch_context_to_iframe(locators.parse_and_get(locator_path, selenium_generics))


# WEB context Predefined Step
@given(parsers.re("I switch back from iframe"))
@when(parsers.re("I switch back from iframe"))
def switch_back_from_iframe(selenium_generics: SeleniumGenerics):
    selenium_generics.switch_context_to_default_content()


# WEB context Predefined Step
@given(parsers.re("I take a screenshot"))
@when(parsers.re("I take a screenshot"))
@then(parsers.re("I take a screenshot"))
def take_a_screenshot(selenium_generics: SeleniumGenerics):
    # Declaration of the BDD step that is used to take a screenshot during the scenario
    ...


# WEB context Predefined Step
@given(parsers.re("I '(?P<cache_option>disable|enable)' the cache"))
@when(parsers.re("I '(?P<cache_option>disable|enable)' the cache"))
def disable_cache(driver, cache_option: str):
    cache_disabled_value = True if cache_option == 'disable' else False
    remote_execute_cmd_commands(driver, "Network.setCacheDisabled", {"cacheDisabled": cache_disabled_value})


# WEB context Predefined Step
# ID 132
@given(parsers.re("I attach file '(?P<file_path>.*)' to input field '(?P<locator_path>.*)'"),
       converters=dict(file_path=data_manager.text_formatted), )
@when(parsers.re("I attach file '(?P<file_path>.*)' to input field '(?P<locator_path>.*)'"),
      converters=dict(file_path=data_manager.text_formatted), )
def attach_file(selenium_generics: SeleniumGenerics, file_path: str, locators: Locators, locator_path):
    relative_path = Path(file_path)
    if relative_path and relative_path.absolute().is_file():
        full_path = relative_path.absolute().as_posix()
        selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), full_path)
    else:
        raise FileNotFoundError(f"The file {file_path}' is not a valid path to a file")


# WEB context Predefined Step
# ID 133
@given(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' contains the value '(?P<value>.*)'"),
    converters=dict(value=data_manager.text_formatted))
@when(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' contains the value '(?P<value>.*)'"),
    converters=dict(value=data_manager.text_formatted))
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' contains the value '(?P<value>.*)'"),
    converters=dict(value=data_manager.text_formatted))
def check_cookie_content(selenium_generics: SeleniumGenerics, soft_assert: str, name, value: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(selenium_generics.cookie_value(name)).contains(value)
    else:
        assert_that(selenium_generics.cookie_value(name)).contains(value)


# WEB context Predefined Step
# ID 134
@given(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' does not contain the value '(?P<value>.*)'"),
    converters=dict(value=data_manager.text_formatted))
@when(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' does not contain the value '(?P<value>.*)'"),
    converters=dict(value=data_manager.text_formatted))
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' does not contain the value '(?P<value>.*)'"),
    converters=dict(value=data_manager.text_formatted))
def check_cookie_content_is_not(selenium_generics: SeleniumGenerics, soft_assert: str, name, value: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(selenium_generics.cookie_value(name)).does_not_contain(value)
    else:
        assert_that(selenium_generics.cookie_value(name)).does_not_contain(value)


# WEB context Predefined Step
# ID 135
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' exists"))
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' exists"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' exists"))
def check_cookie_exists(selenium_generics: SeleniumGenerics, soft_assert: str, name):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert_that(selenium_generics.cookie_name(name)).is_equal_to(name)
    else:
        assert_that(selenium_generics.cookie_name(name)).is_equal_to(name)


# WEB context Predefined Step
# ID 136
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' does not exist"))
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' does not exist"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?The cookie '(?P<name>.*)' does not exist"))
def check_cookie_does_not_exist(selenium_generics: SeleniumGenerics, soft_assert: str, name):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.get_cookie(name) is None
    else:
        assert selenium_generics.get_cookie(name) is None


# WEB context Predefined Step
# ID 137
@given("I fetch existing cookies from the site")
@when("I fetch existing cookies from the site")
def fetch_cookies(selenium_generics: SeleniumGenerics):
    selenium_generics.get_all_cookies()


# WEB context Predefined Step
# ID 138, 139
@given(
    parsers.re("I update the value of newly added cookie '(?P<name>.*)' with '(?P<value>.*)' for path '(?P<path>.*)'"),
    converters=dict(value=data_manager.text_formatted))
@given(parsers.re("I set the cookie '(?P<name>.*)' with value '(?P<value>.*)' for path '(?P<path>.*)'"),
       converters=dict(value=data_manager.text_formatted))
@when(
    parsers.re("I update the value of newly added cookie '(?P<name>.*)' with '(?P<value>.*)' for path '(?P<path>.*)'"),
    converters=dict(value=data_manager.text_formatted))
@when(parsers.re("I set the cookie '(?P<name>.*)' with value '(?P<value>.*)' for path '(?P<path>.*)'"),
      converters=dict(value=data_manager.text_formatted))
def check_cookie_content(selenium_generics: SeleniumGenerics, name, value: str, path="/"):
    selenium_generics.add_cookie(name, value, path=path)


# WEB context Predefined Step
# ID 140
@given(parsers.re("I delete the cookie '(?P<name>.*)'"))
@when(parsers.re("I delete the cookie '(?P<name>.*)'"))
def delete_cookie(selenium_generics: SeleniumGenerics, name):
    selenium_generics.delete_cookie(name)


# WEB context Predefined Step
# ID 141
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect the cookies to be present"))
def check_cookies_presence(selenium_generics: SeleniumGenerics, soft_assert: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.get_all_cookies()
    else:
        assert selenium_generics.get_all_cookies()


# WEB context Predefined Step
# ID 142, 143
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?I expect cookie '(?P<name>.*)' with value '(?P<value>.*)' to be present"),
    converters=dict(value=data_manager.text_formatted))
@then(parsers.re(
    "(With soft assertion '(?P<soft_assert>.*)' )?I expect the value of newly added cookie '(?P<name>.*)' to be updated with '(?P<value>.*)'"),
    converters=dict(value=data_manager.text_formatted))
def check_cookie_presence(selenium_generics: SeleniumGenerics, soft_assert: str, name, value: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.cookie_value(name) == value
    else:
        assert selenium_generics.cookie_value(name) == value


# WEB context Predefined Step
# ID 144
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I expect cookie '(?P<name>.*)' to be deleted"))
def check_cookie_delete(selenium_generics: SeleniumGenerics, soft_assert: str, name):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics.get_cookie(name) is None
    else:
        assert selenium_generics.get_cookie(name) is None


# WEB context Predefined Step
# ID 145
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?A (alertbox|confirmbox|prompt) is opened"))
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?A (alertbox|confirmbox|prompt) is opened"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?A (alertbox|confirmbox|prompt) is opened"))
def step_presence_of_alert(selenium_generics: SeleniumGenerics, soft_assert: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert selenium_generics._wait_for_presence_of_an_alert()
    else:
        assert selenium_generics._wait_for_presence_of_an_alert()


# WEB context Predefined Step
# ID 146
@given(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?A (alertbox|confirmbox|prompt) is not opened"))
@when(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?A (alertbox|confirmbox|prompt) is not opened"))
@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?A (alertbox|confirmbox|prompt) is not opened"))
def check_modal_not_present(selenium_generics: SeleniumGenerics, soft_assert: str):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert not selenium_generics._wait_for_presence_of_an_alert()
    else:
        assert not selenium_generics._wait_for_presence_of_an_alert()


# WEB context Predefined Step
# ID 147
@given(parsers.re("I accept popup (prompt|alertbox|confirmbox)"))
@when(parsers.re("I accept popup (prompt|alertbox|confirmbox)"))
def accept_alert(selenium_generics: SeleniumGenerics):
    selenium_generics.accept_alert()


# WEB context Predefined Step
# ID 148
@given(parsers.re("I dismiss popup (prompt|alertbox|confirmbox)"))
@when(parsers.re("I dismiss popup (prompt|alertbox|confirmbox)"))
def dismiss_modal(selenium_generics: SeleniumGenerics):
    selenium_generics.dismiss_alert()


# WEB context Predefined Step
# ID 149
@given(parsers.re("I enter '(?P<text>.*)' into popup (alertbox|confirmbox|prompt)"),
       converters=dict(text=data_manager.text_formatted), )
@when(parsers.re("I enter '(?P<text>.*)' into popup (alertbox|confirmbox|prompt)"),
      converters=dict(text=data_manager.text_formatted), )
def check_modal(selenium_generics: SeleniumGenerics, text: str):
    selenium_generics.answer_alert_prompt(text)


# WEB context Predefined Step
# ID 150, 151
@given(parsers.re("I set the (locale|language) for locators to '(?P<locale>.*)'"),
       converters=dict(locale=data_manager.text_formatted), )
@when(parsers.re("I set the (locale|language) for locators to '(?P<locale>.*)'"),
      converters=dict(locale=data_manager.text_formatted), )
def set_locale(locators: Locators, locale):
    # TODO: Check Why is setting a locale a step def? Shouldn't this be a CLI argument / config value?
    locators.locale = locale
