from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChoiceSubmission:
    grammar_id: str
    selected_option: str
    result: str


@dataclass(frozen=True)
class SentenceReview:
    grammar_id: str
    feedback: str
