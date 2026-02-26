import time
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


async def create_document_record(name: str, file_type: str) -> int:
    """Insert a new document record with 'processing' status and return its ID."""
    async with async_session() as session:
        result = await session.execute(
            text(
                "INSERT INTO documents (name, file_type, status, ingested_at) "
                "VALUES (:name, :file_type, 'processing', :ts) "
                "ON CONFLICT (name) DO UPDATE SET "
                "file_type = :file_type, status = 'processing', ingested_at = :ts "
                "RETURNING id"
            ),
            {"name": name, "file_type": file_type, "ts": datetime.now(timezone.utc)},
        )
        doc_id = result.scalar_one()
        await session.commit()
        return doc_id


async def update_document_status(doc_id: int, status: str):
    """Update document ingestion status."""
    async with async_session() as session:
        await session.execute(
            text("UPDATE documents SET status = :status WHERE id = :doc_id"),
            {"status": status, "doc_id": doc_id},
        )
        await session.commit()


async def store_chunks(
    chunks: list[dict], vectors: list[list[float]], document_name: str
):
    """Insert document chunks and their embeddings into pgvector (legacy helper)."""
    async with async_session() as session:
        result = await session.execute(
            text(
                "INSERT INTO documents (name, status, ingested_at) "
                "VALUES (:name, 'complete', :ts) "
                "ON CONFLICT (name) DO UPDATE SET "
                "status = 'complete', ingested_at = :ts "
                "RETURNING id"
            ),
            {"name": document_name, "ts": datetime.now(timezone.utc)},
        )
        doc_id = result.scalar_one()

        await session.execute(
            text("DELETE FROM chunks WHERE document_id = :doc_id"),
            {"doc_id": doc_id},
        )

        for idx, (chunk, vector) in enumerate(zip(chunks, vectors)):
            await session.execute(
                text(
                    "INSERT INTO chunks "
                    "(document_id, content, source, chunk_index, metadata, embedding) "
                    "VALUES (:doc_id, :content, :source, :idx, :meta, :embedding)"
                ),
                {
                    "doc_id": doc_id,
                    "content": chunk["text"],
                    "source": chunk["source"],
                    "idx": idx,
                    "meta": chunk.get("metadata", "{}"),
                    "embedding": str(vector),
                },
            )

        await session.commit()


async def store_chunks_for_doc(
    doc_id: int, chunks: list[dict], vectors: list[list[float]]
):
    """Store chunks for a document identified by its integer ID."""
    async with async_session() as session:
        await session.execute(
            text("DELETE FROM chunks WHERE document_id = :doc_id"),
            {"doc_id": doc_id},
        )

        for idx, (chunk, vector) in enumerate(zip(chunks, vectors)):
            await session.execute(
                text(
                    "INSERT INTO chunks "
                    "(document_id, content, source, chunk_index, metadata, embedding) "
                    "VALUES (:doc_id, :content, :source, :idx, :meta, :embedding)"
                ),
                {
                    "doc_id": doc_id,
                    "content": chunk["text"],
                    "source": chunk["source"],
                    "idx": idx,
                    "meta": chunk.get("metadata", "{}"),
                    "embedding": str(vector),
                },
            )

        await session.commit()


async def search_similar(query_vector: list[float], top_k: int) -> list[dict]:
    """Find the most similar chunks by cosine distance (semantic search)."""
    async with async_session() as session:
        result = await session.execute(
            text(
                "SELECT c.id, c.content, c.source, "
                "1 - (c.embedding <=> :qvec::vector) AS similarity "
                "FROM chunks c "
                "JOIN documents d ON d.id = c.document_id "
                "WHERE d.status = 'complete' "
                "ORDER BY c.embedding <=> :qvec::vector "
                "LIMIT :k"
            ),
            {"qvec": str(query_vector), "k": top_k},
        )
        rows = result.fetchall()
        return [
            {"id": row.id, "text": row.content, "source": row.source,
             "similarity": row.similarity}
            for row in rows
        ]


