import pytest
import os
import sys
from pytest import ExitCode

# Ensure root project directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api_clients.auth_client import AuthClient
from api_clients.order_client import OrderClient
from api_clients.category_client import CategoryClient
from api_clients.product_client import ProductClient
from utils.db_connector import DBConnector


def pytest_sessionfinish(session, exitstatus):
    """Make skipped tests fail CI when the application stack is required."""
    if os.getenv("FAIL_ON_SKIPPED", "false").lower() != "true":
        return

    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    if reporter and reporter.stats.get("skipped"):
        session.exitstatus = ExitCode.TESTS_FAILED

@pytest.fixture
def auth_client():
    """Fixture providing AuthClient instance."""
    client = AuthClient()
    yield client
    client.session.close()

@pytest.fixture
def order_client():
    """Fixture providing OrderClient instance."""
    client = OrderClient()
    yield client
    client.session.close()

@pytest.fixture
def category_client():
    """Fixture providing CategoryClient instance."""
    client = CategoryClient()
    yield client
    client.session.close()

@pytest.fixture
def product_client():
    """Fixture providing ProductClient instance."""
    client = ProductClient()
    yield client
    client.session.close()

@pytest.fixture
def db_connector():
    """Fixture providing DBConnector instance with automatic teardown."""
    db = DBConnector()
    yield db
    db.close()
