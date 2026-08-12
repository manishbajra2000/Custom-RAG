from app.services.embeddings import EmbeddingService

embedding_service = EmbeddingService()

vector = embedding_service.embed_text(
    "The company has three interview rounds."
)

print(type(vector))
print(len(vector))
print(vector[:5])


chunks = [
    "Python is a programming language.",
    "FastAPI is a Python web framework.",
    "The company has three interview rounds.",
]

vectors = embedding_service.embed_documents(chunks)

print(len(vectors))
print(len(vectors[0]))
print(vectors)