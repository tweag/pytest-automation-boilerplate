import typing
import warnings
from collections import UserList, namedtuple
from enum import Enum

from main.utils.exceptions import LocatorException

WindowSize = namedtuple("WindowSize", "width height")
WindowPosition = namedtuple("WindowPosition", "x y")


class ValidLocatorTypes(Enum):
    ID = "ID"
    XP = "XP"
    TN = "TP"
    NM = "NM"
    CN = "CN"
    CS = "CS"
    LT = "LT"
    PL = "PL"


class Locator:
    def __init__(self, type: ValidLocatorTypes, identifier: str):
        self.type = type
        self.identifier = identifier

    def __repr__(self):
        return f"Locator(type={self.type}, identifier={self.identifier})"

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, loc_type):
        if isinstance(loc_type, str):
            if loc_type.upper() not in (
                valid_locator_types := ValidLocatorTypes._member_names_
            ):
                raise LocatorException(
                    f"Provided Invalid locator type: {loc_type}. Valid Locator Types: {valid_locator_types}"
                )
            self._type = getattr(ValidLocatorTypes, loc_type.upper())
        elif isinstance(loc_type, ValidLocatorTypes):
            self._type = loc_type
        else:
            raise LocatorException(
                f"Provided Invalid locator type: {loc_type}. Valid Locator Types: {ValidLocatorTypes._member_map_}"
            )


class ShadowLocator(UserList):
    def __init__(self, locator: typing.List[Locator]):
        self.locator = locator
        self.__check()
        super().__init__(locator)

    def __repr__(self):
        return " -> ".join(map(str, self.locator))

    @staticmethod
    def update_id(locator: Locator, _: int):
        locator.type = "CS"
        locator.identifier = f"#{locator.identifier}"

    @staticmethod
    def update_class(locator: Locator, _: int):
        locator.type = "CS"
        locator.identifier = f".{locator.identifier}"

    @staticmethod
    def update_tag(locator: Locator, _: int):
        locator.type = "CS"

    @staticmethod
    def update_name(locator: Locator, _: int):
        locator.type = "CS"
        locator.identifier = f"*[name={locator.identifier}]"

    def raise_error_invalid_types(self, locator: Locator, ind: int):
        if ind == 0 and locator.type == ValidLocatorTypes.XP:
            warnings.warn(
                "For accessing Shadow Elements, it is recommended to use CSS Selector, in place of Xpath. Using XPath for Shadow Elements is in path of deprecation. Will be deprecated in BP_v3.6 and removed in BP_v3.8",
                PendingDeprecationWarning,
            )
        else:
            raise TypeError(
                f"Locator Type: {locator.type} is invalid for {self.__class__.__name__}. Please use CSS Selectors"
            )

    def __check(self):
        dispatcher = {
            ValidLocatorTypes.ID: self.update_id,
            ValidLocatorTypes.CN: self.update_class,
            ValidLocatorTypes.TN: self.update_tag,
            ValidLocatorTypes.NM: self.update_name,
            ValidLocatorTypes.XP: self.raise_error_invalid_types,
            ValidLocatorTypes.LT: self.raise_error_invalid_types,
            ValidLocatorTypes.PL: self.raise_error_invalid_types,
            ValidLocatorTypes.CS: lambda x, _: x,
        }
        for ind, locator in enumerate(self.locator):
            if not isinstance(locator, Locator):
                raise TypeError(
                    f"All elements of {self.__class__.__name__} should be of type Locator."
                )
            dispatcher[locator.type](locator, ind)
