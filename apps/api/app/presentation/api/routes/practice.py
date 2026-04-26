from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.application.ports.ai_generation_service import AiProviderError
from app.domain.entities.auth import AuthenticatedUser
from app.infrastructure.container import Container
from app.presentation.api.dependencies.auth import get_optional_user, require_approved_user
from app.presentation.api.errors import ApiError

router = APIRouter()


class SubmitChoiceRequest(BaseModel):
    grammar_id: str
    selected_option: str


class SentenceFeedbackRequest(BaseModel):
    grammar_id: str
    sentence: str


@router.post("/choice/submit")
def submit_choice_route(
    payload: SubmitChoiceRequest,
    user: AuthenticatedUser | None = Depends(get_optional_user),
) -> dict[str, str]:
    try:
        result = Container.submit_choice(
            grammar_id=payload.grammar_id,
            selected_option=payload.selected_option,
            user=user,
        )
    except ValueError as exc:
        raise ApiError(404, "grammar_not_found", "Grammar not found.") from exc
    return result.__dict__


@router.post("/sentence-feedback")
def sentence_feedback_route(
    payload: SentenceFeedbackRequest,
    user: AuthenticatedUser = Depends(require_approved_user),
) -> dict[str, str]:
    try:
        result = Container.review_sentence(
            grammar_id=payload.grammar_id,
            sentence=payload.sentence,
            user=user,
        )
    except ValueError as exc:
        raise ApiError(404, "grammar_not_found", "Grammar not found.") from exc
    except AiProviderError as exc:
        raise ApiError(502, "ai_provider_failed", "AI provider request failed.") from exc
    return result.__dict__
