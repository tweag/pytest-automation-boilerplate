"""
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
"""
import time
import structlog
import re

from datetime import datetime, timedelta
from pytest_bdd import parsers, given, when
from bp_core.frontend.common.helpers.app import context_manager
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from bp_core.frontend.common.helpers.selenium_generics import SeleniumGenerics
from bp_core.frontend.common.step_definitions.steps_common import MOBILE_SUFFIX
from bp_core.frontend.common.utils.locator_parser import Locators
from bp_core.utils import data_manager
from bp_core.utils.exceptions import YearAscendingException

logger = structlog.get_logger(__name__)


# WEB context Predefined Step
# ID 1301
@given(parsers.re("(On '(?P<mobile_platform>Android|iOS)' )?I click on element with text '(?P<element_text>.*)' on wheel picker '(?P<locator_path>.*)'"),
      converters=dict(element_text=data_manager.text_formatted),)
@when(parsers.re("(On '(?P<mobile_platform>Android|iOS)' )?I click on element with text '(?P<element_text>.*)' on wheel picker '(?P<locator_path>.*)'"),
      converters=dict(element_text=data_manager.text_formatted),)
def click_on_wheel_picker_element(selenium_generics: SeleniumGenerics, locators: Locators, locator_path: str, element_text: str, mobile_platform: str):
    current_platform = selenium_generics.driver.capabilities['platformName'].lower()
    mobile_platform = mobile_platform.lower() if mobile_platform else current_platform
    picker_elements = selenium_generics.get_elements(locators.parse_and_get(locator_path, selenium_generics))

    def get_currently_displayed_elements(elements, starting_from, direction):
        elements_ = elements[starting_from::-1] if direction else elements[starting_from:]
        is_displayed = False
        result = dict()
        for idx, element in enumerate(elements_):
            if element.is_displayed():
                is_displayed = True
                result[idx] = element
            else:
                if is_displayed:
                    break
        keys = list(result.keys())
        keys.sort()
        new_first_displayed_element = starting_from - keys[-1] if direction else keys[0] + starting_from
        sorted_displayed_elements = {k: result[k] for k in keys}
        return sorted_displayed_elements, new_first_displayed_element

    def try_to_click_on_the_element(elements, text):
        for index in elements.keys():
            if displayed_elements[index].text == text:
                selenium_generics.click(displayed_elements[index], max_wait_time=1)
                return True
        return False

    if current_platform == mobile_platform.lower():
        first_displayed_element = 0
        reverse = False
        for _ in range(len(picker_elements)):
            displayed_elements, first_displayed_element = get_currently_displayed_elements(picker_elements, first_displayed_element, reverse)
            highest_key = max(displayed_elements.keys())
            if try_to_click_on_the_element(elements=displayed_elements, text=element_text):
                return
            try:
                displayed_elements[highest_key].click()
            except ElementNotVisibleException:
                continue
        # If the element is not found we search the other direction
        else:
            first_displayed_element = len(picker_elements)
            reverse = True
            for _ in range(len(picker_elements)):
                displayed_elements, first_displayed_element = get_currently_displayed_elements(picker_elements, first_displayed_element, reverse)
                highest_key = max(displayed_elements.keys())
                if try_to_click_on_the_element(elements=displayed_elements, text=element_text):
                    return
                try:
                    displayed_elements[highest_key].click()
                except ElementNotVisibleException:
                    continue
        raise NoSuchElementException(f"Wheel picker element with text: {element_text} not found")


