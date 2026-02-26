import { useEffect, useRef } from "react";
import Message from "./Message";
import LoadingSpinner from "./LoadingSpinner";

export default function MessageList({ messages, isLoading }) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="space-y-5 py-2">
      {messages.map((msg, i) => (
        <Message
          key={i}
          role={msg.role}
          content={msg.content}
          sources={msg.sources}
          streaming={msg.streaming}
        />
      ))}
      {isLoading && messages[messages.length - 1]?.content === "" && (
        <div className="flex items-center gap-3 pl-10 animate-fade-in">
          <LoadingSpinner />
          <span className="text-xs text-gray-400 dark:text-gray-500">CodeSage is thinking...</span>
        </div>
      )}
      <div ref={endRef} />
    </div>
  );
}
