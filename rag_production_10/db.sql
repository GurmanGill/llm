CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS rag_lab;

CREATE TABLE IF NOT EXISTS rag_lab.production_chunks (
    id BIGSERIAL PRIMARY KEY,
    document_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,

    pipeline TEXT,
    environment TEXT,
    execution_date DATE,

    embedding VECTOR(768) NOT NULL,

    search_vector TSVECTOR
        GENERATED ALWAYS AS (
            to_tsvector('english', content)
        ) STORED,

    UNIQUE (document_id, chunk_index)
);

-- Vector similarity index
CREATE INDEX IF NOT EXISTS production_chunks_hnsw_idx
ON rag_lab.production_chunks
USING hnsw (embedding vector_cosine_ops);


-- Full-text search index
CREATE INDEX IF NOT EXISTS production_chunks_fts_idx
ON rag_lab.production_chunks
USING gin (search_vector);


-- Metadata filtering index
CREATE INDEX IF NOT EXISTS production_chunks_metadata_idx
ON rag_lab.production_chunks (
    pipeline,
    execution_date
);