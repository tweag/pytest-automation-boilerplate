import base64
import typing
import time
from io import BytesIO
from pathlib import Path

import cv2
import numpy
import structlog
from sys import platform
from PIL import Image
from assertpy import assert_that
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from main.frontend.common.utils import wait
from main.frontend.common.utils.containers import Locator, ShadowLocator, ValidLocatorTypes
from main.frontend.common.utils.locator_parser import parse_locator
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from main.frontend.common.utils.wait import wait_until

logger = structlog.get_logger(__name__)


class _Find:
    type_dispatcher = {
        ValidLocatorTypes.ID: By.ID,
        ValidLocatorTypes.XP: By.XPATH,
        ValidLocatorTypes.LT: By.LINK_TEXT,
        ValidLocatorTypes.PL: By.PARTIAL_LINK_TEXT,
        ValidLocatorTypes.NM: By.NAME,
        ValidLocatorTypes.TN: By.TAG_NAME,
        ValidLocatorTypes.CN: By.CLASS_NAME,
        ValidLocatorTypes.CS: By.CSS_SELECTOR,
    }

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def execute_sync_js(self, js_script: str, *args):
        return self.driver.execute_script(js_script, *args)

    def __get_parent_shadow_element(self, locator: ShadowLocator):
        return self.driver.find_element(_Find.type_dispatcher.get(locator[0].type, _Find.type_dispatcher[ValidLocatorTypes.XP]),
            locator[0].identifier)

    def __find_shadow_element_chromium(self, locator: ShadowLocator):
        element = self.__get_parent_shadow_element(locator)

        for _ in locator[1:]:
            element = element.shadow_root.find_element(
                _Find.type_dispatcher.get(_.type, _Find.type_dispatcher[ValidLocatorTypes.CS]),
                _.identifier,
            )
        return element

    def __find_shadow_element_non_chromium(self, locator: ShadowLocator):
        parent_element = self.__get_parent_shadow_element(locator)

        js_str = f"return arguments[0]"
        for _ in locator[1:]:
            js_str += f".shadowRoot.querySelector('{_.identifier}')"
        return self.execute_sync_js(js_str, parent_element)

    def __find_shadow_elements_chromium(self, locator: ShadowLocator):
        element = self.__get_parent_shadow_element(locator)

        for _ in locator[1:-1]:
            element = element.shadow_root.find_element(
                _Find.type_dispatcher.get(_.type, _Find.type_dispatcher[ValidLocatorTypes.CS]),
                _.identifier,
            )
        elements = element.shadow_root.find_elements(
            _Find.type_dispatcher.get(locator[-1].type, _Find.type_dispatcher[ValidLocatorTypes.CS]),
            locator[-1].identifier,
        )
        return elements

    def __find_shadow_elements_non_chromium(self, locator: ShadowLocator):
        parent_element = self.__get_parent_shadow_element(locator)

        js_str = f"return arguments[0]"
        for _ in locator[1:-1]:
            js_str += f".shadowRoot.querySelector('{_.identifier}')"
        element = self.execute_sync_js(js_str, parent_element)

        elements = self.execute_sync_js(f"return arguments[0].shadowRoot.querySelectorAll('{locator[-1].identifier}')", element)
        return elements

    def perform_action_on_shadow_element_non_chromium(self, locator: ShadowLocator, action: str):
        parent_element = self.__get_parent_shadow_element(locator)

        js_str = f"return arguments[0]"
        for _ in locator[1:]:
            js_str += f".shadowRoot.querySelector('{_.identifier}')"
        js_str += f".{action}"
        return self.execute_sync_js(js_str, parent_element)

    def find_element(self, locator: typing.Union[Locator, ShadowLocator]) -> WebElement:
        if isinstance(locator, Locator):
            return self.driver.find_element(
                _Find.type_dispatcher.get(
                    locator.type, _Find.type_dispatcher[ValidLocatorTypes.XP]
                ),
                locator.identifier,
            )
        if isinstance(locator, ShadowLocator):
            if self.driver.capabilities.get("browserName", "").lower() in ("firefox", "safari") \
               or self.driver.capabilities.get("platformName", False):
                return self.__find_shadow_element_non_chromium(locator)
            else:
                return self.__find_shadow_element_chromium(locator)
        raise TypeError(
            "Invalid Locator Provided. Either provide a Locator or ShadowLocators Type."
        )

    def find_elements(self, locator: typing.Union[Locator, ShadowLocator]) -> typing.List[WebElement]:
        if isinstance(locator, Locator):
            return self.driver.find_elements(
                _Find.type_dispatcher.get(locator.type, _Find.type_dispatcher[ValidLocatorTypes.XP]),
                locator.identifier,
            )

        if isinstance(locator, ShadowLocator):
            if self.driver.capabilities.get("browserName", "").lower() in ("firefox", "safari") \
               or self.driver.capabilities.get("platformName", False):
                return self.__find_shadow_elements_non_chromium(locator)
            else:
                return self.__find_shadow_elements_chromium(locator)
        raise TypeError(
            "Invalid Locator Provided. Either provide a Locator or ShadowLocators Type."
        )

    def get_element(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
    ):
        if isinstance(locator, WebElement):
            return locator
        if isinstance(locator, str):
            locator = parse_locator(locator)

        return self.find_element(locator)

    def get_elements(
        self, locator: typing.Union[Locator, typing.List[WebElement], str]
    ):
        if isinstance(locator, WebElement):
            return locator

        if isinstance(locator, str):
            locator = parse_locator(locator)

        return self.find_elements(locator)


