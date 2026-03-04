from src.scraper.extractors.links import is_product, is_category

def test_product_urls():
    assert is_product("https://www.alza.sk/18851104.htm")
    assert is_product("https://www.alza.sk/samsung-galaxy-s26-ultra-16-gb-1-tb-black-d13233601.htm")
    assert not is_product("https://www.alza.sk/privacy-policy")

def test_category_urls():
    assert is_category("https://www.alza.sk/e76.htm")
    assert is_category("https://www.alza.sk/mega-zlavy/y842.htm")
    assert not is_category("https://www.alza.sk/18851104.htm")