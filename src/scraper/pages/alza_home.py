# src/scraper/pages/alza_home.py

from urllib.parse import urljoin, urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from scraper.pages.base import BasePage


class AlzaHomePage(BasePage):
    def get_links(self, url: str) -> list[str]:
        self.open(url)
        self.wait_dom_ready()
        self.wait_body()
        #banner
        self.remove_overlays_best_effort()
        
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))
        links: set[str] = set()
        for a in self.driver.find_elements(By.TAG_NAME, "a"):
            href = a.get_attribute("href")
            if not href:
                continue
            href = href.strip()
            if href.startswith(("javascript:", "mailto:", "tel:")):
                continue
            href = urljoin(url, href)
            links.add(href)
        base_domain = urlparse(url).netloc
        return sorted([l for l in links if urlparse(l).netloc.endswith("alza.sk") or urlparse(l).netloc == base_domain])