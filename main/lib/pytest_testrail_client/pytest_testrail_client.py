from __future__ import print_function
import functools
import glob
import json
import operator
import os
from collections import defaultdict
from copy import deepcopy
from os import environ
from pathlib import Path
from typing import List, Dict

import pytest
import pytest_bdd.parser
import structlog

from main.lib.pytest_testrail_client.model.case import Case
from main.lib.pytest_testrail_client.model.plan import Entry
from main.lib.pytest_testrail_client.model.result import Result
from main.lib.pytest_testrail_client.model.section import Section
from main.lib.pytest_testrail_client.model.suite import Suite
from main.lib.pytest_testrail_client.testrail_api import TestRailAPI, validate_setup
from main.utils.bp_storage import BPStorage
from main.utils.utils import remove_chars_from_string, TEMP_SCREENSHOTS, remove_multiple_spaces

from ._exception import TestRailError
from ._utils import _get_feature, _get_list_of_files, _write_feature
from .model.run import Run

logger = structlog.get_logger(__name__)

SEPARATOR_CHAR = " - "
TESTRAIL_TAG_PREFIX = "@TR-C"
PYTEST_BDD_TAG_PREFIX = "TR-C"
DEFAULT_SECTION_NAME = "Default Section"
NOT_ALLOWED_CHARACTERS = ["/", "\\", '"', ":", "<", ">", "|", "*", "?", "#", "%", "{", "}", "$", "!", "'", "@", "=",
                          "+", "-", "(", ")"]


def pytest_configure(config):
    config.option.markexpr = "not not_in_scope"
    pytest.testrail_client_dict = defaultdict()


def pytest_addoption(parser):
    group = parser.getgroup("pytest-testrail-client")

    _help = "Enable plugin"
    group.addoption("--pytest-testrail-client", action="store_true", help=_help)
    parser.addini("pytest-testrail-client", type="bool", default=None, help=_help)

    _help = "TestRail address"
    group.addoption("--testrail-url", action="store", default=None, help=_help)
    parser.addini("testrail-url", default=None, help=_help)

    _help = "TestRail email"
    group.addoption("--testrail-email", action="store", default=None, help=_help)
    parser.addini("testrail-email", default=None, help=_help)

    _help = "TestRail key"
    group.addoption("--testrail-key", action="store", default=None, help=_help)
    parser.addini("testrail-key", default=None, help=_help)

    _help = "TestRail project_id"
    group.addoption("--testrail-project-id", action="store", default=None, help=_help)
    parser.addini("testrail-project-id", default=None, help=_help)

    group.addoption("--jira-project-key", action="store", default=None, help=_help)
    parser.addini("jira-project-key", default=None, help=_help)

    _help = "TestRail export test cases form given file or directory. No test will be executed"
    group.addoption(
        "--pytest-testrail-export-test-cases", action="store_true", help=_help
    )
    group.addoption(
        "--pytest-testrail-feature-files-relative-path",
        action="store",
        default=None,
        help=_help,
    )

    _help = "TestRail export test results"
    group.addoption(
        "--pytest-testrail-export-test-results", action="store_true", help=_help
    )

    _help = "TestRail test plan to export results"
    group.addoption(
        "--pytest-testrail-test-plan-id",
        action="store",
        type=int,
        default=None,
        help=_help,
    )

    _help = "TestRail test run name used for exporting results"
    group.addoption(
        "--pytest-testrail-test-run-name",
        action="store",
        default=None,
        help=_help,
    )
    _help = "TestRail test configuration used for testing"
    group.addoption(
        "--pytest-testrail-test-configuration-name",
        action="store",
        default=None,
        help=_help,
    )

    _help = "TestRail update test title"
    group.addoption(
        "--pytest-testrail-update-title", action="store_true", help=_help)

    _help = "TestRail skip exporting step level results"
    group.addoption(
        "--pytest-testrail-skip-step-results", action="store_true", help=_help)


def pytest_collection_modifyitems(config, items):
    if (
        "pytest_testrail_export_test_cases" in config.option
        and config.option.pytest_testrail_export_test_cases is True
    ):
        print("\nUn-select all tests. Exporting is selected")
        for item in items:
            item.add_marker(pytest.mark.not_in_scope)


