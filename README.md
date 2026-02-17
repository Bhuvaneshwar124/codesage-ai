# CodeSage AI

CodeSage AI is a full-stack Retrieval-Augmented Generation (RAG) platform that enables intelligent analysis, search, and contextual understanding of enterprise codebases and documents.

## Architecture

```
codesage-ai/
├── backend/
│   ├── main.py          # FastAPI application & API endpoints
│   ├── ingest.py         # Document ingestion pipeline
│   ├── retriever.py      # Vector similarity search
│   ├── generator.py      # LLM response generation
│   └── config.py         # Centralized configuration
├── vector_store/          # Persisted FAISS index
├── data/                  # Source files to ingest
├── requirements.txt
└── README.md
```

## How It Works

1. **Ingest** — Place source code or documents in `data/`. The ingestion pipeline reads, chunks, embeds (Sentence Transformers), and stores them in a FAISS vector store.
2. **Retrieve** — A user query is embedded and matched against the vector store to find the most relevant chunks.
3. **Generate** — Retrieved context is passed to an LLM (via Ollama) which produces a grounded answer.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Make sure Ollama is running with a model pulled
ollama pull mistral
```

## Usage

```bash
# 1. Place files in the data/ directory

# 2. Start the API server
cd backend
uvicorn main:app --reload

# 3. Trigger ingestion
curl -X POST http://localhost:8000/ingest

# 4. Ask a question
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How does the authentication module work?"}'
```

## API Endpoints

| Method | Endpoint  | Description                          |
|--------|-----------|--------------------------------------|
| GET    | /health   | Health check                         |
| POST   | /ingest   | Run the document ingestion pipeline  |
| POST   | /query    | Ask a question (RAG)                 |

## Configuration

All settings are in `backend/config.py` and can be overridden via environment variables:

| Variable          | Default               | Description                    |
|-------------------|-----------------------|--------------------------------|
| EMBEDDING_MODEL   | all-MiniLM-L6-v2      | Sentence Transformer model     |
| LLM_MODEL         | mistral               | Ollama model name              |
| OLLAMA_BASE_URL   | http://localhost:11434 | Ollama server URL              |
| CHUNK_SIZE        | 500                   | Characters per chunk           |
| CHUNK_OVERLAP     | 50                    | Overlap between chunks         |
| TOP_K             | 5                     | Number of results to retrieve  |
