import json
import logging
from typing import AsyncGenerator

import httpx

from config import settings

logger = logging.getLogger("codesage.generation")

_SYSTEM_PROMPTS = {
    "document_qa": (
        "You are CodeSage, an expert AI assistant for understanding technical documents. "
        "Answer the user's question using ONLY the provided context. "
        "If the context does not contain enough information, say so clearly."
    ),
    "code_assistant": (
        "You are CodeSage, an expert AI code assistant. "
        "Answer the user's question using ONLY the provided code context. "
        "Use code formatting when referencing code. "
        "Explain code behavior clearly and concisely."
    ),
}

# Keep legacy constant for backward compatibility
SYSTEM_PROMPT = _SYSTEM_PROMPTS["document_qa"]


def _build_prompt(
    query: str,
    context_chunks: list[dict],
    mode: str = "document_qa",
    history: list[dict] | None = None,
) -> str:
    """Build an augmented prompt from retrieved context and optional history."""
    system = _SYSTEM_PROMPTS.get(mode, _SYSTEM_PROMPTS["document_qa"])
    context_block = "\n\n---\n\n".join(
        f"Source: {c['source']}\n{c['text']}" for c in context_chunks
    )

    history_block = ""
    if history:
        turns = "\n".join(
            f"User: {turn['query']}\nAssistant: {turn['response']}"
            for turn in history
        )
        history_block = f"\n\n### Conversation History\n{turns}"

    return (
        f"{system}{history_block}\n\n"
        f"### Context\n{context_block}\n\n"
        f"### Question\n{query}\n\n"
        f"### Answer\n"
    )


async def generate(
    query: str,
    context_chunks: list[dict],
    mode: str = "document_qa",
    history: list[dict] | None = None,
) -> str:
    """Call Ollama's API to generate an answer from the augmented prompt."""
    prompt = _build_prompt(query, context_chunks, mode=mode, history=history)

    logger.info("Generating answer (non-streaming) with model=%s", settings.LLM_MODEL)
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.LLM_MODEL,
                "prompt": prompt,
                "stream": False,
            },
        )
        response.raise_for_status()
        return response.json()["response"]


async def generate_stream(
    query: str,
    context_chunks: list[dict],
    mode: str = "document_qa",
    history: list[dict] | None = None,
) -> AsyncGenerator[str, None]:
    """Stream tokens from Ollama as Server-Sent Events."""
    prompt = _build_prompt(query, context_chunks, mode=mode, history=history)

    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST",
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.LLM_MODEL,
                "prompt": prompt,
                "stream": True,
            },
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                token = data.get("response", "")
                if token:
                    yield token
                if data.get("done"):
                    break

