from playwright.sync_api import Page, expect
from .base_page import BasePage

class ProfilePage(BasePage):
    """
    Page Object Model representing the React User Profile Page (/profile).
    Encapsulates profile details, address section, and order history locators.
    """

    # Locators
    PROFILE_PAGE_CONTAINER = ".profile-page"
    GREETING_HEADER = ".profile-page h2"
    LOGOUT_BUTTON = "button:has-text('Log Out')"
    ADDRESS_BUTTON = "button.profile-button"
    ORDER_HISTORY_LIST = ".profile-page ul"
    ERROR_MESSAGE = ".error-message"

    def __init__(self, page: Page):
        super().__init__(page)
        self.path = "/profile"

    def load(self):
        """Navigate directly to Profile page."""
        self.navigate_to(self.path)
        self.page.wait_for_timeout(1000)

    def is_user_greeting_visible(self) -> bool:
        """Check if user greeting header is visible."""
        return self.is_element_visible(self.GREETING_HEADER, timeout=3000)

    def click_logout(self):
        """Click logout button in profile header."""
        self.click_element(self.LOGOUT_BUTTON)
