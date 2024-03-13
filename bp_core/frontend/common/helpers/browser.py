import typing
import time
from pathlib import Path
from PIL import Image
from io import BytesIO

import structlog
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from bp_core.frontend.common.utils.containers import WindowPosition, WindowSize
from bp_core.utils.exceptions import BrowserException

logger = structlog.get_logger(__name__)


class BrowserInteraction:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def navigate_to_url(self, url: str):
        self.driver.get(url)

    def switch_tab_by_url(self, url: str):
        windows = self.window_handles
        for window in windows:
            self.switch_to_known_window(window)
            if self.current_url == url:
                return
        raise BrowserException(f"No such url: {url}")

    # method brought in as-is from browser actions
    def go_to_protected_url(self, full_url: str, username: str, password: str):
        http_protocol = "http"
        https = f"{http_protocol}s://"
        http = f"{http_protocol}://"

        protocol = ""
        if full_url.startswith(https):
            protocol = https
        elif full_url.startswith(http):
            protocol = http

        url = full_url
        if protocol:
            url = full_url.replace(protocol, "")

        self.driver.get(f"{protocol}{username}:{password}@{url}")

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    def open_new_tab(self, url: str):
        self.switch_to_last_window()
        self.driver.switch_to.new_window("tab")
        self.driver.get(url)

    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def current_window_handle(self) -> str:
        return self.driver.current_window_handle

    @property
    def window_handles(self) -> typing.List[str]:
        return self.driver.window_handles

    @property
    def num_of_windows(self) -> int:
        return len(self.window_handles)

    @property
    def page_source(self) -> str:
        return self.driver.page_source

    def does_current_url_contains(self, content: str, *, wait_for: int = 10) -> bool:
        try:
            return WebDriverWait(self.driver, wait_for).until(EC.url_contains(content))
        except selenium_exceptions.TimeoutException:
            return False

    def does_current_url_matches(self, pattern: str, *, wait_for: int = 10) -> bool:
        try:
            return WebDriverWait(self.driver, wait_for).until(EC.url_matches(pattern))
        except selenium_exceptions.TimeoutException:
            return False

    def does_url_equals(self, url: str, *, wait_for: int = 10) -> bool:
        try:
            return WebDriverWait(self.driver, wait_for).until(EC.url_to_be(url))
        except selenium_exceptions.TimeoutException:
            return False

    def does_url_not_equals(self, url: str, *, wait_for: int = 10) -> bool:
        try:
            return WebDriverWait(self.driver, wait_for).until(EC.url_changes(url))
        except selenium_exceptions.TimeoutException:
            return False

    def does_title_equals(self, title: str, *, wait_for: int = 10) -> bool:
        try:
            return WebDriverWait(self.driver, wait_for).until(EC.title_is(title))
        except selenium_exceptions.TimeoutException:
            return False

    def does_title_contains(self, content: str, *, wait_for: int = 10) -> bool:
        try:
            return WebDriverWait(self.driver, wait_for).until(
                EC.title_contains(content)
            )
        except selenium_exceptions.TimeoutException:
            return False

    def one_page_backward(self):
        self.driver.back()

    def one_page_forward(self):
        self.driver.forward()

    def refresh_page(self):
        self.driver.refresh()

    def add_cookie(self, cookie_name: str, cookie_value: str, **optional_cookie_kwargs):
        cookie_dict = {"name": cookie_name, "value": cookie_value}
        cookie_dict |= optional_cookie_kwargs
        self.driver.add_cookie(cookie_dict)

    def get_cookie(self, cookie_name: str) -> typing.Union[dict, None]:
        return self.driver.get_cookie(cookie_name)

    def cookie_name(self, cookie_name: str) -> str:
        cookie_dict = self.get_cookie(cookie_name)
        return cookie_dict.get("name", "")

    def cookie_value(self, cookie_name: str) -> str:
        cookie_dict = self.get_cookie(cookie_name)
        return cookie_dict.get("value", "")

    def get_all_cookies(self) -> typing.List[dict]:
        return self.driver.get_cookies()

    def delete_cookie(self, cookie_name: str):
        self.driver.delete_cookie(cookie_name)

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    def switch_context_to_default_content(self):
        self.driver.switch_to.default_content()

    def create_and_switch_to_new_window(self, window_name: str) -> str:
        self.driver.switch_to.new_window(window_name)
        return self.current_window_handle

    def switch_to_known_window(self, window_handle_or_name: str):
        self.driver.switch_to.window(window_handle_or_name)

    def switch_to_window_by_position(self, position: int):
        # position starts at 1 - rationale: first window, second window, etc.
        windows = self.window_handles
        if self.driver.capabilities["browserName"].lower() == "safari":
            windows = windows[::-1]
        num_windows = len(windows)
        position = num_windows if position == -1 else position
        # pre-requisite: position should be within the range of available windows
        assert (
            1 <= position <= num_windows
        ), f"Invalid Position provided. Please provide value from 1 to {num_windows} (number of windows)"

        self.switch_to_known_window(windows[position - 1])

    def switch_to_last_window(self):
        self.switch_to_window_by_position(-1)

    def quit_driver_session(self):
        self.driver.quit()

    def close_active_window(self):
        self.driver.close()

    def close_window_by_position(self, pos: int):
        self.switch_to_window_by_position(pos)
        self.close_active_window()

    def close_last_window(self):
        self.close_window_by_position(-1)

    def close_window_by_url(self, url: str):
        self.switch_tab_by_url(url)
        self.close_active_window()

    def window_size(self) -> WindowSize:
        size = self.driver.get_window_size()
        return WindowSize(size.get("width"), size.get("height"))

    def set_window_size(self, window_size: WindowSize):
        if not isinstance(window_size, WindowSize):
            raise TypeError(
                "Expecting an argument of type WindowSize. Ex:- WindowSize(1024, 800)"
            )
        self.driver.set_window_size(*window_size)

    def window_position(self) -> WindowPosition:
        pos = self.driver.get_window_position()
        return WindowPosition(pos.get("x"), pos.get("y"))

    def set_window_position(self, window_position: WindowPosition):
        if not isinstance(window_position, WindowPosition):
            raise TypeError(
                "Expecting an argument of type WindowPosition. Ex:- WindowPosition(0, 0)"
            )
        self.driver.set_window_size(*window_position)

    def maximize_window(self):
        self.driver.maximize_window()

    def minimize_window(self):
        self.driver.minimize_window()

    def set_fullscreen_window(self):
        self.driver.fullscreen_window()

    def capture_screenshot(self, file_path_to_save: Path) -> Path:
        if not isinstance(file_path_to_save, Path):
            raise TypeError("Pass a valid Path argument.")
        is_saved = self.driver.save_screenshot(str(file_path_to_save))
        if not is_saved:
            raise IOError(f"There was error saving screenshot to {file_path_to_save}")
        return file_path_to_save

    @property
    def page_size(self):
        pagesize = {
            "height": self.driver.execute_script("return document.body.offsetHeight"),
            "width": self.driver.execute_script("return document.body.offsetWidth"),
        }
        logger.info(
            "page size is: height = %s, width = %s"
            % (str(pagesize["height"]), str(pagesize["width"]))
        )
        return pagesize

    def full_screenshot(self, file_path_to_save: Path, scroll_delay: float):
        device_pixel_ratio = self.driver.execute_script('return window.devicePixelRatio')

        total_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
        viewport_height = self.driver.execute_script('return window.innerHeight')
        total_width = self.driver.execute_script('return document.body.offsetWidth')
        viewport_width = self.driver.execute_script("return document.body.clientWidth")

        # this implementation assume (viewport_width == total_width)
        assert (viewport_width == total_width)

        # scroll the page, take screenshots and save screenshots to slices
        offset = 0  # height
        slices = {}
        while offset < total_height:
            if offset + viewport_height > total_height:
                offset = total_height - viewport_height

            self.driver.execute_script('window.scrollTo({0}, {1})'.format(0, offset))
            time.sleep(scroll_delay)

            img = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
            slices[offset] = img

            offset = offset + viewport_height

        # combine image slices
        stitched_image = Image.new('RGB', (total_width * device_pixel_ratio, total_height * device_pixel_ratio))
        for offset, image in slices.items():
            stitched_image.paste(image, (0, offset * device_pixel_ratio))
        stitched_image.save(file_path_to_save)
