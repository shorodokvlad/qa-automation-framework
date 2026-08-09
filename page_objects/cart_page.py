from playwright.sync_api import Page, expect
from .base_page import BasePage

class CartPage(BasePage):
    """
    Page Object Model representing the React E-Commerce Cart Page (/cart).
    Encapsulates shopping cart locators and interaction methods.
    """

    # Locators
    CART_PAGE_CONTAINER = ".cart-page"
    EMPTY_CART_CONTAINER = ".cart-empty"
    BROWSE_CATALOG_LINK = ".cart-empty a"
    CART_LAYOUT = ".cart-layout"
    CART_ITEMS_LIST = ".cart-items"
    CART_ITEM = ".cart-item"
    CHECKOUT_BUTTON = ".checkout-button"
    SUMMARY_SECTION = ".cart-summary"
    RESPONSE_MESSAGE = ".response-message"

    def __init__(self, page: Page):
        super().__init__(page)
        self.path = "/cart"

    def load(self):
        """Navigate directly to Cart page."""
        self.navigate_to(self.path)
        self.page.wait_for_selector(self.CART_PAGE_CONTAINER)

    def is_cart_empty(self) -> bool:
        """Check if empty cart banner is displayed."""
        return self.is_element_visible(self.EMPTY_CART_CONTAINER, timeout=3000)

    def click_browse_catalog(self):
        """Click 'Browse the Catalogue' link in empty cart state."""
        self.click_element(self.BROWSE_CATALOG_LINK)

    def get_cart_item_count(self) -> int:
        """Get total number of rendered item cards in cart."""
        if self.is_element_visible(self.CART_ITEM, timeout=2000):
            return self.page.locator(self.CART_ITEM).count()
        return 0

    def click_checkout(self):
        """Click Place Order checkout button."""
        self.click_element(self.CHECKOUT_BUTTON)
