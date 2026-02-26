from pydantic import BaseModel, Field


# ── Ingest ──
class UploadResponse(BaseModel):
    status: str
    document_id: int
    filename: str
    message: str


class IngestResponse(BaseModel):
    status: str
    files_processed: int
    chunks_created: int


class IngestStatusResponse(BaseModel):
    document_id: int
    name: str
    status: str
    chunk_count: int
    ingested_at: str


# ── Query ──
class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    top_k: int | None = Field(default=None, ge=1, le=20)
    session_id: str | None = Field(default=None, max_length=255)
    mode: str = Field(default="document_qa", pattern="^(document_qa|code_assistant)$")


class SourceInfo(BaseModel):
    source: str
    text: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceInfo]
    session_id: str | None = None


# ── Documents ──
class DocumentInfo(BaseModel):
    id: int
    name: str
    file_type: str | None = None
    status: str
    ingested_at: str
    chunk_count: int


class ChunkInfo(BaseModel):
    id: int
    chunk_index: int
    content: str
    source: str
    metadata: dict
