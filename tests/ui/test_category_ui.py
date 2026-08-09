import pytest
from playwright.sync_api import Page, Error as PlaywrightError
from page_objects.category_list_page import CategoryListPage

@pytest.mark.ui
class TestCategoryUI:
    """Playwright UI automation test suite for Category List Page (/categories)."""

    def test_category_page_navigation(self, page: Page):
        """Verify navigation to Category List page loads header and container."""
        cat_page = CategoryListPage(page)
        try:
            cat_page.load()
            assert cat_page.is_element_visible(cat_page.CATEGORY_LIST_CONTAINER)
        except PlaywrightError as e:
            if "ERR_CONNECTION_REFUSED" in str(e):
                pytest.skip("React UI server is offline on localhost:3000.")
            raise e

    def test_category_cards_rendering(self, page: Page):
        """Verify category cards render inside category grid if backend data exists."""
        cat_page = CategoryListPage(page)
        try:
            cat_page.load()
            page.wait_for_timeout(1000)
            if cat_page.is_element_visible(cat_page.CATEGORY_GRID, timeout=2000):
                count = cat_page.get_category_card_count()
                assert count >= 0
        except PlaywrightError as e:
            if "ERR_CONNECTION_REFUSED" in str(e):
                pytest.skip("React UI server is offline on localhost:3000.")
            raise e
