from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def resolve_env_file() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / ".env"
        if candidate.exists():
            return candidate
    return Path(".env")


ENV_FILE = resolve_env_file()


class Settings(BaseSettings):
    app_name: str = "Grammar Study API"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/grammar_study"
    jwt_secret: str = "replace-me-with-at-least-32-bytes"
    access_token_expires_in: int = 60 * 60 * 24 * 7
    admin_email: str = "admin@example.com"
    admin_password: str = "change-this-admin-password"
    approval_mode: str = "invite_or_review"
    model_provider: str = "openai"
    model_name: str = "gpt-5-mini"
    openai_api_key: str | None = None
    ai_timeout_seconds: float = 60.0

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
