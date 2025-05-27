from functools import lru_cache
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtConfig(BaseSettings):
    hash_alg_token: str = os.getenv("JWT_HASH_ALG", "HS256")
    secret_key: str = os.getenv("JWT_SECRET_KEY", "")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class PasswordConfig(BaseSettings):
    hash_alg: str = os.getenv("PASSWORD_HASH_ALG", "bcrypt")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AwsConfig(BaseSettings):
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    aws_region: str = os.getenv("AWS_REGION", "eu-north-1")
    aws_endpoint_url: str = os.getenv("AWS_ENDPOINT_URL", "")
    aws_bucket_name: str = os.getenv("AWS_BUCKET_NAME", "")
    aws_sender_email: str = os.getenv("AWS_SENDER_EMAIL", "")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class NotificationConfig(BaseSettings):
    my_sender_email: str = os.getenv("NOTIFICATION_SENDER_EMAIL", "")
    my_sender_password: str = os.getenv("NOTIFICATION_SENDER_PASSWORD", "")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


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
    password: PasswordConfig = PasswordConfig()
    aws: AwsConfig = AwsConfig()
    notification: NotificationConfig = NotificationConfig()
    secret: JwtConfig = JwtConfig()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> BaseApplicationSettings:
    return BaseApplicationSettings()
