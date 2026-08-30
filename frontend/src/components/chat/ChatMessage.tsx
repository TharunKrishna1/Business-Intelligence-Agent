import React from 'react';
import { ChatMessageItem } from '../../types';
import { MetricCard } from '../insights/MetricCard';
import { InsightPanel } from '../insights/InsightPanel';
import { DataQualityAlert } from '../insights/DataQualityAlert';
import { PipelineChart } from '../charts/PipelineChart';
import { SectorChart } from '../charts/SectorChart';
import { DollarSign, Briefcase, Activity, AlertCircle, Cpu } from 'lucide-react';

interface ChatMessageProps {
  message: ChatMessageItem;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  const payload = message.responsePayload;

  if (isUser) {
    return (
      <div className="flex justify-end my-3">
        <div className="max-w-2xl rounded-2xl rounded-tr-none bg-sky-600 px-4 py-3 text-sm text-white shadow-md">
          <p>{message.text}</p>
          <span className="mt-1 block text-right text-[10px] text-sky-200">{message.timestamp}</span>
        </div>
      </div>
    );
  }

  const pipeline = payload?.metrics?.pipeline;
  const operations = payload?.metrics?.operations;

  return (
    <div className="my-4 flex flex-col space-y-4 rounded-2xl border border-slate-800 bg-slate-900/60 p-5 shadow-xl">
      {/* Header Badge */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Cpu className="h-5 w-5 text-sky-400" />
          <span className="font-semibold text-slate-200 text-sm">Skylark BI Agent</span>
          {payload?.query_plan?.intent && (
            <span className="rounded-md bg-slate-800 px-2 py-0.5 text-xs font-mono text-sky-400 border border-slate-700">
              {payload.query_plan.intent}
            </span>
          )}
        </div>
        <span className="text-xs text-slate-500">{message.timestamp}</span>
      </div>

      {/* Data Quality Alert */}
      {payload?.data_quality_report && (
        <DataQualityAlert report={payload.data_quality_report} />
      )}

      {/* Metric Cards Grid */}
      {payload?.metrics && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {pipeline?.total_pipeline_value !== undefined && (
            <MetricCard
              title="Total Pipeline"
              value={`$${(pipeline.total_pipeline_value / 1000).toFixed(0)}k`}
              subtitle={`${pipeline.deal_count} Total Deals`}
              icon={DollarSign}
              variant="sky"
            />
          )}
          {pipeline?.average_deal_value !== undefined && (
            <MetricCard
              title="Avg Deal Size"
              value={`$${(pipeline.average_deal_value / 1000).toFixed(0)}k`}
              subtitle="Per Opportunity"
              icon={Briefcase}
              variant="emerald"
            />
          )}
          {operations?.active_work_orders !== undefined && (
            <MetricCard
              title="Active Work Orders"
              value={operations.active_work_orders}
              subtitle={`${operations.completed_work_orders} Completed`}
              icon={Activity}
              variant="slate"
            />
          )}
          {operations?.delayed_work_orders !== undefined && (
            <MetricCard
              title="Delayed Operations"
              value={operations.delayed_work_orders}
              subtitle={`Delay Rate: ${operations.operational_delay_rate_pct}%`}
              icon={AlertCircle}
              variant={operations.delayed_work_orders > 0 ? 'amber' : 'emerald'}
            />
          )}
        </div>
      )}

      {/* Visualizations Grid */}
      {payload?.chart_data && payload.chart_data.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <PipelineChart data={payload.chart_data} title="Sales Pipeline Breakdown" />
          <SectorChart data={payload.chart_data} title="Industry Sector Share" />
        </div>
      )}

      {/* Executive Narrative Insights Panel */}
      {payload?.insights && (
        <InsightPanel insights={payload.insights} />
      )}
    </div>
  );
};
