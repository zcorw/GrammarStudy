from __future__ import annotations

from typing import Protocol

from app.domain.entities.grammar import GrammarEntry, SearchGrammarResult


class GrammarRepository(Protocol):
    def list_recommended(self) -> list[GrammarEntry]:
        ...

    def get_by_id(self, grammar_id: str) -> GrammarEntry | None:
        ...

    def search(self, query: str) -> SearchGrammarResult:
        ...
