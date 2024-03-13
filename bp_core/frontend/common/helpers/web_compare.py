import typing
from selenium.webdriver.remote.webelement import WebElement

from bp_core.frontend.common.helpers.selenium_generics import SeleniumGenerics
from bp_core.frontend.common.utils.containers import Locator, ShadowLocator
from bp_core.frontend.common.utils import visual_utils


def are_two_webelements_look_same(
    base_image_name_with_ext: str,
    selenium_generics: SeleniumGenerics,
    locator: typing.Union[Locator, ShadowLocator, WebElement, str],
) -> bool:
    """Function to check if two webelements are same

    Args:
        selenium_generics: SeleniumGenerics instance
        base_image_name_with_ext: str - Base Image File Name for comparison
        locator: Locator instance

    Returns:
        Boolean Value indicating if elements are same (True) or different (False)

    """
    file_pths = visual_utils.file_paths(base_image_name_with_ext)
    assert (
        file_pths.base.is_file()
    ), f"Base Image Not present at location {file_pths.base}"

    elem = selenium_generics.is_element_visible(locator)
    assert elem, "WebElement: {locator} is not displayed or enabled to capture screenshot !!"

    png_screenshot = elem.screenshot_as_png

    with open(file_pths.test, "wb") as f:
        f.write(png_screenshot)
    return visual_utils.are_images_same(base_image_name_with_ext)


def are_two_webpages_look_same(
    base_image_name_with_ext: str,
    selenium_generics: SeleniumGenerics,
):
    """Function to check if two web pages look same.

    Args:
        base_image_name_with_ext: str - Base Image Name against which comparison should run.
        selenium_generics: SeleniumGenerics instance

    Returns:
        Boolean indicating if the web pages are same.
    """
    file_pths = visual_utils.file_paths(base_image_name_with_ext)
    assert (
        file_pths.base.is_file()
    ), f"Base Image Not present at location {file_pths.base}"

    selenium_generics.full_screenshot(file_pths.test, scroll_delay=1.0)
    return visual_utils.are_images_same(base_image_name_with_ext)
