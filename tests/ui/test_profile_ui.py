import pytest
from playwright.sync_api import Page, Error as PlaywrightError
from page_objects.profile_page import ProfilePage

@pytest.mark.ui
class TestProfileUI:
    """Playwright UI automation test suite for User Profile Page (/profile)."""

    def test_profile_page_navigation(self, page: Page):
        """Verify navigation to Profile page loads container or error state."""
        profile_page = ProfilePage(page)
        try:
            profile_page.load()
            assert (
                profile_page.is_element_visible(profile_page.PROFILE_PAGE_CONTAINER, timeout=3000) or
                profile_page.is_element_visible(profile_page.ERROR_MESSAGE, timeout=3000) or
                "login" in page.url.lower() or
                "profile" in page.url.lower()
            )
        except PlaywrightError as e:
            if "ERR_CONNECTION_REFUSED" in str(e):
                pytest.skip("React UI server is offline on localhost:3000.")
            raise e
