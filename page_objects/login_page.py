from playwright.sync_api import Page, expect
from .base_page import BasePage

class LoginPage(BasePage):
    """
    Page Object Model representing the React E-Commerce Login Page (/login).
    Hides internal locators (CSS/XPath) and exposes action methods.
    """

    # Locators
    EMAIL_INPUT = "input[name='email']"
    PASSWORD_INPUT = "input[name='password']"
    SUBMIT_BUTTON = ".register-page form button[type='submit'], form button:has-text('Login')"
    MESSAGE_BANNER = ".message"
    REGISTER_LINK = ".register-link a"
    PAGE_HEADER = "h2"

    def __init__(self, page: Page):
        super().__init__(page)
        self.path = "/login"

    def load(self):
        """Navigate directly to the Login page."""
        self.navigate_to(self.path)
        self.page.wait_for_selector(self.PAGE_HEADER)

    def enter_email(self, email: str):
        """Fill email input field."""
        self.fill_input(self.EMAIL_INPUT, email)

    def enter_password(self, password: str):
        """Fill password input field."""
        self.fill_input(self.PASSWORD_INPUT, password)

    def click_login(self):
        """Click submit button."""
        self.click_element(self.SUBMIT_BUTTON)

    def perform_login(self, email: str, password: str):
        """High-level method to enter credentials and click login."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Fetch error message from error banner."""
        if self.is_element_visible(self.MESSAGE_BANNER):
            return self.get_element_text(self.MESSAGE_BANNER)
        return ""

    def click_register_link(self):
        """Click link to navigate to registration page."""
        self.click_element(self.REGISTER_LINK)
