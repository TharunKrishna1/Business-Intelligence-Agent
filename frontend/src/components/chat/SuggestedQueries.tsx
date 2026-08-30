import React from 'react';
import { Sparkles } from 'lucide-react';

interface SuggestedQueriesProps {
  onSelectQuery: (query: string) => void;
  disabled?: boolean;
}

const SUGGESTIONS = [
  'How is our overall pipeline looking?',
  'How is the energy sector performing this quarter?',
  'Which projects are delayed?',
  'Which sector has the strongest pipeline?',
  'Are there operational risks associated with high-value opportunities?',
  'Prepare a leadership update',
];

export const SuggestedQueries: React.FC<SuggestedQueriesProps> = ({
  onSelectQuery,
  disabled,
}) => {
  return (
    <div className="mb-4">
      <div className="mb-2 flex items-center space-x-1 text-xs text-sky-400 font-medium">
        <Sparkles className="h-3.5 w-3.5" />
        <span>Suggested Founder Questions:</span>
      </div>
      <div className="flex flex-wrap gap-2">
        {SUGGESTIONS.map((query, idx) => (
          <button
            key={idx}
            onClick={() => onSelectQuery(query)}
            disabled={disabled}
            className="rounded-full border border-slate-700 bg-slate-800/80 px-3 py-1 text-xs text-slate-300 transition-all hover:border-sky-500 hover:bg-sky-950/40 hover:text-sky-300 disabled:opacity-50"
          >
            {query}
          </button>
        ))}
      </div>
    </div>
  );
};
