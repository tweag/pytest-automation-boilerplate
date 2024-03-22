"""
Description
"""
from __future__ import annotations

from . import _category
from ._exception import TestRailConfigurationError
from ._session import Session


def validate_setup(tr: TestRailAPI, project_id):
    if not project_id:
        TestRailConfigurationError(
            f"Project ID must be set. Invalid value {project_id}"
        )


class TestRailAPI(Session):
    """API reference: https://support.testrail.com/hc/en-us/sections/7077185274644-API-reference"""

    @property
    def cases(self):
        return _category.Cases(self)

    @property
    def case_fields(self):
        return _category.CaseFields(self)

    @property
    def case_types(self):
        return _category.CaseTypes(self)

    @property
    def configurations(self):
        return _category.Configurations(self)

    @property
    def milestones(self):
        return _category.Milestones(self)

    @property
    def plans(self):
        return _category.Plans(self)

    @property
    def priorities(self):
        return _category.Priorities(self)

    @property
    def projects(self):
        return _category.Projects(self)

    @property
    def results(self):
        return _category.Results(self)

    @property
    def result_fields(self):
        return _category.ResultFields(self)

    @property
    def runs(self):
        return _category.Runs(self)

    @property
    def sections(self):
        return _category.Sections(self)

    @property
    def statuses(self):
        return _category.Statuses(self)

    @property
    def suites(self):
        return _category.Suites(self)

    @property
    def templates(self):
        return _category.Templates(self)

    @property
    def tests(self):
        return _category.Tests(self)

    @property
    def users(self):
        return _category.Users(self)

    @property
    def attachments(self) -> _category.Attachments:
        return _category.Attachments(self)
