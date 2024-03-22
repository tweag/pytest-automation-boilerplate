"""
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
"""
import random
import time
import structlog

from datetime import datetime, timedelta
from pytest_bdd import parsers, given, when
from main.frontend.common.helpers.app import context_manager
from main.frontend.common.helpers.selenium_generics import SeleniumGenerics
from main.frontend.common.step_definitions.steps_common import MOBILE_SUFFIX
from main.frontend.common.utils.locator_parser import Locators

logger = structlog.get_logger(__name__)


# WEB context Predefined Step
# ID 1001
@given(parsers.re("I pause for '(?P<seconds>.*)' s"), converters=dict(seconds=int))
@when(parsers.re("I pause for '(?P<seconds>.*)' s"), converters=dict(seconds=int))
def pause_execution(seconds: int):
    time.sleep(seconds)


# WEB & MOBILE contexts Predefined Step
# ID 1002
@given(parsers.re(r"I add current date to '(?P<locator_path>.*)' with '(?P<date_format>MM/dd/yyyy|MM/dd/yy|dd/MM/yyyy|dd/MM/yy|dd MMM yyyy)'"))
@when(parsers.re(r"I add current date to '(?P<locator_path>.*)' with '(?P<date_format>MM/dd/yyyy|MM/dd/yy|dd/MM/yyyy|dd/MM/yy|dd MMM yyyy)'"))
def add_current_date_for_element(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, date_format: str):
    if date_format == "MM/dd/yyyy":
        date_text = datetime.now().date().strftime("%m/%d/%Y")
    elif date_format == "MM/dd/yy":
        date_text = datetime.now().date().strftime("%m/%d/%y")
    elif date_format == "dd/MM/yyyy":
        date_text = datetime.now().date().strftime("%d/%m/%Y")
    elif date_format == "dd/MM/yy":
        date_text = datetime.now().date().strftime("%d/%m/%y")
    elif date_format == "dd MMM yyyy":
        date_text = datetime.now().date().strftime("%d %b %Y")
    else:
        raise ValueError(f"Date format: {date_format} is invalid")
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), date_text)
    else:
        selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), date_text)


# WEB & MOBILE contexts Predefined Step
# ID 1003
@given(parsers.re(r"I add random '(?P<direction>future|past)' date to '(?P<locator_path>.*)' with '(?P<date_format>MM/dd/yyyy|MM/dd/yy|dd/MM/yyyy|dd/MM/yy|dd MMM yyyy)' format"))
@when(parsers.re(r"I add random '(?P<direction>future|past)' date to '(?P<locator_path>.*)' with '(?P<date_format>MM/dd/yyyy|MM/dd/yy|dd/MM/yyyy|dd/MM/yy|dd MMM yyyy)' format"))
def add_custom_date_for_element(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, date_format: str, direction: str):
    now = datetime.now()
    delta = timedelta(days=random.SystemRandom().randint(1, 365 * 20))
    if direction == "future":
        random_date = now + delta
    elif direction == "past":
        random_date = now - delta
    else:
        raise ValueError(f"Time direction: {direction} is invalid")

    if date_format == "MM/dd/yyyy":
        date_text = random_date.strftime("%m/%d/%Y")
    elif date_format == "MM/dd/yy":
        date_text = random_date.strftime("%m/%d/%y")
    elif date_format == "dd/MM/yyyy":
        date_text = random_date.strftime("%d/%m/%Y")
    elif date_format == "dd/MM/yy":
        date_text = random_date.strftime("%d/%m/%y")
    elif date_format == "dd MMM yyyy":
        date_text = random_date.strftime("%d %b %Y")
    else:
        raise ValueError(f"Date format: {date_format} is invalid")
    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), date_text)
    else:
        selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), date_text)


# WEB & MOBILE contexts Predefined Step
# ID 1004
@given(parsers.re(r"I add '(?P<direction>Past|Current|Future)' time to '(?P<locator_path>.*)' with '(?P<time_format>HH:MM:SS|HH:MM)' format(\s+)?((?:and clock format)\s+(?:')(?P<clock_format>\w+)(?:'))?(\s+)?((?:and delimiter)\s+(?:')(?P<delimiter>.*)(?:'))?$"))
@when(parsers.re(r"I add '(?P<direction>Past|Current|Future)' time to '(?P<locator_path>.*)' with '(?P<time_format>HH:MM:SS|HH:MM)' format(\s+)?((?:and clock format)\s+(?:')(?P<clock_format>\w+)(?:'))?(\s+)?((?:and delimiter)\s+(?:')(?P<delimiter>.*)(?:'))?$"))
def add_custom_time_for_element(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, time_format: str, direction: str, delimiter: str, clock_format: str):
    delimiter = delimiter if delimiter else ":"
    clock_format = clock_format if clock_format else "24h"
    now = datetime.now()
    _from = now - now.replace(hour=0, minute=0, second=0, microsecond=0)
    _to = now.replace(hour=23, minute=59, second=59, microsecond=0) - now
    if clock_format == "24h":
        cf = "%H"
    elif clock_format == "12h":
        cf = "%I"
    else:
        raise ValueError(f"Clock format: {clock_format} is invalid")

    if direction == "Future":
        random_seconds = random.SystemRandom().randint(1, _to.seconds)
        delta = timedelta(seconds=random_seconds)
        future_date = now + delta
        _time = future_date
    elif direction == "Past":
        random_seconds = random.SystemRandom().randint(1, _from.seconds)
        delta = timedelta(seconds=random_seconds)
        past_date = now - delta
        _time = past_date
    elif direction == "Current":
        _time = now
    else:
        raise ValueError(f"Time direction: {direction} is invalid")

    if time_format == "HH:MM:SS":
        time_text = _time.strftime(f"{cf}{delimiter}%M{delimiter}%S")
    elif time_format == "HH:MM":
        time_text = _time.strftime(f"{cf}{delimiter}%M")
    else:
        raise ValueError(f"Time format: {time_format} is invalid")

    if MOBILE_SUFFIX in locator_path:
        with context_manager(selenium_generics):
            selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), time_text)
    else:
        selenium_generics.enter_text(locators.parse_and_get(locator_path, selenium_generics), time_text)
