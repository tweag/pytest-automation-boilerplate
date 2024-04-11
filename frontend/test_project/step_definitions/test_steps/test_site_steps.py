import os

from pytest_bdd import scenarios
from frontend.test_project.step_definitions.shared_steps.common_steps import *
from main.plugin import PROJECT_DIR

scenarios(os.path.join(PROJECT_DIR, "frontend/test_project/features/web/web_tests.feature"))
scenarios(os.path.join(PROJECT_DIR, "frontend/test_project/features/visual/visual_tests.feature"))
scenarios(os.path.join(PROJECT_DIR, "frontend/test_project/features/web/email_tests.feature"))





