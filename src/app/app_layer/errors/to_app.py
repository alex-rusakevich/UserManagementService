from fastapi import FastAPI

from app.app_layer.errors.exceptions.base_custom import BaseCustomException
from app.app_layer.errors.handlers import custom_exception


def add_exceptions(application: FastAPI):
    application.exception_handler(BaseCustomException)(custom_exception)
