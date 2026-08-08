import pytest
import os
import sys

# Ensure root project directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api_clients.auth_client import AuthClient
from api_clients.order_client import OrderClient
from utils.db_connector import DBConnector
from utils.pyats_health import ContainerNetworkHealthChecker

@pytest.fixture(scope="session", autouse=True)
def run_network_health_check():
    """Session fixture to check container and port reachability before executing tests."""
    checker = ContainerNetworkHealthChecker()
    results = checker.run_pyats_testbed_check()
    yield results

@pytest.fixture(scope="session")
def browser(playwright):
    """Override Playwright browser fixture to handle missing browser binaries gracefully."""
    try:
        browser = playwright.chromium.launch()
        yield browser
        browser.close()
    except Exception as e:
        pytest.skip(f"Playwright browser binary launch skipped: {e}")

@pytest.fixture
def auth_client():
    """Fixture providing AuthClient instance."""
    return AuthClient()

@pytest.fixture
def order_client():
    """Fixture providing OrderClient instance."""
    return OrderClient()

@pytest.fixture
def db_connector():
    """Fixture providing DBConnector instance with automatic teardown."""
    db = DBConnector()
    yield db
    db.close()
