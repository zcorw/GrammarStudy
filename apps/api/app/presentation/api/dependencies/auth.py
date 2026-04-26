from __future__ import annotations

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError

from app.domain.entities.auth import AuthenticatedUser
from app.infrastructure.container import token_service, user_repository
from app.presentation.api.errors import ApiError

bearer_scheme = HTTPBearer(auto_error=False)


def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> AuthenticatedUser | None:
    if credentials is None:
        return None

    try:
        user = token_service.decode_access_token(credentials.credentials)
    except ExpiredSignatureError as exc:
        raise ApiError(401, "auth_token_expired", "Access token expired.") from exc
    except InvalidTokenError as exc:
        raise ApiError(401, "auth_invalid_token", "Access token is invalid.") from exc

    persisted_user = user_repository.get_by_id(user.id)
    if persisted_user is None:
        raise ApiError(401, "auth_user_missing", "User account no longer exists.")
    return persisted_user


def require_current_user(
    user: AuthenticatedUser | None = Depends(get_optional_user),
) -> AuthenticatedUser:
    if user is None:
        raise ApiError(401, "auth_required", "Login is required.")
    return user


def require_approved_user(
    user: AuthenticatedUser = Depends(require_current_user),
) -> AuthenticatedUser:
    if user.access_state != "approved":
        raise ApiError(403, "approval_pending", "Account is pending review.")
    return user
