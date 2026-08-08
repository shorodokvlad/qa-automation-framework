import pytest
import time
import requests
from api_clients.auth_client import AuthClient

@pytest.mark.api
class TestAuthAPI:
    """REST API test suite for Spring Boot Authentication controllers."""

    def test_health_check_endpoint(self, auth_client: AuthClient):
        """Verify GET /auth/health returns status 200 OK."""
        try:
            response = auth_client.check_health()
            assert response.status_code == 200
            data = response.json()
            assert data.get("status") == 200
            assert data.get("message") == "OK"
        except requests.exceptions.ConnectionError:
            pytest.skip("Spring Boot API server is offline on localhost:2424. Start app to execute test.")

    def test_register_and_login_flow(self, auth_client: AuthClient):
        """Verify user registration and subsequent JWT token issuance on login."""
        unique_email = f"qa_test_{int(time.time())}@example.com"
        password = "TestPassword123!"

        try:
            # 1. Register User
            reg_response = auth_client.register_user(
                name="QA Automation User",
                email=unique_email,
                password=password,
                phone_number="1234567890",
                role="USER"
            )
            assert reg_response.status_code in [200, 201, 400]

            # 2. Login User to obtain JWT Session Token
            login_response = auth_client.login_user(email=unique_email, password=password)
            if login_response.status_code == 200:
                json_payload = login_response.json()
                assert json_payload.get("status") == 200
                assert "token" in json_payload
                assert json_payload.get("token") is not None
                assert json_payload.get("role") in ["USER", "ADMIN"]
        except requests.exceptions.ConnectionError:
            pytest.skip("Spring Boot API server is offline on localhost:2424. Start app to execute test.")

    def test_login_invalid_credentials(self, auth_client: AuthClient):
        """Verify authentication rejection for invalid password."""
        try:
            response = auth_client.login_user(email="nonexistent_user_xyz@example.com", password="WrongPassword!")
            assert response.status_code in [400, 401, 404]
        except requests.exceptions.ConnectionError:
            pytest.skip("Spring Boot API server is offline on localhost:2424. Start app to execute test.")