def pytest_sessionstart(session):
    if (
        "pytest_testrail_export_test_results" in session.config.option
        and session.config.option.pytest_testrail_export_test_results is True
    ):
        pytest.testrail_client_dict["scenarios_run"] = {}

        tr, project_data = get_testrail_api(session.config)
        tr_configs = functools.reduce(
            operator.iconcat,
            [
                tr_cg["env_configs"]
                for tr_cg in tr.configurations.get_configs(project_data["project_id"])
            ],
        )
        project_data[
            "configuration_name"
        ] = session.config.option.pytest_testrail_test_configuration_name
        if project_data["configuration_name"] not in [
            tr_config["name"] for tr_config in tr_configs
        ]:
            TestRailError(
                f"Configuration {project_data['configuration_name']} not available. \n"
                f"Please use one of the following configurations or manually create a new one: "
                f"{[tr_config['name'] for tr_config in tr_configs]}"
            )


def pytest_sessionfinish(session):
    if (
        "pytest_testrail_export_test_cases" in session.config.option
        and session.config.option.pytest_testrail_export_test_cases is True
    ):
        print("Initialize TestRail client")
        absolute_path = f"{session.config.rootdir}/{session.config.option.pytest_testrail_feature_files_relative_path}"
        files_abs_path = _get_list_of_files(absolute_path)

        try:
            tr, project_data = get_testrail_api(session.config)
            for file_path in files_abs_path:
                feature = _get_feature(file_path)
                export_test_cases(session,
                                  tr,
                                  project_data["project_id"],
                                  project_data["jira_project_key"],
                                  feature["feature"],
                                  file_path,
                                  )
        except ImportError:
            pass
    if (
        "pytest_testrail_export_test_results" in session.config.option
        and session.config.option.pytest_testrail_export_test_results is True
    ):
        print("Initialize TestRail client")
        scenarios_run = pytest.testrail_client_dict["scenarios_run"]

        try:
            tr, project_data = get_testrail_api(session.config)
            testrail_plan_id = session.config.option.pytest_testrail_test_plan_id
            project_data["plan_id"] = testrail_plan_id
            project_data[
                "configuration_name"
            ] = session.config.option.pytest_testrail_test_configuration_name
            export_tests_results(session, tr, project_data, scenarios_run)
        except ImportError:
            pass


def get_testrail_api(config):
    tr = TestRailAPI(config)
    project_id = (
        config.getoption("--testrail-project-id")
        or config.inicfg.get("testrail-project-id")
        or environ.get("TESTRAIL_PROJECT_ID")
    )
    jira_project_key = (
        config.getoption("--jira-project-key")
        or config.inicfg.get("jira-project-key")
        or environ.get("JIRA_PROJECT_KEY")
    )
    validate_setup(tr, project_id)
    return tr, {"project_id": project_id, "jira_project_key": jira_project_key}


