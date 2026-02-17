# Phase 2 — Ingestion Pipeline

## Goals
- File upload endpoint (multi-file)
- Text parsing for code and document files
- Recursive chunking with configurable size/overlap
- Sentence Transformer embedding (all-MiniLM-L6-v2)
- Vector storage in pgvector

## Deliverables
- `POST /api/ingest` endpoint
- `services/parsers.py` — file reading & text extraction
- `utils/chunking.py` — text splitting logic
- `services/embedding.py` — batch embedding
- `services/database.py` — chunk storage with pgvector
- Document management endpoints (list, delete)

## Status: ✅ Complete
