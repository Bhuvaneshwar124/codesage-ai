import { useState, useRef } from "react";
import { uploadFile, getIngestStatus } from "../services/api";
import LoadingSpinner from "./LoadingSpinner";

export default function FileUpload() {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  const handleDrop = (e) => {
    e.preventDefault();
    const dropped = Array.from(e.dataTransfer.files);
    setFiles((prev) => [...prev, ...dropped]);
  };

  const handleSelect = (e) => {
    const selected = Array.from(e.target.files);
    setFiles((prev) => [...prev, ...selected]);
  };

  const removeFile = (index) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const pollStatus = async (documentId, filename) => {
    const maxAttempts = 30;
    for (let i = 0; i < maxAttempts; i++) {
      await new Promise((r) => setTimeout(r, 2000));
      try {
        const status = await getIngestStatus(documentId);
        if (status.status === "complete" || status.status === "failed") {
          return status;
        }
      } catch {
        // ignore transient errors
      }
    }
    return { status: "timeout", filename };
  };

  const handleUpload = async () => {
    if (files.length === 0) return;
    setUploading(true);
    setError(null);
    setResults([]);

    try {
      const uploadResults = await Promise.all(
        files.map(async (f) => {
          const data = await uploadFile(f);
          const finalStatus = await pollStatus(data.document_id, f.name);
          return { ...data, ...finalStatus };
        })
      );
      setResults(uploadResults);
      setFiles([]);
    } catch (err) {
      setError(err.message || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h2 className="text-lg font-semibold mb-4">Upload Documents</h2>

      {/* Drop zone */}
      <div
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={() => inputRef.current?.click()}
        className="border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-xl p-12 text-center cursor-pointer hover:border-sage-500 transition-colors"
      >
        <p className="text-3xl mb-2">📁</p>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Drag & drop files here, or click to browse
        </p>
        <input
          ref={inputRef}
          type="file"
          multiple
          onChange={handleSelect}
          className="hidden"
        />
      </div>

      {/* File list */}
      {files.length > 0 && (
        <div className="mt-4 space-y-2">
          {files.map((f, i) => (
            <div
              key={i}
              className="flex items-center justify-between bg-gray-50 dark:bg-gray-800 rounded-lg px-4 py-2"
            >
              <span className="text-sm truncate">{f.name}</span>
              <button
                onClick={() => removeFile(i)}
                className="text-gray-400 hover:text-red-500 text-sm"
              >
                ✕
              </button>
            </div>
          ))}

          <button
            onClick={handleUpload}
            disabled={uploading}
            className="mt-3 w-full bg-sage-600 hover:bg-sage-700 text-white py-3 rounded-xl text-sm font-medium transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {uploading ? (
              <>
                <LoadingSpinner /> Ingesting...
              </>
            ) : (
              `Upload & Ingest ${files.length} file(s)`
            )}
          </button>
        </div>
      )}

      {/* Results */}
      {results.length > 0 && (
        <div className="mt-4 space-y-2">
          {results.map((r, i) => (
            <div
              key={i}
              className={`rounded-xl px-4 py-3 text-sm ${
                r.status === "complete"
                  ? "bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300"
                  : "bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300"
              }`}
            >
              {r.status === "complete"
                ? `✅ ${r.filename || r.name}: ingested ${r.chunk_count ?? ""} chunks`
                : `❌ ${r.filename || r.name}: ${r.status}`}
            </div>
          ))}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="mt-4 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 rounded-xl px-4 py-3 text-sm">
          ❌ {error}
        </div>
      )}
    </div>
  );
}

