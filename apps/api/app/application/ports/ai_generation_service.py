from __future__ import annotations

from typing import Protocol

from app.domain.entities.creation import GeneratedGrammarDraft
from app.domain.entities.grammar import GrammarEntry


class AiProviderError(Exception):
    pass


class AiGenerationService(Protocol):
    def generate_grammar_draft(
        self,
        grammar_text: str,
        description: str | None,
        follow_up_history: list[str],
    ) -> GeneratedGrammarDraft:
        ...

    def review_sentence(
        self,
        grammar: GrammarEntry,
        sentence: str,
    ) -> str:
        ...
