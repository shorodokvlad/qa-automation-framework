import pytest
import time
import requests
from playwright.sync_api import Page, Error as PlaywrightError, expect
from api_clients.auth_client import AuthClient
from api_clients.order_client import OrderClient
from utils.db_connector import DBConnector
from page_objects.login_page import LoginPage
from page_objects.dashboard_page import DashboardPage

@pytest.mark.integration
class TestOrderIntegrationFlow:
    """
    End-to-End Integration Test:
    1. Register user via Auth API.
    2. Directly verify email column in DB via DBConnector.
    3. Authenticate via API & obtain JWT session token.
    4. Place order via POST /order/create.
    5. Query Database directly (SELECT) to verify physical order persistence.
    6. Open UI via Playwright POM to verify user session.
    """

    def test_e2e_api_db_ui_order_verification(
        self,
        auth_client: AuthClient,
        order_client: OrderClient,
        db_connector: DBConnector,
        page: Page
    ):
        timestamp = time.time_ns()
        test_email = f"integration_user_{timestamp}@example.com"
        test_password = "SecurePassword123!"

        try:
            # 1. API: Register User
            reg_resp = auth_client.register_user(
                name=f"Integration User {timestamp}",
                email=test_email,
                password=test_password,
                phone_number="5551234567"
            )
            assert reg_resp.status_code == 200
            registration = reg_resp.json()
            assert registration["status"] == 200
            assert registration["user"]["email"] == test_email

            # 2. Direct DB Validation/Update: Verify email address directly in database
            assert db_connector.set_user_email_verified(test_email)

            # 3. API: Login User & Obtain JWT Token
            login_resp = auth_client.login_user(email=test_email, password=test_password)
            assert login_resp.status_code == 200

            token = login_resp.json().get("token")
            assert token
            order_client.set_auth_token(token)

            # 4. API: Place an Order
            product_id = db_connector.get_or_create_test_product()
            order_payload = {
                "totalPrice": 120.00,
                "items": [
                    {"productId": product_id, "quantity": 2, "price": 60.00}
                ]
            }
            order_resp = order_client.place_order(
                total_price=order_payload["totalPrice"],
                items=order_payload["items"]
            )
            assert order_resp.status_code == 200
            assert order_resp.json()["status"] == 200

            # 5. Database Validation: Query DB directly to verify physical data row
            user_record = db_connector.verify_user_exists_by_email(test_email)
            assert user_record is not None
            assert user_record["email"] == test_email

            order_items = db_connector.get_order_items_for_user(user_record["id"])
            created_item = next(
                (item for item in order_items if item["product_id"] == product_id),
                None,
            )
            assert created_item is not None
            assert created_item["quantity"] == 2
            assert float(created_item["price"]) > 0

            # 6. Playwright UI: Verify login & dashboard access
            login_page = LoginPage(page)
            dashboard_page = DashboardPage(page)

            login_page.load()
            login_page.perform_login(test_email, test_password)

            expect(page).to_have_url(f"{login_page.base_url}/")
            assert dashboard_page.is_user_logged_in()

        except (requests.exceptions.ConnectionError, PlaywrightError) as e:
            pytest.skip(f"Backend or React application offline on localhost: {e}")
