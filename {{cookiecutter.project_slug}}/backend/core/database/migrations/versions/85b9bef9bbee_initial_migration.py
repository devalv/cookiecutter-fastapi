# -*- coding: utf-8 -*-
"""Initial migration.

Revision ID: 85b9bef9bbee
Revises:
Create Date: 2021-05-10 13:23:59.761097

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "85b9bef9bbee"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Apply changes on database."""
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("ext_id", sa.Unicode(length=255), nullable=False),
        sa.Column("disabled", sa.Boolean(), nullable=False),
        sa.Column("superuser", sa.Boolean(), nullable=False),
        sa.Column(
            "created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("username", sa.Unicode(length=255), nullable=False),
        sa.Column("given_name", sa.Unicode(length=255), nullable=True),
        sa.Column("family_name", sa.Unicode(length=255), nullable=True),
        sa.Column("full_name", sa.Unicode(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ext_id"),
    )
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=False)
    op.create_table(
        "token_info",
        sa.Column("user_id", postgresql.UUID(), nullable=False),
        sa.Column("refresh_token", sa.Unicode(), nullable=False),
        sa.Column(
            "created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_index(
        op.f("ix_token_info_refresh_token"),
        "token_info",
        ["refresh_token"],
        unique=False,
    )


def downgrade():
    """Revert changes on database."""
    op.drop_index(op.f("ix_token_info_refresh_token"), table_name="token_info")
    op.drop_table("token_info")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_table("user")
