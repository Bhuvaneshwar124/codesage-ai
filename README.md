# CodeSage AI

CodeSage AI is a full-stack Retrieval-Augmented Generation (RAG) platform that enables intelligent analysis, search, and contextual understanding of enterprise codebases and documents.

## Tech Stack

| Layer      | Technology                                      |
|------------|--------------------------------------------------|
| Frontend   | React 18, Vite, Tailwind CSS                    |
| Backend    | FastAPI, SQLAlchemy (async), Sentence Transformers |
| Database   | PostgreSQL 17 + pgvector                         |
| LLM        | Ollama (Mistral, Llama, etc.)                    |
| Infra      | Docker Compose                                   |

## Architecture

```
codesage-ai/
├── docker-compose.yml
├── .env
├── .gitignore
├── start.sh
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py               # FastAPI app entry point
│   ├── config.py             # Pydantic Settings
│   ├── routers/              # API route handlers
│   │   ├── health.py
│   │   ├── ingest.py
│   │   ├── query.py
│   │   └── documents.py
│   ├── services/             # Business logic
│   │   ├── database.py       # PostgreSQL + pgvector
│   │   ├── embedding.py      # Sentence Transformers
│   │   ├── retrieval.py      # Vector similarity search
│   │   ├── generation.py     # Ollama LLM
│   │   └── parsers.py        # File text extraction
│   ├── models/
│   │   └── schemas.py        # Pydantic request/response models
│   ├── utils/
│   │   └── chunking.py       # Text splitting
│   └── tests/
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── src/
│       ├── App.jsx
│       ├── components/       # ChatInterface, FileUpload, DocumentList, etc.
│       ├── hooks/            # useChat, useDocuments, useTheme
│       ├── services/         # API client
│       └── utils/            # Helper functions
│
├── database/
│   ├── init-scripts/         # SQL schema & indexes
│   └── migrations/
│
├── docs/                     # Phase docs, API reference, deployment guide
│
└── uploads/                  # Uploaded files
```

## How It Works

1. **Upload** — Drag & drop code or document files through the web UI.
2. **Ingest** — Files are parsed, split into chunks, embedded with Sentence Transformers, and stored in PostgreSQL + pgvector.
3. **Query** — Your question is embedded and matched against stored vectors via cosine similarity.
4. **Generate** — The most relevant chunks are sent as context to an LLM (Ollama) which produces a grounded, source-attributed answer.

## Quick Start

```bash
# 1. Clone and configure
git clone https://github.com/your-org/codesage-ai.git
cd codesage-ai
cp .env .env.local   # edit as needed

# 2. Start all services
docker compose up --build -d

# 3. Pull an Ollama model
docker compose exec ollama ollama pull mistral

# 4. Open the UI
# → http://localhost:5173

# 5. Or use the API directly
curl http://localhost:8000/health
```

## API Endpoints

| Method | Endpoint                              | Description                          |
|--------|---------------------------------------|--------------------------------------|
| GET    | `/api/health`                         | Health check                         |
| POST   | `/api/ingest/upload`                  | Upload & start background ingestion  |
| GET    | `/api/ingest/status/{document_id}`    | Check ingestion status               |
| POST   | `/api/query/ask`                      | Ask a question (streaming SSE)       |
| POST   | `/api/query/ask-simple`               | Ask a question (JSON response)       |
| GET    | `/api/documents/list`                 | List ingested documents              |
| DELETE | `/api/documents/{document_id}`        | Delete a document                    |
| GET    | `/api/documents/{document_id}/chunks` | Get document chunks                  |

Full API reference: [docs/API.md](docs/API.md)

## Configuration

All settings live in `.env` and are loaded via `backend/config.py` (Pydantic Settings):

| Variable          | Default               | Description                    |
|-------------------|-----------------------|--------------------------------|
| POSTGRES_USER     | codesage              | Database user                  |
| POSTGRES_PASSWORD | changeme              | Database password              |
| EMBEDDING_MODEL   | all-MiniLM-L6-v2      | Sentence Transformer model     |
| LLM_MODEL         | mistral               | Ollama model name              |
| CHUNK_SIZE        | 500                   | Characters per chunk           |
| CHUNK_OVERLAP     | 50                    | Overlap between chunks         |
| TOP_K             | 5                     | Retrieval result count         |

## Documentation

- [Phase 1 — Foundation](docs/PHASE_1.md)
- [Phase 2 — Ingestion Pipeline](docs/PHASE_2.md)
- [Phase 3 — RAG Query Pipeline](docs/PHASE_3.md)
- [Phase 4 — Frontend & Polish](docs/PHASE_4.md)
- [API Reference](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
