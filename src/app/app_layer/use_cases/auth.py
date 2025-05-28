from typing import Dict, cast

from app.app_layer.errors.exceptions.use_cases_exceptions import (
    BlockedException,
    PasswordException,
)
from app.app_layer.errors.strings import (
    BLACK_LIST,
    BLOCKED_USER,
    PASSWORD_VERIFY,
    WRONG_HASH,
)
from app.app_layer.schemas.auth import LoginSchema, ResetPasswordSchema
from app.app_layer.schemas.user import UserCreateForm, UserResponseSchema
from app.infra.repositories.sqla.user import UserRepository
from app.infra.services.hashing import PasswordService
from app.infra.services.jwt import TokenService
from app.infra.services.redis import RedisService
from app.infra.services.s3 import S3Service
from app.infra.services.ses import SESService


class SignupUseCase:
    def __init__(self, user_repo: UserRepository, s3_service: S3Service):
        self.user_repo = user_repo
        self.s3_service = s3_service

    async def __call__(
        self, user_data: UserCreateForm, file: bytes | None
    ) -> UserResponseSchema:
        user = await self.user_repo.create(user_data)

        if file is not None:
            await self.s3_service.upload_file(file, str(user.id))

        return UserResponseSchema.model_validate(user.__dict__)


class LoginUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        password_service: PasswordService,
        token_service: TokenService,
    ):
        self.password_service = password_service
        self.user_repo = user_repo
        self.token_service = token_service

    async def __call__(self, login_data: LoginSchema) -> Dict[TokenService.Scope, str]:
        user = await self.user_repo.get_by_login(login_data.login)

        if user.is_blocked is True:
            raise BlockedException(BLOCKED_USER)

        if not self.password_service.verify(login_data.password, user.password):
            raise PasswordException(WRONG_HASH)

        return self.token_service.create_access_refresh(
            username=user.username,
            user_id=str(user.id),
            group_id=user.group_id,
            role=user.role,
        )


class RefreshTokenUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        redis: RedisService,
        token_service: TokenService,
    ):
        self.token_service = token_service
        self.user_repo = user_repo
        self.redis_service = redis

    async def __call__(self, refresh_token: str) -> Dict[TokenService.Scope, str]:
        token_payload = self.token_service.authenticate(
            refresh_token, TokenService.refresh
        )

        user = await self.user_repo.get(cast(str, token_payload.get("user_id")))

        if user.is_blocked is True:
            raise BlockedException(BLOCKED_USER)

        token_in_redis = await self.redis_service.get_value(str(user.id))

        if token_in_redis is not None and refresh_token == token_in_redis:
            raise BlockedException(BLACK_LIST)

        await self.redis_service.set_value_expire(str(user.id), refresh_token, 200)

        return self.token_service.create_access_refresh(
            username=user.username,
            user_id=str(user.id),
            group_id=user.group_id,
            role=user.role,
        )


class ResetPasswordUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        ses_service: SESService,
        token_service: TokenService,
    ):
        self.token_service = token_service
        self.user_repo = user_repo
        self.ses_service = ses_service

    async def __call__(self, email: str):
        user = await self.user_repo.get_by_email(email)

        if user.is_blocked is True:
            raise BlockedException(BLOCKED_USER)

        token = self.token_service.create_token(
            username=user.username,
            user_id=str(user.id),
            group_id=user.group_id,
            role=user.role,
            scope=TokenService.reset,
        )

        link = f"http://localhost:8000/auth/reset-password/{token}"

        await self.ses_service.send_email(user.email, link)

        return {"Check email, please"}


class ResetPasswordConfirmUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        token_service: TokenService,
        password_service: PasswordService,
    ):
        self.token_service = token_service
        self.password_service = password_service
        self.user_repo = user_repo

    async def __call__(self, reset_token: str, passwords: ResetPasswordSchema):
        token_payload = self.token_service.authenticate(reset_token, TokenService.reset)

        if passwords.password != passwords.password2:
            raise PasswordException(PASSWORD_VERIFY)

        await self.user_repo.update_user_field(
            cast(str, token_payload.get("user_id")),
            "password",
            self.password_service.hash(passwords.password),
        )

        return {"The password has been changed successfully"}
