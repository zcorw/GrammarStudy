from app.application.ports.ai_generation_service import AiProviderError
from app.application.usecases.auth.login_with_email import login_with_email
from app.application.usecases.auth.register_with_email import register_with_email
from app.application.usecases.creation.apply_follow_up import apply_follow_up
from app.application.usecases.creation.complete_creation import complete_creation
from app.application.usecases.creation.create_creation_session import create_creation_session
from app.application.usecases.creation.get_creation_session import get_creation_session
from app.application.usecases.grammar.get_grammar_detail import get_grammar_detail
from app.application.usecases.grammar.get_recommended_grammar import get_recommended_grammar
from app.application.usecases.practice.review_sentence import review_sentence
from app.application.usecases.practice.submit_choice import submit_choice
from app.application.usecases.search.search_grammar import search_grammar
from app.application.usecases.user.get_user_grammar_list import get_user_grammar_list
from app.application.usecases.user.get_user_recent import get_user_recent
from app.application.usecases.user.record_recent_view import record_recent_view
from app.application.usecases.user.toggle_favorite import toggle_favorite
from app.infrastructure.ai.openai_generation_service import OpenAIAiGenerationService
from app.infrastructure.ai.stub_generation_service import StubAiGenerationService
from app.infrastructure.config.settings import get_settings
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.repositories.postgres_creation_session_repository import (
    PostgresCreationSessionRepository,
)
from app.infrastructure.repositories.postgres_grammar_repository import (
    PostgresGrammarRepository,
)
from app.infrastructure.repositories.postgres_user_repository import PostgresUserRepository
from app.infrastructure.security.jwt_token_service import JwtTokenService

settings = get_settings()
grammar_repository = PostgresGrammarRepository(SessionLocal)
user_repository = PostgresUserRepository(SessionLocal)
token_service = JwtTokenService(settings.jwt_secret)


def _build_ai_generation_service():
    if settings.model_provider == "stub":
        return StubAiGenerationService()

    if settings.model_provider == "openai":
        if not settings.openai_api_key:
            return _UnavailableAiGenerationService(
                "OPENAI_API_KEY is required when MODEL_PROVIDER=openai."
            )
        return OpenAIAiGenerationService(
            api_key=settings.openai_api_key,
            model_name=settings.model_name,
            timeout_seconds=settings.ai_timeout_seconds,
        )

    return _UnavailableAiGenerationService(
        f"Unsupported AI provider: {settings.model_provider}."
    )


class _UnavailableAiGenerationService:
    def __init__(self, message: str) -> None:
        self._message = message

    def generate_grammar_draft(
        self,
        grammar_text: str,
        description: str | None,
        follow_up_history: list[str],
    ):
        raise AiProviderError(self._message)

    def review_sentence(self, grammar, sentence: str) -> str:
        raise AiProviderError(self._message)


ai_generation_service = _build_ai_generation_service()
creation_session_repository = PostgresCreationSessionRepository(SessionLocal, ai_generation_service)


class Container:
    @staticmethod
    def register_with_email(
        email: str,
        password: str,
        invite_code: str | None,
    ):
        return register_with_email(
            repository=user_repository,
            email=email,
            password=password,
            invite_code=invite_code,
            approval_mode=settings.approval_mode,
        )

    @staticmethod
    def login_with_email(
        email: str,
        password: str,
    ):
        return login_with_email(
            repository=user_repository,
            token_service=token_service,
            email=email,
            password=password,
            approval_mode=settings.approval_mode,
            expires_in=settings.access_token_expires_in,
        )

    @staticmethod
    def search_grammar(query: str):
        return search_grammar(grammar_repository, query)

    @staticmethod
    def get_grammar_detail(grammar_id: str):
        return get_grammar_detail(grammar_repository, grammar_id)

    @staticmethod
    def get_recommended_grammar():
        return get_recommended_grammar(grammar_repository)

    @staticmethod
    def create_creation_session(user_id: int, grammar_text: str, description: str | None):
        return create_creation_session(
            creation_session_repository,
            user_id,
            grammar_text,
            description,
        )

    @staticmethod
    def get_creation_session(user_id: int, session_id: str):
        return get_creation_session(creation_session_repository, user_id, session_id)

    @staticmethod
    def apply_follow_up(user_id: int, session_id: str, question: str):
        return apply_follow_up(creation_session_repository, user_id, session_id, question)

    @staticmethod
    def complete_creation(user_id: int, session_id: str):
        return complete_creation(creation_session_repository, user_id, session_id)

    @staticmethod
    def submit_choice(grammar_id: str, selected_option: str, user=None):
        return submit_choice(
            grammar_repository,
            user_repository,
            grammar_id,
            selected_option,
            user,
        )

    @staticmethod
    def review_sentence(grammar_id: str, sentence: str, user):
        return review_sentence(
            ai_generation_service,
            grammar_repository,
            user_repository,
            grammar_id,
            sentence,
            user,
        )

    @staticmethod
    def get_user_recent(user_id: int):
        return get_user_recent(user_repository, user_id)

    @staticmethod
    def get_user_grammar_list(user_id: int):
        return get_user_grammar_list(user_repository, user_id)

    @staticmethod
    def record_recent_view(user_id: int, grammar_id: str):
        if grammar_repository.get_by_id(grammar_id) is None:
            raise ValueError("Grammar not found")
        return record_recent_view(user_repository, user_id, grammar_id)

    @staticmethod
    def toggle_favorite(user_id: int, grammar_id: str):
        if grammar_repository.get_by_id(grammar_id) is None:
            raise ValueError("Grammar not found")
        return toggle_favorite(user_repository, user_id, grammar_id)
