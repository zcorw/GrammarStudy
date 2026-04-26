"""add creation sessions

Revision ID: 20260423_0002
Revises: 20260423_0001
Create Date: 2026-04-23 00:30:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260423_0002"
down_revision = "20260423_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "creation_sessions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("grammar_text", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("next_step", sa.String(length=64), nullable=False),
        sa.Column("draft_card_json", sa.Text(), nullable=False),
        sa.Column("follow_up_history_json", sa.Text(), nullable=False),
        sa.Column("published_grammar_id", sa.String(length=64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_creation_sessions_grammar_text",
        "creation_sessions",
        ["grammar_text"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_creation_sessions_grammar_text", table_name="creation_sessions")
    op.drop_table("creation_sessions")
