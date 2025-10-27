import { useQuery } from "@tanstack/react-query";
import type { UseQueryOptions } from "@tanstack/react-query";

import { apiClient } from "./client";
import type { Article, DailyReport, KeywordStat } from "./types";

const defaultQueryOptions = {
  refetchInterval: 1000 * 60 * 5,
  staleTime: 1000 * 60,
} satisfies Partial<UseQueryOptions>;

export const useArticles = () =>
  useQuery<Article[]>({
    queryKey: ["articles"],
    queryFn: async () => {
      const response = await apiClient.get<Article[]>("/articles", { params: { limit: 100 } });
      return response.data;
    },
    ...defaultQueryOptions,
  });

export const useKeywordTrends = (days = 7) =>
  useQuery<KeywordStat[]>({
    queryKey: ["keyword-trends", days],
    queryFn: async () => {
      const response = await apiClient.get<KeywordStat[]>("/reports/keywords/top", {
        params: { days, limit: 12 },
      });
      return response.data;
    },
    ...defaultQueryOptions,
  });

export const useDailyReport = () =>
  useQuery<DailyReport>({
    queryKey: ["daily-report"],
    queryFn: async () => {
      const response = await apiClient.get<DailyReport>("/reports/daily");
      return response.data;
    },
    ...defaultQueryOptions,
  });
