from playwright.sync_api import Page, expect
from .base_page import BasePage

class CategoryListPage(BasePage):
    """
    Page Object Model representing the React Category List Page (/categories).
    Encapsulates category grid locators and card interactions.
    """

    # Locators
    CATEGORY_LIST_CONTAINER = ".category-list"
    CATEGORY_GRID = ".category-grid"
    CATEGORY_CARD = ".category-card"
    SHOP_BAND_HEADER = ".shop-band"
    ERROR_MESSAGE = ".error-message"

    def __init__(self, page: Page):
        super().__init__(page)
        self.path = "/categories"

    def load(self):
        """Navigate directly to Category List page."""
        self.navigate_to(self.path)
        self.page.wait_for_selector(self.CATEGORY_LIST_CONTAINER)

    def get_category_card_count(self) -> int:
        """Get count of category cards rendered in category grid."""
        if self.is_element_visible(self.CATEGORY_CARD, timeout=3000):
            return self.page.locator(self.CATEGORY_CARD).count()
        return 0

    def click_category_card(self, index: int = 0):
        """Click category card at specific index."""
        cards = self.page.locator(self.CATEGORY_CARD)
        if cards.count() > index:
            cards.nth(index).click()
