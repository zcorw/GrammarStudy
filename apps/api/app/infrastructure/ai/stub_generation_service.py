from __future__ import annotations

from app.application.ports.ai_generation_service import AiGenerationService
from app.domain.entities.creation import GeneratedGrammarDraft
from app.domain.entities.grammar import GrammarEntry, GrammarExample, PracticeQuestion


class StubAiGenerationService(AiGenerationService):
    def generate_grammar_draft(
        self,
        grammar_text: str,
        description: str | None,
        follow_up_history: list[str],
    ) -> GeneratedGrammarDraft:
        detail_hint = description or "No extra note yet."
        follow_up_hint = (
            f"Latest follow-up: {follow_up_history[-1]}"
            if follow_up_history
            else "No follow-up yet."
        )
        return GeneratedGrammarDraft(
            title=grammar_text,
            meaning=f"Structured draft for {grammar_text}. {detail_hint}",
            level="N3",
            tags=["N3", "AI Draft", "Needs Review"],
            connection=(
                f"名詞[普通形] + {grammar_text}\n"
                f"動詞[普通形] + {grammar_text}\n"
                f"い形容詞[普通形] + {grammar_text}\n"
                f"な形容詞[語幹/である] + {grammar_text}"
            ),
            context=f"Draft generated in creation flow. {follow_up_hint}",
            examples=[
                GrammarExample(
                    japanese=f"{grammar_text} を使った例文（草稿）1",
                    chinese="AI 生成例句草稿 1",
                ),
                GrammarExample(
                    japanese=f"{grammar_text} を使った例文（草稿）2",
                    chinese="AI 生成例句草稿 2",
                ),
            ],
            questions=[
                PracticeQuestion(
                    question=f"{grammar_text} 的选择题草稿 1",
                    options=["选项 A", "选项 B", "选项 C"],
                    explanation="Placeholder explanation before real AI integration.",
                )
            ],
        )

    def review_sentence(
        self,
        grammar: GrammarEntry,
        sentence: str,
    ) -> str:
        return (
            f"Sentence accepted for {grammar.title}. "
            "Keep the sentence natural and match the target nuance."
        )
