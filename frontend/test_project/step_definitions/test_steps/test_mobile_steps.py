import os

from pytest_bdd import scenarios
from bp_core.plugin import PROJECT_DIR
from frontend.test_project.step_definitions.shared_steps.common_steps import *
from bp_core.frontend.common.step_definitions import *


scenarios(os.path.join(PROJECT_DIR, "frontend/test_project/features/mobile/ios_login.feature"))
scenarios(os.path.join(PROJECT_DIR, "frontend/test_project/features/mobile/android_login.feature"))





