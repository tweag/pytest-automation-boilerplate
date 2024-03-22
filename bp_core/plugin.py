import re
import shutil
import subprocess
import time

import structlog
import os
import json
import copy
from _pytest.fixtures import FixtureLookupError

from py.xml import html
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import List

from pytest_html import extras
import pytest
import pytest_html

from _pytest import config as pytest_config

from _pytest.config import argparsing as pytest_argparsing

from cucumber_tag_expressions import parse

from bp_core.utils.dataset_handler import DatasetHandler
# do not remove this unused import. this sets up pytest short summary.

from selenium.common.exceptions import WebDriverException

# do not remove this unused import. this sets up logging.
from bp_core.utils import log_handler
from bp_core.utils.env_variables import EnvVariables, load_env_from_local_dotenv_file
from bp_core.utils.bp_storage import BPStorage
from bp_core.utils.utils import initialize_output_dirs, remove_chars_from_string, zip_screenshots_files, \
    save_base64_as_png, TEMP_SCREENSHOTS

logger = structlog.get_logger(__name__)
PROJECT_DIR = Path.cwd().resolve()
DEFAULT_ASSETS_DIR = Path(os.path.join(PROJECT_DIR, "output", "reports", "assets"))
ALLURE_RESULTS_DIR = Path(os.path.join(PROJECT_DIR, "output", "allure", "results"))
ALLURE_REPORT_DIR = Path(os.path.join(PROJECT_DIR, "output", "allure", "reports"))

bp_storage = BPStorage()
NOW = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
NOT_ALLOWED_CHARACTERS = ["/", "\\", '"', ":", "<", ">", "|", "*", "?", "#", "%", "{", "}", "$", "!", "'", "@", "=",
                          "+", "-"]
TESTCASE_TAG_PREFIX = ("TR-C", "TC")

"1. Pytest default hooks & fixtures for the UI & API tests"


# Test annotations are configured & env variables are loaded
def pytest_configure(config: pytest_config.Config) -> None:
    """Allow plugins and conftest files to perform initial configuration.

    This hook is called for every plugin and initial conftest file
    after command line options have been parsed.

    After that, the hook is called for other conftest files as they are
    imported.

    .. note::
        This hook is incompatible with ``hookwrapper=True``.

    :param _pytest.config.Config config: The pytest config object.

    Reference for docstring:
    https://docs.pytest.org/en/6.2.x/_modules/_pytest/hookspec.html#pytest_configure
    """
    config.option.keyword = "automated"
    config.option.markexpr = "not not_in_scope"
    is_driver = [arg for arg in config.invocation_params.args if "driver" in arg]
    if is_driver and not os.environ.get('BOILERPLATE_INSTALLATION'):
        config.pluginmanager.import_plugin("bp_core.frontend.frontend_plugin")

    # reset values & delete files when using BPStorage
    bp_storage.set_api_testing(False)
    if os.path.exists("html_env_vars.pickle"):
        os.remove("html_env_vars.pickle")

    # pre-load env. variables in order to meet TestRail requirements
    load_env_from_local_dotenv_file()

    # delete temporary screenshots directory if exist
    if Path(f"{os.getcwd()}/{TEMP_SCREENSHOTS}").exists():
        try:
            shutil.rmtree(Path(f"{os.getcwd()}/{TEMP_SCREENSHOTS}"))
        finally:
            ...

    # HTML Report: Report name
    if config.option.htmlpath:
        not_allowed_filename_characters = ["/", "\\"]
        report_path: Path = Path(config.option.htmlpath)
        prefix = "TestReport"
        test_scripts_version = ""
        app_version = ""
        html_env_var = ""
        ci_ = os.getenv("CI")
        if isinstance(ci_, str) and str(ci_).lower() == 'true':
            if not os.environ.get("TEST_SCRIPTS_VERSION", "").startswith("refs"):
                test_scripts_version = os.environ.get('TEST_SCRIPTS_VERSION', "")
                test_scripts_version = remove_chars_from_string(test_scripts_version, not_allowed_filename_characters)
            app_version = os.environ.get('APP_VERSION', "")
        if config.option.html_suffix is not None:
            html_env_var = os.getenv(config.option.html_suffix)
        html_report_file_name = "_".join(filter(None, [prefix, NOW, test_scripts_version, app_version,
                                                       html_env_var])) + ".html"
        if report_path.suffix:
            config.option.htmlpath = str(report_path.with_name(html_report_file_name))
        else:
            config.option.htmlpath = str(report_path / str(html_report_file_name))


