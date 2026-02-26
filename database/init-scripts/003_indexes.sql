-- HNSW index for fast approximate nearest-neighbor search
CREATE INDEX IF NOT EXISTS idx_chunks_embedding
    ON chunks
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Full-text search index for hybrid search
CREATE INDEX IF NOT EXISTS idx_chunks_content_fts
    ON chunks
    USING gin (to_tsvector('english', content));

-- Index for document lookup
CREATE INDEX IF NOT EXISTS idx_chunks_document_id
    ON chunks (document_id);

-- Index for document name lookup
CREATE INDEX IF NOT EXISTS idx_documents_name
    ON documents (name);

-- Index for conversation session lookup
CREATE INDEX IF NOT EXISTS idx_conversations_session_id
    ON conversations (session_id);
