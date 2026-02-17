# API Reference

Base URL: `http://localhost:8000`

---

## Health

### `GET /health`

Returns service health status.

**Response:**
```json
{ "status": "ok" }
```

---

## Ingestion

### `POST /api/ingest`

Upload and ingest files into the knowledge base.

**Content-Type:** `multipart/form-data`

| Field  | Type     | Description           |
|--------|----------|-----------------------|
| files  | File[]   | One or more files     |

**Response:**
```json
{
  "status": "success",
  "files_processed": 3,
  "chunks_created": 42
}
```

---

## Query

### `POST /api/query`

Ask a question against the ingested knowledge base.

**Request Body:**
```json
{
  "question": "How does authentication work?",
  "top_k": 5
}
```

| Field    | Type   | Required | Description                    |
|----------|--------|----------|--------------------------------|
| question | string | Yes      | The question to ask            |
| top_k    | int    | No       | Number of results (default: 5) |

**Response:**
```json
{
  "answer": "The authentication module uses JWT tokens...",
  "sources": [
    { "source": "auth.py", "text": "def verify_token(...)..." }
  ]
}
```

---

## Documents

### `GET /api/documents`

List all ingested documents.

**Response:**
```json
[
  {
    "name": "main.py",
    "ingested_at": "2026-02-17T10:30:00Z",
    "chunk_count": 12
  }
]
```

### `DELETE /api/documents/{document_name}`

Delete a document and its chunks.

**Response:**
```json
{ "status": "success", "message": "Deleted 'main.py'" }
```
