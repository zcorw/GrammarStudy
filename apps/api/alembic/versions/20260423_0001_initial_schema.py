"""initial schema

Revision ID: 20260423_0001
Revises:
Create Date: 2026-04-23 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260423_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "grammar_entries",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("title_raw", sa.String(length=128), nullable=False),
        sa.Column("title_normalized", sa.String(length=128), nullable=False),
        sa.Column("title_reading_kana", sa.String(length=128), nullable=False),
        sa.Column("meaning", sa.Text(), nullable=False),
        sa.Column("connection", sa.Text(), nullable=False),
        sa.Column("context", sa.Text(), nullable=False),
        sa.Column("examples_json", sa.Text(), nullable=False),
        sa.Column("tags_json", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_grammar_entries_title_normalized",
        "grammar_entries",
        ["title_normalized"],
        unique=False,
    )
    op.create_index(
        "ix_grammar_entries_title_reading_kana",
        "grammar_entries",
        ["title_reading_kana"],
        unique=False,
    )

    op.create_table(
        "practice_questions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("grammar_id", sa.String(length=64), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("options_json", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["grammar_id"], ["grammar_entries.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_practice_questions_grammar_id",
        "practice_questions",
        ["grammar_id"],
        unique=False,
    )

    op.create_table(
        "user_accounts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("invite_code", sa.String(length=64), nullable=True),
        sa.Column("approved", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("approval_note", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(
        "ix_user_accounts_email",
        "user_accounts",
        ["email"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_user_accounts_email", table_name="user_accounts")
    op.drop_table("user_accounts")
    op.drop_index("ix_practice_questions_grammar_id", table_name="practice_questions")
    op.drop_table("practice_questions")
    op.drop_index("ix_grammar_entries_title_reading_kana", table_name="grammar_entries")
    op.drop_index("ix_grammar_entries_title_normalized", table_name="grammar_entries")
    op.drop_table("grammar_entries")
