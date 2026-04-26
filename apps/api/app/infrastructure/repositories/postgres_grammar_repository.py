from __future__ import annotations

import json
from collections.abc import Callable

from sqlalchemy import Select, desc, or_, select
from sqlalchemy.orm import Session

from app.application.ports.grammar_repository import GrammarRepository
from app.domain.entities.grammar import (
    GrammarEntry,
    GrammarExample,
    PracticeQuestion,
    SearchGrammarResult,
)
from app.infrastructure.persistence.models.grammar import (
    GrammarEntryModel,
    PracticeQuestionModel,
)


class PostgresGrammarRepository(GrammarRepository):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory

    def list_recommended(self) -> list[GrammarEntry]:
        with self._session_factory() as session:
            statement = (
                select(GrammarEntryModel)
                .order_by(desc(GrammarEntryModel.created_at))
                .limit(12)
            )
            entries = session.execute(statement).scalars().all()
            return [self._to_entity(entry) for entry in entries]

    def get_by_id(self, grammar_id: str) -> GrammarEntry | None:
        with self._session_factory() as session:
            entry = session.get(GrammarEntryModel, grammar_id)
            if entry is None:
                return None
            return self._to_entity(entry)

    def search(self, query: str) -> SearchGrammarResult:
        with self._session_factory() as session:
            lowered = query.strip()
            statement: Select[tuple[GrammarEntryModel]] = (
                select(GrammarEntryModel)
                .where(
                    or_(
                        GrammarEntryModel.title_raw.ilike(f"%{lowered}%"),
                        GrammarEntryModel.title_normalized.ilike(f"%{lowered}%"),
                        GrammarEntryModel.title_reading_kana.ilike(f"%{lowered}%"),
                        GrammarEntryModel.meaning.ilike(f"%{lowered}%"),
                        GrammarEntryModel.tags_json.ilike(f"%{lowered}%"),
                    )
                )
                .order_by(desc(GrammarEntryModel.created_at))
                .limit(8)
            )
            matches = session.execute(statement).scalars().all()
            entities = [self._to_entity(entry) for entry in matches]

        return SearchGrammarResult(
            best_match=entities[0] if entities else None,
            similar_cards=entities[1:],
            search_confidence=0.9 if entities else 0.2,
            should_offer_ai_generation=not entities,
        )

    def _to_entity(self, entry: GrammarEntryModel) -> GrammarEntry:
        questions = sorted(entry.practice_questions, key=lambda item: item.id)
        return GrammarEntry(
            id=entry.id,
            title=entry.title_raw,
            meaning=entry.meaning,
            level=self._extract_level(entry.tags_json),
            tags=self._load_json_list(entry.tags_json),
            connection=entry.connection,
            context=entry.context,
            examples=[
                GrammarExample(**item) for item in self._load_json_list(entry.examples_json)
            ],
            questions=[self._to_question(question) for question in questions],
        )

    @staticmethod
    def _to_question(question: PracticeQuestionModel) -> PracticeQuestion:
        return PracticeQuestion(
            question=question.question,
            options=PostgresGrammarRepository._load_json_list(question.options_json),
            explanation=question.explanation,
        )

    @staticmethod
    def _load_json_list(raw: str):
        return json.loads(raw) if raw else []

    @staticmethod
    def _extract_level(tags_json: str) -> str:
        tags = PostgresGrammarRepository._load_json_list(tags_json)
        return next((tag for tag in tags if tag.startswith("N")), "N/A")