def export_test_cases(session,
                      tr: TestRailAPI, project_id: int, jira_project_key, feature, feature_file_path
                      ):
    """Function to export test cases to Testrail based on feature.

    Args:
        tr: Instance of TestRailAPI
        project_id: int Testrail Project ID
        jira_project_key: str
        feature: Feature Name
        feature_file_path: Feature File Path in Project Repository

    Function:
        Exports Test Cases to Testrail

    Notes:
        Example dictionary returned for variable `scenario` in `for scenario in reversed(feature['children'])`
        {
            'scenario': {
                'id': '103',
                'tags': [{'id': '102', 'location': {'line': 95, 'column': 5}, 'name': '@sample-delete-cookie'}],
                'location': {'line': 96, 'column': 5},
                'keyword': 'Scenario',
                'name': 'Delete cookie from the site',
                'description': '',
                'steps': [{'id': '100', 'location': {'line': 97, 'column': 9}, 'keyword': 'When ', 'text': "I delete the cookie 'foo'"}, {'id': '101', 'location': {'line': 98, 'column': 9}, 'keyword': 'Then ', 'text': "I expect cookie 'foo' to be deleted"}],
                'examples': []
            }
        }

        * Variable `scenario` in this case would return a dictionary with key as either "scenario" or "background", as appropriate
        * Key `examples` will always be present, and an empty list if there are no Examples provided in the scenario.
    """
    tr_project_suite_id = get_project_suite_id(tr, project_id, feature)
    tr_suite_sections_id = get_suite_section_id(
        tr, project_id, tr_project_suite_id, feature
    )
    if tr_suite_sections_id["tr_suite_sub_sub_section_id"] is not None:
        tr_suite_section_id_final = tr_suite_sections_id["tr_suite_sub_sub_section_id"]
    elif tr_suite_sections_id["tr_suite_sub_section_id"] is not None:
        tr_suite_section_id_final = tr_suite_sections_id["tr_suite_sub_section_id"]
    else:
        tr_suite_section_id_final = tr_suite_sections_id["tr_suite_section_id"]

    tr_suite_section_id = (
        tr_suite_section_id_final
    )
    background = {}
    for child in feature["children"]:
        # See this function Docstring Notes for details on reasoning for modification.
        if "background" in child:
            background = child["background"]

        if "scenario" in child:
            scenario = child["scenario"]
            raw_cases = []
            # If there are no examples, i.e an empty list - then below condition would return False
            # Also, if there is no example key, condition would return None, which would be Falsy.
            # In previous instance, where it checked for 'examples' in scenario, it would return True if there is an
            # examples key and even though it is empty. This would make the subsequent line throw an index out of range error
            # Walrus/Assignment operator usage details: https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions
            if scenario_examples := scenario.get("examples"):
                examples_raw = scenario_examples[0]
                scenario['original_name'] = scenario['name']
                table_rows = []
                table_header = examples_raw["tableHeader"]["cells"]
                for i in range(examples_raw["tableBody"].__len__()):
                    table_row = examples_raw["tableBody"][i]
                    row = {}
                    for j in range(table_row["cells"].__len__()):
                        row.update(
                            {table_header[j]["value"]: table_row["cells"][j]["value"]}
                        )
                    table_rows.append(row)

                for table_row in table_rows:
                    raw_custom_data_set = json.dumps(
                        table_row, indent=4, ensure_ascii=False
                    )

                    scenario['name'] = scenario['original_name'] + " -> " + raw_custom_data_set.replace('{',
                                                                                                        '').replace('}',
                                                                                                                    '').replace(
                        '"', '').strip()
                    raw_cases.append(
                        build_case(
                            tr=tr,
                            project_id=project_id,
                            suite_id=tr_project_suite_id,
                            section_id=tr_suite_section_id,
                            feature=feature,
                            scenario=scenario,
                            background=background,
                            raw_custom_data_set=raw_custom_data_set,
                            project_name=jira_project_key,
                        )
                    )

                set_test_case(session,
                              tr, tr_suite_section_id, feature_file_path, scenario, raw_cases
                              )
            else:
                raw_case = build_case(
                    tr=tr,
                    project_id=project_id,
                    suite_id=tr_project_suite_id,
                    section_id=tr_suite_section_id,
                    feature=feature,
                    scenario=scenario,
                    background=background,
                    raw_custom_data_set=None,
                    project_name=jira_project_key,
                )
                set_test_case(session,
                              tr, tr_suite_section_id, feature_file_path, scenario, [raw_case]
                              )


def set_test_case(session, tr: TestRailAPI, section_id, feature_file_path, scenario, raw_cases):
    tags = [tag for tag in scenario["tags"] if TESTRAIL_TAG_PREFIX in tag["name"]]
    if tags.__len__() != 0:
        if (
            "pytest_testrail_update_title" in session.config.option
            and session.config.option.pytest_testrail_update_title is True
        ):
            print(f'Scenario {scenario["name"]} already exists in TestRail. Updating title.')
            if scenario_examples := scenario.get("examples"):
                if scenario_examples[0]["tableBody"].__len__() != tags.__len__():
                    print(
                        f'Cannot update Scenario {scenario["name"]}. The number of Examples not matching the no of '
                        f'test_id(TR) tags. Please manually add all the test_id tags.')
                    return
            for index, raw_case in enumerate(raw_cases, start=0):
                tr.cases.update_case_field(
                    case_id=tags[index]["name"].replace(TESTRAIL_TAG_PREFIX, ""),
                    title=raw_case.title,
                )
        else:
            print(f'Scenario {scenario["name"]} already exists in TestRail. Updating test.')
            # If there are no examples, i.e an empty list - then below condition would return False
            # Also, if there is no example key, condition would return None, which would be Falsy.
            # In previous instance, where it checked for 'examples' in scenario, it would return True if there is an
            # examples key and even though it is empty. This would make the subsequent line throw an index out of range error
            # Walrus/Assignment operator usage details: https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions
            if scenario_examples := scenario.get("examples"):
                if scenario_examples[0]["tableBody"].__len__() != tags.__len__():
                    print(
                        f'Cannot update Scenario {scenario["name"]}. The number of Examples changed. '
                        f'Please manually remove {[tag["name"] + " " for tag in tags]} and import Scenario as new one and delete the previously imported scenario(s) from TestRail. '
                    )
                    return
            for index, raw_case in enumerate(raw_cases, start=0):
                tr.cases.update_case(
                    case_id=tags[index]["name"].replace(TESTRAIL_TAG_PREFIX, ""),
                    case=raw_case,
                )
    else:
        print(f'Creating scenario {scenario["name"]} in TestRail.')
        line = (
            scenario["location"]["line"] - 1
            if scenario["tags"].__len__() > 0
            else scenario["location"]["line"]
        )
        column = scenario["location"]["column"]
        tag = ""
        for raw_case in raw_cases:
            tr_case = tr.cases.add_case(section_id=section_id, case=raw_case)
            tag += f"{TESTRAIL_TAG_PREFIX}{tr_case.id} "
        tag += f'\n{" " * int(column - 1)}' if scenario["tags"].__len__() == 0 else ""
        _write_feature(feature_file_path, line, column, tag)


