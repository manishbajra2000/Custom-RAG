from app.services.embeddings import EmbeddingService
from app.services.ingestion import IngestionService
from app.services.qdrant import QdrantService


embedding_service = EmbeddingService()
qdrant_service = QdrantService()

qdrant_service.create_collection()

ingestion_service = IngestionService(
    embedding_service=embedding_service,
    qdrant_service=qdrant_service,
)