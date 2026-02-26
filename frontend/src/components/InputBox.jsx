import { useState } from "react";

export default function InputBox({ onSend, disabled }) {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setInput("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="flex items-end gap-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl shadow-sm focus-within:ring-2 focus-within:ring-sage-500/40 focus-within:border-sage-400 transition-all duration-200">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about your codebase..."
          disabled={disabled}
          rows={1}
          className="flex-1 bg-transparent px-4 py-3 text-sm resize-none focus:outline-none disabled:opacity-50 placeholder-gray-400 dark:placeholder-gray-500 max-h-32"
          style={{ minHeight: "44px" }}
        />
        <button
          type="submit"
          disabled={disabled || !input.trim()}
          className="m-1.5 p-2 bg-sage-600 hover:bg-sage-700 text-white rounded-xl text-sm font-medium transition-all duration-200 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-sage-600 flex items-center justify-center"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19V5m0 0l-7 7m7-7l7 7" />
          </svg>
        </button>
      </div>
      <p className="text-[10px] text-gray-400 dark:text-gray-600 text-center mt-1.5">
        CodeSage can make mistakes. Verify important information.
      </p>
    </form>
  );
}
