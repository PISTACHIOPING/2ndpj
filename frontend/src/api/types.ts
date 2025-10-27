export interface Article {
  id: number;
  title: string;
  url: string;
  source?: string | null;
  category?: string | null;
  summary?: string | null;
  impact?: string | null;
  keywords: string[];
  published_at: string;
}

export interface KeywordStat {
  keyword: string;
  count: number;
}

export interface DailyReportItem {
  category: string | null;
  count: number;
}

export interface DailyReport {
  date: string;
  total_articles: number;
  categories: DailyReportItem[];
}
