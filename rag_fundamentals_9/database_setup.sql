CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS rag_lab;

CREATE TABLE IF NOT EXISTS rag_lab.documents_chunks (
    id BIGSERIAL PRIMARY KEY,
    document_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(768) NOT NULL,
    UNIQUE (document_id, chunk_index)
);