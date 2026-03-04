# src/scraper/pages/alza_category.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from urllib.parse import urljoin

from selenium.webdriver.common.by import By

from scraper.pages.base import BasePage
from scraper.utils.rate_limit import RateLimiter

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ScrollConfig:
    max_scrolls: int = 30               # максимум попыток прокрутки
    stable_rounds_to_stop: int = 3      # сколько раз подряд нет новых ссылок -> стоп
    min_links_to_start: int = 5         # сколько ссылок должно быть до старта (иначе ждём)
    scroll_min_delay: float = 0.6       # пауза после scroll
    scroll_max_delay: float = 1.2       # пауза после scroll


class AlzaCategoryPage(BasePage):
    """
    Страница списка товаров (категория/бренд/акция).

    Сценарий:
    - открыть URL
    - дождаться контента
    - собрать ссылки на товары (href с '-d<digits>.htm')
    - скроллить вниз, пока количество уникальных ссылок растёт
    - остановиться, если рост прекратился stable_rounds_to_stop раз подряд
    """

    # Ссылки на товарные карточки Alza (строго): ...-d12345678.htm
    PRODUCT_LINKS_SELECTOR = "a[href*='-d'][href$='.htm']"

    def collect_product_links(
        self,
        url: str,
        scroll: ScrollConfig | None = None,
        rate: RateLimiter | None = None,
    ) -> list[str]:
        scroll = scroll or ScrollConfig()
        rate = rate or RateLimiter(scroll.scroll_min_delay, scroll.scroll_max_delay)

        logger.info("Open category: %s", url)
        self.open(url)
        self.wait_dom_ready()
        self.wait_body()
        self.remove_overlays_best_effort()

        # ждём, что появились хотя бы какие-то товарные ссылки
        self.wait.until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, self.PRODUCT_LINKS_SELECTOR)) >= scroll.min_links_to_start
        )

        links: set[str] = set()
        last_count = 0
        stable_rounds = 0

        for i in range(scroll.max_scrolls):
            # 1) собрать ссылки, которые сейчас в DOM
            elems = self.driver.find_elements(By.CSS_SELECTOR, self.PRODUCT_LINKS_SELECTOR)
            for a in elems:
                href = a.get_attribute("href")
                if not href:
                    continue
                links.add(urljoin(url, href))

            current_count = len(links)
            logger.debug("scroll=%d links=%d", i, current_count)

            # 2) проверка роста
            if current_count == last_count:
                stable_rounds += 1
            else:
                stable_rounds = 0

            if stable_rounds >= scroll.stable_rounds_to_stop:
                logger.info("Stop scrolling: no new links (%d stable rounds). total=%d", stable_rounds, current_count)
                break

            last_count = current_count

            # 3) прокрутка вниз
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # 4) вежливая пауза (rate limiting)
            slept = rate.wait()
            logger.debug("rate_limit scroll sleep=%.2fs", slept)

        return sorted(links)