-- IVFFlat index for fast approximate nearest-neighbor search
CREATE INDEX IF NOT EXISTS idx_chunks_embedding
    ON chunks
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Index for document lookup
CREATE INDEX IF NOT EXISTS idx_chunks_document_id
    ON chunks (document_id);

-- Index for document name lookup
CREATE INDEX IF NOT EXISTS idx_documents_name
    ON documents (name);
