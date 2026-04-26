from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.application.ports.ai_generation_service import AiProviderError
from app.domain.entities.auth import AuthenticatedUser
from app.domain.entities.creation import CreationSessionState, GeneratedGrammarDraft
from app.infrastructure.container import Container
from app.presentation.api.dependencies.auth import require_approved_user
from app.presentation.api.errors import ApiError

router = APIRouter()


class CreateSessionRequest(BaseModel):
    grammar_text: str
    description: str | None = None


class FollowUpRequest(BaseModel):
    question: str


class DraftCardSchema(BaseModel):
    title: str
    meaning: str
    level: str
    tags: list[str]
    connection: str
    context: str
    examples: list[dict[str, str]]
    questions: list[dict[str, str | list[str]]]


class CreationSessionResponse(BaseModel):
    id: str
    grammar_text: str
    description: str | None
    status: str
    next_step: str
    draft_card: DraftCardSchema
    follow_up_history: list[str]
    published_grammar_id: str | None


class CompleteCreationResponse(BaseModel):
    card_id: str
    status: str


def _to_draft_card(draft: GeneratedGrammarDraft) -> DraftCardSchema:
    return DraftCardSchema(
        title=draft.title,
        meaning=draft.meaning,
        level=draft.level,
        tags=draft.tags,
        connection=draft.connection,
        context=draft.context,
        examples=[example.__dict__ for example in draft.examples],
        questions=[question.__dict__ for question in draft.questions],
    )


def _to_session_response(session_state: CreationSessionState) -> CreationSessionResponse:
    return CreationSessionResponse(
        id=session_state.id,
        grammar_text=session_state.grammar_text,
        description=session_state.description,
        status=session_state.status,
        next_step=session_state.next_step,
        draft_card=_to_draft_card(session_state.draft_card),
        follow_up_history=session_state.follow_up_history,
        published_grammar_id=session_state.published_grammar_id,
    )


@router.post("/sessions", response_model=CreationSessionResponse)
def create_session(
    payload: CreateSessionRequest,
    user: AuthenticatedUser = Depends(require_approved_user),
) -> CreationSessionResponse:
    try:
        result = Container.create_creation_session(
            user_id=user.id,
            grammar_text=payload.grammar_text,
            description=payload.description,
        )
    except AiProviderError as exc:
        raise ApiError(502, "ai_provider_failed", "AI provider request failed.") from exc
    return _to_session_response(result)


@router.get("/sessions/{session_id}", response_model=CreationSessionResponse)
def get_session(
    session_id: str,
    user: AuthenticatedUser = Depends(require_approved_user),
) -> CreationSessionResponse:
    result = Container.get_creation_session(user.id, session_id)
    if result is None:
        raise ApiError(404, "creation_session_not_found", "Creation session not found.")
    return _to_session_response(result)


@router.post("/sessions/{session_id}/follow-up", response_model=CreationSessionResponse)
def follow_up(
    session_id: str,
    payload: FollowUpRequest,
    user: AuthenticatedUser = Depends(require_approved_user),
) -> CreationSessionResponse:
    try:
        result = Container.apply_follow_up(user.id, session_id, payload.question)
    except ValueError as exc:
        raise ApiError(404, "creation_session_not_found", "Creation session not found.") from exc
    except AiProviderError as exc:
        raise ApiError(502, "ai_provider_failed", "AI provider request failed.") from exc
    return _to_session_response(result)


@router.post("/sessions/{session_id}/complete", response_model=CompleteCreationResponse)
def complete_creation(
    session_id: str,
    user: AuthenticatedUser = Depends(require_approved_user),
) -> CompleteCreationResponse:
    try:
        result = Container.complete_creation(user.id, session_id)
    except ValueError as exc:
        raise ApiError(404, "creation_session_not_found", "Creation session not found.") from exc
    return CompleteCreationResponse(**result.__dict__)
