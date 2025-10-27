import { useMemo, useState } from "react";

import { useArticles, useDailyReport, useKeywordTrends } from "./api/hooks";
import type { Article } from "./api/types";
import { ArticleCard } from "./components/ArticleCard";
import { KeywordTrendChart } from "./components/KeywordTrendChart";
import "./App.css";

type CategoryOption = {
  label: string;
  value: string;
  count: number;
};

function App() {
  const { data: articles = [], isLoading: articlesLoading } = useArticles();
  const { data: report, isLoading: reportLoading } = useDailyReport();
  const { data: keywordStats = [], isLoading: keywordLoading } = useKeywordTrends();
  const [categoryFilter, setCategoryFilter] = useState<string>("all");

  const categoryOptions = useMemo<CategoryOption[]>(() => {
    const counts: Record<string, number> = {};
    articles.forEach((article) => {
      const key = article.category ?? "기타";
      counts[key] = (counts[key] ?? 0) + 1;
    });
    return [
      { label: "전체", value: "all", count: articles.length },
      ...Object.entries(counts).map(([label, count]) => ({
        label,
        value: label,
        count,
      })),
    ];
  }, [articles]);

  const filteredArticles = useMemo<Article[]>(() => {
    if (categoryFilter === "all") {
      return articles;
    }
    return articles.filter((article) => (article.category ?? "기타") === categoryFilter);
  }, [articles, categoryFilter]);

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <h1>AI 기술 동향 대시보드</h1>
          <p className="app-subtitle">컨설턴트와 PO를 위한 일일 요약 리포트</p>
        </div>
        <div className="app-stats">
          <span className="app-stats__label">오늘 분석 기사</span>
          <span className="app-stats__value">{report?.total_articles ?? "—"}</span>
        </div>
      </header>

      <main className="app-content">
        <section className="panel panel--highlight">
          <h2>카테고리 요약</h2>
          {reportLoading && <p className="muted">로딩 중...</p>}
          {!reportLoading && report && (
            <ul className="category-summary">
              {report.categories.map((item) => (
                <li key={item.category ?? "기타"}>
                  <strong>{item.category ?? "기타"}</strong>
                  <span>{item.count}건</span>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="panel">
          <div className="panel__header">
            <h2>키워드 트렌드 (최근 7일)</h2>
          </div>
          {keywordLoading && <p className="muted">키워드를 불러오는 중...</p>}
          {!keywordLoading && keywordStats.length > 0 && <KeywordTrendChart data={keywordStats} />}
          {!keywordLoading && keywordStats.length === 0 && <p className="muted">데이터가 없습니다.</p>}
        </section>

        <section className="panel panel--wide">
          <div className="panel__header">
            <h2>요약 기사</h2>
            <div className="filters">
              {categoryOptions.map((option) => (
                <button
                  key={option.value}
                  className={`filter-button ${categoryFilter === option.value ? "is-active" : ""}`}
                  onClick={() => setCategoryFilter(option.value)}
                >
                  {option.label} ({option.count})
                </button>
              ))}
            </div>
          </div>

          {articlesLoading && <p className="muted">기사 데이터를 불러오는 중...</p>}
          {!articlesLoading && filteredArticles.length === 0 && (
            <p className="muted">선택한 카테고리에 기사가 없습니다.</p>
          )}
          <div className="article-list">
            {filteredArticles.map((article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
