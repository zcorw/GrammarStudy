"""admin account password columns

Revision ID: 20260423_0004
Revises: 20260423_0003
Create Date: 2026-04-23 13:30:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260423_0004"
down_revision: str | None = "20260423_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("user_accounts", sa.Column("password_hash", sa.Text(), nullable=True))
    op.add_column(
        "user_accounts",
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_column("user_accounts", "is_admin")
    op.drop_column("user_accounts", "password_hash")
