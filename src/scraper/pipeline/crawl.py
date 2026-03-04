# src/scraper/pipeline/crawl.py

import logging

from scraper.pages.alza_home import AlzaHomePage
from scraper.pages.alza_product import AlzaProductPage
from scraper.pages.alza_category import AlzaCategoryPage, ScrollConfig

from scraper.extractors.links import is_product
from scraper.utils.rate_limit import RateLimiter

logger = logging.getLogger(__name__)


from scraper.extractors.links import is_category  

def crawl_home_categories_and_products(
    driver,
    base_url: str,
    timeout_sec: int,
    max_categories: int = 3,
    products_per_category: int = 5,
    rate_min: float = 1.5,
    rate_max: float = 3.0,
):
    home = AlzaHomePage(driver, timeout_sec)
    cat = AlzaCategoryPage(driver, timeout_sec)
    prod = AlzaProductPage(driver, timeout_sec)

    page_rate = RateLimiter(rate_min, rate_max)

    # скролл можно делать быстрее, чем переходы по товарам
    scroll_cfg = ScrollConfig(
        max_scrolls=30,
        stable_rounds_to_stop=3,
        min_links_to_start=5,
        scroll_min_delay=0.6,
        scroll_max_delay=1.2,
    )
    scroll_rate = RateLimiter(scroll_cfg.scroll_min_delay, scroll_cfg.scroll_max_delay)

    links = home.get_links(base_url)
    category_links = [l for l in links if is_category(l)]
    logger.info("Home: found %d category links", len(category_links))

    out = []

    for idx, category_url in enumerate(category_links[:max_categories], start=1):
        logger.info("Category %d/%d: %s", idx, max_categories, category_url)

        product_links = cat.collect_product_links(category_url, scroll=scroll_cfg, rate=scroll_rate)
        logger.info("Category: collected %d product links", len(product_links))

        for url in product_links[:products_per_category]:
            slept = page_rate.wait()
            logger.debug("rate_limit page sleep=%.2fs url=%s", slept, url)

            logger.info("Parsing product page: %s", url)
            out.append(prod.parse(url))

    return out