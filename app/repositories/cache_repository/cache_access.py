import pickle

from redis import Redis, RedisError

from app.models.dto.repository_data_transfer_objs import UrlEntry
from app.models.shared.shared_models import Error


def retrieve_cache_url_pair(postfix: str, cache: Redis) -> UrlEntry | Error:
    try:
        if pickled_entry := cache.get(postfix):
            return pickle.loads(pickled_entry)
    except RedisError as e:
        return Error(e.args[0], 500)


def persist_cache_url_pair(postfix: str, db_entry: UrlEntry, cache: Redis) -> None | Error:
    try:
        cache.set(postfix, pickle.dumps(db_entry))
    except RedisError as e:
        return Error(e.args[0], 500)
