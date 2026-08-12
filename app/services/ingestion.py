from fastapi import UploadFile

from app.schemas.document import ChunkingStrategy
from app.services.chunking import chunk_text
from app.services.document_extractor import extract_text

async def ingest_document(
        file: UploadFile,
        chunking_strategy: ChunkingStrategy
) -> list[str]:
    text = await extract_text(file)
    chunks = chunk_text(
        text=text,
        chunking_strategy=chunking_strategy
    )
    return chunks