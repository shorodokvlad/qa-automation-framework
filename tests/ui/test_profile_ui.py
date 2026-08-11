import pytest
from playwright.sync_api import Page, Error as PlaywrightError, expect
from page_objects.profile_page import ProfilePage

@pytest.mark.ui
class TestProfileUI:
    """Playwright UI automation test suite for User Profile Page (/profile)."""

    def test_profile_page_navigation(self, page: Page):
        """Verify an unauthenticated user is redirected from Profile to Login."""
        profile_page = ProfilePage(page)
        try:
            page.add_init_script(
                "window.localStorage.removeItem('token'); window.localStorage.removeItem('role')"
            )
            profile_page.load()
            expect(page).to_have_url(f"{profile_page.base_url}/login")
        except PlaywrightError as e:
            if "ERR_CONNECTION_REFUSED" in str(e):
                pytest.skip("React UI server is offline on localhost:3000.")
            raise e
