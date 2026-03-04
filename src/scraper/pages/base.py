# src/scraper/pages/base.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver, timeout_sec: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout_sec)
        
    def open(self, url: str):
        self.driver.get(url)

    def wait_dom_ready(self) -> None:
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        
    def wait_body(self) -> None:
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
    def remove_overlays_best_effort(self) -> None:
        # This is a best effort to remove cookie consent popups and similar overlays that might interfere with scraping.
        self.driver.execute_script("""
            const kill = (sel) => document.querySelectorAll(sel).forEach(e => e.remove());
            kill('[id*="cookie"]');
            kill('[class*="cookie"]');
            kill('[class*="consent"]');
        """)