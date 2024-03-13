import pytest


# We need this fixture to override the pytest_selenium default implementation for non-bdd tests
@pytest.fixture
def driver():
    return