class _Verification(_Find):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        super().__init__(self.driver)

    def _is_in_viewport(
        self, locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ):
        logger.info("Verifying if element is in view port", element=locator)
        script = (
            "if (!arguments[0].getBoundingClientRect) { \n"
            "    return false \n"
            "}; \n"
            "const rect = arguments[0].getBoundingClientRect(); \n"
            "const windowHeight = (window.innerHeight || document.documentElement.clientHeight); \n"
            "const windowWidth = (window.innerWidth || document.documentElement.clientWidth); \n"
            "const vertInView = (rect.top <= windowHeight) && ((rect.top + rect.height) > 0); \n"
            "const horInView = (rect.left <= windowWidth) && ((rect.left + rect.width) > 0); \n"
            "return (vertInView && horInView);"
        )
        is_in_view = self.execute_sync_js(script, self.get_element(locator))
        logger.info(
            "Is element present in view port: ", element=locator, is_in_view=is_in_view
        )
        return is_in_view

    def scroll_into_view(
        self, locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ):
        self.execute_sync_js(
            "arguments[0].scrollIntoView(true)", self.get_element(locator)
        )

    def _is_element_in_viewport(
        self, locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ) -> typing.Union[WebElement, bool]:
        # first check if the element is present in dom
        # if yes, check if it is in viewport
        # if not, scroll the element to view
        # verify information...
        if not self._is_element_present_on_dom(locator):
            return False
        counter = 0
        while not self._is_in_viewport(locator):
            counter += 1
            self.scroll_into_view(locator)
            wait.be_idle_for(1)
            if counter > 3:
                return False
        return self.get_element(locator)

    def is_element_in_viewport(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        wait_for: int = 20,
    ):
        return wait.wait_until(
            self._is_element_in_viewport, locator, max_wait_time=wait_for
        )

    def _is_element_present_on_dom(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
    ) -> typing.Union[WebElement, bool]:
        try:
            element = self.get_element(locator)
            return element
        except selenium_exceptions.NoSuchElementException:
            return False

    def is_element_present_on_dom(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        wait_for: int = 20,
    ) -> typing.Union[WebElement, bool]:
        return wait.wait_until(
            self._is_element_present_on_dom, locator, max_wait_time=wait_for
        )

    def _is_element_visible(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
    ) -> typing.Union[WebElement, bool]:

        _locator = None
        if isinstance(locator, str):
            _locator = parse_locator(locator)

        if not isinstance(_locator, ShadowLocator) or self.driver.capabilities.get("platformName", "") != "iOS":
            try:
                element = self.get_element(locator)
                return element if element.is_displayed() else False
            except (selenium_exceptions.NoSuchElementException, selenium_exceptions.StaleElementReferenceException):
                return False
        else:
            try:
                is_displayed = True if self.perform_action_on_shadow_element_non_chromium(_locator, "style.display") \
                    not in ("none", None) else False
                element = self.get_element(locator)
                return element if element and is_displayed else False
            except (selenium_exceptions.NoSuchElementException, selenium_exceptions.StaleElementReferenceException):
                return False

    def is_element_visible(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        wait_for: int = 60,
    ) -> typing.Union[WebElement, bool]:
        return wait.wait_until(
            self._is_element_visible, locator, max_wait_time=wait_for
        )

    def is_element_clickable(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        wait_for: int = 60,
    ) -> typing.Union[WebElement, bool]:
        return WebDriverWait(self.driver, wait_for).until(
            EC.element_to_be_clickable(self.get_element(locator))
        )

    def is_element_invisible(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        wait_for: int = 10,
    ) -> typing.Union[WebElement, bool]:
        try:
            return WebDriverWait(self.driver, wait_for).until(
                EC.invisibility_of_element(self.get_element(locator))
            )
        except selenium_exceptions.NoSuchElementException:
            return True

    def is_selected(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        wait_for: int = 10,
    ) -> typing.Union[WebElement, bool]:
        try:
            return WebDriverWait(self.driver, wait_for).until(
                EC.element_to_be_selected(self.get_element(locator))
            )
        except selenium_exceptions.TimeoutException:
            return False

    def is_enabled(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        wait_for: int = 10,
    ) -> typing.Union[WebElement, bool]:

        _locator = None
        if isinstance(locator, str):
            _locator = parse_locator(locator)

        if not isinstance(_locator, ShadowLocator) or self.driver.capabilities.get("platformName", "") != "iOS":
            try:
                return WebDriverWait(self.driver, wait_for).until(
                    EC.element_to_be_clickable(self.get_element(locator))
                )
            except selenium_exceptions.TimeoutException:
                return False
        else:
            try:
                wait_until(self.get_element, "locator", max_wait_time=wait_for)
                is_displayed = True if self.perform_action_on_shadow_element_non_chromium(_locator, "style.display") \
                    not in ("none", None) else False
                return True if is_displayed else False
            except (selenium_exceptions.TimeoutException, selenium_exceptions.NoSuchElementException, selenium_exceptions.StaleElementReferenceException):
                return False

    # Below two methods - __validate_style and validate_element_style ported as-is from selenium_generics.
    # might need refactoring at future releases
    @staticmethod
    def __validate_style(elem, data_table):
        error_messages = []
        for key, value in data_table.items():
            if key == "font-family":
                if value.lower() not in elem.value_of_css_property(key).lower():
                    error_messages.append(
                        f"\n{key} not correct. \nActual: {elem.value_of_css_property(key)} \nExpected: {value}"
                    )
            else:
                if elem.value_of_css_property(key).lower() not in value.lower():
                    error_messages.append(
                        f"\n{key} not correct. \nActual: {elem.value_of_css_property(key)} \nExpected: {value}"
                    )

            assert (
                error_messages.__len__() == 0
            ), f'Element style failed with errors: {"".join(error_messages)}'
            logger.error("Element style failed with errors: ", error_messages)

    def validate_element_style(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        data_table: dict,
    ):
        logger.info("About to validate the element style")
        self.__validate_style(self.get_element(locator), data_table)
        logger.info("Element style validation successful")


