from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database_conntection import get_db_session
from app.infra.repositories.sqla.user import UserRepository


def get_user_repo(session: AsyncSession = Depends(get_db_session)):
    return UserRepository(session)
