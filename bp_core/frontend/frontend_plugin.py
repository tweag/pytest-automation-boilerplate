import copy
from collections import defaultdict

import allure
import pytest

from allure_commons.types import AttachmentType

from pytest_bdd import parser as pytest_bdd_parser
from selenium.webdriver.common.proxy import Proxy, ProxyType

from bp_core.frontend.common.step_definitions import *
from bp_core.frontend.common.utils.locator_parser import Locators

from pytest_selenium.drivers import appium
from pytest_selenium.drivers import remote

import logging

from bp_core.lib.pytest_testrail_client.pytest_testrail_client import _step_error
from bp_core.utils.utils import save_base64_as_png, TEMP_SCREENSHOTS, logger

from pytest_selenium import drivers, split_class_and_test_names

blank_logger = logging.getLogger(__name__)
blank_logger.propagate = False


def pytest_bdd_before_scenario(
        request: FixtureRequest,
        feature: pytest_bdd_parser.Feature,
        scenario: pytest_bdd_parser.Scenario,
):
    """Called before every scenario execution"""
    request.node.scenarioDict = defaultdict()
    # Use built-in logger with default level warning to display only a separation line between each scenario
    blank_logger.warning("\n")

    logger.info(
        "Scenario Execution Started.", scenario_name=scenario.name, feature=feature.name
    )


# Add logging after each scenario
def pytest_bdd_after_scenario(
        feature: pytest_bdd_parser.Feature, scenario: pytest_bdd_parser.Scenario
):
    """Called after every scenario is executed"""
    logger.info(
        "Scenario Execution Completed.",
        scenario_name=scenario.name,
        feature=feature.name,
    )


# Add logging for each step
def pytest_bdd_after_step(
        request: FixtureRequest,
        feature: pytest_bdd_parser.Feature,
        scenario: pytest_bdd_parser.Scenario,
        step: pytest_bdd_parser.Step
):
    """Called after every step execution"""
    logger.info(
        "Step Executed.",
        step=step.name,
    )
    driver_ = request.getfixturevalue("selenium")
    if driver_:
        allure.attach(driver_.get_screenshot_as_png(), name="Screenshot Step : " + step.name,
                      attachment_type=AttachmentType.PNG)

    if "I take a screenshot" in step.name:
        if driver_:
            screenshot_source = driver_.get_screenshot_as_base64()
            dest_folder = Path(os.path.join(Path.cwd().resolve(), TEMP_SCREENSHOTS))
            file_name = f"{request.node.name}_{str(step.line_number)}.png"
            save_base64_as_png(data=screenshot_source, dest_folder=dest_folder,
                               dest_file_name=file_name)
            scenario_cache = request.config.cache.get(f"{feature.name}/{scenario.name}", None)
            if scenario_cache and isinstance(scenario_cache, dict):
                if request.node.name not in scenario_cache:
                    scenario_cache[request.node.name] = [screenshot_source]
                    request.config.cache.set(f"{feature.name}/{scenario.name}", scenario_cache)
                elif scenario_cache.get(request.node.name, None):
                    scenario_cache.get(request.node.name, []).append(screenshot_source)
                    request.config.cache.set(f"{feature.name}/{scenario.name}", scenario_cache)
            else:
                request.config.cache.set(f"{feature.name}/{scenario.name}",
                                         {f"{request.node.name}": [screenshot_source]})


def pytest_bdd_step_error(request: FixtureRequest,
                          feature: pytest_bdd_parser.Feature,
                          scenario: pytest_bdd_parser.Scenario,
                          step: pytest_bdd_parser.Step, exception):
    """Called on step error. Logs the error and takes a screenshot."""
    _step_error(exception, feature, scenario, step)

    driver_ = request.getfixturevalue("selenium")
    if driver_:
        allure.attach(driver_.get_screenshot_as_png(), name="Screenshot Step : " + step.name,
                      attachment_type=AttachmentType.PNG)


