import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { ChartDataItem } from '../../types';

interface PipelineChartProps {
  data: ChartDataItem[];
  title?: string;
}

const COLORS = ['#0284c7', '#38bdf8', '#818cf8', '#a7f3d0', '#f43f5e'];

export const PipelineChart: React.FC<PipelineChartProps> = ({
  data,
  title = 'Pipeline Distribution',
}) => {
  if (!data || data.length === 0) return null;

  const formattedData = data.map((d) => ({
    ...d,
    formattedValue: d.value ? `$${(d.value / 1000).toFixed(0)}k` : '$0',
  }));

  return (
    <div className="rounded-xl border border-slate-700 bg-slate-800/40 p-4 shadow-md">
      <h4 className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-400">{title}</h4>
      <div className="h-56 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={formattedData} margin={{ top: 10, right: 10, left: 10, bottom: 25 }}>
            <XAxis
              dataKey="name"
              stroke="#94a3b8"
              fontSize={11}
              tickLine={false}
              axisLine={{ stroke: '#475569' }}
              interval={0}
              angle={-20}
              textAnchor="end"
            />
            <YAxis
              stroke="#94a3b8"
              fontSize={11}
              tickLine={false}
              axisLine={{ stroke: '#475569' }}
              tickFormatter={(val) => `$${val / 1000}k`}
            />
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
              formatter={(val: any) => [`$${Number(val).toLocaleString()}`, 'Pipeline Value']}
            />
            <Bar dataKey="value" radius={[4, 4, 0, 0]}>
              {formattedData.map((_, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
