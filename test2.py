import numpy as np

from app.services.embeddings import EmbeddingService


embedding_service = EmbeddingService()

texts = [
    "The company provides 20 days of annual leave.",
    "Python is a programming language.",
    "Employees receive twenty days of vacation each year.",
]

query = "How many vacation days do employees get?"

vectors = embedding_service.embed_documents(texts)
query_vector = embedding_service.embed_text(query)

for text, vector in zip(texts, vectors):
    similarity = np.dot(query_vector, vector)

    print(f"{similarity:.4f} → {text}")