import { useState } from "react";
import MessageList from "./MessageList";
import InputBox from "./InputBox";
import { useChat } from "../hooks/useChat";

const SUGGESTIONS = [
  "Explain how the ingestion pipeline works",
  "What file types are supported?",
  "Summarize the main architecture",
];

export default function ChatInterface() {
  const { messages, isLoading, sendMessage, clearMessages } = useChat();

  return (
    <div className="flex flex-col h-[calc(100vh-3.75rem)]">
      {/* Chat body */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full px-4">
            <div className="text-center max-w-md animate-fade-in">
              <div className="w-16 h-16 mx-auto mb-5 rounded-2xl bg-gradient-to-br from-sage-400 to-sage-600 flex items-center justify-center shadow-lg shadow-sage-500/20">
                <span className="text-3xl">🧠</span>
              </div>
              <h2 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-2">
                Ask CodeSage anything
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
                Upload documents first, then ask questions about your codebase.
                I'll find relevant context and answer with sources.
              </p>
              <div className="flex flex-col gap-2">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    onClick={() => sendMessage(s)}
                    className="text-left px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800/50 text-sm text-gray-600 dark:text-gray-300 hover:border-sage-400 hover:bg-sage-50 dark:hover:bg-sage-900/20 transition-all duration-200"
                  >
                    <span className="text-sage-600 dark:text-sage-400 mr-2">→</span>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="max-w-3xl mx-auto px-4 py-4">
            <MessageList messages={messages} isLoading={isLoading} />
          </div>
        )}
      </div>

      {/* Input area */}
      <div className="border-t border-gray-200/60 dark:border-gray-800/60 bg-white/60 dark:bg-gray-900/60 glass-header">
        <div className="max-w-3xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between mb-2">
            {messages.length > 0 && (
              <button
                onClick={clearMessages}
                className="text-xs text-gray-400 hover:text-red-500 transition-colors flex items-center gap-1"
              >
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Clear chat
              </button>
            )}
          </div>
          <InputBox onSend={sendMessage} disabled={isLoading} />
        </div>
      </div>
    </div>
  );
}
