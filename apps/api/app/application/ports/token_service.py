from __future__ import annotations

from typing import Protocol

from app.domain.entities.auth import AuthenticatedUser


class TokenService(Protocol):
    def issue_access_token(
        self,
        user: AuthenticatedUser,
        expires_in: int,
    ) -> str:
        ...

    def decode_access_token(self, token: str) -> AuthenticatedUser:
        ...
