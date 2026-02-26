import { formatDate } from "../utils/helpers";

const STATUS_STYLES = {
  complete: {
    dot: "bg-green-500",
    text: "text-green-600 dark:text-green-400",
    label: "Complete",
  },
  failed: {
    dot: "bg-red-500",
    text: "text-red-600 dark:text-red-400",
    label: "Failed",
  },
  processing: {
    dot: "bg-yellow-500 animate-pulse",
    text: "text-yellow-600 dark:text-yellow-400",
    label: "Processing",
  },
};

export default function DocumentCard({ document, onDelete }) {
  const status = STATUS_STYLES[document.status] || STATUS_STYLES.processing;

  return (
    <div className="group flex items-center gap-4 bg-white dark:bg-gray-800/80 border border-gray-100 dark:border-gray-700/50 rounded-xl px-4 py-3.5 hover:shadow-sm hover:border-gray-200 dark:hover:border-gray-600/50 transition-all duration-200">
      {/* File icon */}
      <div className="w-10 h-10 rounded-xl bg-sage-50 dark:bg-sage-900/20 flex items-center justify-center flex-shrink-0">
        <svg className="w-5 h-5 text-sage-600 dark:text-sage-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-800 dark:text-gray-200 truncate">
          {document.name}
        </p>
        <div className="flex items-center gap-3 mt-1">
          <span className="flex items-center gap-1">
            <span className={`w-1.5 h-1.5 rounded-full ${status.dot}`}></span>
            <span className={`text-[11px] font-medium ${status.text}`}>{status.label}</span>
          </span>
          <span className="text-[11px] text-gray-400 dark:text-gray-500">
            {document.chunk_count} chunks
          </span>
          {document.file_type && (
            <span className="text-[11px] text-gray-400 dark:text-gray-500 font-mono uppercase">
              .{document.file_type}
            </span>
          )}
          <span className="text-[11px] text-gray-400 dark:text-gray-500">
            {formatDate(document.ingested_at)}
          </span>
        </div>
      </div>

      {/* Delete button */}
      <button
        onClick={onDelete}
        className="opacity-0 group-hover:opacity-100 p-2 rounded-lg text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-all duration-200"
        title="Delete document"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </div>
  );
}

