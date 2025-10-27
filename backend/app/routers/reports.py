from datetime import date, datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlmodel import Session, select

from ..database import get_session
from ..models import Article
from ..schemas import DailyReportItem, DailyReportResponse, KeywordStatResponse

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/daily", response_model=DailyReportResponse)
def daily_report(
    target_date: date | None = Query(default=None, description="기본값: 오늘"),
    session: Session = Depends(get_session),
) -> DailyReportResponse:
    if target_date is None:
        target_date = date.today()

    day_start = datetime.combine(target_date, datetime.min.time())
    day_end = day_start + timedelta(days=1)

    total_stmt = select(func.count(Article.id)).where(
        Article.published_at >= day_start,
        Article.published_at < day_end,
    )
    total = session.exec(total_stmt).one()

    category_stmt = (
        select(Article.category, func.count(Article.id))
        .where(Article.published_at >= day_start, Article.published_at < day_end)
        .group_by(Article.category)
    )
    items = [
        DailyReportItem(category=row[0], count=row[1])
        for row in session.exec(category_stmt).all()
    ]

    return DailyReportResponse(date=target_date, total_articles=total, categories=items)


@router.get("/keywords/top", response_model=List[KeywordStatResponse])
def keyword_trends(
    days: int = Query(default=7, ge=1, le=90),
    limit: int = Query(default=10, ge=1, le=50),
    session: Session = Depends(get_session),
) -> List[KeywordStatResponse]:
    since = datetime.utcnow() - timedelta(days=days)
    # Unnest JSON keywords while remaining within SQLModel by using lateral join
    keyword_expr = func.jsonb_array_elements_text(Article.keywords).label("keyword")
    keyword_stmt = (
        select(keyword_expr, func.count().label("frequency"))
        .select_from(Article)
        .where(Article.published_at >= since)
        .group_by(keyword_expr)
        .order_by(func.count().desc())
        .limit(limit)
    )

    rows = session.exec(keyword_stmt).all()
    return [KeywordStatResponse(keyword=row.keyword, count=row.frequency) for row in rows]
