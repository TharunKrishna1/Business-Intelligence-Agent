import { useState } from 'react';
import { ChatWindow } from './components/chat/ChatWindow';
import { ChatInput } from './components/chat/ChatInput';
import { SuggestedQueries } from './components/chat/SuggestedQueries';
import { sendChatMessage, fetchLeadershipUpdate } from './api/client';
import { ChatMessageItem } from './types';
import { Activity, ShieldCheck, Database, RefreshCw } from 'lucide-react';

export default function App() {
  const [messages, setMessages] = useState<ChatMessageItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);

  const handleSendMessage = async (text: string) => {
    const userMsg: ChatMessageItem = {
      id: Date.now().toString(),
      sender: 'user',
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const responsePayload = await sendChatMessage(text, sessionId);
      if (responsePayload.session_id) {
        setSessionId(responsePayload.session_id);
      }

      const assistantMsg: ChatMessageItem = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: responsePayload.insights,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        responsePayload,
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessageItem = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: `Error: ${err.message || 'Failed to process request.'}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLeadershipUpdate = async () => {
    const userMsg: ChatMessageItem = {
      id: Date.now().toString(),
      sender: 'user',
      text: 'Prepare a comprehensive executive leadership update.',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const responsePayload = await fetchLeadershipUpdate(sessionId);
      if (responsePayload.session_id) {
        setSessionId(responsePayload.session_id);
      }

      const assistantMsg: ChatMessageItem = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: responsePayload.insights,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        responsePayload,
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessageItem = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: `Error generating leadership update: ${err.message}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-950 text-slate-100 font-sans">
      {/* Header Bar */}
      <header className="flex items-center justify-between border-b border-slate-800 bg-slate-900/80 px-6 py-3.5 backdrop-blur-md">
        <div className="flex items-center space-x-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-sky-600 shadow-md shadow-sky-900/30">
            <Activity className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white tracking-tight">
              Skylark Drones <span className="text-sky-400 font-normal">| monday.com BI Agent</span>
            </h1>
            <p className="text-[11px] text-slate-400">Conversational Founder Intelligence Platform</p>
          </div>
        </div>

        <div className="flex items-center space-x-4 text-xs">
          <div className="hidden md:flex items-center space-x-1.5 text-emerald-400 bg-emerald-950/40 border border-emerald-800/60 px-2.5 py-1 rounded-full">
            <ShieldCheck className="h-3.5 w-3.5" />
            <span>Read-Only monday.com API</span>
          </div>
          <div className="hidden md:flex items-center space-x-1.5 text-sky-400 bg-sky-950/40 border border-sky-800/60 px-2.5 py-1 rounded-full">
            <Database className="h-3.5 w-3.5" />
            <span>Deterministic Python BI</span>
          </div>
          <button
            onClick={() => setMessages([])}
            className="flex items-center space-x-1 text-slate-400 hover:text-white transition-colors"
            title="Clear conversation"
          >
            <RefreshCw className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">Reset</span>
          </button>
        </div>
      </header>

      {/* Main Chat Container */}
      <main className="flex-1 flex flex-col max-w-6xl w-full mx-auto overflow-hidden px-4">
        {messages.length === 0 && (
          <div className="mt-4">
            <SuggestedQueries onSelectQuery={handleSendMessage} disabled={isLoading} />
          </div>
        )}

        <ChatWindow messages={messages} isLoading={isLoading} />

        <ChatInput
          onSendMessage={handleSendMessage}
          onRequestLeadershipUpdate={handleLeadershipUpdate}
          isLoading={isLoading}
        />
      </main>
    </div>
  );
}
