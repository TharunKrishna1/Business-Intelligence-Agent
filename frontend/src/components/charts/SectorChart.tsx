import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { ChartDataItem } from '../../types';

interface SectorChartProps {
  data: ChartDataItem[];
  title?: string;
}

const SECTOR_COLORS = ['#38bdf8', '#34d399', '#fbbf24', '#f87171', '#c084fc'];

export const SectorChart: React.FC<SectorChartProps> = ({
  data,
  title = 'Sector Market Share',
}) => {
  if (!data || data.length === 0) return null;

  return (
    <div className="rounded-xl border border-slate-700 bg-slate-800/40 p-4 shadow-md">
      <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-400">{title}</h4>
      <div className="h-56 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={50}
              outerRadius={75}
              paddingAngle={4}
              dataKey="value"
            >
              {data.map((_, index) => (
                <Cell key={`sector-cell-${index}`} fill={SECTOR_COLORS[index % SECTOR_COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
              formatter={(val: any) => [`$${Number(val).toLocaleString()}`, 'Pipeline Value']}
            />
            <Legend
              verticalAlign="bottom"
              height={36}
              iconType="circle"
              formatter={(val) => <span className="text-xs text-slate-300">{val}</span>}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
