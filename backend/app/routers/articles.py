from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from ..database import get_session
from ..models import Article
from ..schemas import ArticleIngestRequest, ArticlePayload, ArticleResponse

router = APIRouter(prefix="/articles", tags=["articles"])


@router.post("/", response_model=List[ArticleResponse], status_code=status.HTTP_201_CREATED)
def ingest_articles(
    payload: ArticleIngestRequest,
    session: Session = Depends(get_session),
) -> List[ArticleResponse]:
    if not payload.articles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No articles provided.")

    stored: list[Article] = []
    for article_data in payload.articles:
        stored.append(_upsert_article(session, article_data))

    session.commit()
    for article in stored:
        session.refresh(article)
    return stored


def _upsert_article(session: Session, article_data: ArticlePayload) -> Article:
    statement = select(Article).where(Article.url == str(article_data.url))
    existing = session.exec(statement).first()

    if existing:
        existing.title = article_data.title
        existing.category = article_data.category
        existing.source = article_data.source
        existing.summary = article_data.summary
        existing.impact = article_data.impact
        existing.keywords = article_data.keywords
        existing.published_at = article_data.published_at
        existing.created_at = existing.created_at or datetime.utcnow()
        return existing

    article = Article(
        title=article_data.title,
        url=str(article_data.url),
        source=article_data.source,
        category=article_data.category,
        summary=article_data.summary,
        impact=article_data.impact,
        keywords=article_data.keywords,
        published_at=article_data.published_at,
    )
    session.add(article)
    try:
        session.flush()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Article already exists: {article_data.url}",
        ) from exc
    return article


@router.get("/", response_model=List[ArticleResponse])
def list_articles(
    limit: int = 50,
    session: Session = Depends(get_session),
) -> List[ArticleResponse]:
    limit = min(limit, 200)
    statement = select(Article).order_by(Article.published_at.desc()).limit(limit)
    return list(session.exec(statement).all())

