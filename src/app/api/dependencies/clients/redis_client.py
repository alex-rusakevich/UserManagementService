from fastapi import Depends
from redis.asyncio import Redis

from app.infra.database_conntection import get_redis_instance
from app.infra.services.redis import RedisService


def get_redis_service(redis: Redis = Depends(get_redis_instance)) -> RedisService:
    return RedisService(redis)
