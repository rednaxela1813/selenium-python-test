# src/scraper/utils/rate_limit.py
import time
import random


class RateLimiter:
    def __init__(self, min_delay: float = 1.0, max_delay: float = 2.5):
        if min_delay < 0 or max_delay < 0:
            raise ValueError("Delays must be non-negative")
        if max_delay < min_delay:
            raise ValueError("max_delay must be >= min_delay")

        self.min_delay = float(min_delay)
        self.max_delay = float(max_delay)
        self._last_call = 0.0

    def wait(self) -> float:
        """
        Waits enough time to respect rate limits.
        Returns the actual sleep duration (seconds).
        """
        now = time.time()
        elapsed = now - self._last_call

        target = random.uniform(self.min_delay, self.max_delay)
        sleep_for = max(0.0, target - elapsed)

        if sleep_for > 0:
            time.sleep(sleep_for)

        self._last_call = time.time()
        return sleep_for