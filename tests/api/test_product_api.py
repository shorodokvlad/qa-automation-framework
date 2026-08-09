import pytest
import requests
from api_clients.product_client import ProductClient

@pytest.mark.api
class TestProductAPI:
    """REST API test suite for Spring Boot Product Controller (/product/*)."""

    def test_get_all_products(self, product_client: ProductClient):
        """Verify GET /product/get-all returns 200 OK and product list payload."""
        try:
            response = product_client.get_all_products(page=0, size=10)
            assert response.status_code == 200
            data = response.json()
            assert data.get("status") == 200
            assert "productList" in data
            assert isinstance(data.get("productList"), list)
        except requests.exceptions.ConnectionError:
            pytest.skip("Spring Boot API server is offline on localhost:2424.")

    def test_search_products(self, product_client: ProductClient):
        """Verify GET /product/search?searchValue=... returns filtered results."""
        try:
            response = product_client.search_products(search_value="a", page=0, size=10)
            assert response.status_code == 200
            data = response.json()
            assert data.get("status") == 200
            assert "productList" in data
        except requests.exceptions.ConnectionError:
            pytest.skip("Spring Boot API server is offline on localhost:2424.")

    def test_get_product_by_id(self, product_client: ProductClient):
        """Verify GET /product/get-by-product-id/{id} for existing product."""
        try:
            all_resp = product_client.get_all_products()
            if all_resp.status_code == 200:
                products = all_resp.json().get("productList", [])
                if products:
                    target_id = products[0]["id"]
                    response = product_client.get_product_by_id(target_id)
                    assert response.status_code == 200
                    data = response.json()
                    assert data.get("product")["id"] == target_id
        except requests.exceptions.ConnectionError:
            pytest.skip("Spring Boot API server is offline on localhost:2424.")
