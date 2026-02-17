import { useState } from "react";
import MessageList from "./MessageList";
import InputBox from "./InputBox";
import { useChat } from "../hooks/useChat";

export default function ChatInterface() {
  const { messages, isLoading, sendMessage, clearMessages } = useChat();

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold">Chat</h2>
        {messages.length > 0 && (
          <button
            onClick={clearMessages}
            className="text-sm text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            Clear
          </button>
        )}
      </div>

      <div className="flex-1 overflow-y-auto mb-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-400">
            <div className="text-center">
              <p className="text-4xl mb-3">🧠</p>
              <p className="text-lg font-medium">Ask CodeSage anything</p>
              <p className="text-sm mt-1">
                Upload documents first, then ask questions about your codebase.
              </p>
            </div>
          </div>
        ) : (
          <MessageList messages={messages} isLoading={isLoading} />
        )}
      </div>

      <InputBox onSend={sendMessage} disabled={isLoading} />
    </div>
  );
}