# CLI params are added (we need this hook for every new parameters that will need to be added)
def pytest_addoption(parser: pytest_argparsing.Parser) -> None:
    """Register argparse-style options and ini-style config values,
    called once at the beginning of a test run.

    .. note::

        This function should be implemented only in plugins or ``conftest.py``
        files situated at the tests root directoy due to how pytest
        :ref:`discovers plugins during startup <pluginorder>`.

    :param _pytest.config.argparsing.Parser parser:
        To add command line options, call
        :py:func:`parser.addoption(...) <_pytest.config.argparsing.Parser.addoption>`.
        To add ini-file values call :py:func:`parser.addini(...)
        <_pytest.config.argparsing.Parser.addini>`.

    :param _pytest.config.PytestPluginManager pluginmanager:
        pytest plugin manager, which can be used to install :py:func:`hookspec`'s
        or :py:func:`hookimpl`'s and allow one plugin to call another plugin's hooks
        to change how command line options are added.

    Options can later be accessed through the
    :py:class:`config <_pytest.config.Config>` object, respectively:

    - :py:func:`config.getoption(name) <_pytest.config.Config.getoption>` to
      retrieve the value of a command line option.

    - :py:func:`config.getini(name) <_pytest.config.Config.getini>` to retrieve
      a value read from an ini-style file.

    The config object is passed around on many internal objects via the ``.config``
    attribute or can be retrieved as the ``pytestconfig`` fixture.

    .. note::
        This hook is incompatible with ``hookwrapper=True``.

    Reference for docstring:
    https://docs.pytest.org/en/6.2.x/_modules/_pytest/hookspec.html#pytest_addoption
    """
    parser.addoption(
        "--language",
        action="store",
        default="en",
        type=str,
        help="Application language",
    )
    parser.addoption(
        "--conf",
        action="store",
        default="mock",
        type=str
    )
    parser.addoption(
        "--proxy-url",
        metavar="str",
        help="The proxy to be used by any network request - browser or otherwise",
    )
    parser.addoption(
        "--locators",
        metavar="str",
        help="The path to a json file or a folder of json files containing the locators needed for the test(s)",
    )
    parser.addoption(
        "--tags",
        metavar="str",
        help="Will filter tests by given tags"
    )
    parser.addoption(
        "--html_suffix",
        metavar="str",
        help="Append a suffix to the HTML report name"
    )


