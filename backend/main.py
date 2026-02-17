from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from generator import generate
from ingest import ingest
from retriever import retrieve

app = FastAPI(
    title="CodeSage AI",
    description="RAG-powered codebase and document analysis API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/ingest")
def run_ingest():
    """Trigger the document ingestion pipeline."""
    try:
        ingest()
        return {"status": "success", "message": "Ingestion complete."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    """Ask a question against the ingested codebase/documents."""
    try:
        context_chunks = retrieve(request.question, top_k=request.top_k)
        answer = generate(request.question, context_chunks)
        sources = [chunk["metadata"] for chunk in context_chunks]
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
