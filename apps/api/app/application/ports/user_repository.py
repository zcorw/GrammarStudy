from __future__ import annotations

from typing import Protocol

from app.domain.entities.auth import AuthenticatedUser
from app.domain.entities.user import UserGrammarListItem, UserRecent


class UserRepository(Protocol):
    def register_with_email(
        self,
        email: str,
        password: str,
        invite_code: str | None,
    ) -> AuthenticatedUser:
        ...

    def login_with_email(
        self,
        email: str,
        password: str,
    ) -> AuthenticatedUser:
        ...

    def get_by_id(self, user_id: int) -> AuthenticatedUser | None:
        ...

    def list_my_grammar(self, user_id: int) -> list[UserGrammarListItem]:
        ...

    def get_recent(self, user_id: int) -> UserRecent:
        ...

    def toggle_favorite(self, user_id: int, grammar_id: str) -> bool:
        ...

    def record_recent_view(self, user_id: int, grammar_id: str) -> None:
        ...

    def record_practice_attempt(
        self,
        user_id: int,
        grammar_id: str,
        selected_option: str,
        result: str,
    ) -> None:
        ...

    def save_sentence_feedback(
        self,
        user_id: int,
        grammar_id: str,
        sentence: str,
        feedback: str,
    ) -> None:
        ...