# pylint: disable=too-many-arguments
def build_case(
    tr: TestRailAPI,
    project_id: int,
    suite_id: int,
    section_id: int,
    feature,
    scenario,
    background,
    raw_custom_data_set=None,
    project_name=None,
) -> Case:
    # Setting Case references - for adding JIRA task reference
    feature_refs = [ft for ft in feature["tags"] if project_name + "-" in ft["name"]]
    scenario_refs = [sc for sc in scenario["tags"] if project_name + "-" in sc["name"]]
    raw_refs = ", ".join(
        tg["name"].replace("@", "") for tg in (feature_refs + scenario_refs)
    )

    raw_custom_tags = [
                          sc["name"]
                          for sc in scenario["tags"]
                          if ("automated" not in sc["name"] and "manual" not in sc["name"])
                      ] + [
                          ft["name"]
                          for ft in feature["tags"]
                          if (
            "automated" not in ft["name"]
            and "manual" not in ft["name"]
            and "nondestructive" not in ft["name"]
            and project_name + "-" not in ft["name"]
        )
                      ]

    # Setting Case priority - Sets the priority based on scenario tags. If "smoke" -> "Critical", "sanity" -> "High",
    # "regression" -> "Medium" and else "Low"
    priority_name = (
        "Critical"
        if list(filter(lambda sc: "smoke" in sc["name"], scenario["tags"]))
        else "High"
        if list(filter(lambda sc: "sanity" in sc["name"], scenario["tags"]))
        else "Medium"
        if list(filter(lambda sc: "regression" in sc["name"], scenario["tags"]))
        else "Low"
    )
    raw_priority = next(
        (pr.id for pr in tr.priorities.get_priorities() if pr.name == priority_name),
        None,
    )

    # Setting Case type - Case type is hardcoded to "Functional"
    raw_type = next(
        (ct.id for ct in tr.case_types.get_case_types() if ct.name == "1. Functional"),
        None,
    )

    # Setting Case template - Template is hardcoded to use "Test Case (Steps)"
    raw_template = next(
        (
            ct.id
            for ct in tr.templates.get_templates(project_id)
            if ct.name == "Test Case (Steps)"
        ),
        None,
    )

    # Setting Case automation - Sets "Automated" -> "Yes" if scenario has tag "automated" else default "None"
    raw_custom_automation_type = (
        "2"
        if any("automated" in sc["name"] for sc in scenario["tags"])
        else "0"
    )

    # Setting Case background
    raw_custom_precondition = []
    if background:
        raw_custom_precondition.extend(["**" + rs["keyword"].strip() + "** "
                                        + rs["text"].strip()
                                        for rs in background["steps"]])

    # Setting Case steps
    raw_steps = [
        {
            "content": "**"
                       + rs["keyword"].strip()
                       + "** "
                       + rs["text"].strip()
                       + add_data_table(rs),
            "expected": "",
        }
        for rs in scenario["steps"]
    ]

    raw_case = Case(
        {
            "estimate": "10m",
            "priority_id": raw_priority,
            "refs": raw_refs,
            "custom_tags": ", ".join(raw_custom_tags),
            "suite_id": suite_id,
            "section_id": section_id,
            "title": scenario["name"],
            "type_id": raw_type,
            "template_id": raw_template,
            "custom_automation_type": raw_custom_automation_type,
            "custom_data_set": raw_custom_data_set,
            "custom_preconds": "\n".join(str(rp) for rp in raw_custom_precondition),
            "custom_steps_separated": raw_steps,
        }
    )
    return raw_case


