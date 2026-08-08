import requests
from typing import Dict, Any, List, Optional
from .base_client import BaseClient

class OrderClient(BaseClient):
    """
    API client for Spring Boot Order Management Endpoints (/order/*).
    """

    def place_order(self, total_price: float, items: List[Dict[str, Any]]) -> requests.Response:
        """
        POST /order/create
        Payload format:
        {
           "totalPrice": 150.00,
           "items": [
               {"productId": 1, "quantity": 2, "price": 75.00}
           ]
        }
        """
        payload = {
            "totalPrice": total_price,
            "items": items
        }
        return self.post("/order/create", json_data=payload)

    def update_order_item_status(self, order_item_id: int, status: str) -> requests.Response:
        """PUT /order/update-item-status/{orderItemId}?status=COMPLETED"""
        endpoint = f"/order/update-item-status/{order_item_id}"
        return self.put(endpoint, params={"status": status})

    def filter_order_items(self, status: Optional[str] = None, page: int = 0, size: int = 100) -> requests.Response:
        """GET /order/filter"""
        params = {"page": page, "size": size}
        if status:
            params["status"] = status
        return self.get("/order/filter", params=params)
