from app.services.chat import ChatService
from app.services.chat_memory import ChatMemoryService
from app.services.embeddings import EmbeddingService
from app.services.ingestion import IngestionService
from app.services.llm import LLMService
from app.services.qdrant import QdrantService
from app.services.redis import RedisService
from app.services.rag import RAGService


embedding_service = EmbeddingService()
qdrant_service = QdrantService()
llm_service = LLMService()
redis_service = RedisService()

qdrant_service.create_collection()

ingestion_service = IngestionService(
    embedding_service=embedding_service,
    qdrant_service=qdrant_service,
)

memory_service = ChatMemoryService(redis_service)

rag_service = RAGService(
    embedding_service=embedding_service,
    qdrant_service=qdrant_service,
    llm_service=llm_service,
)

chat_service = ChatService(
    memory_service=memory_service,
    rag_service=rag_service,
)


def get_ingestion_service() -> IngestionService:
    return ingestion_service


def get_chat_service() -> ChatService:
    return chat_service