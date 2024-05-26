import redis


def create_redis():
    return redis.ConnectionPool(
        host='redis-container',
        port=6379,
        db=0,
        decode_responses=False
    )


pool = create_redis()
