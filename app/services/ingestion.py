from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from qdrant_client.models import PointStruct
from sqlalchemy.orm import Session

from app.db.models import Document
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
        db: Session,
    ) -> tuple[str, int]:

        document_id = uuid4()

        file_contents = await file.read()
        file_size = len(file_contents)

        await file.seek(0)

        text = await extract_text(file)

        chunks = chunk_text(
            text,
            chunking_strategy=chunking_strategy,
        )

        embeddings = self.embedding_service.embed_documents(chunks)

        points: list[PointStruct] = []

        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "document_id": str(document_id),
                        "chunk_index": index,
                        "text": chunk,
                        "filename": file.filename or "unknown",
                    },
                )
            )

        self.qdrant_service.upsert_chunks(points)

        file_type = Path(
            file.filename or ""
        ).suffix.lower().lstrip(".")

        document = Document(
            document_id=document_id,
            filename=file.filename or "unknown",
            file_type=file_type,
            file_size=file_size,
            chunking_strategy=chunking_strategy.value,
            chunk_count=len(chunks),
        )

        db.add(document)
        db.commit()

        return str(document_id), len(chunks)