import { useState, useRef } from "react";
import { uploadFile, getIngestStatus } from "../services/api";
import LoadingSpinner from "./LoadingSpinner";

const FILE_ICONS = {
  py: "🐍", js: "📜", ts: "📘", jsx: "⚛️", tsx: "⚛️",
  java: "☕", cpp: "⚙️", c: "⚙️", go: "🔵", rs: "🦀",
  md: "📝", json: "📋", yaml: "📋", yml: "📋",
  html: "🌐", css: "🎨", sql: "🗄️",
};

function getFileIcon(name) {
  const ext = name.split(".").pop()?.toLowerCase();
  return FILE_ICONS[ext] || "📄";
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1048576).toFixed(1)} MB`;
}

export default function FileUpload() {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef(null);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
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

  const pollStatus = async (documentId) => {
    const maxAttempts = 30;
    for (let i = 0; i < maxAttempts; i++) {
      await new Promise((r) => setTimeout(r, 2000));
      try {
        const status = await getIngestStatus(documentId);
        if (status.status === "complete" || status.status === "failed") return status;
      } catch { /* ignore */ }
    }
    return { status: "timeout" };
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
          const finalStatus = await pollStatus(data.document_id);
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
    <div className="animate-fade-in">
      <div className="mb-6">
        <h2 className="text-lg font-bold text-gray-800 dark:text-gray-100">Upload Documents</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Upload code files or documents to build your knowledge base.
        </p>
      </div>

      {/* Drop zone */}
      <div
        onDrop={handleDrop}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onClick={() => inputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-300 ${
          dragOver
            ? "border-sage-500 bg-sage-50 dark:bg-sage-900/20 scale-[1.01]"
            : "border-gray-200 dark:border-gray-700 hover:border-sage-400 hover:bg-gray-50 dark:hover:bg-gray-800/50"
        }`}
      >
        <div className="w-14 h-14 mx-auto mb-4 rounded-2xl bg-sage-50 dark:bg-sage-900/30 flex items-center justify-center">
          <svg className="w-7 h-7 text-sage-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>
        <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Drag & drop files here
        </p>
        <p className="text-xs text-gray-400 dark:text-gray-500">
          or click to browse · .py .js .ts .md .json and more
        </p>
        <input ref={inputRef} type="file" multiple onChange={handleSelect} className="hidden" />
      </div>

      {/* File list */}
      {files.length > 0 && (
        <div className="mt-5 space-y-2 animate-slide-up">
          <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">
            {files.length} file{files.length > 1 ? "s" : ""} selected
          </p>
          {files.map((f, i) => (
            <div
              key={i}
              className="flex items-center gap-3 bg-white dark:bg-gray-800/80 border border-gray-100 dark:border-gray-700/50 rounded-xl px-4 py-2.5 group"
            >
              <span className="text-lg">{getFileIcon(f.name)}</span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate text-gray-700 dark:text-gray-200">{f.name}</p>
                <p className="text-[10px] text-gray-400">{formatSize(f.size)}</p>
              </div>
              <button
                onClick={(e) => { e.stopPropagation(); removeFile(i); }}
                className="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-500 transition-all p-1 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          ))}

          <button
            onClick={handleUpload}
            disabled={uploading}
            className="mt-3 w-full bg-gradient-to-r from-sage-600 to-sage-700 hover:from-sage-700 hover:to-sage-800 text-white py-3 rounded-xl text-sm font-semibold transition-all duration-200 disabled:opacity-50 flex items-center justify-center gap-2 shadow-sm shadow-sage-500/20"
          >
            {uploading ? (
              <>
                <LoadingSpinner /> Processing...
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                Upload & Ingest {files.length} file{files.length > 1 ? "s" : ""}
              </>
            )}
          </button>
        </div>
      )}

      {/* Results */}
      {results.length > 0 && (
        <div className="mt-5 space-y-2 animate-slide-up">
          {results.map((r, i) => (
            <div
              key={i}
              className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm ${
                r.status === "complete"
                  ? "bg-green-50 dark:bg-green-900/10 border border-green-200/60 dark:border-green-800/30 text-green-700 dark:text-green-400"
                  : "bg-red-50 dark:bg-red-900/10 border border-red-200/60 dark:border-red-800/30 text-red-700 dark:text-red-400"
              }`}
            >
              {r.status === "complete" ? (
                <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              ) : (
                <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )}
              <span>
                <strong>{r.filename || r.name}</strong>
                {r.status === "complete"
                  ? ` — ${r.chunk_count ?? 0} chunks ingested`
                  : ` — ${r.status}`}
              </span>
            </div>
          ))}
        </div>
      )}

      {error && (
        <div className="mt-5 flex items-center gap-2 bg-red-50 dark:bg-red-900/10 border border-red-200/60 dark:border-red-800/30 text-red-600 dark:text-red-400 rounded-xl px-4 py-3 text-sm animate-slide-up">
          <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {error}
        </div>
      )}
    </div>
  );
}

