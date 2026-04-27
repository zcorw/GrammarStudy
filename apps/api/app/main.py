import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.infrastructure.bootstrap.seed_demo_data import seed_admin_account, seed_demo_grammar
from app.infrastructure.config.settings import get_settings
from app.infrastructure.database.session import SessionLocal
from app.presentation.api.errors import install_error_handlers
from app.presentation.api.router import api_router

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
            if settings.seed_demo_data:
                seed_demo_grammar(session, settings)
            else:
                seed_admin_account(session, settings)
    except SQLAlchemyError as exc:
        logger.warning("Database bootstrap skipped: %s", exc)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

install_error_handlers(app)
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    return {"message": "Grammar Study API"}