class _Action(_Verification):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        super().__init__(self.driver)

    def click_by_action(
        self, locator: typing.Union[Locator, ShadowLocator, WebElement, str], *, max_wait_time: int = 20
    ):
        assert self.is_element_visible(locator, max_wait_time)
        actions = ActionChains(self.driver)
        actions.click(self.get_element(locator)).perform()

    def click_and_hold(
        self, locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ):
        actions = ActionChains(self.driver)
        actions.click_and_hold(self.get_element(locator)).perform()

    def context_click(
        self, locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ):
        actions = ActionChains(self.driver)
        actions.context_click(self.get_element(locator)).perform()

    def double_click(
        self, locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ):
        actions = ActionChains(self.driver)
        actions.double_click(self.get_element(locator)).perform()

    def hover(self, locator: typing.Union[Locator, ShadowLocator, WebElement, str]):
        actions = ActionChains(self.driver)
        actions.move_to_element(self.get_element(locator)).perform()

    def move_to_element_by_offset(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        x_offset: int,
        y_offset: int,
    ):
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(
            self.get_element(locator), x_offset, y_offset
        )

    def hover_and_click(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        sub_locator: typing.Union[Locator, ShadowLocator, WebElement, str, None] = None,
    ):
        actions = ActionChains(self.driver)
        if sub_locator:
            actions.move_to_element(self.get_element(locator)).click(
                self.get_element(sub_locator)
            ).perform()
        else:
            actions.move_to_element(self.get_element(locator)).click().perform()

    def move_by_offset(self, x_offset: int, y_offset: int):
        actions = ActionChains(self.driver)
        actions.move_by_offset(x_offset, y_offset)

    def drag_and_drop(
        self,
        source_locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        target_locator: typing.Union[Locator, ShadowLocator, WebElement, str],
    ):
        actions = ActionChains(self.driver)
        actions.drag_and_drop(self.get_element(source_locator), self.get_element(target_locator)).perform()

    def drag_and_drop_by_offset(
        self,
        source_locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        target_x_offset: int,
        target_y_offset: int,
    ):
        actions = ActionChains(self.driver)
        actions.drag_and_drop_by_offset(
            self.get_element(source_locator), target_x_offset, target_y_offset
        ).perform()

    def release_left_mouse_button(
        self, locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ):
        actions = ActionChains(self.driver)
        actions.release(self.get_element(locator)).perform()

    def enter_text_key_down(
        self,
        key_to_press: str,
        focus_locator: typing.Union[
            Locator, ShadowLocator, WebElement, str, None
        ] = None,
        text: str = "",
    ):
        # similar to CTRL+A, SHIFT+"QWERTY", etc.
        actions = ActionChains(self.driver)
        if focus_locator:
            focus_locator = self.get_element(focus_locator)
        key_to_press = getattr(Keys, key_to_press, Keys.RETURN)
        if text:
            actions.key_down(key_to_press, focus_locator).send_keys(text).perform()
        else:
            actions.key_down(key_to_press, focus_locator).perform()

    def enter_text_key_up(
        self,
        key_to_release: str,
        focus_locator: typing.Union[
            Locator, ShadowLocator, WebElement, str, None
        ] = None,
        text: str = "",
    ):
        actions = ActionChains(self.driver)
        if focus_locator:
            focus_locator = self.get_element(focus_locator)
        key_to_release = getattr(Keys, key_to_release, Keys.RETURN)
        if text:
            actions.key_up(key_to_release, focus_locator).send_keys(text).perform()
        else:
            actions.key_up(key_to_release, focus_locator).perform()

    def press_key(self, key_to_press: str):
        key_to_press = getattr(Keys, key_to_press, Keys.RETURN)
        actions = ActionChains(self.driver)
        actions.send_keys(key_to_press).perform()

    def simulate_realistic_typing(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        text: str,
        *,
        gap_seconds: typing.Union[int, float] = 0.5,
    ):
        assert self.is_element_visible(locator)
        actions = ActionChains(self.driver)
        actions.click(self.get_element(locator)).perform()
        for _ in text:
            actions.key_down(_).perform()
            time.sleep(0.5)
            actions.key_up(_).perform()
            wait.be_idle_for(gap_seconds)

    def scroll_to_edge(self, direction: str):
        if direction == "bottom":
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        elif direction == "top":
            self.driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")


