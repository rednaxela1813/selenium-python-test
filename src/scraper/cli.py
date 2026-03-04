# src/scraper/cli.py
from scraper.config import Settings
from scraper.drivers.chrome import create_driver
from scraper.pipeline.crawl import crawl_home_categories_and_products
from scraper.storage.output import save_to_csv
from scraper.logging_conf import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

# Выбери режим
MODE = "home"        # "home" или "category"



def main():
    settings = Settings()
    driver = create_driver(settings)

    try:
        if MODE == "home":
            rows = crawl_home_categories_and_products(
                driver=driver,
                base_url=settings.base_url,
                timeout_sec=settings.timeout_sec,
                max_categories=3,
                products_per_category=5,
                rate_min=settings.rate_min_delay,
                rate_max=settings.rate_max_delay,
            )
       
        else:
            raise ValueError(f"Unknown MODE: {MODE}")

        print("ROWS:", len(rows))
        for r in rows:
            print(r)
        save_to_csv(rows)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()