from fastapi import APIRouter, Body, Depends, Header

from app.api.dependencies.user_use_cases import (
    get_delete_me_use_case,
    get_get_by_id_use_case,
    get_getme_use_case,
    get_patch_by_id_use_case,
    get_patchme_use_case,
)
from app.app_layer.schemas.user import UserUpdateSchema
from app.app_layer.use_cases.user import (
    DeleteMeUseCase,
    GetMeUseCase,
    GetUserUseCase,
    PatchMeUseCase,
    PatchUserUseCase,
)
from app.app_layer.schemas.user import UserResponseSchema

user_router = APIRouter(tags=["user"])


@user_router.get("/me")
async def get_me(
    access_token: str = Header(), use_case: GetMeUseCase = Depends(get_getme_use_case)
) -> UserResponseSchema:
    return await use_case(access_token)


@user_router.patch("/me")
async def update_me(
    access_token: str = Header(),
    new_user_data: UserUpdateSchema = Body(),
    use_case: PatchMeUseCase = Depends(get_patchme_use_case),
) -> UserResponseSchema:
    return await use_case(access_token, new_user_data)


@user_router.delete("/me")
async def delete_me(
    access_token: str = Header(),
    use_case: DeleteMeUseCase = Depends(get_delete_me_use_case),
):
    return await use_case(access_token)


@user_router.get("/{user_id}")
async def get_user(
    user_id: str,
    access_token: str = Header(),
    use_case: GetUserUseCase = Depends(get_get_by_id_use_case),
) -> UserResponseSchema:
    return await use_case(access_token, user_id)


@user_router.patch("/{user_id}")
async def update_user(
    user_id: str,
    access_token: str = Header(),
    new_user_data: UserUpdateSchema = Body(),
    use_case: PatchUserUseCase = Depends(get_patch_by_id_use_case),
) -> UserResponseSchema:
    return await use_case(access_token, user_id, new_user_data)
