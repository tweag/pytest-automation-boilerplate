import structlog
import re

from pytest_bdd import parsers, then
from pytest_check import check

from main.frontend.common.helpers.selenium_generics import SeleniumGenerics
from main.frontend.common.utils.locator_parser import Locators
from main.frontend.common.helpers.standalone_compare import are_two_images_look_same
from main.utils.gherkin_utils import data_table_horizontal_converter
from main.frontend.common.helpers.web_compare import (are_two_webelements_look_same, are_two_webpages_look_same)

logger = structlog.get_logger(__name__)


@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I verify images '(?P<name>.*)' have no visual regression"))
def image_visual_is_valid(soft_assert: str, name):

    if soft_assert is not None and soft_assert.lower() == 'true':
        with check:
            assert are_two_images_look_same(name)
    else:
        assert are_two_images_look_same(name)


@then(parsers.re("(With soft assertion '(?P<soft_assert>.*)' )?I verify that element '(?P<locator_path>.*)' is not visually regressed:(?P<data_table>.*)",
                 flags=re.S, ), converters=dict(data_table=data_table_horizontal_converter), )
def element_visual_is_valid(selenium_generics: SeleniumGenerics, locators: Locators, soft_assert: str, locator_path: str, data_table: dict):
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