class _Information(_Verification):
    MAX_SCROLL_DISTANCE = 100000

    def __init__(self, driver: WebDriver):
        self.driver = driver
        super().__init__(self.driver)

    def get_current_active_element(self) -> WebElement:
        return self.driver.switch_to.active_element

    def get_tag_name(
        self, locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ):
        return self.get_element(locator).tag_name

    def get_attribute_of_element(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        attribute: str,
    ):
        try:
            return self.get_element(locator).get_attribute(attribute)
        except Exception:
            return self.execute_sync_js(
                "return arguments[0].getAttribute(arguments[1])",
                self.get_element(locator),
                attribute,
            )

    def get_input_text(
        self, locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ) -> str:
        # prerequisite - element should be visible
        assert self.is_element_visible(
            locator
        ), f"Locator {locator} is not visible on screen to get text."
        try:
            return self.get_attribute_of_element(locator, "value")
        except Exception:
            return self.execute_sync_js(
                "return arguments[0].value;", self.get_element(locator)
            )

    def get_element_size_position(
        self, locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ) -> dict:
        return self.get_element(locator).rect

    def get_css_value(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        css_property: str,
    ):
        return self.get_element(locator).value_of_css_property(css_property)

    def get_element_text(
        self, locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ) -> str:
        # prerequisite - element should be visible
        assert self.is_element_visible(
            locator
        ), f"Locator {locator} is not visible on screen to get text."

        _locator = None
        if isinstance(locator, str):
            _locator = parse_locator(locator)

        if not isinstance(_locator, ShadowLocator) or self.driver.capabilities.get("platformName", "") != "iOS":
            return self.get_element(locator).text
        else:
            return self.perform_action_on_shadow_element_non_chromium(_locator, "textContent")

    def get_property(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        property: str,
    ):
        return self.get_element(locator).get_property(property)

    def get_cropped_screenshot_as_base64(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        y_point: int = 0,
    ):
        # Scroll element into view
        logger.debug("About to get the screenshot cropped")
        self.execute_sync_js(f"window.scrollBy(0,{self.MAX_SCROLL_DISTANCE})")
        wait.be_idle_for(1)
        self.execute_sync_js(
            "arguments[0].scrollIntoView(true);", self.get_element(locator)
        )
        wait.be_idle_for(1)
        image_base_64 = self.driver.get_screenshot_as_base64()

        im = Image.open(BytesIO(base64.b64decode(image_base_64)))
        im = im.crop((0, y_point, im.width, (im.height * 0.75 - y_point)))
        logger.debug("Image cropping completed")

        return cv2.cvtColor(numpy.array(im), cv2.COLOR_RGB2BGR)

    # Does not work on mobile where location and size are not correctly calculated
    def get_screenshot_as_base64(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        threshold: int = 0,
    ):
        logger.debug("Started getting screenshot as base64")
        element = self.get_element(locator)
        location = element.location
        size = element.size

        if self.driver.desired_capabilities["browserName"] in [
            "Chrome",
            "chrome",
            "MicrosoftEdge",
            "microsoftedge",
        ]:
            self.execute_sync_js(f"window.scrollBy(0,{self.MAX_SCROLL_DISTANCE})")
            wait.be_idle_for(1)
            # Scroll element into view
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            wait.be_idle_for(1)
            location = element.location_once_scrolled_into_view

        if self.driver.capabilities["browserName"] in ["Safari", "safari"]:
            self.execute_sync_js(f"window.scrollBy(0,{self.MAX_SCROLL_DISTANCE})")
            wait.be_idle_for(1)
            # Scroll element into view
            self.execute_sync_js("arguments[0].scrollIntoView(true);", element)
            wait.be_idle_for(1)
            location = element.location_once_scrolled_into_view

        x_point = location["x"]
        width = location["x"] + size["width"]

        # Is needed for iOS screenshot to remove browser header controls.
        # On iOS the screenshot includes browser header and footer controls
        y_point = location["y"] + threshold
        height = location["y"] + size["height"] - threshold

        logger.debug("Calling WebElement class get screenshot method ")
        image_base_64 = self.driver.get_screenshot_as_base64()

        img = Image.open(BytesIO(base64.b64decode(image_base_64)))
        img = img.crop((int(x_point), int(y_point), int(width), int(height)))
        logger.info("Get screenshot as Base64 completed")
        return cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)


