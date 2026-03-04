# src/scraper/extractors/links.py

import re
from urllib.parse import urlparse


PRODUCT_RE = re.compile(r"-d\d+\.htm$") 
CAT_RE = re.compile(r"/[evy]\d+\.htm$")

def is_alza(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc.endswith("alza.sk")

def is_product(url: str) -> bool:
    return is_alza(url) and bool(PRODUCT_RE.search(urlparse(url).path))


def is_category(url: str) -> bool:
    return is_alza(url) and bool(CAT_RE.search(urlparse(url).path))