# Initialize output directories & override selenium fixture based on the platform
def pytest_sessionstart(session: pytest.Session) -> None:
    """Called after the ``Session`` object has been created and before performing collection
    and entering the run test loop.

    :param pytest.Session session: The pytest session object.

    Reference for docstring:
    https://docs.pytest.org/en/6.2.x/_modules/_pytest/hookspec.html#pytest_sessionstart
    """
    initialize_output_dirs()

    # HTML Report: Environment section: removing unnecessary data
    html_metadata = session.config._metadata
    while html_metadata.get("Server") is not None:
        html_metadata.pop("Server")

    # Add environment data for pytest-json report
    json_env = session.config._json_environment
    json_env.clear()
    if 'browserstack' in json.dumps(html_metadata['Capabilities']) and html_metadata['Driver'] != 'Appium':
        json_env.append(('Operating System', html_metadata['Capabilities']['bstack:options']['os']))
        json_env.append(('Browser', html_metadata['Capabilities']['browserName']))
    else:
        json_env.append(('Operating System', html_metadata['Platform']))
        json_env.append(('Browser', html_metadata['Driver']))


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus) -> None:
    """Called after whole test run finished, right before returning the exit status to the system.

        :param pytest.Session session: The pytest session object.
        :param int exitstatus: The status which pytest will return to the system.
    """

    if exitstatus == 0 or exitstatus == 1 or exitstatus == 6:
        command_generate_allure_report = [
            'allure generate ' + ALLURE_RESULTS_DIR.__str__() + ' -o ' + ALLURE_REPORT_DIR.__str__() + ' --clean']
        result = subprocess.Popen(command_generate_allure_report, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  shell=True)
        print(f"Allure Process ID : {result.pid}")
        print('Allure Report is being generated...')
        stdout, stderr = result.communicate()
        print('Allure Report has been generated successfully...')
        time.sleep(5)
    else:
        print(f"Report not generated because of no tag found")

    # HTML Report: Environment section: removing unnecessary data
    base_url_meta_key = "Base URL"
    chars_to_remove = ['{', '}', '"']
    metadata = session.config._metadata
    metadata.pop("JAVA_HOME", "")
    metadata.pop("Packages", "")

    if not metadata.get(base_url_meta_key, False):
        if os.getenv("BASE_URL", False):
            metadata[base_url_meta_key] = os.getenv("BASE_URL")
        else:
            metadata.pop(base_url_meta_key, "")
    if metadata.get('Capabilities', False):
        caps = json.dumps(metadata['Capabilities'])
        metadata['Capabilities'] = remove_chars_from_string(caps, chars_to_remove)
    else:
        metadata.pop("Capabilities", "")
    if metadata.get('Driver', False):
        _driver = json.dumps(metadata['Driver'])
        metadata['Driver'] = remove_chars_from_string(_driver, chars_to_remove)
    else:
        metadata.pop("Driver", "")
    if metadata.get('Plugins', False):
        plugins = json.dumps(metadata['Plugins'])
        metadata['Plugins'] = remove_chars_from_string(plugins, chars_to_remove)

    metadata['CI'] = 'GitHub' if os.getenv("CI") else 'Local'
    metadata['Run from'] = metadata.pop("CI")

    # HTML Report: Show Tests Scripts Version and App Version in the HTML report
    if os.getenv("CI") == "true":
        if os.environ.get("TEST_SCRIPTS_VERSION", None) and not \
                os.environ.get("TEST_SCRIPTS_VERSION", "").startswith("refs"):
            metadata["Test Scripts Version"] = os.environ.get("TEST_SCRIPTS_VERSION", "")
        if os.environ.get("APP_VERSION", None):
            metadata["App Version"] = os.environ.get("APP_VERSION")

    # Reorder of the Environment section
    environment_values = ('Run from', 'Server', 'Base URL', 'Capabilities', 'Driver', 'Platform', 'Plugins', 'Python')

    # Log the environment variable values on demand within HTML report
    if BPStorage.get_env_vars_for_html() is not None:
        for key, value in BPStorage.get_env_vars_for_html().items():
            environment_values = environment_values + (key,)
            metadata[key] = value

    if session.config.option.html_suffix is not None:
        environment_values = environment_values + (session.config.option.html_suffix,)
        metadata[session.config.option.html_suffix] = os.environ.get(session.config.option.html_suffix)

    ordered_metadata = OrderedDict()
    for key in environment_values:
        if metadata.get(key, None):
            ordered_metadata[key] = metadata[key]

    session.config._metadata = ordered_metadata


# Collect all tags / markers for the tests
def pytest_collection_modifyitems(
        config: pytest_config.Config, items: List[pytest.Item]
) -> None:
    """Called after collection has been performed. May filter or re-order
    the items in-place.

    :param _pytest.config.Config config: The pytest config object.
    :param List[pytest.Item] items: List of item objects.

    Reference for docstring:
    https://docs.pytest.org/en/6.2.x/_modules/_pytest/hookspec.html#pytest_collection_modifyitems
    """
    for item in items:
        if item.cls:
            for marker in item.cls.pytestmark:
                item.add_marker(marker.name)
    if (
            "pytest_testrail_export_test_cases" not in config.option
            or config.option.pytest_testrail_export_test_cases is False
    ):
        raw_tags = config.option.tags
        if raw_tags is not None:
            for item in items:
                item_tags = [marker.name for marker in item.own_markers]
                if not parse(raw_tags).evaluate(item_tags):
                    item.add_marker(pytest.mark.not_in_scope)

    for item in items:
        if pytest.mark.api.mark in item.own_markers and pytest.mark.not_in_scope.mark not in item.own_markers:
            bp_storage.set_api_testing(True)
            config.pluginmanager.import_plugin("bp_core.backend.backend_plugin")
            break

    if not bp_storage.is_api_testing() and not os.environ.get('BOILERPLATE_INSTALLATION'):
        config.pluginmanager.import_plugin("bp_core.frontend.frontend_plugin")


"2. API & UI - common implementation"