class _Interaction(_Verification):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        super().__init__(self.driver)

    def enter_text(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        text_to_enter: str,
        *,
        max_wait_time: int = 20,
    ):
        # prerequisite: element should be visible and enabled for entering text
        assert self.is_element_visible(
            locator, max_wait_time
        ), f"{locator} is not visible for entering text.."

        _locator = None
        if isinstance(locator, str):
            _locator = parse_locator(locator)

        try:
            self.get_element(locator).send_keys(text_to_enter)
        except Exception:
            if isinstance(_locator, ShadowLocator) and self.driver.capabilities.get("platformName", "") == "iOS":
                self.perform_action_on_shadow_element_non_chromium(_locator, f"textContent={text_to_enter}")
            else:
                self.execute_sync_js(
                    "arguments[0].value = arguments[1];",
                    self.get_element(locator),
                    text_to_enter,
                )

    def clear_text(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        *,
        max_wait_time: int = 20,
    ):
        # prerequisite: element should be visible and enabled for entering text
        assert self.is_element_visible(
            locator, max_wait_time
        ), f"{locator} is not visible for clearing text.."

        _locator = None
        if isinstance(locator, str):
            _locator = parse_locator(locator)

        try:
            self.get_element(locator).clear()
        except Exception:
            if isinstance(_locator, ShadowLocator) and self.driver.capabilities.get("platformName", "") == "iOS":
                self.perform_action_on_shadow_element_non_chromium(_locator, f'textContent=""')
            else:
                self.execute_sync_js(
                    "arguments[0].value=arguments[1];", self.get_element(locator), ""
                )

    def clear_text_using_keys(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        *,
        max_wait_time: int = 20,
    ):
        # prerequisite: element should be visible and enabled for entering text
        assert self.is_element_visible(
            locator, max_wait_time
        ), f"{locator} is not visible for clearing text.."
        element = self.get_element(locator)
        actions = ActionChains(self.driver)
        if self.driver.capabilities["platformName"].lower() in ["windows", "win32", "linux"]:
            actions.move_to_element(element).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(Keys.DELETE).perform()
        elif self.driver.capabilities["platformName"].lower() in ["mac os x", "macos", "mac", "os x", "darwin"]:
            actions.move_to_element(element).click().key_down(
                Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND).send_keys(Keys.DELETE).perform()
        elif self.driver.capabilities["platformName"].lower() == "android":
            actions.move_to_element(element).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(Keys.DELETE).perform()
            # In case on some Android devices text is still visible
            if self.execute_sync_js("return arguments[0].value;", self.get_element(locator)):
                actions.move_to_element(element).click().key_down(Keys.COMMAND).send_keys('a').key_up(
                    Keys.COMMAND).send_keys(Keys.DELETE).perform()
        elif self.driver.capabilities["platformName"].lower() == "ios":
            self.execute_sync_js("arguments[0].value = arguments[1];", element, "")

    def press_key_on_element(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        key_to_press: str = "RETURN",
    ):
        key_to_press = getattr(Keys, key_to_press, Keys.RETURN)
        self.get_element(locator).send_keys(key_to_press)

    def click(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        *,
        max_wait_time: int = 20,
    ):
        _locator = None
        if isinstance(locator, str):
            _locator = parse_locator(locator)

        # prerequisite: element should be visible and enabled for click operation to succeed
        assert (self.is_element_visible(locator) and self.is_enabled(locator, max_wait_time)), \
                f"{locator} is either not visible or enabled for the click operation to succeed.."
        try:
            self.get_element(locator).click()
        except Exception:
            if self.driver.capabilities.get("platformName", "") == "iOS" and isinstance(_locator, ShadowLocator):
                if wait_until(self.get_element, locator, max_wait_time=max_wait_time):
                    self.perform_action_on_shadow_element_non_chromium(_locator, "click()")
                else:
                    raise ElementNotVisibleException
            else:
                self.execute_sync_js("return arguments[0].click();", self.get_element(locator))

    def capture_element_screenshot(
        self,
        locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        file_path_to_save: Path,
    ):
        if not isinstance(file_path_to_save, Path):
            raise TypeError("Pass a valid Path argument.")
        is_saved = self.get_element(locator).screenshot(str(file_path_to_save))
        if not is_saved:
            raise IOError(f"There was error saving screenshot to {file_path_to_save}")
        return file_path_to_save

    def select_dropdown_value(
        self, locator: typing.Union[Locator, WebElement, str], value: str,
    ):
        # prerequisite: assert element is visible on screen.
        assert self.is_element_visible(
            locator
        ), f"Locator {locator} is not visible on screen ..."
        dropdown_values = self.get_elements(locator)
        for element in dropdown_values:
            element_text = element.text if element.text != '' else element.get_attribute("innerHTML")
            if value == element_text:
                self.click(element)
                break
        else:
            raise NoSuchElementException(f"The element with text value: {value} is not visible")

    def select_dropdown_value_at_index(
        self, locator: typing.Union[Locator, WebElement, str], index: int,
    ):
        # prerequisite: assert element is visible on screen.
        assert self.is_element_visible(
            locator
        ), f"Locator {locator} is not visible on screen ..."
        dropdown_values = self.get_elements(locator)
        for i in range(1, len(dropdown_values) + 1):
            if index == i:
                self.click(dropdown_values[i])
                break
        else:
            raise NoSuchElementException(f"The element with index: {index} is not visible")

    def get_text_of_ui_elements(self, locator):
        ui_elements = self.get_elements(locator + "//*")
        ui_elements_text = []
        for index in range(0, len(ui_elements)):
            element_text = ui_elements[index].text if ui_elements[index].text != '' else ui_elements[
                index].get_attribute("innerHTML")
            ui_elements_text.append(element_text)
        return ui_elements_text

    @staticmethod
    def get_input_values_based_on_expected(table_values):
        return list(table_values.get("expected_values").split(', '))

    def compare_expected_and_ui_values_with_order(
        self, locator: typing.Union[Locator, WebElement, str], table_values
    ):
        for index in range(0, len(self.get_input_values_based_on_expected(table_values))):
            assert_that(self.get_input_values_based_on_expected(table_values)[index]).\
                is_equal_to(self.get_text_of_ui_elements(locator)[index])
        assert_that(len(self.get_text_of_ui_elements(locator))).\
            is_equal_to(len(self.get_input_values_based_on_expected(table_values)))

    def contains_expected_and_ui_values(
        self, locator: typing.Union[Locator, WebElement, str], table_values
    ):
        assert_that(self.get_input_values_based_on_expected(table_values)).\
            is_subset_of(self.get_text_of_ui_elements(locator))

    def does_not_contains_expected_and_ui_values(
        self, locator, table_values
    ):
        for value in self.get_input_values_based_on_expected(table_values):
            assert_that(self.get_text_of_ui_elements(locator)).does_not_contain(value)

