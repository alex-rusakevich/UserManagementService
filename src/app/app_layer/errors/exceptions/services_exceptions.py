from app.app_layer.errors.exceptions.base_custom import BaseCustomException


class RedisException(BaseCustomException):
    def __init__(self, info: str = ""):
        detail = "Redis operation error"
        super().__init__(status_code=503, detail=detail, info=info)


class SESException(BaseCustomException):
    def __init__(self, info: str = ""):
        detail = "SES operation error"
        super().__init__(status_code=500, detail=detail, info=info)


class TokenProcessingException(BaseCustomException):
    def __init__(self, data: str, info: str = ""):
        detail = f"Invalid data: {data}"
        super().__init__(status_code=422, detail=detail, info=info)


class TokenExpireException(BaseCustomException):
    def __init__(self, info: str = ""):
        detail = "Token has expired"
        super().__init__(status_code=403, detail=detail, info=info)
