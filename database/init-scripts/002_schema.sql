-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(500) NOT NULL UNIQUE,
    file_type   VARCHAR(50),
    status      VARCHAR(50)  NOT NULL DEFAULT 'processing',
    ingested_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Document chunks table with pgvector embedding column
CREATE TABLE IF NOT EXISTS chunks (
    id           SERIAL PRIMARY KEY,
    document_id  INTEGER      NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    content      TEXT         NOT NULL,
    source       VARCHAR(500) NOT NULL,
    chunk_index  INTEGER      NOT NULL DEFAULT 0,
    metadata     JSONB        NOT NULL DEFAULT '{}',
    embedding    vector(384)  NOT NULL,
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Conversations table for session-based history
CREATE TABLE IF NOT EXISTS conversations (
    id          UUID         PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id  VARCHAR(255) NOT NULL,
    query       TEXT         NOT NULL,
    response    TEXT         NOT NULL,
    chunk_ids   INTEGER[],
    model       VARCHAR(100),
    response_ms INTEGER,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Metrics table for performance tracking
CREATE TABLE IF NOT EXISTS metrics (
    id         SERIAL      PRIMARY KEY,
    event      VARCHAR(100) NOT NULL,
    value      FLOAT,
    metadata   JSONB        NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
