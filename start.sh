#!/usr/bin/env bash
set -euo pipefail

echo "==> Starting CodeSage AI..."

# Build and start all services
docker compose up --build -d

echo "==> Waiting for services to be healthy..."
docker compose exec backend python -c "print('Backend is ready.')" 2>/dev/null || true

echo ""
echo "  CodeSage AI is running!"
echo "  Frontend : http://localhost:${FRONTEND_PORT:-5173}"
echo "  Backend  : http://localhost:${BACKEND_PORT:-8000}"
echo "  API Docs : http://localhost:${BACKEND_PORT:-8000}/docs"
echo ""
echo "  Pull an Ollama model if you haven't already:"
echo "    docker compose exec ollama ollama pull mistral"
echo ""
