from ollama import embed
import numpy as np
from pprint import pprint

# response = embed(
#     model='nomic-embed-text',
#     input='Apache spark data skew'
# )

# vector = response['embeddings'][0]
# print(len(vector))
# print(vector)

MODEL = 'nomic-embed-text'

documents = [
    "Spark job failed because of data skew",
    "How to optimize PostgreSQL queries",
    "Troubleshooting Spark shuffle operations",
    "Configuring Azure storage accounts",
    "Delta Lake schema evolution"
]

def get_embedding(text: str) -> np.ndarray:

    response = embed(
        model=MODEL,
        input=text
    )

    return np.array(
        response['embeddings'][0],
        dtype=float
    )

def cosine_similarity(a, b):

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

#Generate embeddings for the documents
document_vectors = [ get_embedding(doc) for doc in documents]

#User question
query = 'why is my spark running slow?'
# query = 'Pipeline X failed with error DBX-48291?'
# query = 'DBX-48291'
query_vector = get_embedding(query)

#Caluclate similarities
results = []

for doc, vector in zip(documents, document_vectors):
    score = cosine_similarity(
        query_vector,
        vector
    )

    results.append((doc, score))

#Sort by similarities
results.sort(
    key=lambda x: x[1],
    reverse=True
)

#threshold
threshold = 0.50

filtered_results = [
    (doc, score)
    for doc, score in results
    if score >= threshold
]

#Select top 3
for doc, score in filtered_results[:3]:
    print(f"{score:.3f} - {doc} ")