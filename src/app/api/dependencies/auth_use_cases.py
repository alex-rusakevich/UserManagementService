from fastapi import Depends

from app.api.dependencies.clients.aws_service_client import (
    get_s3_client_service,
    get_ses_client_service,
)
from app.api.dependencies.clients.redis_client import get_redis_service
from app.api.dependencies.clients.user_repo import UserRepository, get_user_repo
from app.infra.services.s3 import S3Service
from app.app_layer.use_cases.auth import (
    LoginUseCase,
    PasswordService,
    RefreshTokenUseCase,
    ResetPasswordConfirmUseCase,
    ResetPasswordUseCase,
    SignupUseCase,
)
from app.infra.services.ses import SESService
from app.api.dependencies.clients.security_services import get_token_service
from app.infra.services.jwt import TokenService
from app.infra.services.redis import RedisService
from app.api.dependencies.clients.security_services import get_password_service


def get_signup_use_case(
    user_repo: UserRepository = Depends(get_user_repo),
    s3_service: S3Service = Depends(get_s3_client_service),
) -> SignupUseCase:
    return SignupUseCase(user_repo, s3_service)


def get_login_use_case(
    user_repo: UserRepository = Depends(get_user_repo),
    token_service: TokenService = Depends(get_token_service),
    password_service: PasswordService = Depends(get_password_service),
) -> LoginUseCase:
    return LoginUseCase(
        user_repo=user_repo,
        password_service=password_service,
        token_service=token_service,
    )


def get_refresh_token_use_case(
    user_repo: UserRepository = Depends(get_user_repo),
    redis_service: RedisService = Depends(get_redis_service),
    token_service=Depends(get_token_service),
) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(user_repo, redis_service, token_service)


def get_reset_password_use_case(
    user_repo: UserRepository = Depends(get_user_repo),
    ses_service: SESService = Depends(get_ses_client_service),
    token_service=Depends(get_token_service),
) -> ResetPasswordUseCase:
    return ResetPasswordUseCase(
        user_repo, ses_service=ses_service, token_service=token_service
    )


def get_reset_password_confirm_use_case(
    user_repo: UserRepository = Depends(get_user_repo),
    token_service: TokenService = Depends(get_token_service),
    password_service: PasswordService = Depends(get_password_service),
) -> ResetPasswordConfirmUseCase:
    return ResetPasswordConfirmUseCase(user_repo, token_service, password_service)
