from typing import Annotated

from fastapi import APIRouter, Body, Depends, File, Header

from app.api.dependencies.auth_use_cases import (
    get_login_use_case,
    get_refresh_token_use_case,
    get_reset_password_confirm_use_case,
    get_reset_password_use_case,
    get_signup_use_case,
)
from app.app_layer.schemas.auth import EmailSchema, LoginSchema, ResetPasswordSchema
from app.app_layer.schemas.user import UserCreateForm
from app.app_layer.use_cases.auth import (
    LoginUseCase,
    RefreshTokenUseCase,
    ResetPasswordUseCase,
    ResetPasswordConfirmUseCase,
    SignupUseCase,
)

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/signup")
async def signup(
    file: Annotated[bytes, File()] = bytes(),
    signup_data: UserCreateForm = Depends(),
    use_case: SignupUseCase = Depends(get_signup_use_case),
):
    return await use_case(signup_data, file)


@auth_router.post("/login")
async def login(
    login_data: LoginSchema = Body(),
    use_case: LoginUseCase = Depends(get_login_use_case),
):
    return await use_case(login_data)


@auth_router.post("/refresh-token")
async def refresh_token(
    refresh_token: str = Header(),
    use_case: RefreshTokenUseCase = Depends(get_refresh_token_use_case),
):
    return await use_case(refresh_token)


@auth_router.post("/reset-password")
async def reset_password(
    email: EmailSchema = Body(),
    use_case: ResetPasswordUseCase = Depends(get_reset_password_use_case),
):
    return await use_case(email.email)


@auth_router.post("/reset-password/{reset_token}")
async def reset_password_confirm(
    reset_token: str,
    password: ResetPasswordSchema = Body(),
    use_case: ResetPasswordConfirmUseCase = Depends(
        get_reset_password_confirm_use_case
    ),
):
    return await use_case(reset_token, password)
