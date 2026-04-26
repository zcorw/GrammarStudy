from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.domain.entities.grammar import GrammarEntry, PracticeQuestion
from app.infrastructure.container import Container

router = APIRouter()


class PracticeQuestionSchema(BaseModel):
    question: str
    options: list[str]
    explanation: str


class GrammarDetailSchema(BaseModel):
    id: str
    title: str
    meaning: str
    level: str
    tags: list[str]
    connection: str
    context: str
    examples: list[dict[str, str]]
    questions: list[PracticeQuestionSchema]


def _to_question(question: PracticeQuestion) -> PracticeQuestionSchema:
    return PracticeQuestionSchema(**question.__dict__)


def _to_detail(entry: GrammarEntry) -> GrammarDetailSchema:
    return GrammarDetailSchema(
        id=entry.id,
        title=entry.title,
        meaning=entry.meaning,
        level=entry.level,
        tags=entry.tags,
        connection=entry.connection,
        context=entry.context,
        examples=[example.__dict__ for example in entry.examples],
        questions=[_to_question(question) for question in entry.questions],
    )


@router.get("/recommended", response_model=list[GrammarDetailSchema])
def get_recommended_grammar_route() -> list[GrammarDetailSchema]:
    return [_to_detail(item) for item in Container.get_recommended_grammar()]


@router.get("/{grammar_id}", response_model=GrammarDetailSchema)
def get_grammar_detail_route(grammar_id: str) -> GrammarDetailSchema:
    grammar = Container.get_grammar_detail(grammar_id)
    if grammar is None:
        raise HTTPException(status_code=404, detail="Grammar not found")
    return _to_detail(grammar)
