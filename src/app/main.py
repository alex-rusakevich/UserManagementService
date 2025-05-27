from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.app_layer.errors.to_app import add_exceptions
from app.infra.database_conntection import get_redis_instance
from app.infra.services.redis import RedisService
from app.api.routes.api import api_router
from app.config import get_settings

from app.infra.services.s3 import S3Service
from app.infra.database_conntection import get_aws_client
from app.infra.services.ses import SESService


async def create_buckets():
    s3_service = S3Service(get_aws_client, get_settings().aws)
    await s3_service.service_create_bucket()


async def check_redis():
    redis = await get_redis_instance()
    redis_service = RedisService(redis)
    await redis_service.ping()


async def verify_email():
    ses_service = SESService(get_aws_client, get_settings().aws)
    await ses_service.verify_email()


@asynccontextmanager
async def lifespan(application: FastAPI):
    await check_redis()
    await verify_email()
    await create_buckets()
    yield


def get_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan)

    application.include_router(api_router)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_exceptions(application)
    return application


def main():
    app = get_application()
    uvicorn.run(app, host="0.0.0.0", port=8000)


def dev():
    app = get_application()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
