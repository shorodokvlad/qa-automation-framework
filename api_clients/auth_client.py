import requests
from typing import Dict, Any, Optional
from .base_client import BaseClient

class AuthClient(BaseClient):
    """
    API client for Spring Boot Authentication Endpoints (/auth/*).
    """

    def register_user(self, name: str, email: str, password: str, phone_number: str, role: str = "USER") -> requests.Response:
        """POST /auth/register"""
        payload = {
            "name": name,
            "email": email,
            "password": password,
            "phoneNumber": phone_number,
            "role": role
        }
        return self.post("/auth/register", json_data=payload)

    def login_user(self, email: str, password: str) -> requests.Response:
        """POST /auth/login - returns JWT token and user info on success."""
        payload = {
            "email": email,
            "password": password
        }
        response = self.post("/auth/login", json_data=payload)
        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            if token:
                self.set_auth_token(token)
        return response

    def check_health(self) -> requests.Response:
        """GET /auth/health"""
        return self.get("/auth/health")
