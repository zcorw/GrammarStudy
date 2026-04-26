from app.application.ports.user_repository import UserRepository
from app.domain.entities.user import UserGrammarListItem


def get_user_grammar_list(
    repository: UserRepository,
    user_id: int,
) -> list[UserGrammarListItem]:
    return repository.list_my_grammar(user_id)
