from redis.asyncio import Redis, ConnectionPool

from app.config import get_settings


settings = get_settings()

redis_pool = ConnectionPool(
    host=settings.redis.redis_host, port=settings.redis.redis_port
)


async def get_redis_instance() -> Redis:
    return Redis(connection_pool=redis_pool)