def add_data_table(scenario_step):
    if "argument" not in scenario_step:
        return ""
    data_table = "\n*Data Table*\n"
    table_rows = [rsa for rsa in scenario_step["argument"]["rows"]]
    for i, table_row in enumerate(table_rows):
        for j, row_cell in enumerate(table_row["cells"]):
            data_table += "|%s" % row_cell["value"]
        data_table += "|\n"
    return data_table


# pylint: disable=protected-access
def export_case(
    tr: TestRailAPI, section_id: int, tr_suite_cases: List[Case], raw_case: Case
):
    tr_suite_case = next(
        (
            sc
            for sc in tr_suite_cases
            if sc.title == raw_case.title
               and sc._custom_methods["custom_data_set"]
               == raw_case._custom_methods["custom_data_set"]
        ),
        None,
    )
    if tr_suite_case:
        print("Updating Case ", tr_suite_case.title)
        tr.cases.update_case(case_id=tr_suite_case.id, case=raw_case)
    else:
        print("Creating Case ", raw_case.title)
        tr.cases.add_case(section_id=section_id, case=raw_case)


def get_project_test_plan(tr, tr_plan_name, test_market):
    test_plan_name = "%s_%s" % (tr_plan_name, test_market)
    tr_plans = tr.plans()
    tr_plan = next((tp for tp in tr_plans if tp.name == test_plan_name), None)
    if tr_plan is None:
        error_message = (
            "There is no Test Plan with name %s set on TestRail" % test_plan_name
        )
        raise TestRailError(error_message)
    print("Collecting Test Plan ", tr_plan.name, " from TestRail")
    return tr_plan


def get_project_suite_id(tr: TestRailAPI, tr_project_id: int, feature) -> int:
    # This condition is currently added to support both project types 1 & 3. This need to be deleted (entire IF block) when
    # completely migrated to project type1
    if tr.projects.get_project(tr_project_id).suite_mode == 3:
        suite_name_raw = feature["name"].strip()
        suite_name_raw = suite_name_raw.split(SEPARATOR_CHAR)[0]
        tr_project_suites = tr.suites.get_suites(tr_project_id)
        if any(
            (tr_project_suite.name == suite_name_raw)
            for tr_project_suite in tr_project_suites
        ):
            print("Collecting Suite ", suite_name_raw, " from TestRail")
            return next(
                (suite.id for suite in tr_project_suites if suite.name == suite_name_raw)
            )

        print("No Suite with name ", suite_name_raw, " was found on TestRail")
        new_project_suite = Suite(
            {
                "name": suite_name_raw,
                "description": "",
                "is_baseline": False,
                "is_completed": False,
                "is_master": False,
                "project_id": tr_project_id,
            }
        )
        print("Creating new Suite ", suite_name_raw)
        tr_project_suite = tr.suites.add_suite(
            project_id=tr_project_id, suite=new_project_suite
        )
        return tr_project_suite.id

    # This condition is currently added to support both project types 1 & 3. This need to be deleted (Only ELIF condition) when
    # completely migrated to project type1
    elif tr.projects.get_project(tr_project_id).suite_mode == 1:
        return tr.suites.get_suites(tr_project_id)[0].id


