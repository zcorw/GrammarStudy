from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.domain.entities.grammar import GrammarEntry
from app.infrastructure.container import Container

router = APIRouter()


class GrammarSummary(BaseModel):
    id: str
    title: str
    meaning: str
    level: str
    tags: list[str]
    connection: str
    context: str
    examples: list[dict[str, str]]


class SearchResponse(BaseModel):
    best_match: GrammarSummary | None
    similar_cards: list[GrammarSummary]
    search_confidence: float
    should_offer_ai_generation: bool


def _to_summary(entry: GrammarEntry) -> GrammarSummary:
    return GrammarSummary(
        id=entry.id,
        title=entry.title,
        meaning=entry.meaning,
        level=entry.level,
        tags=entry.tags,
        connection=entry.connection,
        context=entry.context,
        examples=[example.__dict__ for example in entry.examples],
    )


@router.get("/grammar", response_model=SearchResponse)
def search_grammar_route(q: str = Query(..., min_length=1)) -> SearchResponse:
    result = Container.search_grammar(q)
    return SearchResponse(
        best_match=_to_summary(result.best_match) if result.best_match else None,
        similar_cards=[_to_summary(item) for item in result.similar_cards],
        search_confidence=result.search_confidence,
        should_offer_ai_generation=result.should_offer_ai_generation,
    )
