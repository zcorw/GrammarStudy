from app.application.ports.grammar_repository import GrammarRepository
from app.domain.entities.grammar import GrammarEntry


def get_recommended_grammar(
    repository: GrammarRepository,
) -> list[GrammarEntry]:
    return repository.list_recommended()
