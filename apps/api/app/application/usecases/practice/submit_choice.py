from app.application.ports.grammar_repository import GrammarRepository
from app.application.ports.user_repository import UserRepository
from app.domain.entities.auth import AuthenticatedUser
from app.domain.entities.practice import ChoiceSubmission


def submit_choice(
    grammar_repository: GrammarRepository,
    user_repository: UserRepository,
    grammar_id: str,
    selected_option: str,
    user: AuthenticatedUser | None = None,
) -> ChoiceSubmission:
    if grammar_repository.get_by_id(grammar_id) is None:
        raise ValueError("Grammar not found")

    result = "recorded"
    if user is not None and user.access_state == "approved":
        user_repository.record_practice_attempt(
            user_id=user.id,
            grammar_id=grammar_id,
            selected_option=selected_option,
            result=result,
        )

    return ChoiceSubmission(
        grammar_id=grammar_id,
        selected_option=selected_option,
        result=result,
    )
