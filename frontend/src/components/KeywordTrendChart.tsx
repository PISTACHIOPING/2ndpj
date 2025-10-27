import { ResponsiveContainer, BarChart, XAxis, YAxis, Tooltip, Bar, Cell } from "recharts";

import type { KeywordStat } from "../api/types";

interface KeywordTrendChartProps {
  data: KeywordStat[];
}

const COLORS = ["#3182ce", "#2f855a", "#d53f8c", "#38b2ac", "#ed8936", "#9f7aea", "#dd6b20"];

export function KeywordTrendChart({ data }: KeywordTrendChartProps) {
  return (
    <div className="keyword-chart">
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} layout="vertical" margin={{ top: 16, right: 24, bottom: 16, left: 24 }}>
          <XAxis type="number" />
          <YAxis dataKey="keyword" type="category" width={120} />
          <Tooltip />
          <Bar dataKey="count" radius={[4, 4, 4, 4]}>
            {data.map((entry, index) => (
              <Cell key={entry.keyword} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
