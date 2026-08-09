import requests
from typing import Dict, Any, Optional
from .base_client import BaseClient

class CategoryClient(BaseClient):
    """
    API client for Spring Boot Category Endpoints (/category/*).
    """

    def get_all_categories(self) -> requests.Response:
        """GET /category/get-all"""
        return self.get("/category/get-all")

    def get_category_by_id(self, category_id: int) -> requests.Response:
        """GET /category/get-category-by-id/{categoryId}"""
        return self.get(f"/category/get-category-by-id/{category_id}")

    def create_category(self, name: str) -> requests.Response:
        """POST /category/create (Requires ADMIN authority)"""
        payload = {"name": name}
        return self.post("/category/create", json_data=payload)

    def update_category(self, category_id: int, name: str) -> requests.Response:
        """PUT /category/update/{categoryId} (Requires ADMIN authority)"""
        payload = {"name": name}
        return self.put(f"/category/update/{category_id}", json_data=payload)

    def delete_category(self, category_id: int) -> requests.Response:
        """DELETE /category/delete/{categoryId} (Requires ADMIN authority)"""
        url = f"{self.base_url}/category/delete/{category_id}"
        return self.session.delete(url)
