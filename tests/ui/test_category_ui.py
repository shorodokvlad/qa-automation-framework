import pytest
import requests
from playwright.sync_api import Page, Error as PlaywrightError, expect
from api_clients.category_client import CategoryClient
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

    def test_category_cards_rendering(
        self,
        page: Page,
        category_client: CategoryClient,
    ):
        """Verify the UI renders exactly the categories returned by the API."""
        cat_page = CategoryListPage(page)
        try:
            response = category_client.get_all_categories()
            assert response.status_code == 200
            categories = response.json()["categoryList"]

            cat_page.load()
            expect(page.locator(cat_page.CATEGORY_GRID)).to_be_visible()
            expect(page.locator(cat_page.CATEGORY_CARD)).to_have_count(len(categories))
        except (PlaywrightError, requests.exceptions.ConnectionError) as e:
            if isinstance(e, requests.exceptions.ConnectionError) or "ERR_CONNECTION_REFUSED" in str(e):
                pytest.skip("React UI or Spring Boot API server is offline.")
            raise e
