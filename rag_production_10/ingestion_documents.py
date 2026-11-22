from ollama import embed
from pgvector.psycopg import register_vector
import psycopg

DB_URL = (
    "postgresql://postgres:postgres"
    "@localhost:5434/vector_lab"
)

EMBEDDING_MODEL = "nomic-embed-text"

#Synthetic logs
logs = [
    {
        "document_id": "run_1001",
        "pipeline": "customer_ingestion",
        "environment": "production",
        "execution_date": "2026-11-18",
        "content": (
            "Pipeline customer_ingestion failed during "
            "silver_transform because the customer_type "
            "column was missing from the source schema."
        )
    },
    {
        "document_id": "run_1002",
        "pipeline": "customer_ingestion",
        "environment": "production",
        "execution_date": "2026-11-15",
        "content": (
            "Pipeline customer_ingestion failed during "
            "extract_source because the PostgreSQL "
            "connection timed out."
        )
    },
    {
        "document_id": "run_1003",
        "pipeline": "orders_ingestion",
        "environment": "production",
        "execution_date": "2026-11-18",
        "content": (
            "Pipeline orders_ingestion failed because "
            "of error DBX-48291 during data validation."
        )
    },
    {
        "document_id": "run_1004",
        "pipeline": "customer_ingestion",
        "environment": "development",
        "execution_date": "2026-11-19",
        "content": (
            "Pipeline customer_ingestion completed "
            "successfully after schema validation."
        )
    },
    {
        "document_id": "run_1005",
        "pipeline": "customer_ingestion",
        "environment": "production",
        "execution_date": "2026-11-20",
        "content": (
            "Pipeline customer_ingestion failed with "
            "error DBX-48292 because a Spark executor "
            "ran out of memory during a shuffle."
        )
    }
]

def get_embedding(text: str) -> list[float]:
    response = embed(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response["embeddings"][0]


def ingest_logs(logs: list[dict]) -> None:

    with psycopg.connect(DB_URL) as conn:
        register_vector(conn)

        with conn.cursor() as cursor:

            for log in logs:

                vector = get_embedding(
                    log["content"]
                )

                cursor.execute(
                    """
                    INSERT INTO rag_lab.production_chunks (
                        document_id,
                        chunk_index,
                        content,
                        pipeline,
                        environment,
                        execution_date,
                        embedding
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (document_id, chunk_index)
                    DO UPDATE SET
                        content = EXCLUDED.content,
                        pipeline = EXCLUDED.pipeline,
                        environment = EXCLUDED.environment,
                        execution_date = EXCLUDED.execution_date,
                        embedding = EXCLUDED.embedding
                    """,
                    (
                        log["document_id"],
                        0,
                        log["content"],
                        log["pipeline"],
                        log["environment"],
                        log["execution_date"],
                        vector
                    )
                )


if __name__ == "__main__":
    ingest_logs(logs)
    print("Production logs ingested successfully.")
