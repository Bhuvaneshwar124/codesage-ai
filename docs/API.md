# API Reference

Base URL: `http://localhost:8000`

---

## Health

### `GET /api/health`

Returns service health status.

**Response:**
```json
{ "status": "ok" }
```

---

## Ingestion

### `POST /api/ingest/upload`

Upload a single file; ingestion runs as a background task.

**Content-Type:** `multipart/form-data`

| Field | Type | Description      |
|-------|------|------------------|
| file  | File | Single file      |

**Response:**
```json
{
  "status": "processing",
  "document_id": 1,
  "filename": "main.py",
  "message": "File accepted; ingestion running in the background."
}
```

### `GET /api/ingest/status/{document_id}`

Check the ingestion status of a previously uploaded document.

**Response:**
```json
{
  "document_id": 1,
  "name": "main.py",
  "status": "complete",
  "chunk_count": 12,
  "ingested_at": "2026-02-17T10:30:00Z"
}
```

Status values: `processing`, `complete`, `failed`.

---

## Query

### `POST /api/query/ask`

Ask a question and receive a **streaming SSE** response.

**Request Body:**
```json
{
  "question": "How does authentication work?",
  "top_k": 5,
  "session_id": "optional-session-uuid",
  "mode": "document_qa"
}
```

| Field      | Type   | Required | Description                                     |
|------------|--------|----------|-------------------------------------------------|
| question   | string | Yes      | The question to ask                             |
| top_k      | int    | No       | Number of retrieved chunks (default: 5)         |
| session_id | string | No       | Session ID for conversation history             |
| mode       | string | No       | `document_qa` (default) or `code_assistant`     |

**Response:** `text/event-stream`

```
data: {"type":"sources","sources":[{"source":"auth.py","text":"..."}]}

data: {"type":"token","token":"The "}

data: {"type":"token","token":"authentication "}

data: {"type":"done","session_id":"abc-123"}
```

### `POST /api/query/ask-simple`

Ask a question and receive a complete (non-streaming) JSON response.

**Request Body:** Same as `/api/query/ask`.

**Response:**
```json
{
  "answer": "The authentication module uses JWT tokens...",
  "sources": [
    { "source": "auth.py", "text": "def verify_token(...)..." }
  ],
  "session_id": "abc-123"
}
```

---

## Documents

### `GET /api/documents/list`

List all ingested documents.

**Response:**
```json
[
  {
    "id": 1,
    "name": "main.py",
    "file_type": "py",
    "status": "complete",
    "ingested_at": "2026-02-17T10:30:00Z",
    "chunk_count": 12
  }
]
```

### `DELETE /api/documents/{document_id}`

Delete a document and its chunks by ID.

**Response:**
```json
{ "status": "success", "message": "Deleted document 1" }
```

### `GET /api/documents/{document_id}/chunks`

Retrieve all chunks for a specific document.

**Response:**
```json
[
  {
    "id": 10,
    "chunk_index": 0,
    "content": "def main():\n    ...",
    "source": "main.py",
    "metadata": {"file_type": "code"}
  }
]
```

