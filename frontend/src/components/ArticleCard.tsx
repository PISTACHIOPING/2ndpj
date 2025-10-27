import dayjs from "dayjs";

import type { Article } from "../api/types";

interface ArticleCardProps {
  article: Article;
}

export function ArticleCard({ article }: ArticleCardProps) {
  const published = dayjs(article.published_at).format("YYYY-MM-DD HH:mm");
  return (
    <article className="article-card">
      <header className="article-card__header">
        <span className="article-card__category">{article.category ?? "기타"}</span>
        <time className="article-card__time">{published}</time>
      </header>
      <h3 className="article-card__title">
        <a href={article.url} target="_blank" rel="noreferrer">
          {article.title}
        </a>
      </h3>
      <p className="article-card__summary">{article.summary}</p>
      {article.impact && <p className="article-card__impact">💡 {article.impact}</p>}
      <footer className="article-card__footer">
        <span className="article-card__source">{article.source ?? "출처 미상"}</span>
        <div className="article-card__keywords">
          {article.keywords.map((keyword) => (
            <span key={keyword} className="article-card__keyword">
              #{keyword}
            </span>
          ))}
        </div>
      </footer>
    </article>
  );
}
