from app.application.ports.token_service import TokenService
from app.application.ports.user_repository import UserRepository
from app.domain.entities.auth import LoginDecision


def login_with_email(
    repository: UserRepository,
    token_service: TokenService,
    email: str,
    password: str,
    approval_mode: str,
    expires_in: int,
) -> LoginDecision:
    user = repository.login_with_email(email, password)
    return LoginDecision(
        user_id=user.id,
        email=user.email,
        access_state=user.access_state,
        is_admin=user.is_admin,
        approval_mode=approval_mode,
        access_token=token_service.issue_access_token(user, expires_in),
        token_type="bearer",
        expires_in=expires_in,
    )
