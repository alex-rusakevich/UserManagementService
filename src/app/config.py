from functools import lru_cache
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisConfig(BaseSettings):
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: str = "6379"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DatabaseConfig(BaseSettings):
    pg_password: str = os.getenv("POSTGRES_PASSWORD", "password")
    pg_db: str = os.getenv("POSTGRES_DB", "user_management_service_db")
    pg_port: str = os.getenv("POSTGRES_PORT", "5432")
    pg_host: str = os.getenv("POSTGRES_HOST", "localhost")
    pg_user: str = os.getenv("POSTGRES_USER", "postgres")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class BaseApplicationSettings(BaseSettings):
    redis: RedisConfig = RedisConfig()
    db: DatabaseConfig = DatabaseConfig()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> BaseApplicationSettings:
    return BaseApplicationSettings()
