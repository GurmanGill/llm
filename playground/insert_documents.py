from ollama import embed
import psycopg
from pgvector.psycopg import register_vector
import numpy as np

MODEL = 'nomic-embed-text'
DATABASE_URL = 'postgresql://postgres:postgres@localhost:3333/vector_lab'

documents = [
    (
        "Spark job failed because of data skew",
        "spark"
    ),
    (
        "Troubleshooting Spark shuffle operations",
        "spark"
    ),
    (
        "How to optimize PostgreSQL queries",
        "postgres"
    ),
    (
        "Configuring Azure storage accounts",
        "azure"
    ),
    (
        "Delta Lake schema evolution",
        "delta"
    )
]

def get_embedding(text: str) -> list[float]:

    response = embed(
        model = MODEL,
        input = text
    )

    return response['embeddings'][0]

def insert_embedding() -> None:

    with psycopg.connect(DATABASE_URL) as conn:

        register_vector(conn)

        with conn.cursor() as cursor:

            for content, category in documents:

                vector = get_embedding(content)

                cursor.execute(
                    """
                    INSERT INTO vector_lab.documents (
                        content,
                        category,
                        embedding
                    )
                    VALUES(%s, %s, %s)
                    """,
                    (content, category, vector)
                )

def search_documents(
        query: str,
        top_k: int = 3,
) -> list[tuple]:

    query_vector = np.array(
        get_embedding(query),
        dtype=np.float32
    )

    #Search db
    with psycopg.connect(DATABASE_URL) as conn:

        register_vector(conn)

        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    content,
                    embedding <=> %s AS distance
                FROM vector_lab.documents
                ORDER BY embedding <=> %s
                LIMIT %s
                """,
                (
                    query_vector,
                    query_vector,
                    top_k
                )
            )

            return cursor.fetchall()


results = search_documents(
    "Why is my Spark job running slowly?"
)
print(results)

for content, distance in results:
    print(f"{distance:.3f} - {content}")