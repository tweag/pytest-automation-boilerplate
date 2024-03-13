import structlog
import re

from pytest_bdd import parsers, then
from pytest_check import check

from bp_core.frontend.common.helpers.selenium_generics import SeleniumGenerics
from bp_core.frontend.common.utils.locator_parser import Locators
from bp_core.frontend.common.helpers.standalone_compare import are_two_images_look_same
from bp_core.utils.gherkin_utils import data_table_horizontal_converter
from bp_core.frontend.common.helpers.web_compare import (are_two_webelements_look_same, are_two_webpages_look_same)

logger = structlog.get_logger(__name__)


@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I verify images '(?P<name>.*)' have no visual regression"))
def image_visual_is_valid(soft_assert: str, name):
    """Step Definition to verify if two images are same (Standalone Visual Testing)

    Both Base Image and Test Image are saved in respective directories as defined by boilerplate
    framework, i.e. test_data/visualtesting/base and test_data/visualtesting/test directories, with the
    same name (argument name passed in feature file).

    Args:
        name: str - Image Name to perform visual regression.

    Asserts:
        If Base and Test Images are same. Else raises AssertionError.

    """
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert are_two_images_look_same(name)
    else:
        assert are_two_images_look_same(name)


@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I verify that element '(?P<locator_path>.*)' is not visually regressed:(?P<data_table>.*)",
                 flags=re.S, ), converters=dict(data_table=data_table_horizontal_converter), )
def element_visual_is_valid(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path: str, data_table: dict):
    """Step Definition to verify if a particular webelement is not visually regressed.

    Base Image should be saved in output/screenshots/base directory (name as provided in
    the data table). Test Function would take screenshot of corresponding webelement as
    provided in locator path, and asserts if it is same as base image.

    Args:
        selenium_generics - SeleniumGenerics instance
        locators - Locators instance
        locator_path - as provided in feature file step.
        data_table - retrieved from feature file - scenario - step.

    Asserts:
        If the webelement captured during test is same as the base image provided.
    """
    locator = locators.parse_and_get(locator_path, selenium_generics)
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert are_two_webelements_look_same(data_table["base_image"][0], selenium_generics, locator)
    else:
        assert are_two_webelements_look_same(data_table["base_image"][0], selenium_generics, locator)


@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I verify the page is not visually regressed:(?P<data_table>.*)", flags=re.S),
      converters=dict(data_table=data_table_horizontal_converter), )
def page_visual_is_valid(selenium_generics: SeleniumGenerics, soft_assert: str, data_table: dict):
    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert are_two_webpages_look_same(data_table["base_image"][0], selenium_generics)
    else:
        assert are_two_webpages_look_same(data_table["base_image"][0], selenium_generics)