# Define the environment variables fixture
# This is API & UI specific implementation
@pytest.fixture(scope='session')
def env_variables(request):
    env_vars_file_path = f"{request.session.config.known_args_namespace.confcutdir}/configs/.local.env"
    return EnvVariables(env_vars_file_path)


# Define the base url fixture
# This is API & UI specific implementation
@pytest.fixture(scope="session")
def base_url(request, env_variables) -> str:
    # get base url value from command line
    # if it returns nothing, then look for environment variables and return.
    return request.config.getoption("--base-url") or env_variables.get(
        "BASE_URL", default=""
    )


# Define the language fixture
# This is API & UI specific implementation
@pytest.fixture(scope="session")
def language(request):
    language_value = request.config.getoption("language")
    return language_value if language_value else None


# Define the project directory fixture
# This is API & UI specific implementation
@pytest.fixture(scope="session", autouse=True)
def project_dir(request, pytestconfig) -> str:
    path_str = request.session.config.known_args_namespace.confcutdir
    # the value above is None in some cases(not sure why). so, adding the fallback below
    return path_str if path_str else str(pytestconfig.rootdir)


# Define proxy-url as a fixture
# This is API & UI specific implementation
@pytest.fixture(scope="session")
def proxy_url(request):
    proxy_url_value = request.config.getoption("--proxy-url")
    return proxy_url_value if proxy_url_value else None


@pytest.fixture(autouse=True)
def dataset_handler(dataset):
    return DatasetHandler(dataset)


"3. HTML Reports specific implementation"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
    setattr(rep, "duration_formatter", "%M:%S.%f")
    extra = getattr(rep, "extra", [])

    if not bp_storage.is_api_testing():
        # HTML Report: Store the Scenario Outline data
        if rep.when == "teardown":
            request_ = item.funcargs["request"]
            bdd_example = request_.node.funcargs.get('_pytest_bdd_example', None)
            if bdd_example and isinstance(bdd_example, dict):
                rep.scenario.update({"example": {**bdd_example}})

        if rep.when == "call":
            feature_request = item.funcargs["request"]
            # HTML Report: Added used driver version and Server name
            html_metadata = feature_request.session.config._metadata
            if isinstance(html_metadata.get("Driver", None), str):
                driver_name = html_metadata["Driver"]
                html_metadata["Driver"] = {}
                html_metadata["Driver"]["Name"] = driver_name

            try:
                driver = feature_request.getfixturevalue("selenium")
            except (FixtureLookupError, WebDriverException):
                driver = None

            public_link = None
            if driver is not None:
                capabilities = feature_request.getfixturevalue("session_capabilities")
                if capabilities.get("browserstack", "").strip().lower() == "true":
                    driver.execute_script(
                        'browserstack_executor: {"action": "setSessionName", "arguments": {"name": "' + feature_request.node.name + '"}}')
                    if rep.passed:
                        driver.execute_script(
                            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status": "PASSED"}}'
                        )
                    elif rep.failed:
                        driver.execute_script(
                            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status": "FAILED"}}'
                        )
                        response = driver.execute_script('browserstack_executor: {"action": "getSessionDetails"}')
                        if isinstance(response, str):
                            public_link = json.loads(response)['public_url']

                if driver.capabilities.get("browserVersion", False):
                    html_metadata["Driver"].update({"Browser version": str(driver.capabilities["browserVersion"])})
                if driver.capabilities.get("browserstack", "") == "True" or \
                        html_metadata.get('Capabilities', {}).get('browserstack', None) == "True":
                    html_metadata.update({"Server": "Browserstack"})

                xfail = hasattr(rep, "wasxfail")
                assets_folder = DEFAULT_ASSETS_DIR
                if feature_request.config.option.htmlpath:
                    assets_folder = Path(os.path.abspath(feature_request.config.option.htmlpath)).parent / "assets"
                screenshot_source = None
                if (rep.skipped and xfail) or (rep.failed and not xfail):
                    screenshot_source = driver.get_screenshot_as_base64()
                    ss_file = remove_chars_from_string(feature_request.node.name, NOT_ALLOWED_CHARACTERS)
                    ss_file = f"output/screenshots/{ss_file}.png"
                    driver.save_screenshot(ss_file)
                if (rep.skipped and xfail) or (rep.failed and not xfail) or (rep.passed and not xfail):
                    node_name = feature_request.node.name
                    if (scenario := getattr(rep, "scenario", None)) and (feature := scenario.get('feature', None)):
                        scenario_cache = feature_request.config.cache.get(f"{feature['name']}/{scenario['name']}", {})
                        if node_name not in scenario_cache:
                            scenario_cache[node_name] = [screenshot_source]
                        elif scenario_cache.get(node_name, None):
                            scenario_cache.get(node_name, []).append(screenshot_source)
                        scenario_cache[node_name] = [element for element in scenario_cache.get(node_name, []) if
                                                     element is not None]
                        if len(scenario_cache.get(node_name, [])) > 2:
                            zipped_file_name = "_".join(["screenshots", node_name, NOW])
                            zipped_file_name = remove_chars_from_string(zipped_file_name, NOT_ALLOWED_CHARACTERS)
                            for idx, screenshot in enumerate(scenario_cache.get(node_name, [])):
                                file_name = f"{feature['name']}_{scenario['name']}_{str(idx)}.png"
                                file_name = remove_chars_from_string(file_name, NOT_ALLOWED_CHARACTERS)
                                save_base64_as_png(data=screenshot, dest_folder=assets_folder / zipped_file_name,
                                                   dest_file_name=file_name)
                            zip_screenshots_files(assets_folder / zipped_file_name, zipped_file_name, assets_folder)
                            extra.append(
                                pytest_html.extras.url('assets/' + f'{zipped_file_name}' + '.zip', "Screenshots zip"))
                            if screenshot_source:
                                extra.append(pytest_html.extras.image(screenshot_source))
                        else:
                            extra.extend(
                                [pytest_html.extras.image(screenshot) for screenshot in
                                 reversed(scenario_cache.get(node_name, []))])
                if public_link:
                    extra.append(pytest_html.extras.url(public_link, "BrowserStack View"))
                    rep.test_metadata = f"Browserstack Public Link, {public_link}"
                rep.extra = extra
    else:
        rep.test_name = [test_name.args[0] for test_name in item.iter_markers() if test_name.name == 'test_name']


