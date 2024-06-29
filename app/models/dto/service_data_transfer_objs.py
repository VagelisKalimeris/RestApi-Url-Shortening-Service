from datetime import date


class ShortUrlResult:
    def __init__(self, short_url: str) -> None:
        self.short_url = short_url


class OriginalUrlResult:
    def __init__(self, original_url: str, expiration: date, cached_result: bool):
        self.original_url = original_url
        self.expiration = expiration
        self.cached_result = cached_result
