from app.app_layer.schemas.user import UserResponseSchema, UsersResponseSchema
from app.app_layer.use_cases.security import SecurityPermissionService
from app.infra.repositories.sqla.models import Role
from app.infra.repositories.sqla.user import UserRepository


class UsersQueryUseCase:
    def __init__(
        self, user_repo: UserRepository, permission_service: SecurityPermissionService
    ) -> None:
        self.user_repo = user_repo
        self.permission_service = permission_service

    async def __call__(
        self,
        token: str,
        limit: int,
        page: int,
        order_by: str,
        sort_by: str,
        filter_by_name: str,
    ) -> UsersResponseSchema:
        role, group_id = await self.permission_service(token)

        users = await self.user_repo.param_query(
            limit,
            page,
            order_by,
            sort_by,
            filter_by_name,
            group_id=group_id if role == Role.MODERATOR else None,
        )

        return UsersResponseSchema(
            users=[UserResponseSchema.model_validate(user.__dict__) for user in users],
            page=page,
            limit=limit,
        )
