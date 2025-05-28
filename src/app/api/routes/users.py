from fastapi import APIRouter, Depends, Header, Query

from app.api.dependencies.users_use_cases import get_users_use_case
from app.app_layer.use_cases.users import UsersQueryUseCase

users_router = APIRouter(tags=["users"])


@users_router.get("/")
async def users(
    access_token: str = Header(),
    limit: int = Query(default=10),
    page: int = Query(default=1),
    order_by: str = Query(default="asc"),
    sort_by: str = Query(default="created_at"),
    filter_by_name: str = Query(default=None),
    use_case: UsersQueryUseCase = Depends(get_users_use_case),
):
    return await use_case(access_token, limit, page, order_by, sort_by, filter_by_name)
