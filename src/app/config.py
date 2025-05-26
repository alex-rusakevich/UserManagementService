from functools import lru_cache
from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    redis_host: str = "localhost"
    redis_port: str = "6379"


class BaseApplicationSettings(BaseSettings):
    redis: RedisConfig = RedisConfig()


@lru_cache
def get_settings() -> BaseApplicationSettings:
    return BaseApplicationSettings()
