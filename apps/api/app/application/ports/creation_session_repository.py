from __future__ import annotations

from typing import Protocol

from app.domain.entities.creation import CreationCompletion, CreationSessionState


class CreationSessionRepository(Protocol):
    def create_session(
        self,
        user_id: int,
        grammar_text: str,
        description: str | None,
    ) -> CreationSessionState:
        ...

    def get_session(
        self,
        user_id: int,
        session_id: str,
    ) -> CreationSessionState | None:
        ...

    def apply_follow_up(
        self,
        user_id: int,
        session_id: str,
        question: str,
    ) -> CreationSessionState:
        ...

    def complete_session(
        self,
        user_id: int,
        session_id: str,
    ) -> CreationCompletion:
        ...
