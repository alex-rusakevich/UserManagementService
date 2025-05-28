from app.app_layer.errors.exceptions.base_custom import BaseCustomException


class DBReadException(BaseCustomException):
    def __init__(self, item_id: str, info: str = ""):
        detail = f"User/Item {item_id} not found"
        super().__init__(status_code=404, detail=detail, info=info)
