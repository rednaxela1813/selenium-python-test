# src/scraper/cli.py

from scraper.config import Settings
from scraper.drivers.chrome import create_driver
from scraper.pipeline.crawl import crawl_home_and_products
from scraper.storage.jsonl import write_jsonl


def main():
    settings = Settings()
    driver = create_driver(settings)
    try:
        rows = crawl_home_and_products(
            driver=driver,
            base_url=settings.base_url,
            timeout_sec=settings.timeout_sec,
            limit=10,
        )
        for r in rows:
            print(r)
        write_jsonl("out/alza_products.jsonl", rows)
        print("Saved to out/alza_products.jsonl")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()