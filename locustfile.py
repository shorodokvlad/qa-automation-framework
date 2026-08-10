"""
Locust Performance & Load Testing Suite
========================================
Simulates concurrent user load (e.g., 100 virtual users) searching products,
browsing category catalogs, and calling Spring Boot REST API endpoints.

Usage:
  Interactive Web UI:
    locust -f locustfile.py --host http://localhost:2424
    (Open http://localhost:8089 in your browser)

  Headless CLI Mode (100 concurrent users, spawn rate 10/s, 1 minute duration):
    locust -f locustfile.py --headless -u 100 -r 10 --run-time 1m --host http://localhost:2424
"""

import os
import random
import logging
from locust import HttpUser, task, between, events

logger = logging.getLogger(__name__)

SEARCH_KEYWORDS = [
    "shirt", "phone", "laptop", "shoe", "watch",
    "book", "jacket", "headphones", "bag", "a", "e", "i", "o", "u"
]

SAMPLE_PRODUCT_IDS = list(range(1, 21))
SAMPLE_CATEGORY_IDS = list(range(1, 6))

class SpringEcommerceUser(HttpUser):
    """
    Simulates a realistic customer browsing the Spring Boot E-Commerce application.
    Executes product searches, category browsing, product detail viewings, and health checks.
    """

    # Simulate 1 to 3 seconds of think time between user requests
    wait_time = between(1, 3)

    def on_start(self):
        """
        Executed when a virtual user starts. Attempts optional JWT login or sets up headers.
        """
        self.client.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        
        # Optional: Attempt test user login if backend auth is available
        auth_email = os.getenv("TEST_USER_EMAIL", "testuser@example.com")
        auth_password = os.getenv("TEST_USER_PASSWORD", "Password123!")

        try:
            with self.client.post(
                "/auth/login",
                json={"email": auth_email, "password": auth_password},
                name="/auth/login (on_start)",
                catch_response=True
            ) as response:
                if response.status_code == 200:
                    data = response.json()
                    token = data.get("token")
                    if token:
                        self.client.headers.update({"Authorization": f"Bearer {token}"})
                        logger.info("Locust virtual user successfully authenticated with JWT token.")
                else:
                    # Non-fatal if test user doesn't exist; continue as unauthenticated guest user
                    response.ignore()
        except Exception as e:
            logger.debug(f"Auth login skipped on start: {e}")

    @task(4)
    def search_products(self):
        """
        Simulate product search queries with dynamic search terms.
        Endpoint: GET /product/search?searchValue=...&page=0&size=10
        """
        keyword = random.choice(SEARCH_KEYWORDS)
        params = {
            "searchValue": keyword,
            "page": 0,
            "size": 10
        }
        with self.client.get(
            "/product/search",
            params=params,
            name="/product/search",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # 404 can be acceptable if search returned no products
                response.success()
            else:
                response.failure(f"Product search failed with status code {response.status_code}: {response.text}")

    @task(3)
    def get_all_products(self):
        """
        Simulate browsing all products catalog with pagination.
        Endpoint: GET /product/get-all?page=0&size=10
        """
        params = {"page": 0, "size": 10}
        with self.client.get(
            "/product/get-all",
            params=params,
            name="/product/get-all",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Get all products failed with status {response.status_code}")

    @task(3)
    def get_product_by_id(self):
        """
        Simulate viewing product detail page.
        Endpoint: GET /product/get-by-product-id/{productId}
        """
        product_id = random.choice(SAMPLE_PRODUCT_IDS)
        with self.client.get(
            f"/product/get-by-product-id/{product_id}",
            name="/product/get-by-product-id/[id]",
            catch_response=True
        ) as response:
            if response.status_code in (200, 404):
                response.success()
            else:
                response.failure(f"Get product by ID {product_id} failed with status {response.status_code}")

    @task(2)
    def get_all_categories(self):
        """
        Simulate fetching all product categories.
        Endpoint: GET /category/get-all
        """
        with self.client.get(
            "/category/get-all",
            name="/category/get-all",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Get categories failed with status {response.status_code}")

    @task(2)
    def get_products_by_category(self):
        """
        Simulate filtering products by category ID.
        Endpoint: GET /product/get-by-category-id/{categoryId}?page=0&size=10
        """
        category_id = random.choice(SAMPLE_CATEGORY_IDS)
        params = {"page": 0, "size": 10}
        with self.client.get(
            f"/product/get-by-category-id/{category_id}",
            params=params,
            name="/product/get-by-category-id/[id]",
            catch_response=True
        ) as response:
            if response.status_code in (200, 404):
                response.success()
            else:
                response.failure(f"Get products by category ID {category_id} failed with status {response.status_code}")

    @task(1)
    def check_health(self):
        """
        Simulate auth service health check ping.
        Endpoint: GET /auth/health
        """
        with self.client.get(
            "/auth/health",
            name="/auth/health",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed with status {response.status_code}")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logger.info(">>> Locust Load Test Started: Simulating virtual users on Spring Boot REST API <<<")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    logger.info(">>> Locust Load Test Completed <<<")

