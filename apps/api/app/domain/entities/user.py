from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UserRecent:
    recent_views: list[str]
    practice_records: list[str]
    favorites: list[str]


@dataclass(frozen=True)
class UserGrammarListItem:
    id: str
    title: str
    source: str
    last_activity_at: str


@dataclass(frozen=True)
class FavoriteToggleResult:
    grammar_id: str
    is_favorite: bool
