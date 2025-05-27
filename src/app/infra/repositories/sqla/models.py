from enum import StrEnum
from app.infra.repositories.sqla.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, ForeignKey, Integer, String, DateTime, func, Uuid
from datetime import datetime
from typing import List
import uuid
from sqlalchemy.types import UUID


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    users: Mapped[List["User"]] = relationship("User", back_populates="group")

    def __repr__(self):
        return f"Group(id={self.id}, 'name={self.name})"


class Role(StrEnum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, insert_default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    surname: Mapped[str] = mapped_column(String(64), nullable=False)
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(16), nullable=True, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    role: Mapped[Role] = mapped_column(Enum(Role), insert_default=Role.USER)
    image_path: Mapped[str] = mapped_column(nullable=True)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    modified_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, nullable=True, onupdate=datetime.now()
    )
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=True)

    group: Mapped["Group"] = relationship("Group", back_populates="users")

    def __repr__(self):
        return f"User('id': {self.id}, 'username': {self.username})"
