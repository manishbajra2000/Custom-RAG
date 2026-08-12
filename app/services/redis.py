import redis


REDIS_URL = "redis://localhost:6379"


class RedisService:
    def __init__(self) -> None:
        self.client = redis.Redis.from_url(
            REDIS_URL,
            decode_responses=True,
        )

    def get(self, key: str) -> str | None:
        return self.client.get(key)

    def set(
        self,
        key: str,
        value: str,
    ) -> None:
        self.client.set(key, value)

    def delete(self, key: str) -> None:
        self.client.delete(key)