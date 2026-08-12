from uuid import uuid4

from fastapi import UploadFile
from qdrant_client.models import PointStruct

from app.schemas.document import ChunkingStrategy
from app.services.chunking import chunk_text
from app.services.document_extractor import extract_text
from app.services.embeddings import EmbeddingService
from app.services.qdrant import QdrantService


class IngestionService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        qdrant_service: QdrantService,
    ) -> None:
        self.embedding_service = embedding_service
        self.qdrant_service = qdrant_service

    async def ingest_document(
        self,
        file: UploadFile,
        chunking_strategy: ChunkingStrategy,
    ) -> tuple[str, int]:
        document_id = str(uuid4())

        text = await extract_text(file)

        chunks = chunk_text(
            text,
            chunking_strategy=chunking_strategy,
        )

        embeddings = self.embedding_service.embed_documents(chunks)

        points: list[PointStruct] = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            point_id = str(uuid4())

            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "document_id": document_id,
                        "chunk_index": index,
                        "text": chunk,
                        "filename": file.filename or "unknown",
                    },
                )
            )

        self.qdrant_service.upsert_chunks(points)

        return document_id, len(chunks)