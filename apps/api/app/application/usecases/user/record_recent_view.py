from app.application.ports.user_repository import UserRepository


def record_recent_view(
    repository: UserRepository,
    user_id: int,
    grammar_id: str,
) -> None:
    repository.record_recent_view(user_id, grammar_id)
