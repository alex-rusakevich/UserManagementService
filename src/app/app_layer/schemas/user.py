import datetime
import uuid
from typing import Annotated, Optional

from fastapi import Form
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from app.infra.repositories.sqla.models import Role


class UserResponseSchema(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    username: str
    phone_number: str
    email: str
    image_path: str | None = None
    role: Role
    created_at: datetime.datetime
    modified_at: datetime.datetime | None = None
    group_id: int | None = None


class UsersResponseSchema(BaseModel):
    users: list[UserResponseSchema]
    page: int
    limit: int


class UserCreateSchema(BaseModel):
    name: str
    surname: str
    username: str
    phone_number: str
    email: str
    password: str
    group_id: int | None = None


@dataclass
class UserCreateForm:
    name: Annotated[str, Form()]
    surname: Annotated[str, Form()]
    username: Annotated[str, Form()]
    phone_number: Annotated[str, Form()]
    email: Annotated[str, Form()]
    password: Annotated[str, Form()]
    group_id: Annotated[Optional[int], Form()] = None


class UserUpdateSchema(BaseModel):
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    phone_number: str | None = None
    email: str | None = None
    group_id: str | None = None
