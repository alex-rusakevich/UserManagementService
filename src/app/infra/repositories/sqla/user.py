from datetime import datetime
from typing import Optional

from sqlalchemy import ScalarResult, delete, desc, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.app_layer.errors.exceptions.database_exceptions import DBReadException
from app.app_layer.errors.strings import (
    INVALID_LOGIN,
    INVALID_EMAIL,
    INVALID_GROUP,
    USER_NOT_FOUND,
)
from app.app_layer.schemas.user import UserCreateForm, UserUpdateSchema
from app.infra.repositories.sqla.models import User
from app.infra.services.hashing import PasswordService
from app.config import get_settings


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, new_user: UserCreateForm) -> User:
        password_service = PasswordService(get_settings().password)

        user = User(
            name=new_user.name,
            surname=new_user.surname,
            username=new_user.username,
            phone_number=new_user.phone_number,
            email=new_user.email,
            image_path=new_user.username,
            password=password_service.hash(new_user.password),
            group_id=new_user.group_id,
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get(self, user_id: str) -> User:
        if user := await self.session.get(User, user_id):
            return user

        raise DBReadException(user_id, USER_NOT_FOUND)

    async def get_by_email(self, email: str) -> User:
        statement = select(User).where(User.email == email)

        if user := await self.session.scalar(statement):
            return user

        raise DBReadException(email, INVALID_EMAIL)

    async def get_by_login(self, login: str) -> User:
        statement = select(User).where(
            or_(User.username == login, User.email == login, User.phone_number == login)
        )

        if user := await self.session.scalar(statement):
            return user

        raise DBReadException(login, INVALID_LOGIN)

    async def get_by_id_and_group(self, user_id: str, group_id: int) -> User:
        user = await self.session.scalar(
            select(User).where(User.id == user_id, User.group_id == group_id)
        )

        if user is None:
            raise DBReadException(user_id, INVALID_GROUP)

        return user

    async def update(self, user_id: str, new_data: UserUpdateSchema) -> User:
        user = await self.get(user_id)

        for k, v in dict(new_data).items():
            if not v:
                continue

            if getattr(user, k) == v:
                continue

            setattr(user, k, v)
            user.modified_at = datetime.now()

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def update_user_field(
        self, user_id: str, field_name: str, new_data: Optional[str]
    ):
        user = await self.get(user_id)
        setattr(user, field_name, new_data)
        await self.session.commit()

    async def delete(self, user_id: str):
        await self.session.execute(delete(User).where(User.id == user_id))
        await self.session.commit()

    async def param_query(
        self,
        limit: int,
        page: int,
        order_by: str,
        sort_by: str,
        filter_by_name: str | None,
        group_id: int | None,
    ) -> ScalarResult[User]:
        query = select(User)

        if group_id is not None:
            query = query.where(User.group_id == group_id)

        if filter_by_name is not None:
            query = query.where(User.name == filter_by_name)

        if order_by == "desc":
            query = query.order_by(desc(sort_by))
        else:
            query = query.order_by(sort_by)

        query = query.limit(limit).offset((page - 1) * limit)

        users = await self.session.scalars(query)

        return users
