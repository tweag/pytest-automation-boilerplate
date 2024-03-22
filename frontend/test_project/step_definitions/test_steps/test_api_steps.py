import os

from pytest_bdd import scenarios

from frontend.test_project.step_definitions.shared_steps.api_common import *
from frontend.test_project.step_definitions.shared_steps.api_sample import *
from frontend.test_project.step_definitions.shared_steps.api_assertions import *
from bp_core.plugin import PROJECT_DIR

scenarios(os.path.join(PROJECT_DIR, "frontend/test_project/features/api/api_tests.feature"))



