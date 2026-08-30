import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: LucideIcon;
  badge?: string;
  variant?: 'sky' | 'amber' | 'emerald' | 'slate';
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  badge,
  variant = 'sky',
}) => {
  const variantStyles = {
    sky: 'border-sky-800/50 bg-sky-950/20 text-sky-400',
    amber: 'border-amber-800/50 bg-amber-950/20 text-amber-400',
    emerald: 'border-emerald-800/50 bg-emerald-950/20 text-emerald-400',
    slate: 'border-slate-700 bg-slate-800/50 text-slate-300',
  };

  return (
    <div className={`rounded-xl border p-4 shadow-md backdrop-blur-sm ${variantStyles[variant]}`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">{title}</span>
        {Icon && <Icon className="h-5 w-5 opacity-80" />}
      </div>
      <div className="mt-2 flex items-baseline justify-between">
        <span className="text-2xl font-bold tracking-tight text-white">{value}</span>
        {badge && (
          <span className="rounded-full bg-slate-800 px-2 py-0.5 text-xs font-medium text-slate-300">
            {badge}
          </span>
        )}
      </div>
      {subtitle && <p className="mt-1 text-xs text-slate-400">{subtitle}</p>}
    </div>
  );
};
