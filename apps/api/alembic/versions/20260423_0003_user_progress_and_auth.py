"""user progress and auth tables

Revision ID: 20260423_0003
Revises: 20260423_0002
Create Date: 2026-04-23 12:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260423_0003"
down_revision: str | None = "20260423_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "user_accounts",
        sa.Column("approval_status", sa.String(length=32), nullable=False, server_default="pending_review"),
    )
    op.add_column(
        "user_accounts",
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "user_accounts",
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "invitation_codes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("used_by_user_id", sa.Integer(), nullable=True),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["used_by_user_id"], ["user_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_invitation_codes_code"), "invitation_codes", ["code"], unique=True)

    op.add_column(
        "grammar_entries",
        sa.Column("created_by_user_id", sa.Integer(), nullable=True),
    )
    op.create_index(
        op.f("ix_grammar_entries_created_by_user_id"),
        "grammar_entries",
        ["created_by_user_id"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_grammar_entries_created_by_user_id",
        "grammar_entries",
        "user_accounts",
        ["created_by_user_id"],
        ["id"],
    )

    op.add_column(
        "creation_sessions",
        sa.Column("user_id", sa.Integer(), nullable=True),
    )
    op.create_index(op.f("ix_creation_sessions_user_id"), "creation_sessions", ["user_id"], unique=False)
    op.create_foreign_key(
        "fk_creation_sessions_user_id",
        "creation_sessions",
        "user_accounts",
        ["user_id"],
        ["id"],
    )

    op.create_table(
        "user_favorites",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("grammar_id", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["grammar_id"], ["grammar_entries.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "grammar_id", name="uq_user_favorite"),
    )
    op.create_index(op.f("ix_user_favorites_grammar_id"), "user_favorites", ["grammar_id"], unique=False)
    op.create_index(op.f("ix_user_favorites_user_id"), "user_favorites", ["user_id"], unique=False)

    op.create_table(
        "user_recent_views",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("grammar_id", sa.String(length=64), nullable=False),
        sa.Column("viewed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["grammar_id"], ["grammar_entries.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "grammar_id", name="uq_user_recent_view"),
    )
    op.create_index(op.f("ix_user_recent_views_grammar_id"), "user_recent_views", ["grammar_id"], unique=False)
    op.create_index(op.f("ix_user_recent_views_user_id"), "user_recent_views", ["user_id"], unique=False)

    op.create_table(
        "practice_attempts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("grammar_id", sa.String(length=64), nullable=False),
        sa.Column("selected_option", sa.Text(), nullable=False),
        sa.Column("result", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["grammar_id"], ["grammar_entries.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_practice_attempts_grammar_id"), "practice_attempts", ["grammar_id"], unique=False)
    op.create_index(op.f("ix_practice_attempts_user_id"), "practice_attempts", ["user_id"], unique=False)

    op.create_table(
        "sentence_feedbacks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("grammar_id", sa.String(length=64), nullable=False),
        sa.Column("sentence", sa.Text(), nullable=False),
        sa.Column("feedback", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["grammar_id"], ["grammar_entries.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sentence_feedbacks_grammar_id"), "sentence_feedbacks", ["grammar_id"], unique=False)
    op.create_index(op.f("ix_sentence_feedbacks_user_id"), "sentence_feedbacks", ["user_id"], unique=False)

    op.execute(
        sa.text(
            "INSERT INTO invitation_codes (code, is_active, note) "
            "SELECT 'DEMO-ACCESS', TRUE, 'Seeded demo invite code' "
            "WHERE NOT EXISTS (SELECT 1 FROM invitation_codes WHERE code = 'DEMO-ACCESS')"
        )
    )
    op.execute(
        sa.text(
            "INSERT INTO user_accounts (email, invite_code, approved, approval_status, approval_note) "
            "SELECT 'seed-review@example.com', 'DEMO-ACCESS', TRUE, 'approved', 'System seed user' "
            "WHERE NOT EXISTS (SELECT 1 FROM user_accounts WHERE email = 'seed-review@example.com')"
        )
    )

    op.execute(sa.text("UPDATE user_accounts SET approval_status = CASE WHEN approved THEN 'approved' ELSE 'pending_review' END"))
    op.execute(
        sa.text(
            "UPDATE creation_sessions "
            "SET user_id = (SELECT id FROM user_accounts WHERE email = 'seed-review@example.com' LIMIT 1) "
            "WHERE user_id IS NULL"
        )
    )
    op.alter_column("creation_sessions", "user_id", nullable=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_sentence_feedbacks_user_id"), table_name="sentence_feedbacks")
    op.drop_index(op.f("ix_sentence_feedbacks_grammar_id"), table_name="sentence_feedbacks")
    op.drop_table("sentence_feedbacks")

    op.drop_index(op.f("ix_practice_attempts_user_id"), table_name="practice_attempts")
    op.drop_index(op.f("ix_practice_attempts_grammar_id"), table_name="practice_attempts")
    op.drop_table("practice_attempts")

    op.drop_index(op.f("ix_user_recent_views_user_id"), table_name="user_recent_views")
    op.drop_index(op.f("ix_user_recent_views_grammar_id"), table_name="user_recent_views")
    op.drop_table("user_recent_views")

    op.drop_index(op.f("ix_user_favorites_user_id"), table_name="user_favorites")
    op.drop_index(op.f("ix_user_favorites_grammar_id"), table_name="user_favorites")
    op.drop_table("user_favorites")

    op.drop_constraint("fk_creation_sessions_user_id", "creation_sessions", type_="foreignkey")
    op.drop_index(op.f("ix_creation_sessions_user_id"), table_name="creation_sessions")
    op.drop_column("creation_sessions", "user_id")

    op.drop_constraint("fk_grammar_entries_created_by_user_id", "grammar_entries", type_="foreignkey")
    op.drop_index(op.f("ix_grammar_entries_created_by_user_id"), table_name="grammar_entries")
    op.drop_column("grammar_entries", "created_by_user_id")

    op.drop_index(op.f("ix_invitation_codes_code"), table_name="invitation_codes")
    op.drop_table("invitation_codes")

    op.drop_column("user_accounts", "last_login_at")
    op.drop_column("user_accounts", "approved_at")
    op.drop_column("user_accounts", "approval_status")
