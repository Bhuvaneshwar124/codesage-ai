import { useDocuments } from "../hooks/useDocuments";
import DocumentCard from "./DocumentCard";
import LoadingSpinner from "./LoadingSpinner";

export default function DocumentList() {
  const { documents, loading, error, refresh, removeDocument } = useDocuments();

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold">Ingested Documents</h2>
        <button
          onClick={refresh}
          className="text-sm text-sage-600 hover:text-sage-700 dark:text-sage-500"
        >
          Refresh
        </button>
      </div>

      {loading && (
        <div className="flex items-center gap-2 text-gray-400 py-8 justify-center">
          <LoadingSpinner />
          <span>Loading documents...</span>
        </div>
      )}

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-300 rounded-xl px-4 py-3 text-sm">
          {error}
        </div>
      )}

      {!loading && documents.length === 0 && (
        <div className="text-center text-gray-400 py-12">
          <p className="text-3xl mb-2">📭</p>
          <p>No documents ingested yet.</p>
        </div>
      )}

      <div className="grid gap-3">
        {documents.map((doc) => (
          <DocumentCard
            key={doc.name}
            document={doc}
            onDelete={() => removeDocument(doc.name)}
          />
        ))}
      </div>
    </div>
  );
}