def get_suite_section_id(
    tr: TestRailAPI, project_id: int, project_suite_id: int, feature
) -> dict:
    feature_name_raw = feature["name"].strip()
    feature_name_components = (
        feature_name_raw.split(SEPARATOR_CHAR)
        if SEPARATOR_CHAR in feature_name_raw
        else [feature_name_raw]
    )
    section_name_raw = (
        feature_name_components[0]
    )
    sub_section_name_raw = (
        feature_name_components[1] if feature_name_components.__len__() > 1 else None
    )
    sub_sub_section_name_raw = (
        feature_name_components[2] if feature_name_components.__len__() > 2 else None
    )

    # check for section
    tr_suite_sections = tr.sections.get_sections(project_id, project_suite_id)
    if any(
        tr_suite_section.name == section_name_raw and tr_suite_section.parent_id is None
        for tr_suite_section in tr_suite_sections
    ):
        print(f"Collecting Sections for feature {feature_name_raw} from TestRail")
        tr_suite_section_id = next(
            section.id
            for section in tr_suite_sections
            if section.name == section_name_raw and section.parent_id is None
        )
    else:
        print(
            f"No Section with name {section_name_raw}. Creating new Section.."
        )
        suite_section = {
            "name": section_name_raw,
            "description": feature["description"].replace("\n  ", "\n").strip(),
            "depth": 0,
            "display_order": 2,
            "suite_id": project_suite_id,
        }
        tr_suite_section = tr.sections.add_section(
            project_id=project_id, section=Section(suite_section)
        )
        tr_suite_section_id = tr_suite_section.id

    # check for sub section
    tr_suite_sections = tr.sections.get_sections(project_id, project_suite_id)
    if sub_section_name_raw is not None and any(
        tr_suite_section.name == sub_section_name_raw and tr_suite_section.parent_id == tr_suite_section_id
        for tr_suite_section in tr_suite_sections
    ):
        print(f"Collecting Sub-Sections for feature {feature_name_raw} from TestRail")
        tr_suite_sub_section_id = next(
            section.id
            for section in tr_suite_sections
            if section.name == sub_section_name_raw and section.parent_id == tr_suite_section_id
        )
    elif sub_section_name_raw is not None:
        print(
            f"No Sub-Section with name {sub_section_name_raw} was found under Section {section_name_raw}. Creating new Sub-Section.")
        suite_sub_section = {
            "name": sub_section_name_raw,
            "description": feature["description"].replace("\n  ", "\n").strip(),
            "depth": 0,
            "display_order": 2,
            "suite_id": project_suite_id,
            "parent_id": tr_suite_section_id,
        }
        tr_suite_sub_section = tr.sections.add_section(
            project_id=project_id, section=Section(suite_sub_section)
        )
        tr_suite_sub_section_id = tr_suite_sub_section.id
    else:
        tr_suite_sub_section_id = None

    # check for sub sub section
    if sub_sub_section_name_raw is not None and any(
        tr_suite_section.name == sub_sub_section_name_raw and tr_suite_section.parent_id == tr_suite_sub_section_id
        for tr_suite_section in tr_suite_sections
    ):
        print(f"Collecting Sub-Sub-Sections for feature {feature_name_raw} from TestRail")
        tr_suite_sub_sub_section_id = next(
            section.id
            for section in tr_suite_sections
            if section.name == sub_sub_section_name_raw and section.parent_id == tr_suite_sub_section_id
        )
    elif sub_sub_section_name_raw is not None:
        print(
            f"No Sub-Sub-Section with name {sub_sub_section_name_raw} was found under Sub-Section {sub_section_name_raw} and Section {section_name_raw}. Creating new Sub-Sub-Section.")
        suite_sub_sub_section = {
            "name": sub_sub_section_name_raw,
            "description": feature["description"].replace("\n  ", "\n").strip(),
            "depth": 0,
            "display_order": 2,
            "suite_id": project_suite_id,
            "parent_id": tr_suite_sub_section_id,
        }
        tr_suite_sub_sub_section = tr.sections.add_section(
            project_id=project_id, section=Section(suite_sub_sub_section)
        )
        tr_suite_sub_sub_section_id = tr_suite_sub_sub_section.id
    else:
        tr_suite_sub_sub_section_id = None
    return {
        "tr_suite_section_id": tr_suite_section_id,
        "tr_suite_sub_section_id": tr_suite_sub_section_id,
        "tr_suite_sub_sub_section_id": tr_suite_sub_sub_section_id
    }


