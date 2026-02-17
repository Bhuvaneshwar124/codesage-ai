import { formatDate } from "../utils/helpers";

export default function DocumentCard({ document, onDelete }) {
  return (
    <div className="flex items-center justify-between bg-gray-50 dark:bg-gray-800 rounded-xl px-5 py-4">
      <div>
        <p className="font-medium text-sm">{document.name}</p>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
          {document.chunk_count} chunks · Ingested {formatDate(document.ingested_at)}
        </p>
      </div>
      <button
        onClick={onDelete}
        className="text-gray-400 hover:text-red-500 text-sm transition-colors"
        title="Delete document"
      >
        🗑️
      </button>
    </div>
  );
}
