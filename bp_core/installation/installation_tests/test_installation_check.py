import os
import pytest
from assertpy import assert_that


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.installation_check
def test_check_root_folder():
    assert_that(os.path.isfile("./.editorconfig")).is_true()
    assert_that(os.path.isfile("./.gitignore")).is_true()
    assert_that(os.path.isfile("./conftest.py")).is_true()
    assert_that(os.path.isfile("./setup_install.sh")).is_true()
    assert_that(os.path.isfile("./setup_install.py")).is_true()
    assert_that(os.path.isfile("./pytest.ini")).is_true()
    assert_that(os.path.isfile("./README.md")).is_true()
    assert_that(os.path.isfile("./requirements.txt")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.installation_check
def test_check_bp_core_folder():
    assert_that(os.path.isfile("./bp_core/.pylintrc")).is_true()
    assert_that(os.path.isfile("./bp_core/plugin.py")).is_true()
    assert_that(os.path.isfile("./bp_core/notifications/slack_plugin.py")).is_true()
    assert_that(os.path.isfile("./bp_core/notifications/teams_plugin.py")).is_true()
    assert_that(os.path.isdir("./bp_core/backend")).is_true()
    assert_that(os.path.isdir("./bp_core/frontend")).is_true()
    assert_that(os.path.isdir("./bp_core/installation")).is_true()
    assert_that(os.path.isdir("./bp_core/lib")).is_true()
    assert_that(os.path.isdir("./bp_core/utils")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.installation_check
def test_check_common_ui_folder():
    assert_that(
        os.path.isfile("./bp_core/frontend/common/helpers/elements.py")
    ).is_true()
    assert_that(
        os.path.isfile("./bp_core/frontend/common/helpers/browser.py")
    ).is_true()
    assert_that(
        os.path.isfile("./bp_core/frontend/common/helpers/selenium_generics.py")
    ).is_true()
    assert_that(
        os.path.isfile("./bp_core/frontend/common/helpers/app.py")
    ).is_true()
    assert_that(
        os.path.isfile("./bp_core/frontend/common/helpers/web_compare.py")
    ).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.installation_check
def test_check_screenshots_folder():
    assert_that(os.path.isdir("./output/screenshots")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.installation_check
def test_check_step_definitions_folder():
    assert_that(os.path.isdir("./bp_core/frontend/common/step_definitions")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/api_bdd.py")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/browser_navigation_window_tabs_and_screenshots.py")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/click_touch_and_keyboard_actions.py")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/date_time_and_pause.py")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/dropdowns.py")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/element_existence_visibility_and_attribute_assertion.py")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/environment_variables.py")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/excel_and_csv.py")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/html_tables.py")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/ionic_hybrid_mobile_apps_steps.py")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/mobile_device_actions.py")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/swipe_scroll_move_hover_drag_and_drop.py")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/text_assertion_editing_and_generation.py")).is_true()
    assert_that(os.path.isfile("./bp_core/frontend/common/step_definitions/visual_comparison.py")).is_true()
    assert_that(os.path.isdir("./bp_core/backend/common/step_definitions")).is_true()
    assert_that(os.path.isfile("./bp_core/backend/common/step_definitions/steps_common.py")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.installation_check
def test_check_test_data_folder():
    assert_that(os.path.isdir("./test_data")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.installation_check
def test_check_utils_folder():
    assert_that(os.path.isdir("./bp_core/utils")).is_true()
    assert_that(os.path.isfile("./bp_core/utils/env_variables.py")).is_true()
    assert_that(os.path.isfile("./bp_core/utils/gherkin_utils.py")).is_true()
    assert_that(os.path.isfile("./bp_core/utils/utils.py")).is_true()
    assert_that(os.path.isfile("./bp_core/utils/faker_data.py")).is_true()
    assert_that(os.path.isfile("./bp_core/utils/pytest_terminal_report.py")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.installation_check
def test_check_configs_folder():
    assert_that(os.path.isdir("./env_configs")).is_true()
    assert_that(os.path.isfile("./env_configs/.local.env")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.installation_check
def test_check_lib_folder():
    assert_that(os.path.isdir("./bp_core/lib")).is_true()
    assert_that(os.path.isdir("./bp_core/lib/pytest_testrail_client")).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.installation_check
def test_check_installation_folder():
    assert_that(os.path.isdir("./bp_core/installation")).is_true()
    assert_that(os.path.isdir("./bp_core/installation/installation_scripts")).is_true()
    assert_that(os.path.isdir("./bp_core/installation/installation_tests")).is_true()
    assert_that(
        os.path.isfile("./bp_core/installation/installation_scripts/download_assets.py")
    ).is_true()


@pytest.mark.nondestructive
@pytest.mark.automated
@pytest.mark.installation_check
def test_check_binaries_folder():
    assert_that(os.path.isdir("./webdriver")).is_true()
