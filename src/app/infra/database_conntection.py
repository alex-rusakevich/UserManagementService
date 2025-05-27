from contextlib import asynccontextmanager
from typing import AsyncGenerator
import aioboto3
from redis.asyncio import Redis, ConnectionPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import get_settings


settings = get_settings()

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db.pg_user}:{settings.db.pg_password}@{settings.db.pg_host}:"
    f"{settings.db.pg_port}/{settings.db.pg_db}"
)

database_engine = create_async_engine(DATABASE_URL, echo=False)

redis_pool = ConnectionPool(
    host=settings.redis.redis_host, port=settings.redis.redis_port
)

aws_session = aioboto3.Session(
    aws_access_key_id=settings.aws.aws_access_key_id,
    aws_secret_access_key=settings.aws.aws_secret_access_key,
)


async def get_redis_instance() -> Redis:
    return Redis(connection_pool=redis_pool)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session_maker = async_sessionmaker(database_engine, autoflush=True)

    async with session_maker() as session:
        yield session


@asynccontextmanager
async def get_aws_client(service):
    async with aws_session.client(
        service,
        endpoint_url=settings.aws.aws_endpoint_url,
        region_name=settings.aws.aws_region,
    ) as client:
        yield client