# ID 1302
@given(parsers.re(r"On Android I select (?:the day '(?P<day>.*)' month '(?P<month>.*)' year '(?P<year>.*)'|the date '(?P<days_from_now>.*)' days from now) on Ionic date wheel picker with days '(?P<days_path>.*)' months '(?P<months_path>.*)' years '(?P<years_path>.*)'"))
@when(parsers.re(r"On Android I select (?:the day '(?P<day>.*)' month '(?P<month>.*)' year '(?P<year>.*)'|the date '(?P<days_from_now>.*)' days from now) on Ionic date wheel picker with days '(?P<days_path>.*)' months '(?P<months_path>.*)' years '(?P<years_path>.*)'"))
def click_on_android_date_wheel_picker_element(selenium_generics: SeleniumGenerics, locators: Locators, days_path, months_path, years_path, days_from_now=None, day=None, month=None, year=None):
    if selenium_generics.is_android():
        days_elements = locators.parse_and_get(days_path, selenium_generics)
        months_elements = locators.parse_and_get(months_path, selenium_generics)
        years_elements = locators.parse_and_get(years_path, selenium_generics)

        months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
                  9: "September", 10: "October", 11: "November", 12: "December"}

        def get_current_month_name(given_month: int):
            return next((name_ for month_, name_ in months.items() if month_ == given_month), None)

        if days_from_now:
            days_from_now = int(days_from_now)
            current_date = datetime.now()
            new_date = current_date + timedelta(days=days_from_now)
            day = str(new_date.day)
            month = get_current_month_name(new_date.month)
            year = str(new_date.year)

        def element_generator():
            element_locators = [years_elements, months_elements, days_elements]
            for element_locator in element_locators:
                yield get_elements(element_locator)

        def get_elements(locator_):
            elements = selenium_generics.get_elements(locator_)
            for _ in range(3):
                time.sleep(3)
                if elements == selenium_generics.get_elements(locator_):
                    break
                elements = selenium_generics.get_elements(locator_)
            return elements

        def get_currently_displayed_elements(elements, starting_from, direction):
            elements_ = elements[starting_from::-1] if direction else elements[starting_from:]
            is_displayed = False
            result = dict()
            for idx, element in enumerate(elements_):
                if element.is_displayed():
                    is_displayed = True
                    result[idx] = element
                else:
                    if is_displayed:
                        break
            keys = list(result.keys())
            keys.sort()
            new_first_displayed_element = starting_from - keys[-1] if direction else keys[0] + starting_from
            sorted_displayed_elements = {k: result[k] for k in keys}
            return sorted_displayed_elements, new_first_displayed_element

        def try_to_click_on_the_element(elements, text):
            for index in elements.keys():
                if displayed_elements[index].text == text:
                    try:
                        selenium_generics.click(displayed_elements[index], max_wait_time=1)
                        return True
                    except Exception:
                        selenium_generics.scroll_into_view(displayed_elements[index])
                        selenium_generics.click(displayed_elements[index], max_wait_time=1)
                        return True
            return False

        first_displayed_element = 0
        reverse, clicked = False, False
        element_iterator = element_generator()
        for date_part, element_text in zip(element_iterator, (year, month, day)):
            for _ in range(len(date_part)):
                displayed_elements, first_displayed_element = get_currently_displayed_elements(date_part, first_displayed_element, reverse)
                highest_key = max(displayed_elements.keys())
                if try_to_click_on_the_element(elements=displayed_elements, text=element_text):
                    clicked = True
                    break
                try:
                    displayed_elements[highest_key].click()
                    clicked = False
                except ElementNotVisibleException:
                    continue
        if not clicked:
            for date_part, element_text in zip((years_elements, months_elements, days_elements), (year, month, day)):
                first_displayed_element = len(date_part)
                reverse = True
                for _ in range(len(date_part)):
                    displayed_elements, first_displayed_element = get_currently_displayed_elements(date_part, first_displayed_element, reverse)
                    highest_key = max(displayed_elements.keys())
                    if try_to_click_on_the_element(elements=displayed_elements, text=element_text):
                        clicked = True
                        break
                    try:
                        displayed_elements[highest_key].click()
                        clicked = False
                    except ElementNotVisibleException:
                        continue
                if not clicked:
                    raise NoSuchElementException(f"Wheel picker element with text: {element_text} not found")


