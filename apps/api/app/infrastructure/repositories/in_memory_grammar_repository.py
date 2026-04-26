from app.application.ports.grammar_repository import GrammarRepository
from app.domain.entities.grammar import (
    GrammarEntry,
    GrammarExample,
    PracticeQuestion,
    SearchGrammarResult,
)


class InMemoryGrammarRepository(GrammarRepository):
    def __init__(self) -> None:
        self._entries = [
            GrammarEntry(
                id="g1",
                title="〜に違いない",
                meaning="表示说话人有较强把握的推测，语气偏肯定。",
                level="N2",
                tags=["推测", "书面", "判断"],
                connection=(
                    "名詞[普通形] + に違いない\n"
                    "動詞[普通形] + に違いない\n"
                    "い形容詞[普通形] + に違いない\n"
                    "な形容詞[語幹/である] + に違いない"
                ),
                context="常用于根据明显依据作出较强判断。",
                examples=[
                    GrammarExample(
                        japanese="あの人の表情を見ると、何か事情を知っているに違いない。",
                        chinese="看那个人的表情，他一定知道些什么。",
                    ),
                    GrammarExample(
                        japanese="ここまで準備しているのだから、彼女は本気で留学するに違いない。",
                        chinese="既然都准备到这个程度了，她肯定是认真打算留学。",
                    ),
                ],
                questions=[
                    PracticeQuestion(
                        question="あの表情を見ると、彼は真実を知っている____。",
                        options=["はずだ", "に違いない", "わけだ"],
                        explanation="此处需要表达更强的主观肯定判断。",
                    )
                ],
            ),
            GrammarEntry(
                id="g2",
                title="〜ものの",
                meaning="表示承认前项成立，但后项与预期不一致。",
                level="N3",
                tags=["转折", "书面"],
                connection=(
                    "名詞[普通形] + ものの\n"
                    "動詞[普通形] + ものの\n"
                    "い形容詞[普通形] + ものの\n"
                    "な形容詞[語幹/である] + ものの"
                ),
                context="常见于书面表达，用于带保留的转折。",
                examples=[
                    GrammarExample(
                        japanese="試験には合格したものの、希望の部署には入れなかった。",
                        chinese="虽然考试合格了，但没能进入理想的部门。",
                    ),
                    GrammarExample(
                        japanese="買ってはみたものの、まだ使っていない。",
                        chinese="虽然买了，但还没有用。",
                    ),
                ],
                questions=[
                    PracticeQuestion(
                        question="転職した____、前より忙しくなった。",
                        options=["ものの", "に違いない", "にしては"],
                        explanation="前后转折，选择「ものの」。",
                    )
                ],
            ),
        ]

    def list_recommended(self) -> list[GrammarEntry]:
        return self._entries

    def get_by_id(self, grammar_id: str) -> GrammarEntry | None:
        return next((entry for entry in self._entries if entry.id == grammar_id), None)

    def search(self, query: str) -> SearchGrammarResult:
        matches = [
            entry
            for entry in self._entries
            if query in entry.title
            or query in entry.meaning
            or any(query in tag for tag in entry.tags)
        ]
        return SearchGrammarResult(
            best_match=matches[0] if matches else None,
            similar_cards=matches[1:],
            search_confidence=0.9 if matches else 0.2,
            should_offer_ai_generation=not matches,
        )
