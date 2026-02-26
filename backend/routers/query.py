import json
import time
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from config import settings
from models.schemas import QueryRequest, QueryResponse
from services.database import get_conversation_history, store_conversation
from services.generation import generate, generate_stream
from services.retrieval import retrieve

router = APIRouter(tags=["query"])


async def _run_query(request: QueryRequest) -> tuple[list[dict], str, list[dict]]:
    """Shared logic: retrieve context + fetch history."""
    top_k = request.top_k or settings.TOP_K
    context_chunks = await retrieve(request.question, top_k=top_k)
    history: list[dict] = []
    if request.session_id:
        history = await get_conversation_history(request.session_id)
    return context_chunks, request.session_id or str(uuid.uuid4()), history


@router.post("/query/ask")
async def ask_streaming(request: QueryRequest):
    """Ask a question and receive a streaming SSE response."""
    try:
        context_chunks, session_id, history = await _run_query(request)
        sources = [
            {"source": c["source"], "text": c["text"][:200]} for c in context_chunks
        ]
        chunk_ids = [c["id"] for c in context_chunks if "id" in c]

        async def event_stream():
            start = time.monotonic()
            full_response = ""

            # Send sources as the first SSE event
            yield f"data: {json.dumps({'type': 'sources', 'sources': sources})}\n\n"

            async for token in generate_stream(
                request.question,
                context_chunks,
                mode=request.mode,
                history=history,
            ):
                full_response += token
                yield f"data: {json.dumps({'type': 'token', 'token': token})}\n\n"

            elapsed_ms = int((time.monotonic() - start) * 1000)
            yield f"data: {json.dumps({'type': 'done', 'session_id': session_id})}\n\n"

            # Persist conversation asynchronously (fire-and-forget inside the generator)
            try:
                await store_conversation(
                    session_id=session_id,
                    query=request.question,
                    response=full_response,
                    chunk_ids=chunk_ids,
                    model=settings.LLM_MODEL,
                    response_ms=elapsed_ms,
                )
            except Exception:
                pass

        return StreamingResponse(event_stream(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query/ask-simple", response_model=QueryResponse)
async def ask_simple(request: QueryRequest):
    """Ask a question and receive a complete (non-streaming) JSON response."""
    try:
        start = time.monotonic()
        context_chunks, session_id, history = await _run_query(request)
        answer = await generate(
            request.question,
            context_chunks,
            mode=request.mode,
            history=history,
        )
        elapsed_ms = int((time.monotonic() - start) * 1000)
        sources = [
            {"source": c["source"], "text": c["text"][:200]} for c in context_chunks
        ]
        chunk_ids = [c["id"] for c in context_chunks if "id" in c]

        try:
            await store_conversation(
                session_id=session_id,
                query=request.question,
                response=answer,
                chunk_ids=chunk_ids,
                model=settings.LLM_MODEL,
                response_ms=elapsed_ms,
            )
        except Exception:
            pass

        return QueryResponse(answer=answer, sources=sources, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

