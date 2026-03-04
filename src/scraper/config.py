#src/scraping/config.py

from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    headless: bool = True
    timeout_sec: int = 15
    
    rate_min_delay: float = 1.5
    rate_max_delay: float = 3.0
    
    user_agent: str = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    base_url: str = "https://www.alza.sk/"
