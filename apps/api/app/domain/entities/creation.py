from __future__ import annotations

from dataclasses import dataclass

from app.domain.entities.grammar import GrammarExample, PracticeQuestion


@dataclass(frozen=True)
class GeneratedGrammarDraft:
    title: str
    meaning: str
    level: str
    tags: list[str]
    connection: str
    context: str
    examples: list[GrammarExample]
    questions: list[PracticeQuestion]


@dataclass(frozen=True)
class CreationSessionState:
    id: str
    grammar_text: str
    description: str | None
    status: str
    next_step: str
    draft_card: GeneratedGrammarDraft
    follow_up_history: list[str]
    published_grammar_id: str | None


@dataclass(frozen=True)
class CreationCompletion:
    card_id: str
    status: str
