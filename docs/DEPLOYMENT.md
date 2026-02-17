# Deployment Guide

## Prerequisites

- Docker & Docker Compose
- 4 GB+ RAM (for embedding model + Ollama)

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/your-org/codesage-ai.git
cd codesage-ai

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings

# 3. Start all services
docker compose up --build -d

# 4. Pull an LLM model
docker compose exec ollama ollama pull mistral

# 5. Open the frontend
# http://localhost:5173
```

## Services

| Service   | Port  | Description                    |
|-----------|-------|--------------------------------|
| frontend  | 5173  | React UI                       |
| backend   | 8000  | FastAPI server                 |
| db        | 5432  | PostgreSQL + pgvector          |
| ollama    | 11434 | Local LLM inference            |

## Environment Variables

See `.env` for all configurable values. Key settings:

| Variable          | Default               | Description                    |
|-------------------|-----------------------|--------------------------------|
| POSTGRES_USER     | codesage              | Database user                  |
| POSTGRES_PASSWORD | changeme              | Database password              |
| EMBEDDING_MODEL   | all-MiniLM-L6-v2      | Sentence Transformer model     |
| LLM_MODEL         | mistral               | Ollama model name              |
| CHUNK_SIZE        | 500                   | Characters per chunk           |
| TOP_K             | 5                     | Retrieval result count         |

## Production Considerations

- Change `POSTGRES_PASSWORD` to a strong secret
- Set specific `allow_origins` in CORS middleware
- Add rate limiting to API endpoints
- Use a reverse proxy (nginx/Caddy) with TLS
- Set up proper log aggregation
- Use Docker volumes for persistent data
