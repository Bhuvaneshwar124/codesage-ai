import { useState } from "react";

export default function SourceCard({ source }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <button
      onClick={() => setExpanded(!expanded)}
      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-sage-50 dark:bg-sage-900/20 border border-sage-200/60 dark:border-sage-800/40 text-xs font-mono text-sage-700 dark:text-sage-400 hover:bg-sage-100 dark:hover:bg-sage-900/40 transition-colors cursor-pointer text-left"
    >
      <svg className="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <span className="truncate max-w-[150px]">{source.source}</span>
      {expanded && source.text && (
        <span className="block font-sans text-[10px] text-gray-500 dark:text-gray-400 mt-0.5 line-clamp-2">
          {source.text}
        </span>
      )}
    </button>
  );
}
