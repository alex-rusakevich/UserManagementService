from fastapi import Depends

from app.api.dependencies.clients.security_services import (
    get_security_permission_service,
)
from app.api.dependencies.clients.user_repo import get_user_repo
from app.app_layer.use_cases.security import SecurityPermissionService
from app.app_layer.use_cases.users import UsersQueryUseCase
from app.infra.repositories.sqla.user import UserRepository


def get_users_use_case(
    user_repo: UserRepository = Depends(get_user_repo),
    security_service: SecurityPermissionService = Depends(
        get_security_permission_service
    ),
) -> UsersQueryUseCase:
    return UsersQueryUseCase(user_repo, security_service)
