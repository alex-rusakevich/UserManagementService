from fastapi import Depends

from app.api.dependencies.clients.user_repo import get_user_repo
from app.app_layer.use_cases.security import (
    SecurityCheckMeService,
    SecurityPermissionService,
)
from app.infra.repositories.sqla.user import UserRepository
from src.app.config import get_settings
from src.app.infra.services.jwt import TokenService


def get_token_service():
    settings = get_settings()
    return TokenService(settings.secret)


def get_security_permission_service(
    user_repo: UserRepository = Depends(get_user_repo),
    token_service: TokenService = Depends(get_token_service),
) -> SecurityPermissionService:
    return SecurityPermissionService(user_repo, token_service)


def get_security_check_me_service(
    user_repo: UserRepository = Depends(get_user_repo),
    token_service: TokenService = Depends(get_token_service),
) -> SecurityCheckMeService:
    return SecurityCheckMeService(user_repo, token_service)
