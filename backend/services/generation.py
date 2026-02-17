import httpx

from config import settings

SYSTEM_PROMPT = (
    "You are CodeSage, an expert AI assistant for understanding codebases and "
    "technical documents. Answer the user's question using ONLY the provided context. "
    "If the context does not contain enough information, say so clearly. "
    "Use code formatting when referencing code."
)


def _build_prompt(query: str, context_chunks: list[dict]) -> str:
    """Build an augmented prompt from retrieved context."""
    context_block = "\n\n---\n\n".join(
        f"Source: {c['source']}\n{c['text']}" for c in context_chunks
    )
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"### Context\n{context_block}\n\n"
        f"### Question\n{query}\n\n"
        f"### Answer\n"
    )


async def generate(query: str, context_chunks: list[dict]) -> str:
    """Call Ollama's API to generate an answer from the augmented prompt."""
    prompt = _build_prompt(query, context_chunks)

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
