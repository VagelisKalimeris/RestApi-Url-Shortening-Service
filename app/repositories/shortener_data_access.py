from datetime import date

from redis import Redis
from sqlalchemy.orm import Session

from app.models.dto.repository_data_transfer_objs import UrlEntry, ServerStats
from app.repositories.cache_repository.cache_access import retrieve_cache_url_pair, persist_cache_url_pair
from app.repositories.db_repository.db_access import retrieve_db_url_pair, persist_db_url_pair
from app.models.shared.shared_models import Error


class ShortenerDataAccess:
    cache_reads = db_reads = db_writes = read_errors = write_errors = 0

    @classmethod
    def retrieve_url_pair(cls, postfix: str, cache: Redis, db: Session) -> UrlEntry | Error:
        # Check for existing cache entry first
        if (cache_entry := retrieve_cache_url_pair(postfix, cache)) and not isinstance(cache_entry, Error):
            cls.cache_reads += 1
            cache_entry.cached_result = True
            return cache_entry

        # No cache entry, go to db
        if isinstance(db_entry := retrieve_db_url_pair(postfix, db), Error):
            cls.read_errors += 1
            return db_entry

        if db_entry:
            # Valid db entry found, cache it
            # todo: Handle error
            persist_cache_url_pair(postfix, db_entry, cache)

        cls.db_reads += 1
        return db_entry

    @classmethod
    def persist_url_pair(cls, user_id: int, original_url: str, postfix: str, expiration: date, db: Session) \
            -> None | Error:
        if isinstance(db_insert_result := persist_db_url_pair(postfix, original_url, user_id, expiration, db), Error):
            cls.write_errors += 1
            return db_insert_result

        cls.db_writes += 1

    @classmethod
    def retrieve_statistics(cls) -> ServerStats:
        return ServerStats(cls.cache_reads, cls.db_reads, cls.db_writes, cls.read_errors, cls.write_errors)
