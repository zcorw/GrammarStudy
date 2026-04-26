from app.application.ports.creation_session_repository import CreationSessionRepository
from app.domain.entities.creation import CreationCompletion


def complete_creation(
    repository: CreationSessionRepository,
    user_id: int,
    session_id: str,
) -> CreationCompletion:
    return repository.complete_session(user_id, session_id)
