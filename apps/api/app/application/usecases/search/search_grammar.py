from app.application.ports.grammar_repository import GrammarRepository
from app.domain.entities.grammar import SearchGrammarResult


def search_grammar(
    repository: GrammarRepository,
    query: str,
) -> SearchGrammarResult:
    return repository.search(query)