def export_tests_results(session, tr: TestRailAPI, project_data: dict, scenarios_run: dict):
    print("\nPublishing results")

    # tr_plan = tr.plans.get_plan(project_data["plan_id"])
    tr_statuses = tr.statuses.get_statuses()

    tr_plan = tr.plans.get_plan(project_data["plan_id"])
    for tr_plan_entry in tr_plan.entries:
        for tr_run in tr_plan_entry.runs:
            if (
                tr_run.config == project_data["configuration_name"]
                and tr_run.name in scenarios_run
            ):
                for scenario_run in scenarios_run[tr_run.name]:
                    if not hasattr(scenario_run, 'failed'):
                        scenario_run.failed = False
                    tr_tests = tr.tests.get_tests(tr_run.id)
                    tr_test = next(
                        (
                            test
                            for test in tr_tests
                                if (remove_multiple_spaces(test.title) == remove_multiple_spaces(
                                    scenario_run.name)) or (remove_multiple_spaces(scenario_run.name + " -> " +
                                        json.dumps(scenario_run.data_set).replace('{', ' ').replace('}', '').replace(
                                            '"', '').strip()) == remove_multiple_spaces(
                                                test.title.replace('\n    ', ' ').replace('\n', '')))
                        ),
                        None,
                    )

                    if tr_test is None:
                        print(
                            "Result for test %s not published to TestRail"
                            % scenario_run.name
                        )
                    else:
                        if (
                            "pytest_testrail_skip_step_results" in session.config.option
                            and session.config.option.pytest_testrail_skip_step_results is True
                        ):
                            scenario_status_type = "failed" if scenario_run.failed else "passed"
                            tr_result = Result(
                                {
                                    "test_id": tr_test.id,
                                    "status_id": next(
                                        st.id
                                        for st in tr_statuses
                                        if st.name == scenario_status_type
                                    ),
                                    "comment": print_desired_capabilities(scenario_run.caps),
                                }
                            )

                        else:
                            custom_step_results = []
                            custom_steps_separated = tr_test.custom_methods[
                                "custom_steps_separated"
                            ]
                            passed = True

                            # fix to avoid shifting the test result with a position equals with the no of background steps
                            try:
                                while len(scenario_run.steps) > len(custom_steps_separated):
                                    scenario_run.steps.pop(0)
                            except TypeError:
                                continue

                            # in case of API testing, we don't have functional steps defined in TR
                            if not BPStorage.is_api_testing():
                                for scenario_step, tr_case_step in zip(scenario_run.steps, custom_steps_separated):
                                    step_status_type = (
                                        "blocked"
                                        if not passed
                                        else "passed"
                                        if not scenario_step.failed
                                        else "failed"
                                        if scenario_step.failed
                                        else "untested"
                                    )
                                    if step_status_type == "failed":
                                        passed = False
                                    status_id = next(
                                        (st.id for st in tr_statuses if st.name == step_status_type),
                                        None,
                                    )
                                    exception_message = (
                                        scenario_run.exception_message
                                        if step_status_type == "failed"
                                           and hasattr(scenario_run, "exception_message")
                                        else ""
                                    )
                                    custom_step_results.append(
                                        {
                                            "content": tr_case_step["content"],
                                            "expected": tr_case_step["expected"],
                                            "actual": exception_message,
                                            "status_id": status_id,
                                        }
                                    )
                            scenario_status_type = "failed" if scenario_run.failed else "passed"
                            tr_result = Result(
                                {
                                    "test_id": tr_test.id,
                                    "status_id": next(
                                        st.id
                                        for st in tr_statuses
                                        if st.name == scenario_status_type
                                    ),
                                    "comment": print_desired_capabilities(scenario_run.caps),
                                    "custom_step_results": custom_step_results,
                                }
                            )

                        result = tr.results.add_result(tr_result)
                        if scenario_run.data_set:
                            test_name = "test_" + scenario_run.name.replace(' ', "_").lower() + "[" + ''.join(
                                scenario_run.data_set.values()) + "]"
                        else:
                            test_name = "test_" + scenario_run.name.replace(' ', "_").lower()
                        test_name = remove_chars_from_string(test_name, NOT_ALLOWED_CHARACTERS)
                        # in case of API testing, we don't have attachments / screenshots
                        if not BPStorage.is_api_testing():
                            if scenario_run.failed:
                                failed_step_screenshot = f"output/screenshots/{test_name}.png"
                                if Path(f"{os.getcwd()}/{failed_step_screenshot}").exists():
                                    tr.attachments.add_attachment_to_result(result.id, failed_step_screenshot)
                            if Path(f"{os.getcwd()}/{TEMP_SCREENSHOTS}").exists():
                                filenames = os.listdir(TEMP_SCREENSHOTS)
                                for filename in reversed(filenames):
                                    if test_name in os.path.splitext(filename)[0]:
                                        tr.attachments.add_attachment_to_result(result.id,
                                                                                f"{TEMP_SCREENSHOTS}{filename}")


# print("\nResults published")


def pytest_runtest_teardown(item):
    if (
        "pytest_testrail_export_test_results" in item.session.config.option
        and item.session.config.option.pytest_testrail_export_test_results is True
        and BPStorage.is_api_testing()
    ):
        add_api_test_to_run(item)


