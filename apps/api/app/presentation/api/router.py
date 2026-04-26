from fastapi import APIRouter

from app.presentation.api.routes import auth, creation, grammar, health, practice, search, user

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(grammar.router, prefix="/grammar", tags=["grammar"])
api_router.include_router(creation.router, prefix="/creation", tags=["creation"])
api_router.include_router(practice.router, prefix="/practice", tags=["practice"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
