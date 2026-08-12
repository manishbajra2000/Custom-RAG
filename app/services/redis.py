import redis


REDIS_URL = "redis://localhost:6379"


class RedisService:
    def __init__(self) -> None:
        self.client = redis.Redis.from_url(
            REDIS_URL,
            decode_responses=True,
        )