async def search_hybrid(
    query: str, query_vector: list[float], top_k: int
) -> list[dict]:
    """Hybrid search combining semantic similarity and full-text keyword search."""
    async with async_session() as session:
        result = await session.execute(
            text(
                "SELECT c.id, c.content, c.source, "
                "1 - (c.embedding <=> :qvec::vector) AS semantic_score, "
                "ts_rank(to_tsvector('english', c.content), "
                "        plainto_tsquery('english', :query)) AS text_score "
                "FROM chunks c "
                "JOIN documents d ON d.id = c.document_id "
                "WHERE d.status = 'complete' "
                "ORDER BY "
                "  0.7 * (1 - (c.embedding <=> :qvec::vector)) "
                "  + 0.3 * ts_rank(to_tsvector('english', c.content), "
                "                  plainto_tsquery('english', :query)) DESC "
                "LIMIT :k"
            ),
            {"qvec": str(query_vector), "query": query, "k": top_k},
        )
        rows = result.fetchall()
        return [
            {
                "id": row.id,
                "text": row.content,
                "source": row.source,
                "similarity": float(row.semantic_score),
            }
            for row in rows
        ]


async def get_document_status(doc_id: int) -> dict | None:
    """Return document status and chunk count."""
    async with async_session() as session:
        result = await session.execute(
            text(
                "SELECT d.id, d.name, d.status, d.ingested_at, "
                "COUNT(c.id) AS chunk_count "
                "FROM documents d LEFT JOIN chunks c ON c.document_id = d.id "
                "WHERE d.id = :doc_id "
                "GROUP BY d.id"
            ),
            {"doc_id": doc_id},
        )
        row = result.fetchone()
        if not row:
            return None
        return {
            "document_id": row.id,
            "name": row.name,
            "status": row.status,
            "chunk_count": row.chunk_count,
            "ingested_at": row.ingested_at.isoformat(),
        }


async def get_document_chunks(doc_id: int) -> list[dict]:
    """Return all chunks for a document."""
    async with async_session() as session:
        result = await session.execute(
            text(
                "SELECT c.id, c.chunk_index, c.content, c.source, c.metadata "
                "FROM chunks c WHERE c.document_id = :doc_id "
                "ORDER BY c.chunk_index"
            ),
            {"doc_id": doc_id},
        )
        rows = result.fetchall()
        return [
            {
                "id": row.id,
                "chunk_index": row.chunk_index,
                "content": row.content,
                "source": row.source,
                "metadata": row.metadata or {},
            }
            for row in rows
        ]


async def get_all_documents() -> list[dict]:
    """Return a summary of all ingested documents."""
    async with async_session() as session:
        result = await session.execute(
            text(
                "SELECT d.id, d.name, d.file_type, d.status, d.ingested_at, "
                "COUNT(c.id) AS chunk_count "
                "FROM documents d LEFT JOIN chunks c ON c.document_id = d.id "
                "GROUP BY d.id ORDER BY d.ingested_at DESC"
            )
        )
        rows = result.fetchall()
        return [
            {
                "id": row.id,
                "name": row.name,
                "file_type": row.file_type,
                "status": row.status,
                "ingested_at": row.ingested_at.isoformat(),
                "chunk_count": row.chunk_count,
            }
            for row in rows
        ]


async def delete_document(document_name: str) -> bool:
    """Delete a document and its chunks by name. Returns True if found."""
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


async def delete_document_by_id(doc_id: int) -> bool:
    """Delete a document and its chunks by ID. Returns True if found."""
    async with async_session() as session:
        result = await session.execute(
            text("DELETE FROM documents WHERE id = :doc_id RETURNING id"),
            {"doc_id": doc_id},
        )
        deleted = result.scalar_one_or_none()
        if deleted is not None:
            await session.commit()
            return True
        return False


async def store_conversation(
    session_id: str,
    query: str,
    response: str,
    chunk_ids: list[int],
    model: str,
    response_ms: int,
):
    """Persist a conversation turn to the database."""
    async with async_session() as session:
        await session.execute(
            text(
                "INSERT INTO conversations "
                "(session_id, query, response, chunk_ids, model, response_ms) "
                "VALUES (:sid, :query, :response, :chunk_ids, :model, :response_ms)"
            ),
            {
                "sid": session_id,
                "query": query,
                "response": response,
                "chunk_ids": chunk_ids,
                "model": model,
                "response_ms": response_ms,
            },
        )
        await session.commit()


async def get_conversation_history(session_id: str, limit: int = 5) -> list[dict]:
    """Return the most recent conversation turns for a session."""
    async with async_session() as session:
        result = await session.execute(
            text(
                "SELECT query, response FROM conversations "
                "WHERE session_id = :sid "
                "ORDER BY created_at DESC LIMIT :limit"
            ),
            {"sid": session_id, "limit": limit},
        )
        rows = result.fetchall()
        return [{"query": row.query, "response": row.response} for row in reversed(rows)]

