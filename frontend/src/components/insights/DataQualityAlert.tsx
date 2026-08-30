import React, { useState } from 'react';
import { AlertTriangle, ChevronDown, ChevronUp, CheckCircle2 } from 'lucide-react';
import { DataQualityReport } from '../../types';

interface DataQualityAlertProps {
  report: DataQualityReport;
}

export const DataQualityAlert: React.FC<DataQualityAlertProps> = ({ report }) => {
  const [expanded, setExpanded] = useState(false);

  const hasIssues = report.records_with_missing_values > 0 || report.invalid_dates > 0;

  return (
    <div
      className={`rounded-lg border p-3.5 text-xs transition-all ${
        hasIssues
          ? 'border-amber-700/60 bg-amber-950/30 text-amber-200'
          : 'border-emerald-700/50 bg-emerald-950/20 text-emerald-300'
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          {hasIssues ? (
            <AlertTriangle className="h-4 w-4 text-amber-400 shrink-0" />
          ) : (
            <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" />
          )}
          <span className="font-semibold">
            Data Quality Diagnostic: {report.valid_records} / {report.total_records} Records Valid
          </span>
        </div>

        <button
          onClick={() => setExpanded(!expanded)}
          className="flex items-center space-x-1 font-medium hover:underline text-slate-300"
        >
          <span>{expanded ? 'Hide Details' : 'View Quality Log'}</span>
          {expanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
        </button>
      </div>

      {expanded && (
        <div className="mt-3 space-y-2 border-t border-slate-700/60 pt-2.5 text-slate-300">
          <div>
            <span className="font-semibold text-white">Important Caveats:</span>
            <ul className="mt-1 list-disc pl-4 space-y-0.5">
              {report.important_caveats.map((c, i) => (
                <li key={i}>{c}</li>
              ))}
            </ul>
          </div>

          {report.normalization_actions.length > 0 && (
            <div>
              <span className="font-semibold text-white">Normalization Actions ({report.normalization_actions.length}):</span>
              <ul className="mt-1 max-h-24 overflow-y-auto font-mono text-[11px] text-slate-400 pl-4 space-y-0.5">
                {report.normalization_actions.map((act, i) => (
                  <li key={i}>{act}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
