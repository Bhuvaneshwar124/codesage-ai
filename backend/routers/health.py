import logging

import httpx
from fastapi import APIRouter

from config import settings
from services.database import engine

logger = logging.getLogger("codesage.health")
router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Comprehensive health check — verifies DB and Ollama connectivity."""
    status = {"status": "ok", "database": "unknown", "ollama": "unknown"}

    # Check database
    try:
        from sqlalchemy import text as sa_text

        async with engine.connect() as conn:
            await conn.execute(sa_text("SELECT 1"))
        status["database"] = "connected"
    except Exception as e:
        logger.warning("Health check: DB unreachable — %s", e)
        status["database"] = "unreachable"
        status["status"] = "degraded"

    # Check Ollama
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            resp.raise_for_status()
            models = [m["name"] for m in resp.json().get("models", [])]
            status["ollama"] = "connected"
            status["ollama_models"] = models
    except Exception as e:
        logger.warning("Health check: Ollama unreachable — %s", e)
        status["ollama"] = "unreachable"
        status["status"] = "degraded"

    return status
