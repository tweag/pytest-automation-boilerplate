
import structlog

from pytest_bdd import parsers, given, when
from bp_core.frontend.common.helpers.app import context_manager
from selenium.common.exceptions import NoSuchElementException
from bp_core.frontend.common.helpers.selenium_generics import SeleniumGenerics
from bp_core.frontend.common.utils.locator_parser import Locators
from bp_core.utils import data_manager

logger = structlog.get_logger(__name__)


# WEB context Predefined Step
# ID 301
@given(parsers.re("I drag and drop element '(?P<source>.*)' to element '(?P<target>.*)'"))
@when(parsers.re("I drag and drop element '(?P<source>.*)' to element '(?P<target>.*)'"))
def drag_and_drop_element(selenium_generics: SeleniumGenerics, locators: Locators, source: str, target: str):
    selenium_generics.drag_and_drop(locators.parse_and_get(source, selenium_generics),
                                    locators.parse_and_get(target, selenium_generics))


# WEB context Predefined Step
# ID 302
@given(parsers.re("I drag and drop element '(?P<source>.*)' by offset '(?P<x>.*)' and '(?P<y>.*)'"),
       converters=dict(x=data_manager.text_formatted, y=data_manager.text_formatted), )
@when(parsers.re("I drag and drop element '(?P<source>.*)' by offset '(?P<x>.*)' and '(?P<y>.*)'"),
      converters=dict(x=data_manager.text_formatted, y=data_manager.text_formatted), )
def drag_and_drop_element_by_offset(selenium_generics: SeleniumGenerics, locators: Locators, source: str, x: int,
                                    y: int):
    selenium_generics.drag_and_drop_by_offset(locators.parse_and_get(source, selenium_generics), int(x), int(y))


# WEB context Predefined Step
# ID 303
@given(parsers.re("I scroll to element '(?P<locator_path>.*)'"))
@when(parsers.re("I scroll to element '(?P<locator_path>.*)'"))
def scroll_to_element(selenium_generics: SeleniumGenerics, locators: Locators, locator_path: str):
    selenium_generics.is_element_in_viewport(locators.parse_and_get(locator_path, selenium_generics))
    # element is still not visible after scroll into view
    if not (selenium_generics.is_element_visible(locators.parse_and_get(locator_path, selenium_generics), 2)):
        raise NoSuchElementException(
            f"The web element {locator_path}' is not visible or accessible for interactions")


# WEB context Predefined Step
# ID 304
@given(parsers.re("I scroll to view and click on '(?P<locator_path>.*)'"))
@when(parsers.re("I scroll to view and click on '(?P<locator_path>.*)'"))
def click_on_element(selenium_generics: SeleniumGenerics, locators: Locators, locator_path: str):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    selenium_generics.scroll_into_view(locator)
    selenium_generics.click(locator)


# MOBILE context Predefined Step
# ID 305
@given(parsers.re("I scroll to element '(?P<locator>.*)' for '(?P<iterations>.*)' iterations"),
       converters=dict(iterations=data_manager.text_formatted), )
@when(parsers.re("I scroll to element '(?P<locator>.*)' for '(?P<iterations>.*)' iterations"),
      converters=dict(iterations=data_manager.text_formatted), )
def scroll_to_native_element(selenium_generics: SeleniumGenerics, locators: Locators, locator: str, iterations: int):
    for iterations in range(int(iterations)):
        if selenium_generics.is_element_visible(locators.parse_and_get(locator, selenium_generics)):
            break
        else:
            with context_manager(driver=selenium_generics):
                selenium_generics.swipe_to_element(selenium_generics)


# WEB & MOBILE contexts Predefined Step
# ID 306
@given(parsers.re("I scroll on the '(?P<scroll_direction>top|bottom)' of the page"))
@when(parsers.re("I scroll on the '(?P<scroll_direction>top|bottom)' of the page"))
def scroll_to_edge(selenium_generics: SeleniumGenerics, scroll_direction):
    """
    accepted directions: top,bottom
    """
    if hasattr(selenium_generics.driver, 'current_context'):
        with context_manager(driver=selenium_generics):
            selenium_generics.scroll_to_edge_of_mobile_page(selenium_generics, scroll_direction)
    else:
        selenium_generics.scroll_to_edge(scroll_direction)


