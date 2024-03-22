import json
import os
import re
import typing
from collections import deque
from glob import glob
from pathlib import Path
import structlog

from main.frontend.common.utils.containers import Locator, ShadowLocator, ValidLocatorTypes
from main.utils.exceptions import LocatorException

logger = structlog.get_logger(__name__)

__all__ = ["parse_locator", "Locators"]


def _parse_locator_string(
    locator_string: str, default_loc_type=ValidLocatorTypes.XP
) -> Locator:
    if (
        match := re.match("^[(XP|TN|ID|CS|CN|NM|LT|PL)](.+)$", locator_string)
    ) is not None:
        type_ = getattr(ValidLocatorTypes, match.groups()[0])
        identifier = match.groups()[1]
        return Locator(type_, identifier)
    return Locator(default_loc_type, locator_string)


def _parse_shadow_locator_string(
    shadow_locator_string: str, delimiter: str = " ~ "
) -> ShadowLocator:
    locators = []
    for ind, i in enumerate(shadow_locator_string.split(delimiter)):
        default_loc_type = ValidLocatorTypes.XP if ind == 0 else ValidLocatorTypes.CS
        locators.append(_parse_locator_string(i, default_loc_type=default_loc_type))
    return ShadowLocator(locators)


def parse_locator(
    locator: str, shadow_loc_delimiter: str = " ~ "
) -> typing.Union[Locator, ShadowLocator]:
    is_shadow_loc = shadow_loc_delimiter in locator
    if is_shadow_loc:
        return _parse_shadow_locator_string(locator, shadow_loc_delimiter)
    return _parse_locator_string(locator)


class Locators:
    def __init__(
        self,
        locators_base_path: typing.Union[str, None] = None,
        delimiter: str = " > ",
        locale: str = "en_US",
    ):
        self.locators_base_path = locators_base_path
        self.locators_files = self.get_locator_files()
        self.loaded_locators = self.load_locators()
        self.delimiter = delimiter
        self.locale: str = locale

    @staticmethod
    def _load_data_file(file_path: str):
        if file_path.endswith(".json"):
            with open(file_path, "r", encoding='utf-8') as jf:
                try:
                    return json.load(jf)
                except json.JSONDecodeError:
                    return dict()
        else:
            return dict()

    def get_locator_files(self):
        ls_folder_path = []
        locator_files = []

        if self.locators_base_path is None:
            self.locators_base_path = os.getcwd()
            ls_folder_path.extend(glob(self.locators_base_path + "/**/locators", recursive=True))
        elif not Path(self.locators_base_path).exists():
            raise LocatorException(
                f"Locator file/folder '{self.locators_base_path}' not found. Exiting")
        elif os.path.isdir(self.locators_base_path):
            ls_folder_path.append(self.locators_base_path)
        elif os.path.isfile(self.locators_base_path):
            locator_files.append(self.locators_base_path)
            return locator_files

        for folder_path in ls_folder_path:
            for subdir, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(subdir, file)
                    locator_files.append(file_path)

        return locator_files

    def load_locators(self):
        locator_dict = dict()
        for file in self.locators_files:
            locator_dict.update(self._load_data_file(file))
        if not locator_dict:
            raise LocatorException("Locator Files Empty!!!")
        return locator_dict

    @staticmethod
    def _get_locale_based_locator(locators: dict, locale: str):
        if isinstance(locators, dict) and locale in locators:
            locators = locators[locale]
        return locators

    def parse_and_get(self, locator_key: str, selenium_generics):
        if "_os_locator" in locator_key:
            locator_key = f"{locator_key.split('_os_locator')[0]}{'_android'}" if selenium_generics.is_android() else \
                f"{locator_key.split('_os_locator')[0]}{'_ios'}"
        key_hier = deque(locator_key.split(self.delimiter))
        loc = self.loaded_locators.get(key_hier.popleft())
        while key_hier:
            loc = self._get_locale_based_locator(loc, self.locale)
            loc = loc.get(key_hier.popleft())
        loc = self._get_locale_based_locator(loc, self.locale)
        return loc

    @staticmethod
    def get_radio_option_from_parent(option_attribute, text, parent_attribute, value):
        return f"//*[@{parent_attribute}='{value}']//*[@{option_attribute}='{str(text)}']"

    @staticmethod
    def get_element_by_attribute(attribute, value):
        return f"//*[@{str(attribute)}='{str(value)}']"

    @staticmethod
    def get_element_by_text(value: str, visibility_option: str = "EQUALS"):
        if visibility_option == "EQUALS":
            return f"//*[text()='{value}']"
        elif visibility_option == "CONTAINS":
            return f'//*[contains(text(), "{value}")]'
        elif visibility_option == "STARTS_WITH":
            return f'//*[starts-with(text(),"{value}")]'
        elif visibility_option == "ENDS_WITH":
            # ends-with() only supported in XPath 2.0. Using substring for backward compatibility with XPath 1.0
            return f'//*[substring(text(), string-length(text()) - string-length("{value}") + 1) = "{value}"]'
        else:
            raise ValueError(f"No such option: {visibility_option}")

    @staticmethod
    def get_searchable_dropdown_by_visible_text(value: str, attr: str = "*"):
        return f'//{attr}[normalize-space()="{value}"]//following::input[1]'

    @staticmethod
    def get_select_element_by_parent_label(label: str):
        return f"//*[normalize-space()='{label}']//following::select[1]"

    @staticmethod
    def get_dropdown_option(placeholder: str):
        return f"//option[text()='{placeholder}']/.."
