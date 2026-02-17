from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_async_engine(settings.DATABASE_URL, pool_size=10, max_overflow=20)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Verify the database connection on startup."""
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))


async def close_db():
    """Dispose of the connection pool."""
    await engine.dispose()


async def store_chunks(
    chunks: list[dict], vectors: list[list[float]], document_name: str
):
    """Insert document chunks and their embeddings into pgvector."""
    async with async_session() as session:
        # Insert document record
        result = await session.execute(
            text(
                "INSERT INTO documents (name, ingested_at) VALUES (:name, :ts) "
                "ON CONFLICT (name) DO UPDATE SET ingested_at = :ts "
                "RETURNING id"
            ),
            {"name": document_name, "ts": datetime.now(timezone.utc)},
        )
        doc_id = result.scalar_one()

        # Delete old chunks for this document (re-ingest)
        await session.execute(
            text("DELETE FROM chunks WHERE document_id = :doc_id"),
            {"doc_id": doc_id},
        )

        # Insert new chunks
        for chunk, vector in zip(chunks, vectors):
            await session.execute(
                text(
                    "INSERT INTO chunks (document_id, content, source, embedding) "
                    "VALUES (:doc_id, :content, :source, :embedding)"
                ),
                {
                    "doc_id": doc_id,
                    "content": chunk["text"],
                    "source": chunk["source"],
                    "embedding": str(vector),
                },
            )

        await session.commit()


async def search_similar(query_vector: list[float], top_k: int) -> list[dict]:
    """Find the most similar chunks by cosine distance."""
    async with async_session() as session:
        result = await session.execute(
            text(
                "SELECT c.content, c.source, "
                "1 - (c.embedding <=> :qvec::vector) AS similarity "
                "FROM chunks c "
                "ORDER BY c.embedding <=> :qvec::vector "
                "LIMIT :k"
            ),
            {"qvec": str(query_vector), "k": top_k},
        )
        rows = result.fetchall()
        return [
            {"text": row.content, "source": row.source, "similarity": row.similarity}
            for row in rows
        ]


async def get_all_documents() -> list[dict]:
    """Return a summary of all ingested documents."""
    async with async_session() as session:
        result = await session.execute(
            text(
                "SELECT d.name, d.ingested_at, COUNT(c.id) AS chunk_count "
                "FROM documents d LEFT JOIN chunks c ON c.document_id = d.id "
                "GROUP BY d.id ORDER BY d.ingested_at DESC"
            )
        )
        rows = result.fetchall()
        return [
            {
                "name": row.name,
                "ingested_at": row.ingested_at.isoformat(),
                "chunk_count": row.chunk_count,
            }
            for row in rows
        ]


async def delete_document(document_name: str) -> bool:
    """Delete a document and its chunks. Returns True if found."""
    async with async_session() as session:
        result = await session.execute(
            text("DELETE FROM documents WHERE name = :name RETURNING id"),
            {"name": document_name},
        )
        deleted = result.scalar_one_or_none()
        if deleted is not None:
            await session.commit()
            return True
        return False
