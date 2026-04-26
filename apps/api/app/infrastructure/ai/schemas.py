from __future__ import annotations

from pydantic import BaseModel, Field


class CreationExampleSchema(BaseModel):
    japanese: str = Field(description="Japanese example sentence using the target grammar.")
    chinese: str = Field(description="Chinese explanation or translation of the example sentence.")


class CreationQuestionSchema(BaseModel):
    question: str = Field(description="A multiple-choice question about the target grammar.")
    options: list[str] = Field(
        min_length=3,
        max_length=4,
        description="Three or four answer options in Chinese or Japanese.",
    )
    explanation: str = Field(description="Short explanation for the correct answer.")


class CreationDraftSchema(BaseModel):
    title: str = Field(description="Canonical Japanese grammar title.")
    meaning: str = Field(description="Meaning explained for Chinese-speaking Japanese learners.")
    level: str = Field(description="Approximate JLPT level such as N1-N5.")
    tags: list[str] = Field(
        min_length=2,
        max_length=5,
        description="Short tags such as level, usage, nuance, or register.",
    )
    connection: str = Field(
        description=(
            "Connection patterns. Use one line per pattern. "
            "Each line must be formatted as 品詞[活用形・接続形] + target grammar, "
            "for example: 動詞[普通形] + だけあって."
        )
    )
    context: str = Field(description="Usage context and contrastive nuance summary.")
    examples: list[CreationExampleSchema] = Field(
        min_length=2,
        max_length=3,
        description="Two or three natural example sentences.",
    )
    questions: list[CreationQuestionSchema] = Field(
        min_length=1,
        max_length=2,
        description="One or two multiple-choice questions.",
    )


class SentenceReviewSchema(BaseModel):
    feedback: str = Field(
        description=(
            "Concise sentence review in Chinese with correction, nuance, "
            "and a short suggestion."
        )
    )
