from datetime import date


class UrlEntry:
    def __init__(self, postfix: str, original_url: str, user_id: int, expiration: date) -> None:
        self.postfix = postfix
        self.original_url = original_url
        self.user_id = user_id
        self.expiration = expiration
        self.cached_result = False


class ServerStats:
    def __init__(self, cache_reads: int, db_reads: int, db_writes: int, read_errors: int, write_errors: int) -> None:
        self.cache_reads = cache_reads
        self.db_reads = db_reads
        self.db_writes = db_writes
        self.read_errors = read_errors
        self.write_errors = write_errors
