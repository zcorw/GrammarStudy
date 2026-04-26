from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.models.base import Base


class GrammarEntryModel(Base):
    __tablename__ = "grammar_entries"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title_raw: Mapped[str] = mapped_column(String(128), nullable=False)
    title_normalized: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    title_reading_kana: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    meaning: Mapped[str] = mapped_column(Text, nullable=False)
    connection: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[str] = mapped_column(Text, nullable=False)
    examples_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    tags_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    created_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("user_accounts.id"),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    practice_questions: Mapped[list["PracticeQuestionModel"]] = relationship(
        back_populates="grammar",
        cascade="all, delete-orphan",
    )


class PracticeQuestionModel(Base):
    __tablename__ = "practice_questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    grammar_id: Mapped[str] = mapped_column(ForeignKey("grammar_entries.id"), index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    options_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    explanation: Mapped[str] = mapped_column(Text, nullable=False)

    grammar: Mapped[GrammarEntryModel] = relationship(back_populates="practice_questions")