# ID 1303
@given(parsers.re(r"On iOS I select (?:the day '(?P<day>.*)' month '(?P<month>.*)' year '(?P<year>.*)'|the date '(?P<days_from_now>.*)' days from now) on Ionic date wheel picker '(?P<locator_path>.*)'"))
@when(parsers.re(r"On iOS I select (?:the day '(?P<day>.*)' month '(?P<month>.*)' year '(?P<year>.*)'|the date '(?P<days_from_now>.*)' days from now) on Ionic date wheel picker '(?P<locator_path>.*)'"))
def click_on_ios_date_wheel_picker_element_native(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, days_from_now=None, day=None,  month=None, year=None):
    if selenium_generics.driver.capabilities['platformName'].lower() == 'ios':
        current_day, current_month, current_year = datetime.now().day, datetime.now().month, datetime.now().year
        months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
                  9: "September", 10: "October", 11: "November", 12: "December"}

        def identify_pattern(data):
            year_pattern = re.compile(r"^\d{4}$")
            day_pattern = re.compile(r"^(0?[1-9]|[1-2]\d|3[0-1])$")
            if year_pattern.match(data):
                return "year", f"{year}"
            elif day_pattern.match(data):
                return "day", f"{day}"
            elif not data.isnumeric():
                return "month", f"{month}"
            else:
                raise ValueError(f"Unrecognized element text: {data}")

        def is_year_ascending(elements, types):
            results = identify_current_date_elements(elements, types)
            for key, value in results.items():
                if value[0] == 'year':
                    before, after = None, None
                    try:
                        before = elements[key - 1]
                        if identify_pattern(before.text)[0] != "year":
                            before = None
                            raise YearAscendingException
                    except YearAscendingException:
                        after = elements[key + 1]
                    if before:
                        if int(before.text) > int(elements[key].text):
                            return False
                        return True
                    elif after:
                        if int(after.text) > int(elements[key].text):
                            return True
                        return False

        def get_current_month_name(given_month: int):
            return next((name_ for month_, name_ in months.items() if month_ == given_month), None)

        def is_later(date_part, order=None):
            result = True
            if date_part[0] == 'month':
                given_month_number = next((month_ for month_, name_ in months.items() if name_ == date_part[1]), None)
                if given_month_number is None:
                    raise ValueError(f"Bad month value: {given_month_number}")
                elif given_month_number < current_month:
                    result = False
            elif date_part[0] == 'year':
                if order:
                    if int(date_part[1]) < current_year:
                        result = False
                else:
                    if int(date_part[1]) > current_year:
                        result = False
            elif date_part[0] == 'day' and int(date_part[1]) < current_day:
                result = False
            return result

        def identify_current_date_elements(elements, types):
            results = dict()
            for idx, e in enumerate(elements):
                if e.text in (str(current_day), get_current_month_name(current_month), str(current_year)):
                    _type = identify_pattern(e.text)[0]
                    if _type in types:
                        results[idx] = identify_pattern(e.text)
            return results

        def find_elements(locator, max_attempts=3):
            counter = 0
            while counter < max_attempts:
                result = selenium_generics.get_elements(locator)
                if result:
                    return result
                time.sleep(5)
                counter += 1
            raise NoSuchElementException(f"Elements with locator: {locator} not found")

        if days_from_now:
            days_from_now = int(days_from_now)
            current_date = datetime.now()
            new_date = current_date + timedelta(days=days_from_now)
            day = new_date.day
            month = get_current_month_name(new_date.month)
            year = new_date.year

        if MOBILE_SUFFIX in locator_path:
            with context_manager(selenium_generics):
                types_ = ["day", "month", "year"]
                if all(date_part is not None for date_part in (day, month, year)):
                    for i in range(3):
                        picker_elements = find_elements(locators.parse_and_get(locator_path, selenium_generics))
                        current_elements = identify_current_date_elements(picker_elements, types_)
                        year_order = is_year_ascending(picker_elements, ["year",])
                        key, value = list(current_elements.keys())[0], current_elements[list(current_elements.keys())[0]]
                        if is_later(value, year_order):
                            _elements = picker_elements[key:]
                        else:
                            _elements = picker_elements[:key + 1][::-1]
                        for element in _elements:
                            element_match = element.text == identify_pattern(element.text)[1]
                            selenium_generics.click(element)
                            time.sleep(2)  # Additional wait time once there is a transition in the elements after the click
                            if element_match:
                                types_.remove(identify_pattern(element.text)[0])
                                break
                else:
                    raise ValueError(f"Expected to have all values: day {day}, month: {month}, year: {year}")


