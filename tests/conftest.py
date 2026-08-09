import pytest
import os
import sys

# Ensure root project directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api_clients.auth_client import AuthClient
from api_clients.order_client import OrderClient
from api_clients.category_client import CategoryClient
from api_clients.product_client import ProductClient
from utils.db_connector import DBConnector
from utils.pyats_health import ContainerNetworkHealthChecker

@pytest.fixture(scope="session", autouse=True)
def run_network_health_check():
    """Session fixture to check container and port reachability before executing tests."""
    checker = ContainerNetworkHealthChecker()
    results = checker.run_pyats_testbed_check()
    yield results

@pytest.fixture
def auth_client():
    """Fixture providing AuthClient instance."""
    return AuthClient()

@pytest.fixture
def order_client():
    """Fixture providing OrderClient instance."""
    return OrderClient()

@pytest.fixture
def category_client():
    """Fixture providing CategoryClient instance."""
    return CategoryClient()

@pytest.fixture
def product_client():
    """Fixture providing ProductClient instance."""
    return ProductClient()

@pytest.fixture
def db_connector():
    """Fixture providing DBConnector instance with automatic teardown."""
    db = DBConnector()
    yield db
    db.close()
