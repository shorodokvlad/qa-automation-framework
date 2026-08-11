import pytest
import requests
from api_clients.category_client import CategoryClient

@pytest.mark.api
class TestCategoryAPI:
    """REST API test suite for Spring Boot Category Controller (/category/*)."""

    def test_get_all_categories(self, category_client: CategoryClient):
        """Verify GET /category/get-all returns 200 OK and category list payload."""
        try:
            response = category_client.get_all_categories()
            assert response.status_code == 200
            data = response.json()
            assert data.get("status") == 200
            assert "categoryList" in data
            assert isinstance(data.get("categoryList"), list)
        except requests.exceptions.ConnectionError:
            pytest.skip("Spring Boot API server is offline on localhost:2424.")

    def test_get_category_by_id(self, category_client: CategoryClient):
        """Verify GET /category/get-category-by-id/{id} for valid category."""
        try:
            all_resp = category_client.get_all_categories()
            assert all_resp.status_code == 200
            categories = all_resp.json()["categoryList"]
            assert categories, "At least one seeded category is required for this test"

            target_id = categories[0]["id"]
            response = category_client.get_category_by_id(target_id)
            assert response.status_code == 200
            data = response.json()
            assert data["category"]["id"] == target_id
        except requests.exceptions.ConnectionError:
            pytest.skip("Spring Boot API server is offline on localhost:2424.")

    def test_create_category_unauthorized_fails(self, category_client: CategoryClient):
        """Verify POST /category/create fails without ADMIN JWT authorization header."""
        try:
            category_client.clear_auth_token()
            response = category_client.create_category("Unauthorized Category")
            assert response.status_code in (401, 403)
        except requests.exceptions.ConnectionError:
            pytest.skip("Spring Boot API server is offline on localhost:2424.")
