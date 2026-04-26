from app.application.ports.user_repository import UserRepository
from app.domain.entities.user import FavoriteToggleResult


def toggle_favorite(
    repository: UserRepository,
    user_id: int,
    grammar_id: str,
) -> FavoriteToggleResult:
    return FavoriteToggleResult(
        grammar_id=grammar_id,
        is_favorite=repository.toggle_favorite(user_id, grammar_id),
    )
