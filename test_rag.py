from app.services.embeddings import EmbeddingService
from app.services.llm import LLMService
from app.services.qdrant import QdrantService
from app.services.rag import RAGService


embedding_service = EmbeddingService()
qdrant_service = QdrantService()
llm_service = LLMService()

rag = RAGService(
    embedding_service=embedding_service,
    qdrant_service=qdrant_service,
    llm_service=llm_service,
)

question = "What are the four houses at Hogwarts?"

# query_vector = embedding_service.embed_text(question)

# results = qdrant_service.search(
#     query_vector,
#     limit=5,
# )

# for result in results:
#     print("\nSCORE:", result.score)
#     print("TEXT:", result.payload.get("text"))

answer = rag.answer(question)

print(answer)