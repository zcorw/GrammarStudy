from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GrammarExample:
    japanese: str
    chinese: str


@dataclass(frozen=True)
class PracticeQuestion:
    question: str
    options: list[str]
    explanation: str


@dataclass(frozen=True)
class GrammarEntry:
    id: str
    title: str
    meaning: str
    level: str
    tags: list[str]
    connection: str
    context: str
    examples: list[GrammarExample]
    questions: list[PracticeQuestion]


@dataclass(frozen=True)
class SearchGrammarResult:
    best_match: GrammarEntry | None
    similar_cards: list[GrammarEntry]
    search_confidence: float
    should_offer_ai_generation: bool
