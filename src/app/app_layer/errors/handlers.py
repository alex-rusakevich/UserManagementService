from fastapi import Request
from fastapi.responses import JSONResponse

from app.app_layer.errors.exceptions.base_custom import BaseCustomException


async def custom_exception(request: Request, exception: BaseCustomException):
    return JSONResponse(
        status_code=exception.status_code, content={"detail": exception.detail}
    )
