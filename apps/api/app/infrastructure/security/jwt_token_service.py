from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt

from app.domain.entities.auth import AuthenticatedUser


class JwtTokenService:
    def __init__(self, secret: str) -> None:
        self._secret = secret

    def issue_access_token(
        self,
        user: AuthenticatedUser,
        expires_in: int,
    ) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "access_state": user.access_state,
            "is_admin": user.is_admin,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=expires_in)).timestamp()),
        }
        return jwt.encode(payload, self._secret, algorithm="HS256")

    def decode_access_token(self, token: str) -> AuthenticatedUser:
        payload = jwt.decode(token, self._secret, algorithms=["HS256"])
        return AuthenticatedUser(
            id=int(payload["sub"]),
            email=str(payload["email"]),
            access_state=str(payload["access_state"]),
            is_admin=bool(payload.get("is_admin", False)),
        )
