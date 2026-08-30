import React, { useState } from 'react';
import { Send, Loader2, FileText } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  onRequestLeadershipUpdate: () => void;
  isLoading: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  onRequestLeadershipUpdate,
  isLoading,
}) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  return (
    <div className="border-t border-slate-800 bg-slate-900/90 p-4 backdrop-blur-md">
      <form onSubmit={handleSubmit} className="flex items-center space-x-2">
        <button
          type="button"
          onClick={onRequestLeadershipUpdate}
          disabled={isLoading}
          className="flex items-center space-x-1.5 rounded-lg border border-sky-600/50 bg-sky-950/40 px-3 py-2.5 text-xs font-semibold text-sky-300 transition-all hover:bg-sky-900/50 disabled:opacity-50 shrink-0"
          title="Generate Executive Leadership Update"
        >
          <FileText className="h-4 w-4 text-sky-400" />
          <span className="hidden sm:inline">Leadership Update</span>
        </button>

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask founder-level business question (e.g. How is energy sector pipeline performing?)"
          disabled={isLoading}
          className="flex-1 rounded-lg border border-slate-700 bg-slate-800/90 px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500 disabled:opacity-50"
        />

        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="flex items-center space-x-1 rounded-lg bg-sky-600 px-4 py-2.5 text-sm font-semibold text-white transition-all hover:bg-sky-500 disabled:opacity-50 shrink-0"
        >
          {isLoading ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <>
              <span>Ask</span>
              <Send className="h-3.5 w-3.5" />
            </>
          )}
        </button>
      </form>
    </div>
  );
};