# Define chrome options as a fixture
@pytest.fixture
def chrome_options(chrome_options, variables, proxy_url, env_variables, request):
    file_path = Path(__file__ + "/../../../" + env_variables.get("DOWNLOAD_DIR")).resolve()
    caps = copy.deepcopy(request.getfixturevalue("session_capabilities"))

    if (caps.get("headless", "") == "True") or (
            "capabilities" in variables
            and "headless" in variables["capabilities"]
            and variables["capabilities"]["headless"] == "True"
    ):
        chrome_options.add_argument("--headless")
    caps.pop("headless", None)

    for key, value in caps.items():
        chrome_options.set_capability(key, value)

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1367,768")
    if os.environ.get("USING_DOCKER", False) == 'True':
        chrome_options.add_argument("--ignore-certificate-errors")
    if proxy_url:
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument(f"--proxy-server={proxy_url}")

    if env_variables.get("DOWNLOAD_DIR", default=False):
        chrome_options.add_experimental_option('prefs', {"download.default_directory": str(file_path)})

    chrome_options.capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    return chrome_options


# Define firefox options as a fixture
@pytest.fixture
def firefox_options(firefox_options, request, proxy_url):
    caps = copy.deepcopy(request.getfixturevalue("session_capabilities"))
    if caps.get("headless", "false").strip().lower() != "false":
        firefox_options.add_argument("-headless")
    caps.pop("headless", None)

    for key, value in caps.items():
        firefox_options.set_capability(key, value)

    if proxy_url:
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxy_url,
            'sslProxy': proxy_url
        })

        firefox_options.proxy = proxy
        firefox_options.set_capability("acceptInsecureCerts", True)
    return firefox_options


# Define MSEdge options as a fixture
@pytest.fixture
def edge_options(edge_options, request, proxy_url):
    caps = copy.deepcopy(request.getfixturevalue("session_capabilities"))
    if caps.get("headless", "false").strip().lower() != "false":
        edge_options.add_argument('--window-size=1024,768')
        edge_options.add_argument('--headless')
    caps.pop("headless", None)

    for key, value in caps.items():
        edge_options.set_capability(key, value)

    if proxy_url:
        edge_options.add_argument(f'--proxy-server={request.config.option.proxy_url}')

    return edge_options


# Define session capabilities as a fixture
# This is API & UI specific implementation
@pytest.fixture(scope="session", autouse=True)
def session_capabilities(proxy_url, session_capabilities: dict):
    if os.environ.get('BROWSERSTACK_LOCAL_IDENTIFIER'):
        session_capabilities.get("bstack:options", {}).update(
            localIdentifier=os.environ.get('BROWSERSTACK_LOCAL_IDENTIFIER'))

    return session_capabilities


@pytest.fixture(scope="session")
def driver_options_factory(session_capabilities):
    browser_name = session_capabilities.get("browserName", "").lower()
    platform_name = session_capabilities.get("platformName", "").lower()
    browser_name = "edge" if browser_name and browser_name in ("edge", "microsoftedge") else browser_name

    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.edge.options import Options as EdgeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.safari.options import Options as SafariOptions
    from appium.options.android import UiAutomator2Options as AndroidOptions
    from appium.options.ios import XCUITestOptions as IosOptions
    browser_options = dict(
        {
            "chrome": ChromeOptions,
            "edge": EdgeOptions,
            "microsoftedge": EdgeOptions,
            "firefox": FirefoxOptions,
            "safari": SafariOptions,
        }
    )
    platform_options = dict(
        {
            "android": AndroidOptions,
            "ios": IosOptions,
        }
    )

    if browser_name:
        option_class = browser_options.get(browser_name, None)
        return browser_name, option_class() if option_class else None
    elif platform_name:
        option_class = platform_options.get(platform_name, None)
        return platform_name, option_class() if option_class else None
    raise ValueError(
        f"Capability: 'browserName' or 'platformName' is not provided: browser_name: {browser_name} platform_name: {platform_name}")


