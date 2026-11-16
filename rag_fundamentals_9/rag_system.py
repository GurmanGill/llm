from ollama import embed
import psycopg
from pgvector.psycopg import register_vector

#Vars
EMBEDDING_MODEL = "nomic-embed_text"
DB_URL = ("postgresql://dou1939:postgres@localhost:5432/vector_lab")

#Text
documents = {
    "spark_skew": (
        "Spark data skew occurs when some partitions contain "
        "significantly more data than others. This can cause "
        "some executor tasks to run much longer. Common "
        "solutions include repartitioning, salting skewed "
        "join keys, and using adaptive query execution."
    ),
    "pipeline_failure": (
        "The customer_ingestion pipeline failed during the "
        "silver_transform task. The error message was: "
        "Cannot resolve column customer_type. The source "
        "schema did not contain the expected column."
    ),
    "delta_schema": (
        "Delta Lake supports schema enforcement and schema "
        "evolution. Schema enforcement prevents incompatible "
        "writes. Schema evolution can allow compatible "
        "schema changes when explicitly enabled."
    ),
}

#Functions
def chunk_text(
    text: str,
    chunk_size: int=200,
    overlap_size: int=40
)-> list[str]:

    """
    Splits the input text into chunks of specified size with a given overlap.

    Args:
        text (str): The text to be chunked.
        chunk_size (int, optional): The size of each chunk. Defaults to 200.
        overlap_size (int, optional): The number of overlapping characters between chunks. Defaults to 40.

    Returns:
        list[str]: A list of text chunks.
    """

    if chunk_size <=0:
        raise ValueError("chunk_size must be greater than 0")

    if not 0 <= overlap_size < chunk_size:
        raise ValueError("overlap size must be smaller than chunk_size")

    chunks = []
    step = chunk_size - overlap_size

    for start in range(0, len(text), step):
        chunk = text[start:start+chunk_size]

        if chunk:
            chunks.append(chunk)

        if start + chunk_size >= len(text):
            break

    return chunks

def get_embedding(
        text:str
) ->list[float]:

    """Generate a text embeddings"""

    response = embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response['embeddings'][0]

with psycopg.connect(DB_URL) as conn:
    register_vector(conn)

    with conn.cursor() as cursor:

        for document_id, content in documents.items():
            chunks = chunk_text(content)

            for index, chunk in enumerate(chunks):
                vector = get_embedding(chunk)

                cursor.execute(
                    """
                    INSERT INTO rag_lab.documents_chunks(
                    document_id,
                    chunk_index,
                    content,
                    embedding
                    )
                    VALUES (%s %s %s %s)
                    ON CONFLICT(document_id, chunk_index)
                    DO UPDATE SET
                        content=EXCLUDED.content,
                        embedding=EXCLUDED.embedding
                    """,
                    (document_id, index, chunk, vector)
                )
print("Document ingestion completed")

















