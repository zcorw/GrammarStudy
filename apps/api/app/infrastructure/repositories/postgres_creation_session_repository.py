from __future__ import annotations

import json
from uuid import uuid4

from sqlalchemy.orm import Session, sessionmaker

from app.application.ports.ai_generation_service import AiGenerationService
from app.application.ports.creation_session_repository import CreationSessionRepository
from app.domain.entities.creation import (
    CreationCompletion,
    CreationSessionState,
    GeneratedGrammarDraft,
)
from app.domain.entities.grammar import GrammarExample, PracticeQuestion
from app.infrastructure.persistence.models.creation import CreationSessionModel
from app.infrastructure.persistence.models.grammar import (
    GrammarEntryModel,
    PracticeQuestionModel,
)


class PostgresCreationSessionRepository(CreationSessionRepository):
    def __init__(
        self,
        session_factory: sessionmaker[Session],
        ai_generation_service: AiGenerationService,
    ) -> None:
        self._session_factory = session_factory
        self._ai_generation_service = ai_generation_service

    def create_session(
        self,
        user_id: int,
        grammar_text: str,
        description: str | None,
    ) -> CreationSessionState:
        draft = self._ai_generation_service.generate_grammar_draft(grammar_text, description, [])
        session_model = CreationSessionModel(
            id=f"ses_{uuid4().hex[:16]}",
            user_id=user_id,
            grammar_text=grammar_text,
            description=description,
            status="draft_ready",
            next_step="review_generated_card",
            draft_card_json=self._serialize_draft(draft),
            follow_up_history_json="[]",
        )

        with self._session_factory() as session:
            session.add(session_model)
            session.commit()
            session.refresh(session_model)
            return self._to_entity(session_model)

    def get_session(
        self,
        user_id: int,
        session_id: str,
    ) -> CreationSessionState | None:
        with self._session_factory() as session:
            session_model = session.get(CreationSessionModel, session_id)
            if session_model is None or session_model.user_id != user_id:
                return None
            return self._to_entity(session_model)

    def apply_follow_up(
        self,
        user_id: int,
        session_id: str,
        question: str,
    ) -> CreationSessionState:
        with self._session_factory() as session:
            session_model = session.get(CreationSessionModel, session_id)
            if session_model is None or session_model.user_id != user_id:
                raise ValueError("Creation session not found")

            history = self._load_json_list(session_model.follow_up_history_json)
            history.append(question)
            draft = self._ai_generation_service.generate_grammar_draft(
                session_model.grammar_text,
                session_model.description,
                history,
            )
            session_model.follow_up_history_json = json.dumps(history, ensure_ascii=False)
            session_model.draft_card_json = self._serialize_draft(draft)
            session_model.status = "updated_with_follow_up"
            session_model.next_step = "review_revision"
            session.commit()
            session.refresh(session_model)
            return self._to_entity(session_model)

    def complete_session(
        self,
        user_id: int,
        session_id: str,
    ) -> CreationCompletion:
        with self._session_factory() as session:
            session_model = session.get(CreationSessionModel, session_id)
            if session_model is None or session_model.user_id != user_id:
                raise ValueError("Creation session not found")

            if session_model.published_grammar_id is not None:
                return CreationCompletion(
                    card_id=session_model.published_grammar_id,
                    status="published",
                )

            draft = self._deserialize_draft(session_model.draft_card_json)
            grammar_id = f"grm_{uuid4().hex[:16]}"
            grammar_entry = GrammarEntryModel(
                id=grammar_id,
                title_raw=draft.title,
                title_normalized=draft.title.replace(" ", "").lower(),
                title_reading_kana=draft.title.replace(" ", "").lower(),
                meaning=draft.meaning,
                connection=draft.connection,
                context=draft.context,
                examples_json=json.dumps(
                    [example.__dict__ for example in draft.examples],
                    ensure_ascii=False,
                ),
                tags_json=json.dumps(draft.tags, ensure_ascii=False),
                created_by_user_id=user_id,
            )
            grammar_entry.practice_questions = [
                PracticeQuestionModel(
                    question=question.question,
                    options_json=json.dumps(question.options, ensure_ascii=False),
                    explanation=question.explanation,
                )
                for question in draft.questions
            ]

            session.add(grammar_entry)
            session_model.status = "published"
            session_model.next_step = "published"
            session_model.published_grammar_id = grammar_id
            session.commit()
            return CreationCompletion(card_id=grammar_id, status="published")

    def _to_entity(self, session_model: CreationSessionModel) -> CreationSessionState:
        return CreationSessionState(
            id=session_model.id,
            grammar_text=session_model.grammar_text,
            description=session_model.description,
            status=session_model.status,
            next_step=session_model.next_step,
            draft_card=self._deserialize_draft(session_model.draft_card_json),
            follow_up_history=self._load_json_list(session_model.follow_up_history_json),
            published_grammar_id=session_model.published_grammar_id,
        )

    @staticmethod
    def _serialize_draft(draft: GeneratedGrammarDraft) -> str:
        return json.dumps(
            {
                "title": draft.title,
                "meaning": draft.meaning,
                "level": draft.level,
                "tags": draft.tags,
                "connection": draft.connection,
                "context": draft.context,
                "examples": [item.__dict__ for item in draft.examples],
                "questions": [item.__dict__ for item in draft.questions],
            },
            ensure_ascii=False,
        )

    @staticmethod
    def _deserialize_draft(raw: str) -> GeneratedGrammarDraft:
        payload = json.loads(raw)
        return GeneratedGrammarDraft(
            title=payload["title"],
            meaning=payload["meaning"],
            level=payload["level"],
            tags=payload["tags"],
            connection=payload["connection"],
            context=payload["context"],
            examples=[GrammarExample(**item) for item in payload["examples"]],
            questions=[PracticeQuestion(**item) for item in payload["questions"]],
        )

    @staticmethod
    def _load_json_list(raw: str) -> list[str]:
        return json.loads(raw) if raw else []