@pytest.fixture(scope="session", autouse=True)
def configure_driver_executor(session_capabilities, driver_options_factory):
    if session_capabilities.get("browserstack", "False") == 'True':
        value, options = driver_options_factory

        for k, v in session_capabilities.items():
            options.set_capability(k, v)

        def driver_kwargs(capabilities, host, **kwargs):  # noqa
            _ = capabilities
            if value in ("chrome", "edge", "firefox"):
                browser_options = kwargs.get(f"{value}_options", None)
                browser_options_arguments = getattr(browser_options, "arguments", [])
                browser_options_capabilities = getattr(browser_options, "capabilities", {})
                options.capabilities.update(browser_options_capabilities)
                options.arguments.extend([x for x in browser_options_arguments if x not in options.arguments])

            executor = f"https://{host}/wd/hub"
            kwargs = {"command_executor": executor, "options": options}

            return kwargs

        appium.driver_kwargs = driver_kwargs
        remote.driver_kwargs = driver_kwargs

    # To pass options for local Android and iOS test executions
    elif session_capabilities.get("platformName", "").lower() in ("android", "ios"):
        value, options = driver_options_factory
        for k, v in session_capabilities.items():
            options.set_capability(k, v)

        def driver_kwargs(capabilities, host, port, **kwargs):
            # capabilities and **kwargs variable are required to maintain compatibility with the pytest_selenium fixture
            _ = capabilities, kwargs
            protocol = "http"
            host = host if host.startswith(protocol) else f"{protocol}://{host}"
            executor = f"{host}:{port}"
            kwargs = {"command_executor": executor, "options": options}

            return kwargs

        appium.driver_kwargs = driver_kwargs

    elif os.environ.get("USING_DOCKER", "False") == 'True':
        value, options = driver_options_factory
        for k, v in session_capabilities.items():
            options.set_capability(k, v)

        def driver_kwargs(capabilities, host, port, **kwargs):  # noqa
            _ = capabilities
            if value in ("chrome", "edge", "firefox"):
                browser_options = kwargs.get(f"{value}_options", None)
                browser_options_arguments = getattr(browser_options, "arguments", [])
                browser_options_capabilities = getattr(browser_options, "capabilities", {})
                options.capabilities.update(browser_options_capabilities)
                options.arguments.extend([x for x in browser_options_arguments if x not in options.arguments])

            executor = f"http://{host}:{port}/wd/hub"
            kwargs = {"command_executor": executor, "options": options}

            return kwargs

        remote.driver_kwargs = driver_kwargs


# Define selenium generics as a fixture
# This is UI specific implementation
@pytest.fixture
def selenium_generics(selenium) -> SeleniumGenerics:
    return SeleniumGenerics(selenium)


# Define the locators in case of specific path to the locators values
# This is UI specific implementation
@pytest.fixture(scope="session", autouse=True)
def locators(request) -> Locators:
    locator_path = request.config.getoption("--locators")
    return Locators(locator_path)


# Define capabilities as a fixture
# This is UI specific implementation
@pytest.fixture
def capabilities(capabilities):
    if "browser" in capabilities and capabilities["browser"] in [
        "Edge",
        "MicrosoftEdge",
    ]:
        capabilities["browserstack.edge.enablePopups"] = "true"
    if "browser" in capabilities and capabilities["browser"] in ["safari", "Safari"]:
        capabilities["browserstack.safari.enablePopups"] = "true"
    return capabilities


# This is a temporary solution until the pytest-selenium fix the support for the Selenium 4.10+
@pytest.fixture
def driver_kwargs(
        request,
        chrome_options,
        driver_args,
        driver_class,
        driver_log,
        driver_path,
        firefox_options,
        edge_options,
        pytestconfig,
):
    kwargs = {}
    driver = getattr(drivers, pytestconfig.getoption("driver").lower())

    capabilities = kwargs.get("capabilities", None)

    kwargs.update(
        driver.driver_kwargs(
            capabilities=capabilities,
            chrome_options=chrome_options,
            driver_args=driver_args,
            driver_log=driver_log,
            driver_path=driver_path,
            firefox_options=firefox_options,
            edge_options=edge_options,
            host=pytestconfig.getoption("selenium_host"),
            port=pytestconfig.getoption("selenium_port"),
            service_log_path=None,
            request=request,
            test=".".join(split_class_and_test_names(request.node.nodeid)),
        )
    )
    pytestconfig._driver_log = driver_log

    # Workaround for the pytest-selenium library not to use variables: 'desired_capabilities' and 'service_log_path' in the Selenium lib.
    if "desired_capabilities" in kwargs:
        del kwargs["desired_capabilities"]
    if "service_log_path" in kwargs:
        del kwargs["service_log_path"]

    return kwargs