def pytest_bdd_after_scenario(request, feature, scenario):
    # Adding Scenario to the list of Scenarios ran
    _ = feature
    if (
        "pytest_testrail_export_test_results" in request.config.option
        and request.config.option.pytest_testrail_export_test_results is True
    ):
        add_scenario_to_run(request, scenario)
    if (
        "reruns" in request.config.option
        and request.config.option.reruns is not None
        and request.config.option.reruns >= request.node.execution_count
    ):
        scenario.failed = False
        for scenario_step in scenario.steps:
            scenario_step.failed = False


def pytest_bdd_step_error(feature, scenario, step, exception):
    _step_error(exception, feature, scenario, step)


def pytest_bdd_step_func_lookup_error(request, feature, scenario, step, exception):
    _ = request
    _step_error(exception, feature, scenario, step)


def _step_error(exception, feature, scenario, step):
    _ = feature
    scenario.exception = exception
    scenario.failed = True
    # Setting Scenario and Steps statuses and exception error if the case
    flag = False
    for scenario_step in scenario.steps:
        scenario_step.failed = None if flag else False
        if scenario_step == step:
            scenario_step.exception = exception
            scenario_step.failed = True
            flag = True
    exception_message = (
        exception.msg
        if hasattr(exception, "msg")
        else exception.message
        if hasattr(exception, "message")
        else exception.args[0]
        if hasattr(exception, "args") and exception.args.__len__() > 0
        else "no error message"
    )
    scenario.exception_message = exception_message
    logger.exception(
        "Step FAILED.",
        step=step.name,
    )


def add_api_test_to_run(item):
    # in case of API, we export only the test results based on the test name & TR identifier
    global scenario_name, scenario_tr_identifier
    run_name = item.session.config.option.pytest_testrail_test_run_name
    for marker in item.own_markers:
        if 'name' in marker.name:
            scenario_name = marker.args[0]
        if 'TR' in marker.name:
            scenario_tr_identifier = marker.name
    kwargs = {'feature': None, 'name': scenario_name, 'line_number': None,
              'steps': [], 'tags': scenario_tr_identifier}
    scenario = pytest_bdd.parser.Scenario(**kwargs)
    scenario.caps = {}
    scenario.data_set = {}
    scenario.failed = item.rep_call.failed
    if run_name not in pytest.testrail_client_dict["scenarios_run"]:
        pytest.testrail_client_dict["scenarios_run"][run_name] = []
    pytest.testrail_client_dict["scenarios_run"][run_name].append(deepcopy(scenario))


def add_scenario_to_run(request, scenario):
    scenario.data_set = {}
    scenario.caps = {}
    try:
        desired_capabilities = request.node.funcargs['session_capabilities']
        if desired_capabilities:
            for key, value in desired_capabilities.items():
                scenario.caps.update({key: value})
    except (AttributeError, KeyError) as error:
        logger.warning(f"{error}")

    for key, value in request.node.funcargs.items():
        if '_pytest_bdd_example' in key:
            scenario.data_set.update(value)

    tr = TestRailAPI(request.config)
    project_id = environ.get("TESTRAIL_PROJECT_ID")

    # This condition is currently added to support both project types 1 & 3. This need to be deleted (entire IF block) when
    # completely migrated to project type1
    if tr.projects.get_project(project_id).suite_mode == 3:
        suite_name = scenario.feature.name.split(" - ")[0]
        if suite_name not in pytest.testrail_client_dict["scenarios_run"]:
            pytest.testrail_client_dict["scenarios_run"][suite_name] = []
        pytest.testrail_client_dict["scenarios_run"][suite_name].append(deepcopy(scenario))

    # This condition is currently added to support both project types 1 & 3. This need to be deleted (only ELIF condition) when
    # completely migrated to project type1
    elif tr.projects.get_project(project_id).suite_mode == 1:
        run_name = request.session.config.option.pytest_testrail_test_run_name
        if run_name not in pytest.testrail_client_dict["scenarios_run"]:
            pytest.testrail_client_dict["scenarios_run"][run_name] = []
        pytest.testrail_client_dict["scenarios_run"][run_name].append(deepcopy(scenario))


def print_desired_capabilities(config: Dict):
    """Print given desired capabilities in the TestRail for each test case"""
    output: str = ""
    if config and isinstance(config, dict):
        output += "Capabilities: \n\n"
        for key, value in config.items():
            output += f"{key}: {value}\n"
    return output
