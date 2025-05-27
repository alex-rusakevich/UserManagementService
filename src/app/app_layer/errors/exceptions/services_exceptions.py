from app.app_layer.errors.exceptions.base_custom import BaseCustomException


class RedisException(BaseCustomException):
    def __init__(self, info: str = ""):
        detail = "Redis operation error"
        super().__init__(status_code=503, detail=detail, info=info)


class SESException(BaseCustomException):
    def __init__(self, info: str = ""):
        detail = "SES operation error"
        super().__init__(status_code=500, detail=detail, info=info)