# WEB context Predefined Step
# ID 307
@given(parsers.re("I hover over '(?P<locator_path>.*)'"))
@given(parsers.re("I move to element '(?P<locator_path>.*)'"))
@when(parsers.re("I hover over '(?P<locator_path>.*)'"))
@when(parsers.re("I move to element '(?P<locator_path>.*)'"))
def hover_over_element(selenium_generics: SeleniumGenerics, locators: Locators, locator_path: str):
    locator = locators.parse_and_get(locator_path, selenium_generics)
    selenium_generics.scroll_into_view(locator)
    selenium_generics.hover(locator)


# WEB context Predefined Step
# ID 308
@given(parsers.re("I move to an element '(?P<locator_path>.*)' with offset '(?P<x>.*)' '(?P<y>.*)'"),
       converters=dict(x=data_manager.text_formatted, y=data_manager.text_formatted), )
@when(parsers.re("I move to an element '(?P<locator_path>.*)' with offset '(?P<x>.*)' '(?P<y>.*)'"),
      converters=dict(x=data_manager.text_formatted, y=data_manager.text_formatted), )
def move_to_element_by_offset(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, x: int, y: int):
    selenium_generics.move_to_element_by_offset(locators.parse_and_get(locator_path, selenium_generics), int(x), int(y))


# WEB context Predefined Step
# ID 309
@given(parsers.re("I hover over '(?P<locator_path1>.*)' and click element '(?P<locator_path2>.*)'"))
@when(parsers.re("I hover over '(?P<locator_path1>.*)' and click element '(?P<locator_path2>.*)'"))
def hover_over_and_click_sub_menu(
    selenium_generics: SeleniumGenerics,
    locators: Locators,
    locator_path1: str,
    locator_path2: str,
):
    main_menu = locators.parse_and_get(locator_path1, selenium_generics)
    sub_menu = locators.parse_and_get(locator_path2, selenium_generics)
    selenium_generics.scroll_into_view(main_menu)
    selenium_generics.hover_and_click(main_menu, sub_menu)


# MOBILE context Predefined Step
# ID 310
@given(parsers.re("I swipe down '(?P<percent>.*)' % each time for '(?P<number>.*)' times"),
       converters=dict(percent=data_manager.text_formatted, number=data_manager.text_formatted), )
@when(parsers.re("I swipe down '(?P<percent>.*)' % each time for '(?P<number>.*)' times"),
      converters=dict(percent=data_manager.text_formatted, number=data_manager.text_formatted), )
def swipe_down_each_time_in_percentage(selenium_generics: SeleniumGenerics, percent: int, number: int):
    with context_manager(driver=selenium_generics):
        selenium_generics.swipe_down(int(percent), int(number))


# MOBILE contexts Predefined Step
# ID 311
@given(parsers.re(r"I swipe '(?P<direction>left|right)' on element '(?P<locator_path>.*)'( by '(?P<pixels>\d+)' px)?$"))
@when(parsers.re(r"I swipe '(?P<direction>left|right)' on element '(?P<locator_path>.*)'( by '(?P<pixels>\d+)' px)?$"))
def swipe_horizontally_on_element(selenium_generics: SeleniumGenerics, locators: Locators, direction: str, locator_path,
                                  pixels: int):
    move_by_pixels = int(pixels) if pixels else 200
    with context_manager(driver=selenium_generics):
        element = selenium_generics.get_element(locators.parse_and_get(locator_path, selenium_generics))
        if direction == 'left':
            selenium_generics.swipe_left_on_element(element=element, pixels=move_by_pixels)
        elif direction == 'right':
            selenium_generics.swipe_right_on_element(element=element, pixels=move_by_pixels)


# MOBILE contexts Predefined Step
# ID 312
@given(parsers.re(
    r"I swipe '(?P<direction>left|right)' on the page( from x = '(?P<x>\d+)' px and y = '(?P<y>\d+)' px)?( by '(?P<pixels>\d+)' px)?$"))
@when(parsers.re(
    r"I swipe '(?P<direction>left|right)' on the page( from x = '(?P<x>\d+)' px and y = '(?P<y>\d+)' px)?( by '(?P<pixels>\d+)' px)?$"))
def swipe_to_the_next_page(selenium_generics: SeleniumGenerics, direction, x: int, y: int, pixels: int):
    move_by_pixels = int(pixels) if pixels else 700
    with context_manager(driver=selenium_generics):
        if direction == 'left':
            selenium_generics.swipe_left_by_coordinates(x=x, y=y, pixels=move_by_pixels)
        elif direction == 'right':
            selenium_generics.swipe_right_by_coordinates(x=x, y=y, pixels=move_by_pixels)
