import os
import pytest
from assertpy import assert_that


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.setup_check
def test_check_root_folder():
    assert_that(os.path.isfile("./.editorconfig")).is_true()
    assert_that(os.path.isfile("./.gitignore")).is_true()
    assert_that(os.path.isfile("./conftest.py")).is_true()
    assert_that(os.path.isfile("./setup_install.sh")).is_true()
    assert_that(os.path.isfile("./setup_install.py")).is_true()
    assert_that(os.path.isfile("./pytest.ini")).is_true()
    assert_that(os.path.isfile("./README.md")).is_true()
    assert_that(os.path.isfile("./requirements.txt")).is_true()
    assert_that(os.path.isfile("./docker-compose.yml")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.setup_check
def test_check_main_folder():
    assert_that(os.path.isfile("./main/.pylintrc")).is_true()
    assert_that(os.path.isfile("./main/plugin.py")).is_true()
    assert_that(os.path.isfile("./main/notifications/slack_plugin.py")).is_true()
    assert_that(os.path.isfile("./main/notifications/teams_plugin.py")).is_true()
    assert_that(os.path.isdir("./main/backend")).is_true()
    assert_that(os.path.isdir("./main/frontend")).is_true()
    assert_that(os.path.isdir("./main/setup")).is_true()
    assert_that(os.path.isdir("./main/lib")).is_true()
    assert_that(os.path.isdir("./main/utils")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.setup_check
def test_check_common_ui_folder():
    assert_that(
        os.path.isfile("./main/frontend/common/helpers/elements.py")
    ).is_true()
    assert_that(
        os.path.isfile("./main/frontend/common/helpers/browser.py")
    ).is_true()
    assert_that(
        os.path.isfile("./main/frontend/common/helpers/selenium_generics.py")
    ).is_true()
    assert_that(
        os.path.isfile("./main/frontend/common/helpers/app.py")
    ).is_true()
    assert_that(
        os.path.isfile("./main/frontend/common/helpers/web_compare.py")
    ).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.setup_check
def test_check_screenshots_folder():
    assert_that(os.path.isdir("./output/screenshots")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.setup_check
def test_check_step_definitions_folder():
    assert_that(os.path.isdir("./main/frontend/common/step_definitions")).is_true()
    assert_that(os.path.isfile("./main/frontend/common/step_definitions/browser_navigation.py")).is_true()
    assert_that(os.path.isfile("./main/frontend/common/step_definitions/click_touch_and_keyboard_actions.py")).is_true()
    assert_that(os.path.isfile("./main/frontend/common/step_definitions/date_time.py")).is_true()
    assert_that(os.path.isfile("./main/frontend/common/step_definitions/dropdowns.py")).is_true()
    assert_that(os.path.isfile("./main/frontend/common/step_definitions/attribute_assertion.py")).is_true()
    assert_that(os.path.isfile("./main/frontend/common/step_definitions/environment_variables.py")).is_true()
    assert_that(os.path.isfile("./main/frontend/common/step_definitions/excel_and_csv.py")).is_true()
    assert_that(os.path.isfile("./main/frontend/common/step_definitions/html_tables.py")).is_true()
    assert_that(os.path.isfile("./main/frontend/common/step_definitions/mobile_device_actions.py")).is_true()
    assert_that(os.path.isfile("./main/frontend/common/step_definitions/swipe_drag_and_drop.py")).is_true()
    assert_that(os.path.isfile("./main/frontend/common/step_definitions/text_assertion_editing.py")).is_true()
    assert_that(os.path.isfile("./main/frontend/common/step_definitions/visual_comparison.py")).is_true()
    assert_that(os.path.isfile("./main/backend/common/step_definitions/steps_common.py")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.setup_check
def test_check_test_data_folder():
    assert_that(os.path.isdir("./test_data")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.setup_check
def test_check_utils_folder():
    assert_that(os.path.isdir("./main/utils")).is_true()
    assert_that(os.path.isfile("./main/utils/env_variables.py")).is_true()
    assert_that(os.path.isfile("./main/utils/gherkin_utils.py")).is_true()
    assert_that(os.path.isfile("./main/utils/utils.py")).is_true()
    assert_that(os.path.isfile("./main/utils/faker_data.py")).is_true()
    assert_that(os.path.isfile("./main/utils/pytest_terminal_report.py")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.setup_check
def test_check_configs_folder():
    assert_that(os.path.isdir("./env_configs")).is_true()
    assert_that(os.path.isfile("./env_configs/.local.env")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.setup_check
def test_check_lib_folder():
    assert_that(os.path.isdir("./main/lib")).is_true()
    assert_that(os.path.isdir("./main/lib/pytest_testrail_client")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.setup_check
def test_check_installation_folder():
    assert_that(os.path.isdir("./main/setup")).is_true()
    assert_that(os.path.isdir("./main/setup/setup_scripts")).is_true()
    assert_that(os.path.isdir("./main/setup/setup_tests")).is_true()
    assert_that(
        os.path.isfile("./main/setup/setup_scripts/download_assets.py")
    ).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.setup_check
def test_check_binaries_folder():
    assert_that(os.path.isdir("./webdriver")).is_true()
