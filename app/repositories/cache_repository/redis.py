from os import environ

import redis
from dotenv import load_dotenv


load_dotenv()
redis_password = environ['REDIS_PASSWORD']

def create_redis():
    return redis.ConnectionPool(
        host='redis-container',
        password=redis_password,
        port=6379,
        db=0,
        decode_responses=False
    )


pool = create_redis()
