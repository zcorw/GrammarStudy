from __future__ import annotations

import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.config.settings import Settings
from app.infrastructure.persistence.models.grammar import (
    GrammarEntryModel,
    PracticeQuestionModel,
)
from app.infrastructure.persistence.models.user import InvitationCodeModel, UserAccountModel
from app.infrastructure.security.password_hasher import PasswordHasher


def seed_demo_grammar(session: Session, settings: Settings) -> None:
    _seed_admin_account(session, settings)
    _seed_demo_invite(session)

    existing = session.execute(select(GrammarEntryModel.id).limit(1)).scalar_one_or_none()
    if existing is not None:
        session.commit()
        return

    entries = [
        {
            "id": "g1",
            "title_raw": "にちがいない",
            "title_normalized": "にちがいない",
            "title_reading_kana": "にちがいない",
            "meaning": "表示说话人有较强把握的推测，语气偏肯定。",
            "connection": (
                "名詞[普通形] + にちがいない\n"
                "動詞[普通形] + にちがいない\n"
                "い形容詞[普通形] + にちがいない\n"
                "な形容詞[語幹/である] + にちがいない"
            ),
            "context": "常用于根据明显依据作出较强判断。",
            "examples": [
                {
                    "japanese": "あの人の表情を見ると、何か事情を知っているにちがいない。",
                    "chinese": "看那个人的表情，他一定知道些什么。",
                },
                {
                    "japanese": "ここまで準備しているのだから、彼女は本気で留学するにちがいない。",
                    "chinese": "既然都准备到这个程度了，她肯定是认真打算留学。",
                },
            ],
            "tags": ["N2", "推测", "书面", "判断"],
            "questions": [
                {
                    "question": "あの表情を見ると、彼は真実を知っている___。",
                    "options": ["はずだ", "にちがいない", "わけだ"],
                    "explanation": "此处需要表达更强的主观肯定判断。",
                }
            ],
        },
        {
            "id": "g2",
            "title_raw": "ものの",
            "title_normalized": "ものの",
            "title_reading_kana": "ものの",
            "meaning": "表示承认前项成立，但后项与预期不一致。",
            "connection": (
                "名詞[普通形] + ものの\n"
                "動詞[普通形] + ものの\n"
                "い形容詞[普通形] + ものの\n"
                "な形容詞[語幹/である] + ものの"
            ),
            "context": "常见于书面表达，用于带保留的转折。",
            "examples": [
                {
                    "japanese": "試験に合格したものの、希望の部署には入れなかった。",
                    "chinese": "虽然考试合格了，但没能进入理想的部门。",
                },
                {
                    "japanese": "買ってはみたものの、まだ使っていない。",
                    "chinese": "虽然买了，但还没有用。",
                },
            ],
            "tags": ["N3", "转折", "书面"],
            "questions": [
                {
                    "question": "就職した____、前より忙しくなった。",
                    "options": ["ものの", "にちがいない", "にしては"],
                    "explanation": "前后转折，选择「ものの」。",
                }
            ],
        },
    ]

    for item in entries:
        entry = GrammarEntryModel(
            id=item["id"],
            title_raw=item["title_raw"],
            title_normalized=item["title_normalized"],
            title_reading_kana=item["title_reading_kana"],
            meaning=item["meaning"],
            connection=item["connection"],
            context=item["context"],
            examples_json=json.dumps(item["examples"], ensure_ascii=False),
            tags_json=json.dumps(item["tags"], ensure_ascii=False),
        )
        for question in item["questions"]:
            entry.practice_questions.append(
                PracticeQuestionModel(
                    question=question["question"],
                    options_json=json.dumps(question["options"], ensure_ascii=False),
                    explanation=question["explanation"],
                )
            )
        session.add(entry)

    session.commit()


def _seed_demo_invite(session: Session) -> None:
    invite = session.execute(
        select(InvitationCodeModel).where(InvitationCodeModel.code == "DEMO-ACCESS")
    ).scalar_one_or_none()
    if invite is None:
        invite = InvitationCodeModel(
            code="DEMO-ACCESS",
            is_active=True,
            note="Seeded demo invite code",
        )
        session.add(invite)
    else:
        invite.is_active = True


def _seed_admin_account(session: Session, settings: Settings) -> None:
    admin = session.execute(
        select(UserAccountModel).where(UserAccountModel.email == settings.admin_email)
    ).scalar_one_or_none()
    password_hash = PasswordHasher.hash_password(settings.admin_password)

    if admin is None:
        session.add(
            UserAccountModel(
                email=settings.admin_email,
                password_hash=password_hash,
                is_admin=True,
                approved=True,
                approval_status="approved",
                approval_note="Seeded administrator account",
            )
        )
        return

    admin.password_hash = password_hash
    admin.is_admin = True
    admin.approved = True
    admin.approval_status = "approved"
    admin.approval_note = "Seeded administrator account"
