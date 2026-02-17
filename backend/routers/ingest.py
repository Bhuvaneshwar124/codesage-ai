import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from config import settings
from models.schemas import IngestResponse
from services.embedding import embed_chunks
from services.database import store_chunks
from services.parsers import parse_file
from utils.chunking import chunk_text

router = APIRouter(tags=["ingest"])

ALLOWED_EXTENSIONS = settings.SUPPORTED_EXTENSIONS


@router.post("/ingest", response_model=IngestResponse)
async def ingest_files(files: list[UploadFile]):
    """Upload and ingest one or more files into the knowledge base."""
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    total_chunks = 0

    for file in files:
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {ext}",
            )

        # Save uploaded file
        file_id = uuid.uuid4().hex[:12]
        dest = upload_dir / f"{file_id}_{file.filename}"
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Parse → Chunk → Embed → Store
        text = parse_file(dest)
        chunks = chunk_text(text, source=str(file.filename))
        vectors = embed_chunks([c["text"] for c in chunks])
        await store_chunks(chunks, vectors, document_name=file.filename)
        total_chunks += len(chunks)

    return IngestResponse(
        status="success",
        files_processed=len(files),
        chunks_created=total_chunks,
    )
