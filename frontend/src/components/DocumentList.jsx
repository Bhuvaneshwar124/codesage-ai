import { useDocuments } from "../hooks/useDocuments";
import DocumentCard from "./DocumentCard";
import LoadingSpinner from "./LoadingSpinner";

export default function DocumentList() {
  const { documents, loading, error, refresh, removeDocument } = useDocuments();

  return (
    <div className="animate-fade-in">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-lg font-bold text-gray-800 dark:text-gray-100">Knowledge Base</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
            {documents.length} document{documents.length !== 1 ? "s" : ""} ingested
          </p>
        </div>
        <button
          onClick={refresh}
          className="flex items-center gap-1.5 text-xs font-medium text-sage-600 hover:text-sage-700 dark:text-sage-500 dark:hover:text-sage-400 px-3 py-1.5 rounded-lg hover:bg-sage-50 dark:hover:bg-sage-900/20 transition-colors"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh
        </button>
      </div>

      {loading && (
        <div className="flex flex-col items-center justify-center py-16 text-gray-400">
          <LoadingSpinner size="md" />
          <span className="text-sm mt-3">Loading documents...</span>
        </div>
      )}

      {error && (
        <div className="flex items-center gap-2 bg-red-50 dark:bg-red-900/10 border border-red-200/60 dark:border-red-800/30 text-red-600 dark:text-red-400 rounded-xl px-4 py-3 text-sm">
          <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {error}
        </div>
      )}

      {!loading && documents.length === 0 && (
        <div className="text-center py-16">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
            <svg className="w-8 h-8 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">No documents yet</p>
          <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">Upload files to start building your knowledge base</p>
        </div>
      )}

      <div className="grid gap-2.5">
        {documents.map((doc) => (
          <DocumentCard
            key={doc.id}
            document={doc}
            onDelete={() => removeDocument(doc.id)}
          />
        ))}
      </div>
    </div>
  );
}
