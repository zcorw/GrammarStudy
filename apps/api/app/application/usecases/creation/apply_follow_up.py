from app.application.ports.creation_session_repository import CreationSessionRepository
from app.domain.entities.creation import CreationSessionState


def apply_follow_up(
    repository: CreationSessionRepository,
    user_id: int,
    session_id: str,
    question: str,
) -> CreationSessionState:
    return repository.apply_follow_up(user_id, session_id, question)
