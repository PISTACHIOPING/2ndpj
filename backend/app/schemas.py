from datetime import date, datetime
from typing import List

from pydantic import BaseModel, HttpUrl


class ArticlePayload(BaseModel):
    title: str
    url: HttpUrl
    source: str | None = None
    category: str | None = None
    summary: str
    impact: str | None = None
    keywords: List[str]
    published_at: datetime


class ArticleIngestRequest(BaseModel):
    articles: List[ArticlePayload]


class ArticleResponse(BaseModel):
    id: int
    title: str
    url: HttpUrl
    source: str | None
    category: str | None
    summary: str | None
    impact: str | None
    keywords: List[str]
    published_at: datetime

    class Config:
        from_attributes = True


class KeywordStatResponse(BaseModel):
    keyword: str
    count: int


class DailyReportItem(BaseModel):
    category: str | None
    count: int


class DailyReportResponse(BaseModel):
    date: date
    total_articles: int
    categories: List[DailyReportItem]
