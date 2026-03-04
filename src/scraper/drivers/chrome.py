# src/scraper/drivers/chrome.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scraper.config import Settings


def create_driver(settings: Settings) -> webdriver.Chrome:
    options = Options()
    if settings.headless:
        options.add_argument("--headless=new")
    options.add_argument(f"user-agent={settings.user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.set_page_load_timeout(settings.timeout_sec)
    
    return driver