from redis import Redis

from app.repositories.cache_repository.redis import pool
from app.repositories.db_repository.postgres import SessionLocal


def get_redis() -> Redis:
    return Redis(connection_pool=pool)


def get_postgres() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
