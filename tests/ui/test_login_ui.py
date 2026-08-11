import pytest
import time
import requests
from playwright.sync_api import Page, Error as PlaywrightError, expect
from api_clients.auth_client import AuthClient
from page_objects.login_page import LoginPage
from page_objects.dashboard_page import DashboardPage
from utils.db_connector import DBConnector

@pytest.mark.ui
class TestLoginUI:
    """Playwright UI automation test suite using Page Object Model (POM)."""

    def test_navigation_to_login_page(self, page: Page):
        """Verify navigation to Login page loads form inputs correctly."""
        login_page = LoginPage(page)
        try:
            login_page.load()
            assert login_page.is_element_visible(login_page.EMAIL_INPUT)
            assert login_page.is_element_visible(login_page.PASSWORD_INPUT)
            assert login_page.is_element_visible(login_page.SUBMIT_BUTTON)
        except PlaywrightError as e:
            if "ERR_CONNECTION_REFUSED" in str(e):
                pytest.skip("React UI server is offline on localhost:3000. Start React client to execute UI test.")
            raise e

    def test_login_with_invalid_credentials(self, page: Page):
        """Verify UI displays error message when invalid credentials are submitted."""
        login_page = LoginPage(page)
        try:
            login_page.load()
            login_page.perform_login("invalid_user@example.com", "WrongPass123")
            error_msg = login_page.get_error_message()
            assert error_msg
        except PlaywrightError as e:
            if "ERR_CONNECTION_REFUSED" in str(e):
                pytest.skip("React UI server is offline on localhost:3000. Start React client to execute UI test.")
            raise e

    @pytest.mark.integration
    def test_successful_login_redirects_to_dashboard(
        self,
        page: Page,
        auth_client: AuthClient,
        db_connector: DBConnector,
    ):
        """Verify valid user login redirects user and loads dashboard page."""
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        email = f"ui_login_{time.time_ns()}@example.com"
        password = "UiTestPassword123!"

        try:
            registration = auth_client.register_user(
                name="UI Login Test User",
                email=email,
                password=password,
                phone_number="1234567890",
            )
            assert registration.status_code == 200
            assert db_connector.set_user_email_verified(email)

            login_page.load()
            login_page.perform_login(email, password)

            expect(page).to_have_url(f"{login_page.base_url}/")
            assert page.evaluate("localStorage.getItem('token')")
            assert dashboard_page.is_user_logged_in()
        except (PlaywrightError, requests.exceptions.ConnectionError) as e:
            if isinstance(e, requests.exceptions.ConnectionError) or "ERR_CONNECTION_REFUSED" in str(e):
                pytest.skip("React UI or Spring Boot API server is offline.")
            raise e