# ID 1304
@given(parsers.re(r"On Android I select (?:the hour '(?P<hour>.*)' minute '(?P<minute>.*)' in time period '(?P<time_period>.*)'|the time '(?P<minutes_from_now>.*)' minutes from now) on Ionic time wheel picker with minutes '(?P<minutes_path>.*)' hours '(?P<hours_path>.*)' time period '(?P<time_period_path>.*)'"))
@when(parsers.re(r"On Android I select (?:the hour '(?P<hour>.*)' minute '(?P<minute>.*)' in time period '(?P<time_period>.*)'|the time '(?P<minutes_from_now>.*)' minutes from now) on Ionic time wheel picker with minutes '(?P<minutes_path>.*)' hours '(?P<hours_path>.*)' time period '(?P<time_period_path>.*)'"))
def click_on_android_time_wheel_picker_element(selenium_generics: SeleniumGenerics, locators: Locators, minutes_path, hours_path, time_period_path, minutes_from_now=None, hour=None, minute=None, time_period=None):
    if selenium_generics.is_android():
        minutes_elements = locators.parse_and_get(minutes_path, selenium_generics)
        hours_elements = locators.parse_and_get(hours_path, selenium_generics)
        time_period_elements = locators.parse_and_get(time_period_path, selenium_generics)

        def convert_to_12h(hours_24h):
            if hours_24h == 0:
                return "12", "AM"
            elif 1 <= hours_24h <= 11:
                return str(hours_24h), "AM"
            elif hours_24h == 12:
                return "12", "PM"
            else:
                return str(hours_24h - 12), "PM"

        if minutes_from_now:
            minutes_from_now = int(minutes_from_now)
            current_date = datetime.now()
            new_date = current_date + timedelta(minutes=minutes_from_now)
            minute = str(new_date.minute)
            hour, time_period = convert_to_12h(new_date.hour)

        def get_elements(locator_):
            elements = selenium_generics.get_elements(locator_)
            for _ in range(3):
                time.sleep(3)
                if elements == selenium_generics.get_elements(locator_):
                    break
                elements = selenium_generics.get_elements(locator_)
            return elements

        hours = get_elements(hours_elements)
        for element in hours:
            if element.text == hour:
                try:
                    selenium_generics.click(element, max_wait_time=1)
                    break
                except Exception:
                    selenium_generics.scroll_into_view(element)
                    selenium_generics.click(element, max_wait_time=1)
                    break

        minutes = get_elements(minutes_elements)
        for element in minutes:
            if element.text == minute:
                try:
                    selenium_generics.click(element, max_wait_time=1)
                    break
                except Exception:
                    selenium_generics.scroll_into_view(element)
                    selenium_generics.click(element, max_wait_time=1)
                    break

        time_period_ = get_elements(time_period_elements)
        for element in time_period_:
            if element.text.lower() == time_period.lower():
                try:
                    selenium_generics.click(element, max_wait_time=1)
                    break
                except Exception:
                    selenium_generics.scroll_into_view(element)
                    selenium_generics.click(element, max_wait_time=1)
                    break


