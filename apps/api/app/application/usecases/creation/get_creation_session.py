from app.application.ports.creation_session_repository import CreationSessionRepository
from app.domain.entities.creation import CreationSessionState


def get_creation_session(
    repository: CreationSessionRepository,
    user_id: int,
    session_id: str,
) -> CreationSessionState | None:
    return repository.get_session(user_id, session_id)
