from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct


QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "document_chunks"
VECTOR_SIZE = 384


class QdrantService:
    def __init__(self) -> None:
        self.client = QdrantClient(url=QDRANT_URL)

    def create_collection(self) -> None:
        collections = self.client.get_collections().collections

        collection_names = {
            collection.name
            for collection in collections
        }

        if COLLECTION_NAME in collection_names:
            return

        self.client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )
    def upsert_chunk(
    self,
    point_id: str,
    vector: list[float],
    document_id: str,
    chunk_index: int,
    text: str,
    filename: str,
    ) -> None:
        point = PointStruct(
            id=point_id,
            vector=vector,
            payload={
                "document_id": document_id,
                "chunk_index": chunk_index,
                "text": text,
                "filename": filename,
            },
        )

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point],
        )

    def search(
    self,
    query_vector: list[float],
    limit: int = 5,
    ) -> list:
        return self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
        ).points