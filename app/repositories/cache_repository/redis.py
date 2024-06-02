import redis


def create_redis():
    return redis.ConnectionPool(
        host='redis-container',
        password='hAuv4XoVWDX1zZB',
        port=6379,
        db=0,
        decode_responses=False
    )


pool = create_redis()
