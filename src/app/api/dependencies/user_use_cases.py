from fastapi import Depends

from app.api.dependencies.clients.security_services import (
    get_security_check_me_service,
    get_security_permission_service,
)
from app.api.dependencies.clients.user_repo import get_user_repo
from app.app_layer.use_cases.security import (
    SecurityCheckMeService,
    SecurityPermissionService,
)
from app.app_layer.use_cases.user import (
    DeleteMeUseCase,
    GetMeUseCase,
    GetUserUseCase,
    PatchMeUseCase,
    PatchUserUseCase,
)
from app.infra.repositories.sqla.user import UserRepository


def get_user_use_case_type(UseCase, user_repo: UserRepository = Depends(get_user_repo)):
    return UseCase(user_repo)


def get_getme_use_case(
    user_repo: UserRepository = Depends(get_user_repo),
    security_service: SecurityCheckMeService = Depends(get_security_check_me_service),
) -> GetMeUseCase:
    return GetMeUseCase(user_repo, security_service)


def get_patchme_use_case(
    user_repo: UserRepository = Depends(get_user_repo),
    security_service: SecurityCheckMeService = Depends(get_security_check_me_service),
) -> PatchMeUseCase:
    return PatchMeUseCase(user_repo, security_service)


def get_delete_me_use_case(
    user_repo: UserRepository = Depends(get_user_repo),
    security_service: SecurityCheckMeService = Depends(get_security_check_me_service),
) -> DeleteMeUseCase:
    return DeleteMeUseCase(user_repo, security_service)


def get_get_by_id_use_case(
    user_repo: UserRepository = Depends(get_user_repo),
    security_service: SecurityPermissionService = Depends(
        get_security_permission_service
    ),
) -> GetUserUseCase:
    return GetUserUseCase(user_repo, security_service)


def get_patch_by_id_use_case(
    user_repo: UserRepository = Depends(get_user_repo),
    security_service: SecurityPermissionService = Depends(
        get_security_permission_service
    ),
) -> PatchUserUseCase:
    return PatchUserUseCase(user_repo, security_service)