# Define an extra column for HTML report: Section
# Set the order of the columns
def pytest_html_results_table_header(cells):
    if cells:
        if not bp_storage.is_api_testing():
            cells.insert(0, copy.deepcopy(cells[1]))
            cells.insert(0, copy.deepcopy(cells[0]))
            cells[0][0] = "Section"
            cells[1][0] = "Tag"
            cells[2], cells[3] = cells[3], cells[2]
        else:
            cells[0], cells[1] = cells[1], cells[0]
            for cell in cells:
                attr_ = getattr(cell, "attr", None)
                if attr_ and getattr(attr_, "col", None) == "links":
                    cells.pop(cells.index(cell))
        for cell in cells:
            if cell[0] == "Test":
                cell[0] = "Title"


@pytest.hookimpl(tryfirst=False)
def pytest_html_results_table_row(report, cells):
    # HTML Report: Set downloadable links and Test Name as 'Feature name -> Scenario name' with scenario outline sets
    if cells:
        if not bp_storage.is_api_testing():
            cells.insert(0, copy.deepcopy(cells[1]))
            cells.insert(0, copy.deepcopy(cells[0]))
            cells[0][0] = "Section"
            cells[1][0] = "Tag"
            cells[0].attr.class_ = "col-section"
            cells[1].attr.class_ = "col-tags"
            for cell in cells:
                attr_ = getattr(cell, "attr", None)
                if attr_ and len(cell) and cell[0] == "Section":
                    scenario = getattr(report, "scenario", None)
                    if isinstance(scenario, dict):
                        feature_name = scenario.get("feature", {}).get("name", "")
                        feature_name = feature_name.replace(" - ", " -> ")
                        cell[0] = feature_name
                    elif scenario is None:
                        cell[0] = ""
                if attr_ and len(cell) and cell[0] == "Tag":
                    tc_tag = ""
                    valid_tags = [tag for tag in report.keywords if
                                  isinstance(tag, str) and tag.startswith(TESTCASE_TAG_PREFIX)]
                    if len(valid_tags):
                        tc_tag = sorted(valid_tags, reverse=True)[0]
                    cell[0] = tc_tag
                if attr_ and getattr(attr_, "class_", None) == "col-name":
                    scenario = getattr(report, "scenario", None)
                    if isinstance(scenario, dict) and len(cell):
                        scenario_name = scenario.get("name", "")
                        cell[0] = scenario_name
                        if scenario.get("example", None):
                            example_data = json.dumps(scenario.get("example", ""))
                            cell[0] += "  " + remove_chars_from_string(example_data, ["{", "}", '"'])
                if attr_ and getattr(attr_, "class_", None) == "col-links":
                    for link in cell[0]:
                        if link[0] == "Browser Log":
                            setattr(link.attr, "download", f"{link[0]}")
                        elif link[0] in (
                                "URL", "Driver Log", "HTML", "Syslog Log", "Crashlog Log", "Performance Log",
                                "Logcat Log",
                                "Bugreport Log"):
                            del link[0]
            cells[2], cells[3] = cells[3], cells[2]
        else:
            cells[0], cells[1] = cells[1], cells[0]
            for cell in cells:
                if cell.attr.class_ == "col-name":
                    if hasattr(report, "test_name") and len(report.test_name):
                        cell[0] = report.test_name[0]
                attr_ = getattr(cell, "attr", None)
                if attr_ and getattr(attr_, "class_", None) == "col-links":
                    cells.pop(cells.index(cell))


