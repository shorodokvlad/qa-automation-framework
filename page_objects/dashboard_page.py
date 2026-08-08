from playwright.sync_api import Page, expect
from .base_page import BasePage

class DashboardPage(BasePage):
    """
    Page Object Model representing the React E-Commerce Home / Dashboard Page.
    Handles product catalog interactions, navigation bar, and user session verification.
    """

    # Locators
    NAVBAR = "nav, .navbar"
    LOGOUT_BUTTON = "button.logout-btn, button:has-text('Logout')"
    PROFILE_LINK = "a[href='/profile']"
    CART_LINK = "a[href='/cart']"
    PRODUCT_CARDS = ".product-card, .product-item, div.product"
    SEARCH_INPUT = "input[placeholder*='Search']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.path = "/"

    def load(self):
        """Navigate to the main home/dashboard page."""
        self.navigate_to(self.path)

    def is_user_logged_in(self) -> bool:
        """Verify presence of profile link or logout button."""
        return self.is_element_visible(self.PROFILE_LINK, timeout=3000) or self.is_element_visible(self.LOGOUT_BUTTON, timeout=3000)

    def get_product_count(self) -> int:
        """Get total number of rendered product cards."""
        self.page.wait_for_selector(self.PRODUCT_CARDS, timeout=5000)
        return self.page.locator(self.PRODUCT_CARDS).count()

    def navigate_to_cart(self):
        """Click cart link in navbar."""
        self.click_element(self.CART_LINK)

    def click_logout(self):
        """Perform logout action."""
        if self.is_element_visible(self.LOGOUT_BUTTON):
            self.click_element(self.LOGOUT_BUTTON)
