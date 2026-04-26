from app.application.ports.creation_session_repository import CreationSessionRepository
from app.domain.entities.creation import CreationSessionState


def create_creation_session(
    repository: CreationSessionRepository,
    user_id: int,
    grammar_text: str,
    description: str | None,
) -> CreationSessionState:
    return repository.create_session(user_id, grammar_text, description)