def pytest_html_results_table_html(report, data):
    # HTML Report: Remove Captured Log call
    if report.passed or report.failed:
        for log_data in data:
            attr_ = getattr(log_data, "attr", None)
            if getattr(attr_, "class_", None) == "log":
                for index, element in enumerate(log_data):
                    if isinstance(element, str) and "Captured log call" in element:
                        del log_data[index: index + 4]
                        break


def pytest_html_report_title(report, title="Test Results"):
    if os.getenv("CI") == "true":
        title = title + " - " + os.getenv('GITHUB_WORKFLOW', "")
    report.title = title

    # Update the datetime of the HTML report name at the end of the session to be consistent with the HTML report data
    if getattr(report, "logfile", None) and isinstance(report.logfile, str):
        try:
            report_path = Path(report.logfile)
            substrings = report_path.stem.split('_')
            substrings[1] = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            report.logfile = str(report_path.with_stem("_".join([s for s in substrings])))
        except ValueError:
            pass


def pytest_html_results_summary(prefix, summary, postfix):
    _ = postfix
    passed_count, failed_count, skipped_count = '0', '0', '0'
    pass_rate = None
    pattern = re.compile(r"\d+")
    for element in summary:
        attr_ = getattr(element, "attr", None)
        if attr_ and getattr(attr_, "class_", None) == "passed":
            if element[0] and isinstance(element[0], str):
                result = pattern.match(element[0])
                if result:
                    passed_count = result.group()
        if attr_ and getattr(attr_, "class_", None) == "failed":
            if element[0] and isinstance(element[0], str):
                result = pattern.match(element[0])
                if result:
                    failed_count = result.group()
    if (
            isinstance(passed_count, str)
            and isinstance(failed_count, str)
            and passed_count.isnumeric()
            and failed_count.isnumeric()
            and int(passed_count) + int(failed_count) > 0
    ):
        pass_rate = float((int(passed_count) / (int(passed_count) + int(failed_count))) * 100)
    if pass_rate is not None:
        prefix.extend([html.h3(f"Pass Rate: {round(pass_rate, 2)}%")])
        if pass_rate == 100.0:
            prefix[0].attr.class_ = "green"
        else:
            prefix[0].attr.class_ = "red"

    for element in summary:
        if len(element) and "tests ran in" in element[0]:
            substrings = str(element[0]).split(' ')
            current = float(substrings[4])
            hours_ = int(current // 3600)
            minutes_ = int((current % 3600) // 60)
            seconds_ = float((current % 3600) % 60)
            hours = "{} hours {} minutes {:.2f} seconds".format(hours_, minutes_, seconds_)
            minutes = "{} minutes {:.2f} seconds".format(minutes_, seconds_)
            seconds = "{:.2f} seconds".format(seconds_)
            if current > 3600:
                element[0] = substrings[0] + " " + f"tests ran in {hours}"
            elif current > 60:
                element[0] = substrings[0] + " " + f"tests ran in {minutes}"
            else:
                element[0] = substrings[0] + " " + f"tests ran in {seconds}"
