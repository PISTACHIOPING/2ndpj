from datetime import datetime, timedelta

from celery import Celery
from sqlalchemy import func
from sqlmodel import Session, select

from ..config import get_settings
from ..database import engine
from ..models import Article

settings = get_settings()


def _result_backend_url(broker_url: str) -> str:
    if broker_url.endswith("/0"):
        return broker_url[:-2] + "/1"
    return f"{broker_url.rstrip('/')}/results"


celery_app = Celery(
    "ai_tech_insights",
    broker=settings.redis_url,
    backend=_result_backend_url(settings.redis_url),
)


@celery_app.task(name="reports.generate_weekly_digest")
def generate_weekly_digest() -> dict[str, int]:
    """Return category counts for articles published in the last 7 days."""
    since = datetime.utcnow() - timedelta(days=7)

    with Session(engine) as session:
        statement = (
            select(Article.category, func.count(Article.id))
            .where(Article.published_at >= since)
            .group_by(Article.category)
        )
        rows = session.exec(statement).all()

    summary = {row[0] or "uncategorized": row[1] for row in rows}
    return summary

