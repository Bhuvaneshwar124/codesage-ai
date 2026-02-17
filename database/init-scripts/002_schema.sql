-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(500) NOT NULL UNIQUE,
    ingested_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Chunks table with pgvector embedding column
CREATE TABLE IF NOT EXISTS chunks (
    id           SERIAL PRIMARY KEY,
    document_id  INTEGER      NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    content      TEXT         NOT NULL,
    source       VARCHAR(500) NOT NULL,
    embedding    vector(384)  NOT NULL,
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
