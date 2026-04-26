from app.application.ports.grammar_repository import GrammarRepository
from app.domain.entities.grammar import GrammarEntry


def get_grammar_detail(
    repository: GrammarRepository,
    grammar_id: str,
) -> GrammarEntry | None:
    return repository.get_by_id(grammar_id)
