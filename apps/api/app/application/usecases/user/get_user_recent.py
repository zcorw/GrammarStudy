from app.application.ports.user_repository import UserRepository
from app.domain.entities.user import UserRecent


def get_user_recent(
    repository: UserRepository,
    user_id: int,
) -> UserRecent:
    return repository.get_recent(user_id)
