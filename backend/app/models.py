from datetime import datetime
from typing import Optional

from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class Article(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("url", name="uq_article_url"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    url: str
    source: str | None = None
    category: str | None = Field(default=None, index=True)
    summary: str | None = None
    impact: str | None = None
    keywords: list[str] = Field(
        sa_column=Column(JSONB, nullable=False, server_default="[]"),
        default_factory=list,
    )
    published_at: datetime = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True, nullable=False)


class KeywordStat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    keyword: str = Field(index=True)
    count: int = Field(default=0, ge=0)
    period_start: datetime = Field(index=True)
    period_end: datetime = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
