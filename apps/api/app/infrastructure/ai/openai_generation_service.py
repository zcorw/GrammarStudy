from __future__ import annotations

import logging

from pydantic import ValidationError

from app.application.ports.ai_generation_service import AiGenerationService, AiProviderError
from app.domain.entities.creation import GeneratedGrammarDraft
from app.domain.entities.grammar import GrammarEntry, GrammarExample, PracticeQuestion
from app.infrastructure.ai.schemas import CreationDraftSchema, SentenceReviewSchema

logger = logging.getLogger(__name__)


class OpenAIAiGenerationService(AiGenerationService):
    def __init__(
        self,
        api_key: str,
        model_name: str,
        timeout_seconds: float = 60.0,
    ) -> None:
        from openai import OpenAI

        self._client = OpenAI(api_key=api_key, timeout=timeout_seconds)
        self._model_name = model_name

    def generate_grammar_draft(
        self,
        grammar_text: str,
        description: str | None,
        follow_up_history: list[str],
    ) -> GeneratedGrammarDraft:
        description_text = description or "无额外说明"
        follow_ups = "\n".join(f"- {item}" for item in follow_up_history) or "- 无"
        parsed = self._parse_response(
            system_prompt=(
                "你是一名严谨的日语文法教师，面向中文母语学习者。"
                "请输出结构化文法卡片，内容要准确、自然、可教学。"
                "例句必须自然，且要真正体现目标文法。"
                "选择题必须只有一个最优答案，解释要短。"
                "connection 字段必须每行只写一种接续方式。"
                "每行固定使用“品詞[活用形・接続形] + 目标文法”的格式。"
                "例如：名詞[普通形] + だけあって、動詞[普通形] + だけあって、"
                "い形容詞[普通形] + だけあって、な形容詞[語幹/である] + だけあって。"
            ),
            user_prompt=(
                f"目标文法：{grammar_text}\n"
                f"补充说明：{description_text}\n"
                f"追问历史：\n{follow_ups}\n"
                "请综合以上信息，生成一张适合移动端学习页面展示的文法卡片。"
            ),
            schema=CreationDraftSchema,
            operation="creation_draft",
        )
        return GeneratedGrammarDraft(
            title=parsed.title,
            meaning=parsed.meaning,
            level=parsed.level,
            tags=parsed.tags,
            connection=parsed.connection,
            context=parsed.context,
            examples=[
                GrammarExample(japanese=item.japanese, chinese=item.chinese)
                for item in parsed.examples
            ],
            questions=[
                PracticeQuestion(
                    question=item.question,
                    options=item.options,
                    explanation=item.explanation,
                )
                for item in parsed.questions
            ],
        )

    def review_sentence(
        self,
        grammar: GrammarEntry,
        sentence: str,
    ) -> str:
        parsed = self._parse_response(
            system_prompt=(
                "你是一名严谨的日语写作教练。"
                "请只给出简洁、可执行的中文点评。"
                "优先指出句子是否自然、是否符合目标文法、若不自然如何修改。"
            ),
            user_prompt=(
                f"目标文法：{grammar.title}\n"
                f"文法含义：{grammar.meaning}\n"
                f"接续：{grammar.connection}\n"
                f"语境：{grammar.context}\n"
                f"用户句子：{sentence}\n"
                "请生成简洁点评。"
            ),
            schema=SentenceReviewSchema,
            operation="sentence_review",
        )
        return parsed.feedback

    def _parse_response(self, system_prompt: str, user_prompt: str, schema, operation: str):
        try:
            response = self._client.responses.parse(
                model=self._model_name,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                text_format=schema,
            )
        except Exception as exc:
            logger.exception("OpenAI request failed during %s", operation)
            raise AiProviderError("AI provider request failed.") from exc

        parsed = getattr(response, "output_parsed", None)
        if parsed is None:
            logger.error("OpenAI returned no structured output during %s", operation)
            raise AiProviderError("AI provider returned no structured output.")

        try:
            return schema.model_validate(parsed)
        except ValidationError as exc:
            logger.exception("OpenAI structured validation failed during %s", operation)
            raise AiProviderError("AI provider returned invalid structured output.") from exc