# ID 1305
@given(parsers.re(r"On iOS I select (?:the hour '(?P<hour>.*)' minute '(?P<minute>.*)' in time period '(?P<time_period>.*)'|the time '(?P<minutes_from_now>.*)' minutes from now) on Ionic time wheel picker '(?P<locator_path>.*)'"))
@when(parsers.re(r"On iOS I select (?:the hour '(?P<hour>.*)' minute '(?P<minute>.*)' in time period '(?P<time_period>.*)'|the time '(?P<minutes_from_now>.*)' minutes from now) on Ionic time wheel picker '(?P<locator_path>.*)'"))
def click_on_ios_time_wheel_picker_element_native(selenium_generics: SeleniumGenerics, locators: Locators, locator_path, minutes_from_now=None, hour=None,  minute=None, time_period=None):
    if selenium_generics.driver.capabilities['platformName'].lower() == 'ios':
        def convert_to_12h(hours_24h):
            if hours_24h == 0:
                return "12", "AM"
            elif 1 <= hours_24h <= 11:
                return str(hours_24h), "AM"
            elif hours_24h == 12:
                return "12", "PM"
            else:
                return str(hours_24h - 12), "PM"

        current_time = selenium_generics.driver.device_time
        timestamp_format = '%Y-%m-%dT%H:%M:%S%z'
        timestamp_datetime = datetime.strptime(current_time, timestamp_format)
        current_hour, current_minute = timestamp_datetime.hour, str(timestamp_datetime.minute)
        current_hour, current_time_period = convert_to_12h(current_hour)
        time_period = time_period if time_period else current_time_period

        def find_elements(locator, max_attempts=3):
            counter = 0
            while counter < max_attempts:
                result = selenium_generics.get_elements(locator)
                if result:
                    return result
                time.sleep(5)
                counter += 1
            raise NoSuchElementException(f"Elements with locator: {locator} not found")

        def identify_current_hour_index(elements):
            for idx, e in enumerate(elements):
                if e.text == str(current_hour):
                    return idx
            raise ElementNotVisibleException(f"Element with current hour: {current_hour} not found")

        def identify_current_minute_index(elements):
            for idx, e in enumerate(elements):
                if e.text == str(current_minute):
                    return idx
            raise ElementNotVisibleException(f"Element with current minute: {current_minute} not found")

        def click_on_the_element(elements_, expected_text):
            for e in elements_:
                if e.text == str(expected_text):
                    time.sleep(1)
                    e.click()
                    break
                if e.text == current_hour:
                    continue
                time.sleep(1)
                e.click()

        if minutes_from_now:
            minutes_from_now = int(minutes_from_now)
            new_date = timestamp_datetime + timedelta(minutes=minutes_from_now)
            minute = str(new_date.minute)
            hour, time_period = convert_to_12h(new_date.hour)
        if MOBILE_SUFFIX in locator_path:
            with context_manager(selenium_generics):
                hour_elements = find_elements(locators.parse_and_get(locator_path, selenium_generics))[:12]
                current_hour_index = identify_current_hour_index(hour_elements)
                if int(hour) == 12:
                    hour_elements_ = hour_elements[:current_hour_index + 1][::-1]
                    click_on_the_element(hour_elements_, hour)
                elif int(current_hour) > int(hour) and int(current_hour) != 12:
                    hour_elements_ = hour_elements[:current_hour_index + 1][::-1]
                    click_on_the_element(hour_elements_, hour)
                else:
                    hour_elements_ = hour_elements[current_hour_index:13]
                    click_on_the_element(hour_elements_, hour)

                minute_elements = find_elements(locators.parse_and_get(locator_path, selenium_generics))[12:72]
                current_minute_index = identify_current_minute_index(minute_elements)
                if int(current_minute) > int(minute):
                    minute_elements_ = minute_elements[:current_minute_index + 1][::-1]
                    click_on_the_element(minute_elements_, minute)
                else:
                    minute_elements_ = minute_elements[current_minute_index:72]
                    click_on_the_element(minute_elements_, minute)

                time_period_elements = find_elements(locators.parse_and_get(locator_path, selenium_generics))[72:74]
                click_on_the_element(time_period_elements, time_period)
