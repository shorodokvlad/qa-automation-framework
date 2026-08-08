import os
import logging
from playwright.sync_api import Page, Locator, expect

logger = logging.getLogger(__name__)

class BasePage:
    """
    Base Page Object class encapsulating common Playwright interactions.
    Encapsulates Playwright auto-waiting mechanisms for React dynamic rendering.
    """

    def __init__(self, page: Page, base_url: str = None):
        self.page = page
        self.base_url = (base_url or os.getenv("UI_BASE_URL", "http://localhost:3000")).rstrip('/')

    def navigate_to(self, path: str = ""):
        """Navigate to page URL path."""
        full_url = f"{self.base_url}/{path.lstrip('/')}"
        logger.info(f"Navigating to {full_url}")
        self.page.goto(full_url, wait_until="domcontentloaded")

    def click_element(self, selector: str):
        """Click element after ensuring auto-wait for visibility & interactability."""
        logger.info(f"Clicking element: {selector}")
        self.page.locator(selector).click()

    def fill_input(self, selector: str, text: str):
        """Fill input field after clearing existing text."""
        logger.info(f"Filling input '{selector}' with text")
        locator = self.page.locator(selector)
        locator.fill("")
        locator.fill(text)

    def get_element_text(self, selector: str) -> str:
        """Fetch inner text of locator."""
        return self.page.locator(selector).inner_text()

    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check element visibility within specified timeout."""
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
