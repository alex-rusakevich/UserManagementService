import datetime

from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/healthcheck")
async def healthcheck():
    return {"time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
