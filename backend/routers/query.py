from fastapi import APIRouter, HTTPException

from config import settings
from models.schemas import QueryRequest, QueryResponse
from services.retrieval import retrieve
from services.generation import generate

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """Ask a question against the ingested knowledge base."""
    try:
        context_chunks = await retrieve(request.question, top_k=request.top_k or settings.TOP_K)
        answer = await generate(request.question, context_chunks)
        sources = [
            {"source": c["source"], "text": c["text"][:200]} for c in context_chunks
        ]
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
