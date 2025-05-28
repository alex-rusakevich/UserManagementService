import datetime
from typing import Dict, Literal, cast

from jose import jwt

from app.app_layer.errors.exceptions.services_exceptions import (
    TokenExpireException,
    TokenProcessingException,
)
from app.app_layer.errors.strings import (
    TOKEN_CREATION,
    TOKEN_EXPIRATION,
    TOKEN_EXTRACTION,
    TOKEN_SCOPE,
)
from app.config import JwtConfig


class TokenService:
    access = "access"
    refresh = "refresh"
    reset = "reset"

    Scope = Literal["access", "refresh", "reset"] | str

    scope_expire: Dict[str, int] = {access: 20, refresh: 200, reset: 20}

    def __init__(self, config: JwtConfig):
        self.config = config

    def create_token(
        self, username: str, user_id: str, group_id: int, role: str, scope: Scope
    ) -> str:
        try:
            payload = {
                "username": username,
                "user_id": str(user_id),
                "group_id": group_id,
                "role": role,
                "scope": scope,
                "expires": (
                    datetime.datetime.now()
                    + datetime.timedelta(minutes=TokenService.scope_expire[scope])
                ).isoformat(),
            }

            return jwt.encode(
                payload, self.config.secret_key, algorithm=self.config.hash_alg_token
            )
        except Exception:
            raise TokenProcessingException(data=user_id, info=TOKEN_CREATION)

    def create_access_refresh(
        self, username: str, user_id: str, group_id: int, role: str
    ) -> Dict[Scope, str]:
        return {
            TokenService.access: self.create_token(
                username, user_id, group_id, role, TokenService.access
            ),
            TokenService.refresh: self.create_token(
                username, user_id, group_id, role, TokenService.refresh
            ),
        }

    def _extract_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, self.config.secret_key, self.config.hash_alg_token
            )
            expire_dt = datetime.datetime.strptime(
                cast(str, payload.get("expires")), "%Y-%m-%dT%H:%M:%S.%f"
            )

            if datetime.datetime.now() > expire_dt:
                raise TokenExpireException(TOKEN_EXPIRATION)

            return payload
        except Exception:
            raise TokenProcessingException(data=token, info=TOKEN_EXTRACTION)

    def authenticate(self, token: str, scope: Scope) -> dict:
        token_payload = self._extract_token(token)

        if token_payload.get("scope") != scope:
            raise TokenProcessingException(data=token, info=TOKEN_SCOPE)

        return token_payload

    def get_from_payload(self, token: str, key: str) -> str | None:
        return self._extract_token(token).get(key, None)
