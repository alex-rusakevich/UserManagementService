from functools import lru_cache
from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    redis_host: str = "localhost"
    redis_port: str = "6379"


class DatabaseConfig(BaseSettings):
    pg_password: str = "password"
    pg_db: str = "user_management_service_db"
    pg_port: str = "5432"
    pg_host: str = "localhost"
    pg_user: str = "user"


class BaseApplicationSettings(BaseSettings):
    redis: RedisConfig = RedisConfig()
    db: DatabaseConfig = DatabaseConfig()

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> BaseApplicationSettings:
    return BaseApplicationSettings()
