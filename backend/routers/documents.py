from fastapi import APIRouter, HTTPException

from models.schemas import DocumentInfo
from services.database import get_all_documents, delete_document

router = APIRouter(tags=["documents"])


@router.get("/documents", response_model=list[DocumentInfo])
async def list_documents():
    """List all ingested documents."""
    return await get_all_documents()


@router.delete("/documents/{document_name}")
async def remove_document(document_name: str):
    """Delete a document and its chunks from the knowledge base."""
    deleted = await delete_document(document_name)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "success", "message": f"Deleted '{document_name}'"}
