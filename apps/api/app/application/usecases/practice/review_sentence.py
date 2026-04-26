from app.application.ports.ai_generation_service import AiGenerationService
from app.application.ports.grammar_repository import GrammarRepository
from app.application.ports.user_repository import UserRepository
from app.domain.entities.auth import AuthenticatedUser
from app.domain.entities.practice import SentenceReview


def review_sentence(
    ai_generation_service: AiGenerationService,
    grammar_repository: GrammarRepository,
    user_repository: UserRepository,
    grammar_id: str,
    sentence: str,
    user: AuthenticatedUser,
) -> SentenceReview:
    grammar = grammar_repository.get_by_id(grammar_id)
    if grammar is None:
        raise ValueError("Grammar not found")

    feedback = ai_generation_service.review_sentence(grammar, sentence)
    user_repository.save_sentence_feedback(
        user_id=user.id,
        grammar_id=grammar_id,
        sentence=sentence,
        feedback=feedback,
    )
    return SentenceReview(
        grammar_id=grammar_id,
        feedback=feedback,
    )