class _Select(_Verification):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        super().__init__(self.driver)

    def select_by_index(
        self,
        select_locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        ind: int,
    ):
        # prerequisite: assert element is visible on screen.
        assert self.is_element_visible(
            select_locator
        ), f"Locator {select_locator} is not visible on screen ..."
        select_object = Select(self.get_element(select_locator))
        select_object.select_by_index(ind)

    def select_by_value(
        self,
        select_locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        value: str,
    ):
        # prerequisite: assert element is visible on screen.
        assert self.is_element_visible(
            select_locator
        ), f"Locator {select_locator} is not visible on screen ..."
        select_object = Select(self.get_element(select_locator))
        select_object.select_by_value(value)

    def select_by_visible_text(
        self,
        select_locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        text: str,
    ):
        # prerequisite: assert element is visible on screen.
        assert self.is_element_visible(
            select_locator
        ), f"Locator {select_locator} is not visible on screen ..."
        select_object = Select(self.get_element(select_locator))
        select_object.select_by_visible_text(text)

    def get_all_selected_options(
        self, select_locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ) -> typing.List[WebElement]:
        # prerequisite: assert element is visible on screen.
        assert self.is_element_visible(
            select_locator
        ), f"Locator {select_locator} is not visible on screen ..."
        select_object = Select(self.get_element(select_locator))
        return select_object.all_selected_options

    def get_first_selected_option(
        self, select_locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ) -> typing.List[WebElement]:
        # prerequisite: assert element is visible on screen.
        assert self.is_element_visible(
            select_locator
        ), f"Locator {select_locator} is not visible on screen ..."
        select_object = Select(self.get_element(select_locator))
        return select_object.first_selected_option

    def get_all_options(
        self, select_locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ) -> typing.List[WebElement]:
        # prerequisite: assert element is visible on screen.
        assert self.is_element_visible(
            select_locator
        ), f"Locator {select_locator} is not visible on screen ..."
        select_object = Select(self.get_element(select_locator))
        return select_object.options

    def deselect_by_index(
        self,
        select_locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        ind: int,
    ):
        # prerequisite: assert element is visible on screen.
        assert self.is_element_visible(
            select_locator
        ), f"Locator {select_locator} is not visible on screen ..."
        select_object = Select(self.get_element(select_locator))
        select_object.deselect_by_index(ind)

    def deselect_by_value(
        self,
        select_locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        value: str,
    ):
        # prerequisite: assert element is visible on screen.
        assert self.is_element_visible(
            select_locator
        ), f"Locator {select_locator} is not visible on screen ..."
        select_object = Select(self.get_element(select_locator))
        select_object.deselect_by_value(value)

    def deselect_by_visible_text(
        self,
        select_locator: typing.Union[Locator, ShadowLocator, WebElement, str],
        text: str,
    ):
        # prerequisite: assert element is visible on screen.
        assert self.is_element_visible(
            select_locator
        ), f"Locator {select_locator} is not visible on screen ..."
        select_object = Select(self.get_element(select_locator))
        select_object.deselect_by_visible_text(text)

    def is_multiple_selection(
        self, select_locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ) -> bool:
        # prerequisite: assert element is visible on screen.
        assert self.is_element_visible(
            select_locator
        ), f"Locator {select_locator} is not visible on screen ..."
        select_object = Select(self.get_element(select_locator))
        return select_object.is_multiple

    def deselect_all(
        self, select_locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ):
        # prerequisite: assert element is visible on screen.
        assert self.is_element_visible(
            select_locator
        ), f"Locator {select_locator} is not visible on screen ..."
        select_object = Select(self.get_element(select_locator))
        if self.is_multiple_selection(select_locator):
            select_object.deselect_all()


