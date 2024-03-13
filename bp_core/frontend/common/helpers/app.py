from contextlib import contextmanager
from typing import List

from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
import structlog

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

logger = structlog.get_logger(__name__)


class App:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def back(self):
        self.driver.back()

    def close(self):
        self.driver.terminate_app()

    def reset(self):
        self.driver.reset()

    def launch_app(self):
        self.driver.launch_app()

    def background_app(self, seconds):
        self.driver.background_app(seconds=seconds)

    def get_contexts(self):
        return self.driver.contexts

    def get_current_context(self):
        return self.driver.current_context

    def switch_context(self, name):
        self.driver.switch_to.context(name)

    def is_android(self):
        return True if self.driver.capabilities['platformName'].lower() == 'android' else False

    def long_tap(self, selenium_generics, locator, max_wait_time: int = 20):
        # prerequisite: element should be visible and enabled for click operation to succeed
        assert (selenium_generics.is_element_visible(locator) and selenium_generics.is_enabled(locator, max_wait_time)), \
            f"{locator} is either not visible or enabled for the click operation to succeed.."
        TouchAction(self.driver).long_press(selenium_generics.get_element(locator)).release().perform()

    def swipe_left_on_element(self, element, pixels):
        duration = 1000
        action = TouchAction(self.driver)
        action.press(element).wait(duration).move_to(x=-pixels, y=0).release().perform()

    def swipe_right_on_element(self, element, pixels):
        duration = 1000
        action = TouchAction(self.driver)
        action.press(element).wait(duration).move_to(x=pixels, y=0).release().perform()

    def swipe_left_by_coordinates(self, x, y, pixels):
        start_x = int(x) if x else 800
        start_y = int(y) if y else 700
        end_x = start_x - pixels
        end_y = start_y
        duration = 1000
        action = TouchAction(self.driver)
        action.press(x=start_x, y=start_y).wait(duration).move_to(x=end_x, y=end_y).release().perform()

    def swipe_right_by_coordinates(self, x, y, pixels):
        start_x = int(x) if x else 100
        start_y = int(y) if y else 700
        end_x = start_x + pixels
        end_y = start_y
        duration = 1000
        action = TouchAction(self.driver)
        action.press(x=start_x, y=start_y).wait(duration).move_to(x=end_x, y=end_y).release().perform()

    def swipe_down(self, percent, number):
        window_size = self.driver.get_window_size()
        width = window_size.get('width')
        height = window_size.get('height')
        start_x = end_x = width * 1 / 50
        start_y = height / 2
        end_y = start_y - (start_y * int(percent)) / 100
        for _ in range(int(number)):
            self.driver.swipe(start_x, start_y, end_x, end_y, 500)

    @staticmethod
    def swipe_to_element(selenium_generics):
        if selenium_generics.is_android():
            screen_size = selenium_generics.driver.get_window_size()
            selenium_generics.driver.execute_script('mobile: flingGesture', {
                'direction': 'down',
                'left': screen_size["width"] * 0.4,
                'top': screen_size["height"] * 0.1,
                'width': screen_size["width"] * 0.5,
                'height': screen_size["height"] * 0.5,
                'speed': 500
            })
        else:
            selenium_generics.driver.execute_script('mobile: swipe', {
                'direction': 'up',
            })

    @staticmethod
    def _are_element_positions_the_same(elements_1: List[WebElement], elements_2: List[WebElement]):
        if elements_1 != elements_2:
            return False

        for element_1, element_2 in zip(elements_1, elements_2):
            if element_1.rect != element_2.rect:
                return False

        return True

    def scroll_to_edge_of_mobile_page(self, selenium_generics, direction):
        if direction == 'bottom':
            direction = 'down'
        if direction == 'top':
            direction = 'up'
        previous_elements = []
        new_elements = selenium_generics.get_elements("//*")
        fling_limit = 7
        fling_count = 0
        if selenium_generics.is_android():
            screen_size = selenium_generics.driver.get_window_size()
            while not self._are_element_positions_the_same(previous_elements,
                                                           new_elements) and fling_count < fling_limit:
                fling_count += 1
                selenium_generics.driver.execute_script('mobile: flingGesture', {
                    'direction': direction,
                    'left': screen_size["width"] * 0.4,
                    'top': screen_size["height"] * 0.1,
                    'width': screen_size["width"] * 0.2,
                    'height': screen_size["height"] * 0.7,
                })
                previous_elements = new_elements
                new_elements = selenium_generics.get_elements("//*")
        else:
            while not self._are_element_positions_the_same(previous_elements,
                                                           new_elements) and fling_count < fling_limit:
                fling_count += 1
                selenium_generics.driver.execute_script('mobile: scroll', {
                    'direction': direction,
                })

    def tap_with_percentage(self, selenium_generics, locator, x_offset, y_offset):
        try:
            rect = selenium_generics.is_element_visible(locator).rect
        except Exception:
            raise NoSuchElementException(f"Can't find element {locator}")
        x = ((int(x_offset) / 100) * rect['width'])
        y = ((int(y_offset) / 100) * rect['height'])
        self.driver.tap(positions=[(int(x), int(y))])

    def tap_corner_of_element(self, selenium_generics, corner, locator):

        try:
            rect = selenium_generics.is_element_visible(locator).rect
        except Exception:
            raise NoSuchElementException(f"Can't find element {locator}")
        else:
            offset = 5
            if corner == "TOP_LEFT":
                x = rect["x"] + offset
                y = rect["y"] + offset
            elif corner == "TOP_RIGHT":
                x = rect["x"] + rect["width"] - offset
                y = rect["y"] + offset
            elif corner == "BOTTOM_LEFT":
                x = rect["x"] + offset
                y = rect["y"] + rect["height"] - offset
            elif corner == "BOTTOM_RIGHT":
                x = rect["x"] + rect["width"] - offset
                y = rect["y"] + rect["height"] - offset
            else:
                raise ValueError("Corner value is not correct")
            self.driver.tap(positions=[(x, y)])


@contextmanager
def context_manager(driver, context_name='NATIVE_APP'):
    current_context = driver.get_current_context()
    driver.switch_context(context_name)
    yield
    driver.switch_context(current_context)
