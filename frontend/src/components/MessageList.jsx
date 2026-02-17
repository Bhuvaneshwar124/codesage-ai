import { useEffect, useRef } from "react";
import Message from "./Message";
import LoadingSpinner from "./LoadingSpinner";

export default function MessageList({ messages, isLoading }) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="space-y-4">
      {messages.map((msg, i) => (
        <Message key={i} role={msg.role} content={msg.content} sources={msg.sources} />
      ))}
      {isLoading && (
        <div className="flex items-center gap-2 text-gray-400 py-2">
          <LoadingSpinner />
          <span className="text-sm">Thinking...</span>
        </div>
      )}
      <div ref={endRef} />
    </div>
  );
}
