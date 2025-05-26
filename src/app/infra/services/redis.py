from redis.asyncio import Redis

from app.app_layer.errors.exceptions.services_exceptions import RedisException
from app.app_layer.errors.strings import REDIS_CONN


class RedisService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def ping(self):
        ping = await self.redis.ping()

        if not ping:
            raise RedisException(REDIS_CONN)

    async def set_value(self, key: str, value: str) -> None:
        await self.redis.set(key, value)

    async def get_value(self, key: str) -> str | None:
        value = await self.redis.get(key)

        if value is None:
            return

        return value.decode("utf8")

    async def set_value_expire(self, key: str, value: str, timeout: int) -> None:
        await self.redis.setex(key, timeout, value)
