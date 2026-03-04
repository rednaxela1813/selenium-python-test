# src/scraper/pages/alza_product.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from scraper.pages.base import BasePage
from scraper.extractors.text import parse_eur_price

import logging
logger = logging.getLogger(__name__)
        
        
class AlzaProductPage(BasePage):
    def parse(self, url: str) -> dict:
        self.open(url)
        self.wait_dom_ready()
        self.wait_body()
        self.remove_overlays_best_effort()

        name = self._first_text([
            (By.CSS_SELECTOR, "h1"),
            (By.CSS_SELECTOR, "[data-testid='productTitle']"),
        ])
        

        
        price = self._first_text([
            (By.CSS_SELECTOR, "[data-testid='price']"),
            (By.CSS_SELECTOR, ".price-box__price"),
            (By.CSS_SELECTOR, ".price"),
        ])
        if price is None:
            logger.warning("No price found: %s", url)
        

        return {"url": url, "name": name, "price": price}

    def _first_text(self, selectors: list[tuple[str, str]]) -> str | None:
        for by, sel in selectors:
            try:
                el = self.driver.find_element(by, sel)
                txt = (el.text or "").strip()
                if txt:
                    return txt
            except NoSuchElementException:
                continue
        return None