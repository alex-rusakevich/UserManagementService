from app.app_layer.errors.exceptions.base_custom import BaseCustomException


class BlockedException(BaseCustomException):
    def __init__(self, info: str = ""):
        detail = "Item blocked"
        super().__init__(status_code=403, detail=detail, info=info)


class PasswordException(BaseCustomException):
    def __init__(self, info: str = ""):
        detail = "Password check error"
        super().__init__(status_code=409, detail=detail, info=info)


class PermissionException(BaseCustomException):
    def __init__(self, role: str, info: str = ""):
        detail = f"No permission for {role}"
        super().__init__(status_code=403, detail=detail, info=info)
