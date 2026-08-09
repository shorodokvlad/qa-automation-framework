import requests
from typing import Dict, Any, Optional
from .base_client import BaseClient

class ProductClient(BaseClient):
    """
    API client for Spring Boot Product Endpoints (/product/*).
    """

    def get_all_products(self, page: Optional[int] = None, size: Optional[int] = None) -> requests.Response:
        """GET /product/get-all"""
        params = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        return self.get("/product/get-all", params=params)

    def get_product_by_id(self, product_id: int) -> requests.Response:
        """GET /product/get-by-product-id/{productId}"""
        return self.get(f"/product/get-by-product-id/{product_id}")

    def get_products_by_category(self, category_id: int, page: Optional[int] = None, size: Optional[int] = None) -> requests.Response:
        """GET /product/get-by-category-id/{categoryId}"""
        params = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        return self.get(f"/product/get-by-category-id/{category_id}", params=params)

    def search_products(self, search_value: str, page: Optional[int] = None, size: Optional[int] = None) -> requests.Response:
        """GET /product/search?searchValue=..."""
        params = {"searchValue": search_value}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        return self.get("/product/search", params=params)

    def delete_product(self, product_id: int) -> requests.Response:
        """DELETE /product/delete/{productId} (Requires ADMIN)"""
        url = f"{self.base_url}/product/delete/{product_id}"
        return self.session.delete(url)
