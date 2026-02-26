from fastapi import APIRouter, HTTPException

from models.schemas import ChunkInfo, DocumentInfo
from services.database import (
    delete_document_by_id,
    get_all_documents,
    get_document_chunks,
)

router = APIRouter(tags=["documents"])


@router.get("/documents/list", response_model=list[DocumentInfo])
async def list_documents():
    """List all ingested documents."""
    return await get_all_documents()


@router.delete("/documents/{document_id}")
async def remove_document(document_id: int):
    """Delete a document and its chunks from the knowledge base."""
    deleted = await delete_document_by_id(document_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "success", "message": f"Deleted document {document_id}"}


@router.get("/documents/{document_id}/chunks", response_model=list[ChunkInfo])
async def get_chunks(document_id: int):
    """Retrieve all chunks for a specific document."""
    chunks = await get_document_chunks(document_id)
    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="No chunks found for this document",
        )
    return chunks