class _Alert(_Verification):
    ALERT_NOT_PRESENT_TO_GET_TEXT_MESSAGE = "Alert not present to get text !!"
    ALERT_NOT_PRESENT_TO_ACCEPT_MESSAGE = "Alert not present to accept !!"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        super().__init__(self.driver)

    def _wait_for_presence_of_an_alert(
        self, wait_for: int = 10
    ) -> typing.Union[Alert, bool]:
        try:
            return WebDriverWait(self.driver, wait_for).until(EC.alert_is_present())
        except selenium_exceptions.TimeoutException:
            return False

    def get_alert_text(self) -> str:
        # pre-requisite: presence of alert and switch to it.
        alert = self._wait_for_presence_of_an_alert()
        assert alert, self.ALERT_NOT_PRESENT_TO_GET_TEXT_MESSAGE
        return alert.text

    def accept_alert(self):
        # pre-requisite: presence of alert and switch to it.
        alert = self._wait_for_presence_of_an_alert()
        assert alert, self.ALERT_NOT_PRESENT_TO_ACCEPT_MESSAGE
        alert.accept()

    def dismiss_alert(self):
        # pre-requisite: presence of alert and switch to it.
        alert = self._wait_for_presence_of_an_alert()
        assert alert, self.ALERT_NOT_PRESENT_TO_ACCEPT_MESSAGE
        alert.dismiss()

    def answer_alert_prompt(self, message: str):
        # pre-requisite: presence of alert and switch to it.
        alert = self._wait_for_presence_of_an_alert()
        assert alert, self.ALERT_NOT_PRESENT_TO_ACCEPT_MESSAGE
        alert.send_keys(message)


class _Iframe(_Verification):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        super().__init__(self.driver)

    def switch_context_to_iframe(
        self, locator: typing.Union[Locator, ShadowLocator, WebElement, str]
    ):
        self.driver.switch_to.frame(self.get_element(locator))


class ElementInteraction(
    _Action,
    _Information,
    _Interaction,
    _Select,
    _Alert,
    _Iframe,
):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        super().__init__(self.driver)
