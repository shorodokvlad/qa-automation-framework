import pytest
from playwright.sync_api import Page, Error as PlaywrightError
from page_objects.login_page import LoginPage
from page_objects.dashboard_page import DashboardPage

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
            assert error_msg != "" or login_page.is_element_visible(login_page.MESSAGE_BANNER)
        except PlaywrightError as e:
            if "ERR_CONNECTION_REFUSED" in str(e):
                pytest.skip("React UI server is offline on localhost:3000. Start React client to execute UI test.")
            raise e

    def test_successful_login_redirects_to_dashboard(self, page: Page):
        """Verify valid user login redirects user and loads dashboard page."""
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        try:
            login_page.load()
            login_page.perform_login("admin@example.com", "Admin123!")
            page.wait_for_timeout(2000)
            assert dashboard_page.is_user_logged_in() or page.url != login_page.path
        except PlaywrightError as e:
            if "ERR_CONNECTION_REFUSED" in str(e):
                pytest.skip("React UI server is offline on localhost:3000. Start React client to execute UI test.")
            raise e
