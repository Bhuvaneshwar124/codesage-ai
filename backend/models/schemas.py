from pydantic import BaseModel, Field


# ── Ingest ──
class IngestResponse(BaseModel):
    status: str
    files_processed: int
    chunks_created: int


# ── Query ──
class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    top_k: int | None = Field(default=None, ge=1, le=20)


class SourceInfo(BaseModel):
    source: str
    text: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceInfo]


# ── Documents ──
class DocumentInfo(BaseModel):
    name: str
    ingested_at: str
    chunk_count: int
