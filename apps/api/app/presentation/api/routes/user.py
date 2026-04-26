from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.domain.entities.auth import AuthenticatedUser
from app.infrastructure.container import Container
from app.presentation.api.dependencies.auth import require_approved_user
from app.presentation.api.errors import ApiError

router = APIRouter()


class FavoriteToggleResponse(BaseModel):
    grammar_id: str
    is_favorite: bool


@router.get("/recent")
def get_recent_route(
    user: AuthenticatedUser = Depends(require_approved_user),
) -> dict[str, list[str]]:
    return Container.get_user_recent(user.id).__dict__


@router.get("/my-grammar")
def get_my_grammar_route(
    user: AuthenticatedUser = Depends(require_approved_user),
) -> dict[str, list[dict[str, str]]]:
    items = Container.get_user_grammar_list(user.id)
    return {"items": [item.__dict__ for item in items]}


@router.post("/recent-views/{grammar_id}", status_code=204)
def record_recent_view_route(
    grammar_id: str,
    user: AuthenticatedUser = Depends(require_approved_user),
) -> None:
    try:
        Container.record_recent_view(user.id, grammar_id)
    except ValueError as exc:
        raise ApiError(404, "grammar_not_found", "Grammar not found.") from exc


@router.post("/favorites/{grammar_id}", response_model=FavoriteToggleResponse)
def toggle_favorite_route(
    grammar_id: str,
    user: AuthenticatedUser = Depends(require_approved_user),
) -> FavoriteToggleResponse:
    try:
        result = Container.toggle_favorite(user.id, grammar_id)
    except ValueError as exc:
        raise ApiError(404, "grammar_not_found", "Grammar not found.") from exc
    return FavoriteToggleResponse(**result.__dict__)
