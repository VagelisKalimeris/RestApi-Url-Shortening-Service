from datetime import date

from redis import Redis
from sqlalchemy.orm import Session

from app.config import SERVICE_BASE_URL
from app.models.repository_data_transfer_objs import ServerStats
from app.models.service_data_transfer_objs import ShortUrlResult, OriginalUrlResult
from app.services.helpers.random_key_gen import gen_rand_key
from app.models.shared_models import Error
from app.repositories.shortener_data_access import ShortenerDataAccess


def shorten_url_logic(user_id: int, original_url: str, postfix: str, expiration: date, cache: Redis, db: Session) \
        -> ShortUrlResult | Error:
    if postfix:
        # Postfix key given by user, verify does not already exist in database
        if isinstance(existing_entry := ShortenerDataAccess.retrieve_url_pair(postfix, cache, db), Error):
            return existing_entry
        if existing_entry:
            return Error('Requested postfix already exists. Please try again with a different one!', 409)

    else:
        # Generate new random postfix that does not already exist in database
        postfix = gen_rand_key()
        existing_entry = ShortenerDataAccess.retrieve_url_pair(postfix, cache, db)
        while existing_entry:
            # Avoid being stuck in loop in case db errors out
            if isinstance(existing_entry, Error):
                return Error('Failure while verifying target url does not already exist. '
                             f'Original error: {existing_entry.__dict__}', 500)
            postfix = gen_rand_key()
            existing_entry = ShortenerDataAccess.retrieve_url_pair(postfix, cache, db)

    # Add storage entry
    if isinstance(url_pair := ShortenerDataAccess.persist_url_pair(user_id, original_url, postfix, expiration, db), Error):
        return url_pair

    # Construct short URL
    return ShortUrlResult(SERVICE_BASE_URL + postfix)


def retrieve_url_logic(user_id: int, postfix: str, cache: Redis, db: Session) -> OriginalUrlResult | Error:
    # Access storage
    if isinstance(url_pair := ShortenerDataAccess.retrieve_url_pair(postfix, cache, db), Error):
        return url_pair

    # Verify pair entry exists. Validate user & expiration
    if not url_pair:
        return Error('No entry exists for given short URL!', 404)
    if url_pair.user_id != user_id:
        return Error('No access for given short URL!', 403)
    if url_pair.expiration < date.today():
        return Error('Entry for given URL has expired!', 410)

    return OriginalUrlResult(url_pair.original_url, url_pair.expiration, url_pair.cached_result)


def retrieve_server_statistics() -> ServerStats:
    return ShortenerDataAccess.retrieve_statistics()