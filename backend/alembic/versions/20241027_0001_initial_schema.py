"""initial schema

Revision ID: 20241027_0001
Revises:
Create Date: 2025-10-27 01:40:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20241027_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "article",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("impact", sa.Text(), nullable=True),
        sa.Column("keywords", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("published_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_article")),
        sa.UniqueConstraint("url", name="uq_article_url"),
    )
    op.create_index(op.f("ix_article_category"), "article", ["category"], unique=False)
    op.create_index(op.f("ix_article_created_at"), "article", ["created_at"], unique=False)
    op.create_index(op.f("ix_article_published_at"), "article", ["published_at"], unique=False)

    op.create_table(
        "keywordstat",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("keyword", sa.String(), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.Column("period_start", sa.DateTime(), nullable=False),
        sa.Column("period_end", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_keywordstat")),
    )
    op.create_index(op.f("ix_keywordstat_keyword"), "keywordstat", ["keyword"], unique=False)
    op.create_index(op.f("ix_keywordstat_period_end"), "keywordstat", ["period_end"], unique=False)
    op.create_index(op.f("ix_keywordstat_period_start"), "keywordstat", ["period_start"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_keywordstat_period_start"), table_name="keywordstat")
    op.drop_index(op.f("ix_keywordstat_period_end"), table_name="keywordstat")
    op.drop_index(op.f("ix_keywordstat_keyword"), table_name="keywordstat")
    op.drop_table("keywordstat")
    op.drop_index(op.f("ix_article_published_at"), table_name="article")
    op.drop_index(op.f("ix_article_created_at"), table_name="article")
    op.drop_index(op.f("ix_article_category"), table_name="article")
    op.drop_table("article")
