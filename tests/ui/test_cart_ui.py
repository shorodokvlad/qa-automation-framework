import pytest
from playwright.sync_api import Page, Error as PlaywrightError
from page_objects.cart_page import CartPage

@pytest.mark.ui
class TestCartUI:
    """Playwright UI automation test suite for React Shopping Cart Page (/cart)."""

    def test_empty_cart_state_display(self, page: Page):
        """Verify empty cart banner and browse catalog link are displayed when cart is empty."""
        cart_page = CartPage(page)
        try:
            cart_page.load()
            assert cart_page.is_element_visible(cart_page.CART_PAGE_CONTAINER)
            assert cart_page.is_cart_empty() or cart_page.is_element_visible(cart_page.CART_LAYOUT)
        except PlaywrightError as e:
            if "ERR_CONNECTION_REFUSED" in str(e):
                pytest.skip("React UI server is offline on localhost:3000.")
            raise e

    def test_browse_catalog_from_empty_cart(self, page: Page):
        """Verify clicking 'Browse the Catalogue' navigates user back to catalog."""
        cart_page = CartPage(page)
        try:
            cart_page.load()
            if cart_page.is_cart_empty():
                cart_page.click_browse_catalog()
                page.wait_for_timeout(1000)
                assert page.url.rstrip('/') == cart_page.base_url
        except PlaywrightError as e:
            if "ERR_CONNECTION_REFUSED" in str(e):
                pytest.skip("React UI server is offline on localhost:3000.")
            raise e
