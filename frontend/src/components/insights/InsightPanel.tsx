import React from 'react';

interface InsightPanelProps {
  insights: string;
}

export const InsightPanel: React.FC<InsightPanelProps> = ({ insights }) => {
  // Simple markdown renderer for clean presentation
  const renderFormattedText = (text: string) => {
    const lines = text.split('\n');
    return lines.map((line, idx) => {
      if (line.startsWith('# ')) {
        return <h1 key={idx} className="text-xl font-bold text-sky-400 mt-4 mb-2">{line.replace('# ', '')}</h1>;
      }
      if (line.startsWith('## ')) {
        return <h2 key={idx} className="text-lg font-bold text-sky-300 mt-3 mb-1">{line.replace('## ', '')}</h2>;
      }
      if (line.startsWith('### ')) {
        return <h3 key={idx} className="text-base font-semibold text-slate-200 mt-2 mb-1">{line.replace('### ', '')}</h3>;
      }
      if (line.startsWith('- ')) {
        const content = line.replace('- ', '');
        return (
          <li key={idx} className="ml-4 list-disc text-slate-300 py-0.5">
            {renderInlineFormatting(content)}
          </li>
        );
      }
      if (line.trim() === '') {
        return <div key={idx} className="h-2" />;
      }
      return <p key={idx} className="text-slate-300 my-1 leading-relaxed">{renderInlineFormatting(line)}</p>;
    });
  };

  const renderInlineFormatting = (str: string) => {
    const parts = str.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} className="font-semibold text-white">{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  return (
    <div className="rounded-xl border border-slate-700 bg-slate-800/60 p-5 shadow-lg backdrop-blur-sm">
      <div className="prose prose-invert max-w-none text-sm">
        {renderFormattedText(insights)}
      </div>
    </div>
  );
};
