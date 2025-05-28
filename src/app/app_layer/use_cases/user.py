from typing import Callable
from app.app_layer.schemas.user import UserResponseSchema, UserUpdateSchema
from app.app_layer.use_cases.security import (
    SecurityCheckMeService,
    SecurityPermissionService,
)
from app.infra.repositories.sqla.models import Role, User
from app.infra.repositories.sqla.user import UserRepository


class GetMeUseCase:
    def __init__(
        self, user_repo: UserRepository, security_service: SecurityCheckMeService
    ):
        self.user_repo = user_repo
        self.permission_service = security_service

    async def __call__(self, token: str):
        user = await self.permission_service(token)

        return UserResponseSchema.model_validate(user.__dict__)


class PatchMeUseCase:
    def __init__(
        self, user_repo: UserRepository, security_service: SecurityCheckMeService
    ):
        self.user_repo = user_repo
        self.permission_service = security_service

    async def __call__(self, token: str, update_data: UserUpdateSchema):
        user = await self.permission_service(token)
        user = await self.user_repo.update(str(user.id), update_data)

        return UserResponseSchema.model_validate(user.__dict__)


class DeleteMeUseCase:
    def __init__(
        self, user_repo: UserRepository, security_service: SecurityCheckMeService
    ):
        self.user_repo = user_repo
        self.permission_service = security_service

    async def __call__(self, token: str):
        user = await self.permission_service(token)

        await self.user_repo.delete(str(user.id))


class GetUserUseCase:
    def __init__(
        self, user_repo: UserRepository, security_service: SecurityPermissionService
    ):
        self.user_repo = user_repo
        self.permission_service = security_service

        self.role_mapping: dict[Role, Callable] = {
            Role.ADMIN: self._admin_action,
            Role.MODERATOR: self._moderator_action,
        }

    async def __call__(self, token: str, user_id: str):
        permission = await self.permission_service(token)
        (role, _) = permission
        user = await self.role_mapping[role](user_id, permission)

        return UserResponseSchema.model_validate(user.__dict__)

    async def _admin_action(self, user_id: str, permission: tuple[Role, int]) -> User:
        user = await self.user_repo.get(user_id)

        return user

    async def _moderator_action(
        self, user_id: str, permission: tuple[Role, int]
    ) -> User:
        (_, group_id) = permission
        user = await self.user_repo.get_by_id_and_group(user_id, group_id)

        return user


class PatchUserUseCase:
    def __init__(
        self, user_repo: UserRepository, permission_service: SecurityPermissionService
    ):
        self.user_repo = user_repo
        self.permission_service = permission_service

        self.role_mapping: dict[Role, Callable] = {
            Role.ADMIN: self._admin_action,
            Role.MODERATOR: self._moderator_action,
        }

    async def __call__(self, token: str, user_id: str, update_data: UserUpdateSchema):
        permission = await self.permission_service(token)
        (role, _) = permission
        user = await self.role_mapping[role](user_id, update_data, permission)

        return UserResponseSchema.model_validate(user.__dict__)

    async def _admin_action(
        self, user_id: str, update_data: UserUpdateSchema, permission: tuple[Role, int]
    ) -> User:
        user = await self.user_repo.update(user_id, update_data)

        return user

    async def _moderator_action(
        self, user_id: str, update_data: UserUpdateSchema, permission: tuple[Role, int]
    ) -> User:
        (_, group_id) = permission
        user = await self.user_repo.get_by_id_and_group(user_id, group_id)
        user = await self.user_repo.update(str(user.id), update_data)

        return user
