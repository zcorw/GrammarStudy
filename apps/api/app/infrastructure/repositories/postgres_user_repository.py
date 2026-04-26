from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, sessionmaker

from app.application.ports.user_repository import UserRepository
from app.domain.entities.auth import AuthenticatedUser
from app.domain.entities.user import UserGrammarListItem, UserRecent
from app.infrastructure.persistence.models.grammar import GrammarEntryModel
from app.infrastructure.persistence.models.user import (
    InvitationCodeModel,
    PracticeAttemptModel,
    SentenceFeedbackModel,
    UserAccountModel,
    UserFavoriteModel,
    UserRecentViewModel,
)
from app.infrastructure.security.password_hasher import PasswordHasher


class PostgresUserRepository(UserRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def register_with_email(
        self,
        email: str,
        password: str,
        invite_code: str | None,
    ) -> AuthenticatedUser:
        now = datetime.now(UTC)
        with self._session_factory() as session:
            user = session.execute(
                select(UserAccountModel).where(UserAccountModel.email == email)
            ).scalar_one_or_none()

            if user is not None and (user.is_admin or user.password_hash):
                raise ValueError("Email already registered")

            if user is None:
                user = UserAccountModel(
                    email=email,
                    password_hash=PasswordHasher.hash_password(password),
                    approved=False,
                    approval_status="pending_review",
                )
                session.add(user)
                session.flush()
            else:
                user.password_hash = PasswordHasher.hash_password(password)

            self._apply_access_policy(
                session=session,
                user=user,
                invite_code=invite_code,
                now=now,
            )
            session.commit()
            session.refresh(user)
            return self._to_user(user)

    def login_with_email(
        self,
        email: str,
        password: str,
    ) -> AuthenticatedUser:
        now = datetime.now(UTC)
        with self._session_factory() as session:
            user = session.execute(
                select(UserAccountModel).where(UserAccountModel.email == email)
            ).scalar_one_or_none()
            if user is None or not PasswordHasher.verify_password(password, user.password_hash):
                raise ValueError("Invalid credentials")

            if user.is_admin:
                user.approved = True
                user.approval_status = "approved"
                user.approved_at = user.approved_at or now
            else:
                user.approved = user.approval_status == "approved"

            user.last_login_at = now
            session.commit()
            session.refresh(user)
            return self._to_user(user)

    def get_by_id(self, user_id: int) -> AuthenticatedUser | None:
        with self._session_factory() as session:
            user = session.get(UserAccountModel, user_id)
            if user is None:
                return None
            return self._to_user(user)

    def list_my_grammar(self, user_id: int) -> list[UserGrammarListItem]:
        with self._session_factory() as session:
            favorites = session.execute(
                select(UserFavoriteModel, GrammarEntryModel)
                .join(GrammarEntryModel, GrammarEntryModel.id == UserFavoriteModel.grammar_id)
                .where(UserFavoriteModel.user_id == user_id)
            ).all()
            created = session.execute(
                select(GrammarEntryModel).where(GrammarEntryModel.created_by_user_id == user_id)
            ).scalars().all()
            recents = session.execute(
                select(UserRecentViewModel).where(UserRecentViewModel.user_id == user_id)
            ).scalars().all()
            attempts = session.execute(
                select(PracticeAttemptModel).where(PracticeAttemptModel.user_id == user_id)
            ).scalars().all()

        activity_map: dict[str, datetime] = {}
        source_map: dict[str, str] = {}
        title_map: dict[str, str] = {}

        for favorite, grammar in favorites:
            activity_map[grammar.id] = favorite.created_at
            source_map[grammar.id] = "favorite"
            title_map[grammar.id] = grammar.title_raw

        for grammar in created:
            current = activity_map.get(grammar.id)
            if current is None or grammar.created_at > current:
                activity_map[grammar.id] = grammar.created_at
            source_map[grammar.id] = "created"
            title_map[grammar.id] = grammar.title_raw

        for recent in recents:
            current = activity_map.get(recent.grammar_id)
            if current is None or recent.viewed_at > current:
                activity_map[recent.grammar_id] = recent.viewed_at

        for attempt in attempts:
            current = activity_map.get(attempt.grammar_id)
            if current is None or attempt.created_at > current:
                activity_map[attempt.grammar_id] = attempt.created_at

        ordered_ids = sorted(
            title_map.keys(),
            key=lambda grammar_id: activity_map.get(grammar_id, datetime.min.replace(tzinfo=UTC)),
            reverse=True,
        )
        return [
            UserGrammarListItem(
                id=grammar_id,
                title=title_map[grammar_id],
                source=source_map.get(grammar_id, "favorite"),
                last_activity_at=activity_map[grammar_id].isoformat(),
            )
            for grammar_id in ordered_ids
        ]

    def get_recent(self, user_id: int) -> UserRecent:
        with self._session_factory() as session:
            recent_views = session.execute(
                select(UserRecentViewModel.grammar_id)
                .where(UserRecentViewModel.user_id == user_id)
                .order_by(desc(UserRecentViewModel.viewed_at))
                .limit(10)
            ).scalars().all()
            practice_records = session.execute(
                select(PracticeAttemptModel.grammar_id)
                .where(PracticeAttemptModel.user_id == user_id)
                .order_by(desc(PracticeAttemptModel.created_at))
                .limit(10)
            ).scalars().all()
            favorites = session.execute(
                select(UserFavoriteModel.grammar_id)
                .where(UserFavoriteModel.user_id == user_id)
                .order_by(desc(UserFavoriteModel.created_at))
                .limit(10)
            ).scalars().all()

        return UserRecent(
            recent_views=recent_views,
            practice_records=practice_records,
            favorites=favorites,
        )

    def toggle_favorite(self, user_id: int, grammar_id: str) -> bool:
        with self._session_factory() as session:
            favorite = session.execute(
                select(UserFavoriteModel).where(
                    UserFavoriteModel.user_id == user_id,
                    UserFavoriteModel.grammar_id == grammar_id,
                )
            ).scalar_one_or_none()

            if favorite is None:
                session.add(UserFavoriteModel(user_id=user_id, grammar_id=grammar_id))
                session.commit()
                return True

            session.delete(favorite)
            session.commit()
            return False

    def record_recent_view(self, user_id: int, grammar_id: str) -> None:
        with self._session_factory() as session:
            recent = session.execute(
                select(UserRecentViewModel).where(
                    UserRecentViewModel.user_id == user_id,
                    UserRecentViewModel.grammar_id == grammar_id,
                )
            ).scalar_one_or_none()
            if recent is None:
                recent = UserRecentViewModel(user_id=user_id, grammar_id=grammar_id)
                session.add(recent)
            recent.viewed_at = datetime.now(UTC)
            session.commit()

    def record_practice_attempt(
        self,
        user_id: int,
        grammar_id: str,
        selected_option: str,
        result: str,
    ) -> None:
        with self._session_factory() as session:
            session.add(
                PracticeAttemptModel(
                    user_id=user_id,
                    grammar_id=grammar_id,
                    selected_option=selected_option,
                    result=result,
                )
            )
            session.commit()

    def save_sentence_feedback(
        self,
        user_id: int,
        grammar_id: str,
        sentence: str,
        feedback: str,
    ) -> None:
        with self._session_factory() as session:
            session.add(
                SentenceFeedbackModel(
                    user_id=user_id,
                    grammar_id=grammar_id,
                    sentence=sentence,
                    feedback=feedback,
                )
            )
            session.commit()

    @staticmethod
    def _apply_access_policy(
        session: Session,
        user: UserAccountModel,
        invite_code: str | None,
        now: datetime,
    ) -> None:
        if user.is_admin:
            user.approved = True
            user.approval_status = "approved"
            user.approved_at = user.approved_at or now
            return

        if user.approval_status == "approved":
            user.approved = True
            return

        if invite_code:
            invitation = session.execute(
                select(InvitationCodeModel).where(
                    InvitationCodeModel.code == invite_code,
                    InvitationCodeModel.is_active.is_(True),
                )
            ).scalar_one_or_none()
            if invitation is not None:
                user.approved = True
                user.approval_status = "approved"
                user.approved_at = now
                user.invite_code = invite_code
                if invitation.used_by_user_id is None:
                    invitation.used_by_user_id = user.id
                invitation.used_at = now
                return

        user.approved = False
        user.approval_status = "pending_review"

    @staticmethod
    def _to_user(user: UserAccountModel) -> AuthenticatedUser:
        access_state = "approved" if user.approval_status == "approved" else "pending_review"
        return AuthenticatedUser(
            id=user.id,
            email=user.email,
            access_state=access_state,
            is_admin=user.is_admin,
        )
