from app.application.ports.user_repository import UserRepository
from app.domain.entities.auth import RegistrationDecision


def register_with_email(
    repository: UserRepository,
    email: str,
    password: str,
    invite_code: str | None,
    approval_mode: str,
) -> RegistrationDecision:
    user = repository.register_with_email(email, password, invite_code)
    return RegistrationDecision(
        user_id=user.id,
        email=user.email,
        access_state=user.access_state,
        is_admin=user.is_admin,
        approval_mode=approval_mode,
    )
