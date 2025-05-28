import logging
from typing import cast

from app.app_layer.errors.exceptions.use_cases_exceptions import (
    BlockedException,
    PermissionException,
)
from app.app_layer.errors.strings import BLOCKED_USER, NO_PERMISSION
from app.infra.repositories.sqla.models import Role, User
from app.infra.repositories.sqla.user import UserRepository
from app.infra.services.jwt import TokenService

logging.basicConfig(level=logging.INFO)


class SecurityCheckMeService:
    def __init__(self, user_repo: UserRepository, token_service: TokenService):
        self.token_service = token_service
        self.user_repo = user_repo

    async def __call__(self, token: str) -> User:
        token_payload = self.token_service.authenticate(token, TokenService.access)

        user = await self.user_repo.get(cast(str, token_payload.get("user_id")))

        if user.is_blocked is True:
            logging.error(f"User {user.id} is blocked")
            raise BlockedException(BLOCKED_USER)

        return user


class SecurityPermissionService:
    def __init__(self, user_repo: UserRepository, token_service: TokenService):
        self.token_service = token_service
        self.user_repo = user_repo

    async def __call__(self, token: str) -> tuple[Role, int]:
        """
        user.role == ADMIN -> None
        user.role == MODERATOR -> GroupID
        user.role == USER -> Exception
        """

        token_payload = self.token_service.authenticate(token, TokenService.access)

        if token_payload.get("role") == Role.USER:
            logging.error("Token role is user, access denied")
            raise PermissionException(role=Role.USER, info=NO_PERMISSION)

        user = await self.user_repo.get(cast(str, token_payload.get("user_id")))

        if user.is_blocked is True:
            logging.error(f"User {user.id} is blocked")
            raise BlockedException(BLOCKED_USER)

        logging.info(
            f"User's permissions: role -> {user.role}, group -> {user.group_id}"
        )
        return user.role, user.group_id
