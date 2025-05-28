import datetime

from fastapi import APIRouter

from app.api.routes.user import user_router
from app.api.routes.users import users_router

api_router = APIRouter()

api_router.include_router(router=user_router, prefix="/user")
api_router.include_router(router=users_router, prefix="/users")


@api_router.get("/healthcheck")
async def healthcheck():
    return {"time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
