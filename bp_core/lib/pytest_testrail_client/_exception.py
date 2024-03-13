"""Exceptions"""


class TestRailError(Exception):
    """Base Exception"""


class TestRailConfigurationError(TestRailError):
    """Base API Exception"""


class TestRailAPIError(TestRailError):
    """Base API Exception"""


class StatusCodeError(TestRailAPIError):
    """Status code Exception"""
