import { useState, useCallback, useRef } from "react";
import { queryKnowledgeBaseStream } from "../services/api";

export function useChat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const sessionIdRef = useRef(null);
  const abortRef = useRef(null);

  const sendMessage = useCallback((question) => {
    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setIsLoading(true);

    // Placeholder for the streaming assistant message
    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: "", sources: [], streaming: true },
    ]);

    const cancel = queryKnowledgeBaseStream(question, {
      sessionId: sessionIdRef.current,
      onSources: (sources) => {
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            sources,
          };
          return updated;
        });
      },
      onToken: (token) => {
        setMessages((prev) => {
          const updated = [...prev];
          const last = updated[updated.length - 1];
          updated[updated.length - 1] = {
            ...last,
            content: last.content + token,
          };
          return updated;
        });
      },
      onDone: (sid) => {
        if (sid) sessionIdRef.current = sid;
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            streaming: false,
          };
          return updated;
        });
        setIsLoading(false);
      },
      onError: (err) => {
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            role: "assistant",
            content: `Error: ${err.message}`,
            streaming: false,
          };
          return updated;
        });
        setIsLoading(false);
      },
    });

    abortRef.current = cancel;
  }, [messages.length]);

  const clearMessages = useCallback(() => {
    if (abortRef.current) abortRef.current();
    sessionIdRef.current = null;
    setMessages([]);
    setIsLoading(false);
  }, []);

  return { messages, isLoading, sendMessage, clearMessages };
}

