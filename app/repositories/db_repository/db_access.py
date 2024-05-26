from datetime import date

from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.models.repository_data_transfer_objs import UrlEntry
from app.models.sqlalchemy_models import Url
from app.models.shared_models import Error


def retrieve_db_url_pair(postfix: str, db: Session) -> UrlEntry | Error:
    try:
        url_entry = db.query(Url)\
            .filter(Url.postfix == postfix)\
            .first()
        if url_entry:
            return UrlEntry(url_entry.postfix, url_entry.original_url, url_entry.user_id, url_entry.expiration)
    except exc.SQLAlchemyError as e:
        return Error(e.args[0], 500)


def persist_db_url_pair(postfix: str, original_url: str, user_id: int, expiration: date, db: Session) -> None | Error:
    try:
        new_pair = Url(postfix=postfix, original_url=original_url, user_id=user_id, expiration=expiration)
        db.add(new_pair)
        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        return Error(e.args[0], 500)
