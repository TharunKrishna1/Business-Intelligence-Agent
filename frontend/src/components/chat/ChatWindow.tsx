import React, { useRef, useEffect } from 'react';
import { ChatMessageItem } from '../../types';
import { ChatMessage } from './ChatMessage';
import { Bot } from 'lucide-react';

interface ChatWindowProps {
  messages: ChatMessageItem[];
  isLoading: boolean;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({ messages, isLoading }) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-full text-center text-slate-400 my-16">
          <div className="rounded-full bg-slate-800 p-4 mb-4 border border-slate-700">
            <Bot className="h-10 w-10 text-sky-400" />
          </div>
          <h3 className="text-lg font-bold text-white mb-1">Skylark Drones Business Intelligence Agent</h3>
          <p className="max-w-md text-xs text-slate-400">
            Ask founder-level questions across Deals and Work Orders boards. All metrics are computed deterministically in Python with Gemini executive synthesis.
          </p>
        </div>
      ) : (
        messages.map((msg) => <ChatMessage key={msg.id} message={msg} />)
      )}

      {isLoading && (
        <div className="flex items-center space-x-3 p-4 rounded-xl border border-slate-800 bg-slate-900/40 text-slate-400 text-xs">
          <div className="flex space-x-1">
            <div className="w-2 h-2 rounded-full bg-sky-400 animate-bounce" style={{ animationDelay: '0ms' }}></div>
            <div className="w-2 h-2 rounded-full bg-sky-400 animate-bounce" style={{ animationDelay: '150ms' }}></div>
            <div className="w-2 h-2 rounded-full bg-sky-400 animate-bounce" style={{ animationDelay: '300ms' }}></div>
          </div>
          <span>Retrieving monday.com board data, normalizing records, and calculating BI metrics...</span>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
};
