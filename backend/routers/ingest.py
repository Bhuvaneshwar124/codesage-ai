import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile

from config import settings
from models.schemas import IngestStatusResponse, UploadResponse
from services.database import (
    create_document_record,
    get_document_status,
    store_chunks_for_doc,
    update_document_status,
)
from services.embedding import embed_chunks
from services.parsers import parse_file
from utils.chunking import chunk_text

router = APIRouter(tags=["ingest"])

ALLOWED_EXTENSIONS = settings.SUPPORTED_EXTENSIONS


async def _ingest_background(doc_id: int, dest: Path, filename: str):
    """Background task: parse → chunk → embed → store → mark complete."""
    try:
        text = parse_file(dest)
        chunks = chunk_text(text, source=filename)
        vectors = embed_chunks([c["text"] for c in chunks])
        await store_chunks_for_doc(doc_id, chunks, vectors)
        await update_document_status(doc_id, "complete")
    except Exception:
        await update_document_status(doc_id, "failed")


@router.post("/ingest/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    """Upload a single file and start background ingestion."""
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}",
        )

    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_id = uuid.uuid4().hex[:12]
    dest = upload_dir / f"{file_id}_{file.filename}"
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    doc_id = await create_document_record(file.filename, ext.lstrip("."))
    background_tasks.add_task(_ingest_background, doc_id, dest, file.filename)

    return UploadResponse(
        status="processing",
        document_id=doc_id,
        filename=file.filename,
        message="File accepted; ingestion running in the background.",
    )


@router.get("/ingest/status/{document_id}", response_model=IngestStatusResponse)
async def get_ingest_status(document_id: int):
    """Check the ingestion status of a previously uploaded document."""
    doc = await get_document_status(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return IngestStatusResponse(
        document_id=doc["document_id"],
        name=doc["name"],
        status=doc["status"],
        chunk_count=doc["chunk_count"],
        ingested_at=doc["ingested_at"],
    )
