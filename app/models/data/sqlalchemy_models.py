from sqlalchemy import Column, Integer, String, DATE
from sqlalchemy import engine # noqa

from app.repositories.db_repository.postgres import Base


# todo: Apply foreign key constraints

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, nullable=False)


class Url(Base):
    __tablename__ = 'url'

    postfix = Column(String, primary_key=True, unique=True, nullable=False)
    original_url = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    expiration = Column(DATE, nullable=False)
