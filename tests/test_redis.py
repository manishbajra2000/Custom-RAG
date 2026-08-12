from app.services.redis import RedisService


redis_service = RedisService()

redis_service.client.set(
    "test:key",
    "Hello from Redis!",
)

value = redis_service.client.get("test:key")

print(value)