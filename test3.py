from app.services.embeddings import EmbeddingService
from app.services.qdrant import QdrantService

embedding_service = EmbeddingService()
qdrant = QdrantService()

text = "The company has three interview rounds."

vector = embedding_service.embed_text(text)

len(vector)

qdrant.upsert_chunk(
    point_id=1,
    vector=vector,
    document_id="doc-001",
    chunk_index=0,
    text=text,
    filename="interview-guide.txt",
)

query = "How many interview stages are there?"
query_vector = embedding_service.embed_text(query)
results = qdrant.search(
    query_vector,
    limit=5,
)
for result in results:
    print(result.score)
    print(result.payload)