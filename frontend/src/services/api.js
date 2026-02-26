const API_BASE = "/api";

export async function queryKnowledgeBase(question, topK = 5, sessionId = null) {
  const res = await fetch(`${API_BASE}/query/ask-simple`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      top_k: topK,
      session_id: sessionId,
      mode: "document_qa",
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Query failed");
  }
  return res.json();
}

/**
 * Stream a query answer via Server-Sent Events.
 * Calls onToken(token) for each streamed token,
 * onSources(sources) once sources are received,
 * and returns the session_id when done.
 */
export function queryKnowledgeBaseStream(
  question,
  { onToken, onSources, onDone, onError, topK = 5, sessionId = null, mode = "document_qa" }
) {
  const controller = new AbortController();

  (async () => {
    try {
      const res = await fetch(`${API_BASE}/query/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question,
          top_k: topK,
          session_id: sessionId,
          mode,
        }),
        signal: controller.signal,
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Streaming query failed");
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split("\n");
        buffer = lines.pop(); // keep incomplete line

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          try {
            const event = JSON.parse(line.slice(6));
            if (event.type === "sources" && onSources) onSources(event.sources);
            else if (event.type === "token" && onToken) onToken(event.token);
            else if (event.type === "done" && onDone) onDone(event.session_id);
          } catch {
            // ignore malformed events
          }
        }
      }
    } catch (err) {
      if (err.name !== "AbortError" && onError) onError(err);
    }
  })();

  return () => controller.abort();
}

export async function uploadFile(file) {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API_BASE}/ingest/upload`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Upload failed");
  }
  return res.json();
}

export async function getIngestStatus(documentId) {
  const res = await fetch(`${API_BASE}/ingest/status/${documentId}`);
  if (!res.ok) throw new Error("Failed to fetch ingest status");
  return res.json();
}

export async function fetchDocuments() {
  const res = await fetch(`${API_BASE}/documents/list`);
  if (!res.ok) throw new Error("Failed to fetch documents");
  return res.json();
}

export async function deleteDocument(id) {
  const res = await fetch(`${API_BASE}/documents/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete document");
  return res.json();
}

export async function fetchDocumentChunks(documentId) {
  const res = await fetch(`${API_BASE}/documents/${documentId}/chunks`);
  if (!res.ok) throw new Error("Failed to fetch chunks");
  return res.json();
}

